
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart
from aiogram import Router

import app.markups as nav
from app.callback import return_to_statusMenu
from app.api import init_api_controller

router = Router()
api_controller = init_api_controller()

#Authorization thing
@router.message(CommandStart())
async def command_start_handler(message: Message, state:FSMContext) -> None:

    user_tag = message.from_user.username
    user_id = message.from_user.id

    if user_tag is None: user_is_authorized = False
    else:
        res = await api_controller.auth(user_tag, user_id)
        print(res.json())
        user_is_authorized = res.status_code==200
        print(user_is_authorized)

    if user_is_authorized:
        machines_list=[['machine']]
        if len(machines_list)==1:
            user_is_admin=False
            if user_is_admin:
                await message.answer(text='text',reply_markup=nav.mainMenuAdmin)
            await message.answer(text='text',reply_markup=nav.mainMenu)
    else:
        await message.answer(text="Вы не авторизованы. Обратитесь за помощью к кому скидывались за стиралку")


@router.message()
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