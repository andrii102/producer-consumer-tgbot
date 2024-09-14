from datetime import datetime
from collections import defaultdict
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from telegram import Update, Bot
from typing import Final
from PikaClient import MessageReceiver

from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes,  CallbackContext


TOKEN:Final = ''
BOT_USERNAME:Final = '@reminderfu_bot'

RABBITMQ_BROKER_ID = ''
RABBITMQ_USER = ''
RABBITMQ_PASSWORD = ''
REGION = ''

bot = Bot(token=TOKEN)

message_receiver = MessageReceiver(RABBITMQ_BROKER_ID, RABBITMQ_USER, RABBITMQ_PASSWORD, REGION)

# Dictionary to store reminders
reminders = defaultdict(list)

async def start_command(update: Update, context: CallbackContext):
    await update.message.reply_text("Hi there! It's the Reminder bot!")

# async def remind_command(update: Update, context: CallbackContext):
#     try:
#         time_str = context.args[0]
#         reminder_message = ' '.join(context.args[1:])
#         chat_id = update.message.chat.id

#         # Add reminder to the dictionary
#         reminders[time_str].append((chat_id, reminder_message))
        
#         await update.message.reply_text(f'Reminder set for {time_str}.')
#     except IndexError:
#         await update.message.reply_text('Usage: /remind <HH:MM> <message>')

async def remind_command(update: Update, context: CallbackContext):
    try:
        time_str = context.args[0]
        reminder_message = ' '.join(context.args[1:])
        chat_id = update.message.chat.id

        # Validate datetime format
        try:
            reminder_time = datetime.strptime(time_str, '%Y-%m-%d %H:%M')
        except ValueError:
            await update.message.reply_text('Invalid date/time format. Please use YYYY-MM-DD HH:MM.')
            return

        # Convert datetime to string for use in dictionary keys
        time_key = reminder_time.strftime('%Y-%m-%d %H:%M')

        # Add reminder to the dictionary
        if time_key not in reminders:
            reminders[time_key] = []
        reminders[time_key].append((chat_id, reminder_message))

        await update.message.reply_text(f'Reminder set for {time_key}.')
    except IndexError:
        await update.message.reply_text('Usage: /remind <YYYY-MM-DD HH:MM> <message>')


async def schedule__bot_command():
    message_receiver.consume_messages('rem_queue', reminders)
    print("Consuming Messages")

async def check_reminders():
    current_time_str = datetime.now().strftime('%Y-%m-%d %H:%M')
    if current_time_str in reminders:
        for chat_id, message in reminders[current_time_str]:
            # Send reminder message
            await bot.send_message(chat_id=chat_id, text=message)
        # Clear reminders for the current time
        reminders[current_time_str] = []

async def delete_reminder_command(update: Update, context: CallbackContext):
    time_str = context.args[0]
    reminder_message = ' '.join(context.args[1:])
    chat_id = update.message.chat.id

    if time_str in reminders:
        reminders_at_time = reminders[time_str]
        reminder_tuple = (chat_id, reminder_message)
        if reminder_tuple in reminders_at_time:
            reminders_at_time.remove(reminder_tuple)
            if not reminders_at_time:
                del reminders[time_str]
            await update.message.reply_text(f"Reminder '{reminder_message}' at {time_str} has been deleted.")
        else:
            await update.message.reply_text(f"No reminder found with the message '{reminder_message}' at {time_str}.")
    else:
        await update.message.reply_text(f"No reminders found for the time: {time_str}")


async def schedule_bot_commmand():
    pass

if __name__ == '__main__':
    print("Start")
    app = Application.builder().token(TOKEN).build()

    # Add handlers
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler("remind", remind_command))
    app.add_handler(CommandHandler("delete",delete_reminder_command))
    app.add_handler(CommandHandler("schedule_bot",schedule__bot_command))

    # Scheduler to check reminders every minute
    scheduler = AsyncIOScheduler()
    scheduler.add_job(check_reminders, IntervalTrigger(seconds=30))
    scheduler.start()

    app.run_polling(poll_interval=5)
