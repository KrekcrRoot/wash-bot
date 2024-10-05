
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
from app.dto.machine_entity import MachineEntity, create_machine
from app.dto.status_entity import StatusEntity, create_status
from app.dto.order_entity import OrderEntity, create_orderEntity
from app.dto.elapsed_time_dto import ElapsedTime_Dto, create_time
from app.dto.admin_check_dto import AdminCheckDto, create_admin_check_dto
from app.dto.status_enum import Status
from app.dto.status_codes_enum import StatusCode
from app.dto.callback_codes import CallbackData

router = Router()
api_controller = init_api_controller()

#States to separate some menus
class Form(StatesGroup):
    forgotten_cloth = State()
    occupied_confirmation = State()
    break_confirmation = State()
    machine = State()
    changing_title = State()
    menu = State()
    adminMenu = State()
    adding_user = State()
    kicking_user = State()
    stopping_machine = State()
    transfering_rights = State()

#Authorization thing
@router.message(CommandStart())
async def command_start_handler(message: Message, state:FSMContext) -> None:

    user_tag = message.from_user.username
    user_id = message.from_user.id

    if user_tag is None: 
        user_is_authorized = False
    else:
        res = await api_controller.auth(user_tag, user_id)
        user_is_authorized = StatusCode(res.status_code)==StatusCode.OK

    if user_is_authorized:

        res = await api_controller.user_info(user_id)
        user: UserEntity = create_user(res.json())

        res = await api_controller.user_machines(user_id)
        machines: List[MachineEntity] = create_machine(res.json())

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
    await state.clear()
    await message.answer(text=t.action_canceled)

#Info command interaction
@router.message(Command("info"))
async def help_command(message: Message) -> None:
    user_id = message.from_user.id

    res = await api_controller.user_info(user_id)
    user: UserEntity = create_user(res.json())

    res = await api_controller.user_machines(user_id)
    machines: List[MachineEntity] = create_machine(res.json())

    await message.answer(text=t.menu_info(user, machines))

#Help command interaction
@router.message(Command("help"))
async def help_command(message: Message) -> None:
    await message.answer(text=t.help)

#Changing selected machine
@router.message(Command("change_machine"))
async def changing_machine(message: Message, state:FSMContext) -> None:
    user_tag = message.from_user.username
    user_id = message.from_user.id

    if user_tag is None: 
        user_is_authorized = False
    else:
        res = await api_controller.auth(user_tag, user_id)
        user_is_authorized = StatusCode(res.status_code)==StatusCode.OK

    if user_is_authorized:
        res = await api_controller.user_info(user_id)
        user: UserEntity = create_user(res.json())

        if user.link_machine is not None:
            res = await api_controller.user_machines(user_id)
            machines: List[MachineEntity] = create_machine(res.json())
            if len(machines)>1 or True:
                res = await api_controller.unlink_machine(user_id)
                if StatusCode(res.status_code)==StatusCode.OK:
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

    machines: List[MachineEntity] = create_machine(res.json())
    machine_id=None
    if type(message.text) is str:
        for i in machines:
            if i.title==message.text:
                machine_id=i.uuid
    
    if machine_id is not None:
        res = await api_controller.link_machine(user_id,machine_id)
        if StatusCode(res.status_code)==StatusCode.OK:
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

#Changing machine title
@router.message(Form.changing_title)
async def changing_machine_title(message: Message, state: FSMContext) -> None:
    user_id = message.from_user.id

    res = await api_controller.admin_check(user_id)
    admin: AdminCheckDto = create_admin_check_dto(res.json())
    

    if admin.isAdmin:
        if message.text is not None:
            res = await api_controller.admin_change_machine_title(user_id, message.text)
            status_code = res.status_code

            res = await api_controller.user_info(user_id)
            user: UserEntity = create_user(res.json())
            

            if StatusCode(status_code) == StatusCode:
                await state.set_state(Form.adminMenu)
                await message.answer(text=t.machine_title_changed+'\n\n'+t.admin_machine(user.link_machine.title), reply_markup=nav.adminMenu)
            else:
                await state.set_state(Form.adminMenu)
                await message.answer(text=t.error_machine_changing_title+'\n\n'+t.admin_machine(user.link_machine.title), reply_markup=nav.adminMenu)
        else:
            await message.answer(text=t.error_machine_changing_title_format)
    else:
        await state.set_state(Form.menu)
        await message.answer(text=t.error_user_not_admin, reply_markup=nav.mainMenu)

#Stopping machine
@router.message(Form.stopping_machine)
async def stopping_machine(message: Message, state: FSMContext) -> None:
    user_id = message.from_user.id

    res = await api_controller.admin_check(user_id)
    admin: AdminCheckDto = create_admin_check_dto(res.json())
    

    if admin.isAdmin:
        if message.text is not None:
            res = await api_controller.admin_stop_machine(user_id, message.text)
            status_code = res.status_code

            res = await api_controller.user_info(user_id)
            user: UserEntity = create_user(res.json())
            

            if StatusCode(status_code) == StatusCode.OK:
                await state.set_state(Form.adminMenu)
                await message.answer(text=t.admin_machine_stopped+'\n\n'+t.admin_machine(user.link_machine.title), reply_markup=nav.adminMenu)
            else:
                await state.set_state(Form.adminMenu)
                await message.answer(text=t.error_stopping_machine+'\n\n'+t.admin_machine(user.link_machine.title), reply_markup=nav.adminMenu)
        else:
            await message.answer(text=t.error_stopping_machine_format)
    else:
        await state.set_state(Form.menu)
        await message.answer(text=t.error_user_not_admin, reply_markup=nav.mainMenu)

#Transfering rights
@router.message(Form.transfering_rights)
async def transfering_rights(message: Message, state: FSMContext) -> None:
    user_id = message.from_user.id

    res = await api_controller.admin_check(user_id)
    admin: AdminCheckDto = create_admin_check_dto(res.json())
    

    if admin.isAdmin:
        if type(message.text) is str and message.text[0] == '@' and ' ' not in message.text and '\n' not in message.text:
            res = await api_controller.admin_transfer_rights(user_id, message.text)
            status_code = res.status_code

            res = await api_controller.user_info(user_id)
            user: UserEntity = create_user(res.json())
            

            if StatusCode(status_code) == StatusCode.OK:
                await state.set_state(Form.menu)
                await message.answer(text=t.admin_rights_transfered)
            else:
                await state.set_state(Form.adminMenu)
                await message.answer(text=t.error_transfering_rights+'\n\n'+t.admin_machine(user.link_machine.title), reply_markup=nav.adminMenu)
        else:
            await message.answer(text=t.error_transfering_rights_format)
    else:
        await state.set_state(Form.menu)
        await message.answer(text=t.error_user_not_admin, reply_markup=nav.mainMenu)

#Main menu interaction
@router.message(Form.menu)
@router.message(Form.adminMenu)
async def keyboardMenu_handler(message: Message, state: FSMContext) -> None:
    user_id = message.from_user.id
    
    if message.text == t.menu_status:
        res = await api_controller.wash_status(user_id)
        status: StatusEntity = create_status(res.json())

        await state.set_state(Form.menu)
        
        if Status[status.status] == Status.Broken:
            await message.answer(text=t.status_broken(status.reportBody))
        elif Status[status.status] == Status.Free:
            await message.answer(text=t.status_free,reply_markup=nav.occupyMenu)
        elif Status[status.status] == Status.Busy:
            if status.telegramTag == '@'+message.from_user.username:
                    await message.answer(text=t.wash_executes, reply_markup=nav.endMenu)
            else:
                await message.answer(text=t.status_busy(status.telegramTag, status.timeBegin),reply_markup=nav.queueMenu)
        elif Status[status.status] == Status.Ordered:
            if status.telegramTag == '@'+message.from_user.username:
                    await message.answer(text=t.wash_executes, reply_markup=nav.endMenu)
            else:
                res = await api_controller.get_order(user_id)
                waiter: OrderEntity = create_orderEntity(res.json())

                if waiter.user.telegram_id == str(user_id):
                    await message.answer(text=t.wash_executes_queue, reply_markup=nav.in_queueMenu)
                else:
                    await message.answer(text=t.status_ordered(status.telegramTag, status.timeBegin, waiter.user.telegram_tag))
        elif Status[status.status]==Status.Waiting:
            if status.telegramTag=='@'+message.from_user.username:
                    await message.answer(text=t.wash_queue, reply_markup=nav.waitingMenu)
            else:
                await message.answer(text=t.status_waiting(status.telegramTag, status.timeBegin))
        
    elif message.text == t.menu_admin:
        res = await api_controller.admin_check(user_id)
        admin: AdminCheckDto = create_admin_check_dto(res.json())
        
        if admin.isAdmin:
            res = await api_controller.user_info(user_id)
            user: UserEntity = create_user(res.json())

            await state.set_state(Form.adminMenu)
            await message.answer(text=t.admin_machine(user.link_machine.title), reply_markup=nav.adminMenu)
        else:
            await message.answer(text=t.error_user_not_admin, reply_markup=nav.mainMenu)

    elif message.text == t.menu_help:
        await message.answer(text=t.help)

#Main inline menu actions
@router.callback_query(Form.menu)
async def mainInlineMenu_handler(callback: CallbackQuery, state: FSMContext) -> None:
    user_id=callback.from_user.id
    if callback.data == CallbackData.occupy:
        res = await api_controller.wash_status(user_id)
        status: StatusEntity = create_status(res.json())
        
        if Status[status.status]==Status.Free:
            res = await api_controller.wash_occupy(user_id)
            if StatusCode(res.status_code)==StatusCode.OK:
                await callback.message.edit_text(text=t.wash_executes)
                await callback.message.edit_reply_markup(inline_message_id=callback.inline_message_id,reply_markup=nav.endMenu)
                await callback.answer()
            else:
                await callback.answer(text=t.error_wash_occupy)
        else:
            await callback.answer(text=t.error_wash_occupy)
    elif callback.data == CallbackData.occupy_from_queue:
        res = await api_controller.wash_status(user_id)
        status: StatusEntity = create_status(res.json())

        if Status[status.status]==Status.Waiting and '@'+callback.from_user.username == status.telegramTag:
            res = await api_controller.wash_occupy(user_id)
            if StatusCode(res.status_code) == StatusCode.OK:
                await callback.message.edit_text(text=t.wash_executes)
                await callback.message.edit_reply_markup(inline_message_id=callback.inline_message_id,reply_markup=nav.endMenu)
                await callback.answer()
            else:
                await callback.answer(text=t.error_wash_occupy)
        else:
            await callback.answer(text=t.error_wash_occupy)

    elif callback.data == CallbackData.queue:
        res = await api_controller.wash_status(user_id)
        status: StatusEntity = create_status(res.json())
        
        if Status[status.status]==Status.Busy:
            res = await api_controller.wash_occupy_order(user_id)

            if StatusCode(res.status_code) == StatusCode.OK:
                await callback.message.edit_text(text=t.wash_executes_queue)
                await callback.message.edit_reply_markup(inline_message_id=callback.inline_message_id,reply_markup=nav.in_queueMenu)
                await callback.answer()
            else:
                await callback.answer(text=t.error_wash_queue)
        else:
            await callback.answer(text=t.error_wash_queue)

    elif callback.data == CallbackData.free:
        res = await api_controller.wash_status(user_id)
        status: StatusEntity = create_status(res.json())
        
        if Status[status.status] == Status.Ordered or Status[status.status] == Status.Waiting:
            res = await api_controller.cancel_order(user_id)

            if StatusCode(res.status_code) == StatusCode.OK:
                await return_to_statusMenu(callback)
                await callback.answer()
            else:
                await callback.answer(text=t.error_order_free)
        else:
            await callback.answer(text=t.error_order_free)

    elif callback.data == CallbackData.end:
        res = await api_controller.wash_status(user_id)
        status: StatusEntity = create_status(res.json())
        
        if status.telegramTag == '@'+callback.from_user.username:
            if Status[status.status]==Status.Busy or Status[status.status]==Status.Ordered:
                res = await api_controller.wash_end(user_id)

                if StatusCode(res.status_code) == StatusCode.OK:
                    time: ElapsedTime_Dto = create_time(res.json())

                    await callback.message.edit_text(text=t.time_elapsed(time.elapsedTime))
                    await callback.message.delete_reply_markup()
                    await callback.answer()
                else:
                    await callback.answer(text=t.error_wash_end)
            else:
                await callback.answer(text=t.error_wash_end)
        else:
            await callback.answer(text=t.error_wash_end)

    elif callback.data == CallbackData.report:
        await callback.message.edit_text(text=t.report_select)
        await callback.message.edit_reply_markup(inline_message_id=callback.inline_message_id,reply_markup=nav.reportMenu)
    
    elif callback.data == CallbackData.forgotten:
        await state.set_state(Form.forgotten_cloth)
        await callback.message.edit_text(text=t.report_forgotten_photo)
        await callback.message.edit_reply_markup(inline_message_id=callback.inline_message_id,reply_markup=nav.cancelPrompt)
        await callback.answer()

    elif callback.data == CallbackData.occupied:
        await state.set_state(Form.occupied_confirmation)
        await callback.message.edit_text(text=t.confirm_occupy)
        await callback.message.edit_reply_markup(inline_message_id=callback.inline_message_id,reply_markup=nav.confirmationPrompt)
        await callback.answer()

    elif callback.data == CallbackData.broke:
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
        
        if callback.data == CallbackData.add_user:
            await state.set_state(Form.adding_user)
            await callback.message.edit_text(text=t.admin_add_user)
            await callback.message.delete_reply_markup()
            await callback.answer()

        elif callback.data == CallbackData.kick_user:
            res = await api_controller.admin_get_machine_users(user_id)
            users: List[UserEntity] = create_user(res.json())

            if StatusCode(res.status_code)==StatusCode.OK:
                if len(users)>0:
                    await callback.message.edit_text(text=t.admin_kick_user)
                    await callback.message.edit_reply_markup(inline_message_id=callback.inline_message_id, reply_markup=nav.kickMenu(users))
                    await state.set_state(Form.kicking_user)
                    await callback.answer()
                else:
                    await callback.answer(text=t.error_admin_kick_user_none)
            else:
                await callback.answer(text=t.error_admin_kick_user_list)

        elif callback.data == CallbackData.fix:
            res = await api_controller.admin_fix(user_id)

            if StatusCode(res.status_code) == StatusCode.OK:
                await callback.answer(text=t.admin_machine_fixed)
            else:
                await callback.answer(text=t.error_machine_fix)
            
        elif callback.data == CallbackData.stop_machine:
            await state.set_state(Form.stopping_machine)
            await callback.message.edit_text(text=t.admin_stopping_machine)
            await callback.message.delete_reply_markup()
            await callback.answer()            

        elif callback.data == CallbackData.force_end:
            res = await api_controller.wash_status(user_id)
            status: StatusEntity = create_status(res.json())

            if Status[status.status]==Status.Busy or Status[status.status]==Status.Ordered:
                res = await api_controller.wash_end(user_id)

                if StatusCode(res.status_code) == StatusCode.OK:
                    time: ElapsedTime_Dto = create_time(res.json())

                    await callback.message.edit_text(text=t.time_elapsed(time.elapsedTime))
                    await callback.message.delete_reply_markup()
                    await callback.answer()
                else:
                    await callback.answer(text=t.error_wash_end)
            else:
                await callback.answer(text=t.error_wash_end)
                
        elif callback.data == CallbackData.change_title:
            await state.set_state(Form.changing_title)
            await callback.message.edit_text(text=t.machine_changing_title)
            await callback.message.delete_reply_markup()
            await callback.answer()

        elif callback.data == CallbackData.change_admin:
            await state.set_state(Form.transfering_rights)
            await callback.message.edit_text(text=t.admin_transfering_rights)
            await callback.message.delete_reply_markup()
            await callback.answer()

    else:
        await callback.message.edit_text(text=t.error_user_not_admin)
        await callback.message.delete_reply_markup()
        await callback.answer()

#Adding user prompt
@router.message(Form.adding_user)
async def admin_adding_user(message: Message, state: FSMContext) -> None:
    user_id = message.from_user.id
    wrong_format = False

    if type(message.text)==str:
        m = message.text.split()

        if len(m) == 2:
            if m[0][0] == '@':
                telegram_tag = m[0]
                nums = '0123456789'
                if 5<=len(m[1])<=6 and m[1][-2]=='/' and m[1][-1] in '23' and all([False for i in m[1][:-2] if i not in nums]):
                    room = m[1]
                else:
                    wrong_format = True
            else:
                wrong_format = True
        else:
            wrong_format = True
    else:
        wrong_format = True

    res = await api_controller.admin_check(user_id)
    admin: AdminCheckDto = create_admin_check_dto(res.json())
    
    if admin.isAdmin:
        res = await api_controller.user_info(user_id)
        user: UserEntity = create_user(res.json())
        
        await state.set_state(Form.adminMenu)
        if wrong_format:
            await message.answer(text=t.error_admin_user_wrong_format+'\n\n'+t.admin_machine(user.link_machine.title), reply_markup=nav.adminMenu)
        else:
            res = await api_controller.admin_join(user_id, telegram_tag, room)

            if StatusCode(res.status_code)== StatusCode.OK:
                await message.answer(text=t.admin_user_added+'\n\n'+t.admin_machine(user.link_machine.title), reply_markup=nav.adminMenu)
            else:
                await message.answer(text=t.error_admin_add_user+'\n\n'+t.admin_machine(user.link_machine.title), reply_markup=nav.adminMenu)
    else:
        await message.answer(text=t.error_user_not_admin, reply_markup=nav.mainMenu)     

#Kicking user prompt
@router.callback_query(Form.kicking_user)
async def admin_kicking_user(callback: CallbackQuery, state: FSMContext) -> None:
    user_id = callback.from_user.id
    telegram_tag = callback.data

    res = await api_controller.admin_check(user_id)
    admin: AdminCheckDto = create_admin_check_dto(res.json())
    
    if admin.isAdmin:
        res = await api_controller.user_info(user_id)
        user: UserEntity = create_user(res.json())

        await state.set_state(Form.adminMenu)
        res = await api_controller.admin_kick(user_id, telegram_tag)

        if StatusCode(res.status_code) == StatusCode.OK:
            await callback.message.edit_text(text=t.admin_user_kicked+'\n\n'+t.admin_machine(user.link_machine.title))
            await callback.message.edit_reply_markup(inline_message_id=callback.inline_message_id, reply_markup=nav.adminMenu)
            await callback.answer()
        else:
            await callback.message.edit_text(text=t.error_admin_kick_user+'\n\n'+t.admin_machine(user.link_machine.title))
            await callback.message.edit_reply_markup(inline_message_id=callback.inline_message_id, reply_markup=nav.adminMenu)
            await callback.answer()
    else:
        await state.set_state(Form.menu)
        await callback.message.edit_text(text=t.error_user_not_admin)
        await callback.message.edit_reply_markup(inline_message_id=callback.inline_message_id, reply_markup=nav.mainMenu)
        await callback.answer()         

#Returning inline menu into status menu
async def return_to_statusMenu(callback: CallbackQuery) -> None:
    user_id=callback.from_user.id

    res = await api_controller.wash_status(user_id)
    status: StatusEntity = create_status(res.json())

    if Status[status.status] == Status.Broken:
        await callback.message.edit_text(text=t.status_broken(status.reportBody))
        await callback.message.delete_reply_markup()
        await callback.answer()

    elif Status[status.status]==Status.Free:
        await callback.message.edit_text(text=t.status_free)
        await callback.message.edit_reply_markup(reply_markup=nav.occupyMenu)
        await callback.answer()

    elif Status[status.status]==Status.Busy:
        if status.telegramTag=='@'+callback.from_user.username:
                await callback.message.edit_text(text=t.wash_executes)
                await callback.message.edit_reply_markup(reply_markup=nav.endMenu)
                await callback.answer()
        else:
            await callback.message.edit_text(text=t.status_busy(status.telegramTag, status.timeBegin))
            await callback.message.edit_reply_markup(reply_markup=nav.queueMenu)
            await callback.answer()

    elif Status[status.status]==Status.Ordered:
        if status.telegramTag=='@'+callback.from_user.username:
                await callback.message.edit_text(text=t.wash_executes)
                await callback.message.edit_reply_markup(reply_markup=nav.endMenu)
                await callback.answer()
        else:
            res = await api_controller.get_order(user_id)
            waiter: OrderEntity = create_orderEntity(res.json())

            if waiter.user.telegram_id==user_id:
                await callback.message.edit_text(text=t.wash_executes_queue)
                await callback.message.edit_reply_markup(reply_markup=nav.queueMenu)
                await callback.answer()
            else:
                await callback.message.edit_text(text=t.status_ordered(status.telegramTag, status.timeBegin, waiter.user.telegram_tag))
                await callback.message.delete_reply_markup
                await callback.answer()

    elif Status[status.status]==Status.Waiting:
        if status.telegramTag=='@'+callback.from_user.username:
                await callback.message.edit_text(text=t.wash_executes)
                await callback.message.edit_reply_markup(reply_markup=nav.waitingMenu)
                await callback.answer
        else:
            await callback.message.edit_text(text=t.status_waiting)
            await callback.message.edit_reply_markup(reply_markup=nav.queueMenu)
            await callback.answer()


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
    if callback.data == CallbackData.cancel:
        await state.set_state(Form.menu)
        await return_to_statusMenu(callback)

#Break confirmation
@router.callback_query(Form.break_confirmation)
async def break_confirmation(callback: CallbackQuery, state: FSMContext) -> None:
    user_id=callback.from_user.id
    if callback.data == CallbackData.yes:
        res = await api_controller.report_break(user_id)

        if StatusCode(res.status_code) == StatusCode.OK:
            await state.set_state(Form.menu)
            await callback.answer(text=t.report_broke_noticed)
            await return_to_statusMenu(callback)
        else:
            await state.set_state(Form.menu)
            await callback.answer(text=t.error_report_broke)
            await return_to_statusMenu(callback)
    
    elif callback.data == CallbackData.no:
        await state.set_state(Form.menu)
        await return_to_statusMenu(callback)
        await callback.answer()

#Occupied confirmation
@router.callback_query(Form.occupied_confirmation)
async def occupied_confirmation(callback: CallbackQuery, state: FSMContext) -> None:
    user_id=callback.from_user.id
    if callback.data == CallbackData.yes:
        await state.set_state(Form.menu)
        await return_to_statusMenu(callback)
        await callback.answer(text='occupied')
    
    elif callback.data == CallbackData.no:
        await state.set_state(Form.menu)
        await return_to_statusMenu(callback)
        await callback.answer()

