
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command, CommandStart
from aiogram import Router

import json
import app.markups as nav
from app.api import init_api_controller
from app.dto.user_entity import UserEntity
from app.dto.machine_entity import MachineEntity

router = Router()
api_controller = init_api_controller()

#States to separate some menus
class Form(StatesGroup):
    forgotten_cloth = State()
    break_confirmation = State()
    machine = State()
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
        user = json.loads(res.text)

        if user['link_machine'] is not None:
            await state.set_state(Form.menu)
            user_is_admin=user['type']
            if user_is_admin:
                await message.answer(text='text',reply_markup=nav.mainMenuAdmin)
            else:
                await message.answer(text='text',reply_markup=nav.mainMenu)
        else:
            res = await api_controller.get_machines()
            machines = json.loads(res.text)
            if True:
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
        user = json.loads(res.text)

        if user['link_machine'] is not None:
            res = await api_controller.get_machines()
            machines = json.loads(res.text)
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
    machines = json.loads(res.text)
    machine_id=None
    if type(message.text) is str:
        for i in machines:
            if i['title']==message.text:
                machine_id=i['uuid']
    
    if machine_id is not None:
        user_id = message.from_user.id
        print(user_id,machine_id)
        res = await api_controller.link_machine(user_id,machine_id)
        if res.status_code==201:
            await state.set_state(Form.menu)
            await message.answer(text='text',reply_markup=nav.mainMenu)
        else:
            await state.clear()
            await message.answer(text='Что-то пошло не так при привязке')
    else:
        await message.answer(text="Неверно указана машинка")

#Main menu interaction
@router.message(Form.menu)
async def keyboardMenu_handler(message: Message) -> None:
    user_id = message.from_user.id
    
    if message.text == '📶 Статус':
        res = await api_controller.wash_status(user_id)
        status = json.loads(res.text)

        if status['isActive']==False:
            await message.answer(text='Стиралка не занята',reply_markup=nav.occupyMenu)
        else:
            if status['isActive']==True:
                if status['telegramTag']=='@'+message.from_user.username:
                    await message.answer(text='text', reply_markup=nav.endMenu)
                else:
                    if False:
                        await message.answer(text=f"Стиралка занята\nЕе использует: {status['telegramTag']}\nВремя начала использования: {status['timeBegin']}",reply_markup=nav.queueMenu)
                    else:
                        await message.answer(text=f"Стиралка занята\nЕе использует: {status['telegramTag']}\nВремя начала использования: {status['timeBegin']}")
    elif message.text == '🛠️ Admin menu':
        await message.answer(text='text',reply_markup=nav.adminMenu)

    elif message.text == '❓ Помощь':
        await message.answer(text='text')

#Handling inline menu actions
@router.callback_query(Form.menu)
async def inlineMenu_handler(callback: CallbackQuery, state: FSMContext) -> None:
    user_id=callback.from_user.id
    if callback.data == 'occupy':
        res = await api_controller.wash_status(user_id)
        status = json.loads(res.text)
        
        if status['isActive']==False:
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
        status = json.loads(res.text)
        
        if status['isActive']==True:
            res = await api_controller.wash_end(user_id)

            if res.status_code==201:
                time = json.loads(res.text)
                await return_to_statusMenu(callback)
                await callback.answer(text='Стирка заняла: '+str(time['elapsedTime'])+'мин')
            else:
                await callback.answer(text='Что-то пошло не так')
    
    elif callback.data == 'forgotten':
        await state.set_state(Form.forgotten_cloth)
        await callback.message.edit_text(text='Пришлите фото забытых вещей:')
        await callback.message.edit_reply_markup(inline_message_id=callback.inline_message_id,reply_markup=nav.cancelPrompt)
        await callback.answer()

    elif callback.data == 'break':
        await state.set_state(Form.break_confirmation)
        await callback.message.edit_text(text='Вы уверены?')
        await callback.message.edit_reply_markup(inline_message_id=callback.inline_message_id,reply_markup=nav.confirmationPrompt)
        await callback.answer()

#Returning inline menu into status menu
async def return_to_statusMenu(callback: CallbackQuery) -> None:
    status='free'
    if status=='free':
        await callback.message.edit_text(text='text')
        await callback.message.edit_reply_markup(inline_message_id=callback.inline_message_id,reply_markup=nav.occupyMenu)
    elif status=='in work':
        await callback.message.edit_text(text='text')
        await callback.message.edit_reply_markup(inline_message_id=callback.inline_message_id,reply_markup=nav.queueMenu)
    else:
        await callback.message.edit_text(text='Занято')
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
        await callback.message.edit_text(text='text')
        await callback.message.edit_reply_markup(inline_message_id=callback.inline_message_id,reply_markup=nav.endMenu)
        await callback.answer()
