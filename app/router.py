
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import CommandStart
from aiogram import Router

import json
import app.markups as nav
from app.callback import return_to_statusMenu
from app.api import init_api_controller
from app.dto.user_entity import UserEntity
from app.dto.machine_entity import MachineEntity

router = Router()
api_controller = init_api_controller()

class Form(StatesGroup):
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
        user = json.loads(res.text, object_hook=lambda d: UserEntity(**d))

        if user.link_machine is not None:
            await state.set_state(Form.menu)
            user_is_admin=user.type
            if user_is_admin:
                await message.answer(text='text',reply_markup=nav.mainMenuAdmin)
            else:
                await message.answer(text='text',reply_markup=nav.mainMenu)
        else:
            res = await api_controller.get_machines()
            machines = json.loads(res.text, object_hook=lambda d: MachineEntity(**d))
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

#Machine selection menu interaction
@router.message(Form.machine)
async def keyboardMenu_handler(message: Message, state: FSMContext) -> None:
    res = await api_controller.get_machines()
    machines = json.loads(res.text, object_hook=lambda d: MachineEntity(**d))
    machine_id=None
    for i in machines:
        if i.title==message.text:
            machine_id=i.uuid
    
    if machine_id is not None:
        user_id = message.from_user.id
        res = await api_controller.link_machine(user_id,machine_id)
        if res.status_code==201:
            state.set_state(Form.menu)
            await message.answer(text='text',reply_markup=nav.mainMenu)
        else:
            state.clear()
            await message.answer(text='Что-то пошло не так при привязке')
    else:
        state.clear()
        await message.answer(text="Неверно указана машинка")

#Main menu interaction
@router.message(Form.menu)
async def keyboardMenu_handler(message: Message) -> None:
    if message.text == '📶 Статус':
        status='free'
        if status=='free':
            await message.answer(text='text',reply_markup=nav.occupyMenu)
        elif status=='in work':
            await message.answer(text='text',reply_markup=nav.queueMenu)
        else:
            await message.answer(text='Занято')
    elif message.text == '🛠️ Admin menu':
        await message.answer(text='text',reply_markup=nav.adminMenu)

    elif message.text == '❓ Помощь':
        await message.answer(text='text')



#Handling inline menu actions
@router.callback_query()
async def inlineMenu_handler(callback: CallbackQuery) -> None:

    if callback.data == 'occupy':
        await callback.message.edit_reply_markup(inline_message_id=callback.inline_message_id,reply_markup=nav.endMenu)
        await callback.answer()

    elif callback.data == 'queue':
        await callback.message.edit_reply_markup(inline_message_id=callback.inline_message_id,reply_markup=nav.in_queueMenu)
        await callback.answer()

    elif callback.data == 'free':
        await return_to_statusMenu(callback)
        await callback.answer()

    elif callback.data == 'end':
        await return_to_statusMenu(callback)
        await callback.answer(text='ended')
    
    elif callback.data == 'forgotten':
        await callback.answer(text='forgotten')

    elif callback.data == 'break':
        await callback.message.edit_text(text='Вы уверены?')
        await callback.message.edit_reply_markup(inline_message_id=callback.inline_message_id,reply_markup=nav.confirmationPrompt)
        await callback.answer()
    
    elif callback.data == 'yes':
        await return_to_statusMenu(callback)
        await callback.answer(text='broke')
    
    elif callback.data == 'no':
        await callback.message.edit_text(text='text')
        await callback.message.edit_reply_markup(inline_message_id=callback.inline_message_id,reply_markup=nav.endMenu)
        await callback.answer()