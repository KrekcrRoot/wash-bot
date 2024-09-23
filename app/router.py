
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command, CommandStart
from aiogram import Router
from typing import List

import json
import app.markups as nav
import app.texts as t
from app.api import init_api_controller
from app.dto.user_entity import UserEntity, create_user
from app.dto.machine_entity import MachineEntity, create_machineList
from app.dto.status_entity import StatusEntity, create_status
from app.dto.order_entity import OrderEntity, create_orderEntity
from app.dto.elapsed_time_dto import ElapsedTime_Dto, create_time
from app.dto.admin_check_dto import AdminCheckDto, create_admin_check_dto
from app.dto.status_enum import Status

router = Router()
api_controller = init_api_controller()

#States to separate some menus
class Form(StatesGroup):
    forgotten_cloth = State()
    occupied_confirmation = State()
    break_confirmation = State()
    machine = State()
    menu = State()
    adminMenu = State()

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

        res = await api_controller.user_info(user_id)
        user: UserEntity = create_user(res.json())

        res = await api_controller.get_machines()
        machines: List[MachineEntity] = create_machineList(res.json())

        if user.link_machine is not None:
            await state.set_state(Form.menu)

            res = await api_controller.admin_check(user_id)
            admin: AdminCheckDto = create_admin_check_dto(res.json())

            if len(machines)>1:
                if admin.isAdmin:
                    await message.answer(text=t.auth_success_machine(user.link_machine.title),reply_markup=nav.mainMenuAdmin)
                else:
                    await message.answer(text=t.auth_success_machine(user.link_machine.title),reply_markup=nav.mainMenu)
            else:
                if admin.isAdmin:
                    await message.answer(text=t.auth_success,reply_markup=nav.mainMenuAdmin)
                else:
                    await message.answer(text=t.auth_success,reply_markup=nav.mainMenu)
        else:
            if len(machines)>1 or True:
                await state.set_state(Form.machine)
                await message.answer(text=t.machine_select, reply_markup=nav.machineMenu(machines))
            elif len(machines)==1:
                machine_id = machines[0].uuid
                res = await api_controller.link_machine(user_id,machine_id)
            else:
                message.answer(text=t.machine_no_available)
    else:
        await message.answer(text=t.auth_failed)

#Cancel command (resets state)
@router.message(Command("cancel"))
async def cancel_handler(message: Message, state:FSMContext) -> None:
    if await state.get_state() is not None:
        await state.clear()
        await message.answer(text=t.action_canceled)

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
        res = await api_controller.user_info(user_id)
        user: UserEntity = create_user(res.json())

        if user.link_machine is not None:
            res = await api_controller.get_machines()
            machines: List[MachineEntity] = create_machineList(res.json())
            if len(machines)>1 or True:
                res = await api_controller.unlink_machine(user_id)
                if res.status_code==201:
                    await state.set_state(Form.machine)
                    await message.answer(text=t.machine_select,reply_markup=nav.machineMenu(machines))
            elif len(machines)==1:
                await message.answer(text=t.machine_only_one)
            else:
                await message.answer(text=t.machine_no_available)

    else:
        await message.answer(text=t.auth_failed)

#Machine selection menu interaction
@router.message(Form.machine)
async def keyboardMenu_handler(message: Message, state: FSMContext) -> None:
    user_id = message.from_user.id
    res = await api_controller.user_machines(user_id)

    machines: List[MachineEntity] = create_machineList(res.json())
    machine_id=None
    if type(message.text) is str:
        for i in machines:
            if i.title==message.text:
                machine_id=i.uuid
    
    if machine_id is not None:
        res = await api_controller.link_machine(user_id,machine_id)
        if res.status_code==201:
            await state.set_state(Form.menu)

            res = await api_controller.admin_check(user_id)
            admin: AdminCheckDto = create_admin_check_dto(res.json())

            if admin.isAdmin:
                await message.answer(text=t.auth_success_machine(message.text),reply_markup=nav.mainMenuAdmin)
            else:
                await message.answer(text=t.auth_success_machine(message.text),reply_markup=nav.mainMenu)
            
        else:
            await state.clear()
            await message.answer(text=t.error_machine_link)
    else:
        await message.answer(text=t.error_machine_name)

#Main menu interaction
@router.message(Form.menu)
@router.message(Form.adminMenu)
async def keyboardMenu_handler(message: Message, state: FSMContext) -> None:
    user_id = message.from_user.id
    
    if message.text == '📶 Статус':
        res = await api_controller.wash_status(user_id)
        status: StatusEntity = create_status(res.json())

        await state.set_state(Form.menu)

        if Status[status.status]==Status.Free:
            await message.answer(text=t.status_free,reply_markup=nav.occupyMenu)
        elif Status[status.status]==Status.Busy:
            if status.telegramTag=='@'+message.from_user.username:
                    await message.answer(text='text', reply_markup=nav.endMenu)
            else:
                await message.answer(text=t.status_busy(status.telegramTag, status.timeBegin),reply_markup=nav.queueMenu)
        elif Status[status.status]==Status.Ordered:
            if status.telegramTag=='@'+message.from_user.username:
                    await message.answer(text='text', reply_markup=nav.endMenu)
            else:
                res = await api_controller.order_user(user_id)
                waiter: OrderEntity = create_orderEntity(res.json())


    elif message.text == '🛠️ Admin menu':
        res = await api_controller.user_info(user_id)
        user: UserEntity = create_user(res.json())

        res = await api_controller.admin_check(user_id)
        admin: AdminCheckDto = create_admin_check_dto(res.json())
        
        if admin.isAdmin:
            await state.set_state(Form.adminMenu)
            await message.answer(text=t.admin_machine(user.link_machine.title), reply_markup=nav.adminMenu)
        else:
            await message.answer(text=t.error_user_not_admin, reply_markup=nav.mainMenu)

    elif message.text == '❓ Помощь':
        await message.answer(text='text')

#Main inline menu actions
@router.callback_query(Form.menu)
async def mainInlineMenu_handler(callback: CallbackQuery, state: FSMContext) -> None:
    user_id=callback.from_user.id
    if callback.data == 'occupy':
        res = await api_controller.wash_status(user_id)
        status: StatusEntity = create_status(res.json())
        
        if Status[status.status]==Status.Free:
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
        
        if Status[status.status]==Status.Busy or Status[status.status]==Status.Ordered:
            res = await api_controller.wash_end(user_id)

            if res.status_code==201:
                time: ElapsedTime_Dto = create_time(res.json())

                await callback.message.delete_reply_markup()
                await callback.message.edit_text(text=t.time_elapsed(time.elapsedTime))
                await callback.answer()
            else:
                await callback.answer(text=t.error_wash_end)
    elif callback.data == 'report':
        await callback.message.edit_text(text=t.report_select)
        await callback.message.edit_reply_markup(inline_message_id=callback.inline_message_id,reply_markup=nav.reportMenu)
    
    elif callback.data == 'forgotten':
        await state.set_state(Form.forgotten_cloth)
        await callback.message.edit_text(text=t.report_forgotten_photo)
        await callback.message.edit_reply_markup(inline_message_id=callback.inline_message_id,reply_markup=nav.cancelPrompt)
        await callback.answer()

    elif callback.data == "occupied":
        await state.set_state(Form.occupied_confirmation)
        await callback.message.edit_text(text=t.confirm_occupy)
        await callback.message.edit_reply_markup(inline_message_id=callback.inline_message_id,reply_markup=nav.confirmationPrompt)
        await callback.answer()

    elif callback.data == 'break':
        await state.set_state(Form.break_confirmation)
        await callback.message.edit_text(text=t.confirm_break)
        await callback.message.edit_reply_markup(inline_message_id=callback.inline_message_id,reply_markup=nav.confirmationPrompt)
        await callback.answer()

#Admin inline menu actions
@router.callback_query(Form.adminMenu)
async def adminInlineMenu_handler(callback: CallbackQuery, state: FSMContext) -> None:
    user_id=callback.from_user.id

    res = await api_controller.admin_check(user_id)
    admin: AdminCheckDto = create_admin_check_dto(res.json())
    

    if admin.isAdmin:
        
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
        await callback.message.edit_text(text=t.error_user_not_admin)
        await callback.message.delete_reply_markup()
        await callback.answer()

#Returning inline menu into status menu
async def return_to_statusMenu(callback: CallbackQuery) -> None:
    user_id=callback.from_user.id

    res = await api_controller.wash_status(user_id)
    status: StatusEntity = create_status(res.json())

    if Status[status.status]==Status.Free:
        await callback.message.edit_text(text=t.status_free)
        await callback.message.edit_reply_markup(inline_message_id=callback.inline_message_id,reply_markup=nav.occupyMenu)


#Managing forgotten cloth prompt
@router.message(Form.forgotten_cloth)
async def forgotten_cloth_photo(message: Message, state: FSMContext) -> None:
    user_id=message.from_user.id
    if message.photo is not None:
        await state.set_state(Form.menu)
        await message.answer(text=t.report_forgotten_noticed)

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

