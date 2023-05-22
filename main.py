# pip install python-telegram-bot==13.5 flask
import os
from datetime import datetime
from telegram import *
from telegram.ext import *
from webserver import keep_alive
import keys
import pytz
import subprocess
import inspect
#-----------------------------------
print('Starting up bot...')

keep_alive()


# Lets us use the /start command
def start_command(update, context):
  update.message.reply_text('BOT IS ACTIVE')


# Lets us use the /help command
def help_command(update, context):
  update.message.reply_text('PM @JoshuaForsyth for help!')


# Secret command to access linux terminal (such as log.txt)
def command(update, context):
  chat_id = update.message.chat_id
  if str(update.message.chat.username).lower() == str(keys.admin_username).lower():
    inputtext=str(update.message.text)[3:]
    if len(inputtext) != 0:
        context.bot.send_message(chat_id, text=(subprocess.check_output(inputtext, shell=True)).decode("utf-8"))
    else:
      context.bot.send_message(chat_id, "*Send a UNIX/Windows machine command in this format:* \n \n       `/c \\<Your command here\\!\\>` \n \n*Example: '`/c tail log\\.txt`' \n\\(Grabs log\\.txt contexts for UNIX machines\\)*", parse_mode='MarkdownV2')
  else:
    context.bot.send_message(chat_id, "Sorry! Only the owner has permission to use this command!\n\n <b>Host your own bot to use this command :D</b>", parse_mode="html", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Host your own bot! 🤖", url='https://github.com/forsyth47/telegram-betterflix-bot')]]))

  

def handle_response(new_text, update, context):
  global chat_id
  chat_id = update.message.chat_id
  if 'hello' in new_text:
    context.bot.send_chat_action(chat_id, action=ChatAction.TYPING)
    return 'Hello! :)'
  # If Asked anything else
  context.bot.send_chat_action(chat_id, action=ChatAction.TYPING)
  return ("I'm not programmed to answer that yet ;0" + '\n')


def handle_message(update, context):
  # Get basic info of the incoming message
  message_type = update.message.chat.type
  text = str(update.message.text).lower()
  response = ''

  timezonex = datetime.now(pytz.timezone("Asia/Kolkata"))
  # Print a log for debugging
  logx = (
    timezonex.strftime("[%d/%m/%Y %H:%M:%S] "),
    f'User ({update.message.chat.first_name}, {update.message.chat.username}, {update.message.chat.id}) says: "{text}" in: {message_type}'
  )
  print(logx)

  # React to group messages only if users mention the bot directly
  if message_type == 'group':
    # Replace with your bot username
    botnamex = "@BOTNAMEHERE"
    if botnamex in text:
      new_text = text.replace(botnamex, '').strip()
      response = handle_response(new_text)
  else:
    response = handle_response(new_text, update, context)

  # Reply normal if the message is in private
  update.message.reply_text(response)

  #print log in file.
  fileout = open("log.txt", "a+")
  fileout.writelines(logsss)
  fileout.writelines("\n")
  fileout.close()


# Log errors
def error(update, context):
  nowx = datetime.now(pytz.timezone("Asia/Kolkata"))
  global errorout
  errorout = (nowx.strftime("[%d/%m/%Y %H:%M:%S] "), f'Update {update} caused error {context.error}')
  print(errorout)


# Run the program #use_context=True,
if __name__ == '__main__':
  updater = Updater(keys.token, use_context=True)
  dp = updater.dispatcher

  # Commands
  dp.add_handler(CommandHandler('start', start_command))
  dp.add_handler(CommandHandler('help', help_command))
  dp.add_handler(CommandHandler('c', command))
  #dp.add_handler(CommandHandler('command-in-tg', fun-name))

  # Messages
  dp.add_handler(MessageHandler(Filters.text, handle_message))

  # Log all errors
  dp.add_error_handler(error)

  # Run the bot
  updater.start_polling(1.0)
  updater.idle()
