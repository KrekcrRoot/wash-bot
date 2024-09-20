
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command, CommandStart
from aiogram import Router
from typing import List

import json
import app.markups as nav
from app.api import init_api_controller
from app.dto.user_entity import UserEntity, create_user
from app.dto.machine_entity import MachineEntity, create_machineList
from app.dto.status_entity import StatusEntity, create_status
from app.dto.time_entity import TimeEntity, create_time

router = Router()
api_controller = init_api_controller()

#!1

#States to separate some menus
class Form(StatesGroup):
    forgotten_cloth = State()
    occupied_confirmation = State()
    break_confirmation = State()
    machine = State()
    adminMenu = State()
    menu = State()

#Authorization thing
@router.message(CommandStart())
async def command_start_handler(message: Message, state:FSMContext) -> None:

    user_tag = message.from_user.username
    user_id = message.from_user.id

    if user_tag is None: 
        user_is_authorized = False
    else:
        res = await api_controller.auth(user_tag, user_id)
        user_is_authorized = res.status_code==200

    if user_is_authorized:

        res = await api_controller.get_my(user_id)
        user: UserEntity = create_user(res.json())

        if user.link_machine is not None:
            await state.set_state(Form.menu)
            user_is_admin=user.type
            if user_is_admin:
                await message.answer(text='Вы успешно авторизованы',reply_markup=nav.mainMenuAdmin)
            else:
                await message.answer(text='Вы успешно авторизованы',reply_markup=nav.mainMenu)
        else:
            res = await api_controller.get_machines()
            machines: List[MachineEntity] = create_machineList(res.json())
            if len(machines)>1 or True:
                await state.set_state(Form.machine)
                await message.answer(text="Выберите стиральную машинку из списка",reply_markup=nav.machineMenu(machines))
            elif len(machines)==1:
                machine_id = machines[0].uuid
                res = await api_controller.link_machine(user_id,machine_id)
            else:
                message.answer(text="Something wrong, no machines to link")
    else:
        await message.answer(text="Вы не авторизованы. Обратитесь за помощью к кому скидывались за стиралку")

#Cancel command (resets state)
@router.message(Command("cancel"))
async def cancel_handler(message: Message, state:FSMContext) -> None:
    if await state.get_state() is not None:
        await state.clear()
        await message.answer(text='Действие отменено, напишите "/start" для начала работы')

#Changing selected machine
@router.message(Command("change_machine"))
async def cancel_handler(message: Message, state:FSMContext) -> None:
    user_tag = message.from_user.username
    user_id = message.from_user.id

    if user_tag is None: 
        user_is_authorized = False
    else:
        res = await api_controller.auth(user_tag, user_id)
        user_is_authorized = res.status_code==200

    if user_is_authorized:
        res = await api_controller.get_my(user_id)
        user: UserEntity = create_user(res.json())

        if user.link_machine is not None:
            res = await api_controller.get_machines()
            machines: List[MachineEntity] = create_machineList(res.json())
            if len(machines)>1 or True:
                res = await api_controller.unlink_machine(user_id)
                if res.status_code==201:
                    await state.set_state(Form.machine)
                    await message.answer(text="Выберите стиральную машинку из списка",reply_markup=nav.machineMenu(machines))
            elif len(machines)==1:
                await message.answer(text="Вам доступна только одна машинка, менять не на что")
            else:
                await message.answer(text='Something wrong, no machines to link\n"/start" to continue')

    else:
        await message.answer(text="Вы не авторизованы. Обратитесь за помощью к кому скидывались за стиралку")

#Machine selection menu interaction
@router.message(Form.machine)
async def keyboardMenu_handler(message: Message, state: FSMContext) -> None:
    res = await api_controller.get_machines()
    machines: List[MachineEntity] = create_machineList(res.json())
    machine_id=None
    if type(message.text) is str:
        for i in machines:
            if i.title==message.text:
                machine_id=i.uuid
    
    if machine_id is not None:
        user_id = message.from_user.id
        res = await api_controller.link_machine(user_id,machine_id)
        if res.status_code==201:
            await state.set_state(Form.menu)
            await message.answer(text='Вы успешно авторизованы',reply_markup=nav.mainMenu)
        else:
            await state.clear()
            await message.answer(text='Что-то пошло не так при привязке')
    else:
        await message.answer(text="Неверно указана машинка")

#Main menu interaction
@router.message(Form.menu)
async def keyboardMenu_handler(message: Message, state: FSMContext) -> None:
    user_id = message.from_user.id
    
    if message.text == '📶 Статус':
        res = await api_controller.wash_status(user_id)
        status: StatusEntity = create_status(res.json())

        if status.isActive==False:
            await message.answer(text='Стиралка не занята',reply_markup=nav.occupyMenu)
        else:
            if status.isActive==True:
                if status.telegramTag=='@'+message.from_user.username:
                    await message.answer(text='text', reply_markup=nav.endMenu)
                else:
                    if False:
                        await message.answer(text=f"Стиралка занята\nЕе использует: {status.telegramTag}\nВремя начала использования: {status.timeBegin}",reply_markup=nav.queueMenu)
                    else:
                        await message.answer(text=f"Стиралка занята\nЕе использует: {status.telegramTag}\nВремя начала использования: {status.timeBegin}")
    elif message.text == '🛠️ Admin menu':
        res = await api_controller.get_my(user_id)
        user: UserEntity = create_user(res.json())
        user_is_admin=user.type
        
        if user_is_admin:
            await state.set_state(Form.adminMenu)
            await message.answer(text=f'Вы сейчас администрируете стиралку: {user.link_machine.title}',reply_markup=nav.adminMenu)
        else:
            await message.answer(text='Вы не админ',reply_markup=nav.mainMenu)

    elif message.text == '❓ Помощь':
        await message.answer(text='text')

#Main inline menu actions
@router.callback_query(Form.menu)
async def mainInlineMenu_handler(callback: CallbackQuery, state: FSMContext) -> None:
    user_id=callback.from_user.id
    if callback.data == 'occupy':
        res = await api_controller.wash_status(user_id)
        status: StatusEntity = create_status(res.json())
        
        if status.isActive==False:
            res = await api_controller.wash_occupy(user_id)
            if res.status_code==201:
                await callback.message.edit_reply_markup(inline_message_id=callback.inline_message_id,reply_markup=nav.endMenu)
                await callback.answer()
            else:
                await callback.answer()
        else:
            await callback.answer()

    elif callback.data == 'queue':
        await callback.message.edit_reply_markup(inline_message_id=callback.inline_message_id,reply_markup=nav.in_queueMenu)
        await callback.answer()

    elif callback.data == 'free':
        await return_to_statusMenu(callback)
        await callback.answer()

    elif callback.data == 'end':
        res = await api_controller.wash_status(user_id)
        status: StatusEntity = create_status(res.json())
        
        if status.isActive:
            res = await api_controller.wash_end(user_id)

            if res.status_code==201:
                time: TimeEntity = create_time(res.json())
                await return_to_statusMenu(callback)
                await callback.answer(text=f'Стирка заняла: {time.elapsedTime} мин')
            else:
                await callback.answer(text='Что-то пошло не так')
    elif callback.data == 'report':
        await callback.message.edit_text(text='Выберите проблему из списка:')
        await callback.message.edit_reply_markup(inline_message_id=callback.inline_message_id,reply_markup=nav.reportMenu)
    
    elif callback.data == 'forgotten':
        await state.set_state(Form.forgotten_cloth)
        await callback.message.edit_text(text='Пришлите фото забытых вещей:')
        await callback.message.edit_reply_markup(inline_message_id=callback.inline_message_id,reply_markup=nav.cancelPrompt)
        await callback.answer()

    elif callback.data == "occupied":
        await state.set_state(Form.occupied_confirmation)
        await callback.message.edit_text(text='Вы уверены?')
        await callback.message.edit_reply_markup(inline_message_id=callback.inline_message_id,reply_markup=nav.confirmationPrompt)
        await callback.answer()

    elif callback.data == 'break':
        await state.set_state(Form.break_confirmation)
        await callback.message.edit_text(text='Вы уверены?')
        await callback.message.edit_reply_markup(inline_message_id=callback.inline_message_id,reply_markup=nav.confirmationPrompt)
        await callback.answer()

#Admin inline menu actions
@router.callback_query(Form.adminMenu)
async def adminInlineMenu_handler(callback: CallbackQuery, state: FSMContext) -> None:
    user_id=callback.from_user.id

    res = await api_controller.get_my(user_id)
    user: UserEntity = create_user(res.json())
    user_is_admin=user.type
    

    if user_is_admin:
        
        if callback.data == 'add_user':
            pass
        elif callback.data == 'kick_user':
            pass
        elif callback.data == 'stop_machine':
            pass
        elif callback.data == 'force_end':
            pass
        elif callback.data == 'fix':
            pass
        elif callback.data == 'change_admin':
            pass

    else:
        await callback.message.edit_text(text='Вы не админ')
        await callback.message.delete_reply_markup()
        await callback.answer()

#Returning inline menu into status menu
async def return_to_statusMenu(callback: CallbackQuery) -> None:
    user_id=callback.from_user.id

    res = await api_controller.wash_status(user_id)
    status: StatusEntity = create_status(res.json())

    if not status.isActive:
        await callback.message.edit_text(text='Стиралка не занята')
        await callback.message.edit_reply_markup(inline_message_id=callback.inline_message_id,reply_markup=nav.occupyMenu)
    else:
        if status.isActive:
            if status.telegramTag=='@'+callback.from_user.username:
                await callback.message.edit_text(text='text')
                await callback.message.edit_reply_markup(inline_message_id=callback.inline_message_id, reply_markup=nav.endMenu)
            else:
                if False:
                    await callback.message.edit_text(text=f"Стиралка занята\nЕе использует: {status['telegramTag']}\nВремя начала использования: {status['timeBegin']}")
                    await callback.message.edit_reply_markup(inline_message_id=callback.inline_message_id,reply_markup=nav.queueMenu)
                else:
                    await callback.message.edit_text(text=f"Стиралка занята\nЕе использует: {status['telegramTag']}\nВремя начала использования: {status['timeBegin']}")
                    await callback.message.delete_reply_markup()

#Managing forgotten cloth prompt
@router.message(Form.forgotten_cloth)
async def forgotten_cloth_photo(message: Message, state: FSMContext) -> None:
    user_id=message.from_user.id
    if message.photo is not None:
        await state.set_state(Form.menu)
        await message.answer(text='Люди были уведомлены')

@router.callback_query(Form.forgotten_cloth)
async def forgotten_cloth_cancel(callback: CallbackQuery, state: FSMContext) -> None:
    user_id=callback.from_user.id
    if callback.data == 'cancel':
        await state.set_state(Form.menu)
        await return_to_statusMenu(callback)

#Break confirmation
@router.callback_query(Form.break_confirmation)
async def break_confirmation(callback: CallbackQuery, state: FSMContext) -> None:
    user_id=callback.from_user.id
    if callback.data == 'yes':
        await state.set_state(Form.menu)
        await return_to_statusMenu(callback)
        await callback.answer(text='broke')
    
    elif callback.data == 'no':
        await state.set_state(Form.menu)
        await return_to_statusMenu(callback)
        await callback.answer()

#Occupied confirmation
@router.callback_query(Form.occupied_confirmation)
async def occupied_confirmation(callback: CallbackQuery, state: FSMContext) -> None:
    user_id=callback.from_user.id
    if callback.data == 'yes':
        await state.set_state(Form.menu)
        await return_to_statusMenu(callback)
        await callback.answer(text='occupied')
    
    elif callback.data == 'no':
        await state.set_state(Form.menu)
        await return_to_statusMenu(callback)
        await callback.answer()

