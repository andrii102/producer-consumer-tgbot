from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import asyncio
from PikaClient import MessageSender

TOKEN = ''
BOT_USERNAME = ''

RABBITMQ_BROKER_ID = ''
RABBITMQ_USER = ''
RABBITMQ_PASSWORD = ''
REGION = ''

message_sender = MessageSender(RABBITMQ_BROKER_ID, RABBITMQ_USER, RABBITMQ_PASSWORD, REGION)
message_sender.declare_queue("rem_queue")

async def start_command(update: Update, context:CallbackContext): 
    await update.message.reply_text('Hello! Use /schedule <time> <message> to schedule a task.Time format: YYYY-MM-DD HH:MM')
                              
async def schedule_command(update: Update, context:CallbackContext):
    try:    
        time = context.args[0]
        message = ''.join(context.args[1:])
        user_id = update.message.from_user.id   

        rem_message = f"{user_id}:{time}:{message}"
        

        # Send the message to RabbitMQ
        message_sender.send_message(exchange='',
                                    routing_key='rem_queue',
                                    body=rem_message)        
    except:
         await update.message.reply_text('Usage: /schedule <YYYY-MM-DD HH:MM> <message>')



