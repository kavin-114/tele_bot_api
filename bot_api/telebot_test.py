from typing import Final
import asyncio
import telegram
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ApplicationBuilder, CallbackQueryHandler
import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

TOKEN: Final = 'BOT_API_TOKEN'
BOT_USERNAME: Final = '@api_testt_bot'

async def start_command(update: Update, context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hellow, Welcome to API TEST Bot")

async def handle_message(update: Update, context:ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    print(f"User ID {update.message.chat.id} sends message as {text} in {update.message.chat.type}")
    await update.message.reply_text("BOT is in developing stage... Will send you notification once the build is done")

async def send_notification(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message()

async def test_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Create an inline keyboard with "Approve" and "Decline" buttons
    keyboard = [
        [InlineKeyboardButton("Approve", callback_data='approve')],
        [InlineKeyboardButton("Decline", callback_data='decline')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send the message with the inline keyboard
    await update.message.reply_text("Do you approve or decline?", reply_markup=reply_markup)

async def button_click(update, context):
    query = update.callback_query
    query.answer()

    # Handle button clicks here
    if query.data == 'approve':
        query.edit_message_text(text="You approved!")
    elif query.data == 'decline':
        query.edit_message_text(text="You declined!")

    # You can also edit the original message if needed
    await context.bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text=f"User {query.from_user.id} has {query.data}d."
    )


if __name__ == '__main__':
    print("Starting bot...")
    application = ApplicationBuilder().token(token=TOKEN).build()
   
    #Commands
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("test", test_command))
    application.add_handler(CallbackQueryHandler(button_click))

    #Messages
    application.add_handler(MessageHandler(filters.TEXT, handle_message))

    #Polls
    print("Polling...")
    application.run_polling(poll_interval=3)
