from aiogram.types import CallbackQuery
import app.markups as nav

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