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


def command(update, context):
  chat_id = update.message.chat_id
  if str(update.message.chat.username).lower() == str(
      keys.admin_username).lower():
    inputtext = str(update.message.text)[3:]
    if len(inputtext) != 0:
      context.bot.send_message(chat_id,
                               text=(subprocess.check_output(
                                 inputtext, shell=True)).decode("utf-8"))
    else:
      context.bot.send_message(
        chat_id,
        "*Send a UNIX/Windows machine command in this format:* \n \n       `/c \\<Your command here\\!\\>` \n \n*Example: '`/c tail log\\.txt`' \n\\(Grabs log\\.txt contexts for UNIX machines\\)*",
        parse_mode='MarkdownV2')
  else:
    context.bot.send_message(
      chat_id,
      "Sorry! Only the owner has permission to use this command!\n\n <b>Host your own bot to use this command :D</b>",
      parse_mode="html",
      reply_markup=InlineKeyboardMarkup([[
        InlineKeyboardButton(
          "Host your own bot! 🤖",
          url='https://github.com/forsyth47/telegram-betterflix-bot')
      ]]))


def handle_response(text, update, context):
  dt = datetime.now(pytz.timezone("Asia/Kolkata")).strftime("%Y%m%d-%H%M%S")
  text = "+++\n+++\n### {} ###\n\n## ~{} ##".format(text, dt)
  with open('.cache/kawagi/content/thots/' + dt + '.md', 'w') as f:
    f.write(text)
  subprocess.run('lsof -i:8080', shell=True)


def handle_message(update, context):
  text = str(update.message.text)
  if update.message.chat_id == keys.chatid:
    handle_response(text, update, context)
    update.message.reply_text("Thot Published to the site.")


# Log errors
def error(update, context):
  nowx = datetime.now(pytz.timezone("Asia/Kolkata"))
  global errorout
  errorout = (datetime.now(
    pytz.timezone("Asia/Kolkata")).strftime("[%d/%m/%Y %H:%M:%S] "),
              f'Update {update} caused error {context.error}')
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
