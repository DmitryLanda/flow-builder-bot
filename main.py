#!/usr/bin/env python
# -*- coding: utf-8 -*-

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import requests

updater = Updater(token='371554719:AAGEGPfjdIFYMpEVJfZ68HR2KOV6CMVyALo')
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
config = {
    "ciUrl": "http://localhost:8000"
}

def start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="Greeting!\nThis is a bot to help you to interract with pipeline based CI server\nTry /help to see available commands")

def help(bot, update):
    bot.sendMessage(
        chat_id=update.message.chat_id, 
        text="/help to see help info\n/addRepo <url> to start tracking your github repo on CI server\n/settings to check bot setttings\n/settings <url> - to change CI API url"
    )

def add_repo(bot, update, args):
    if len(args) == 0:
        bot.sendMessage(chat_id=update.message.chat_id, text="Please add repository url after command")

        return
    url = "%s/newpipe" % config['ciUrl']
    try:
        resp = requests.post(url, json={
            "URL": args[0],
            "CHAT_ID": "%s" % update.message.chat_id,
            "TOKEN": "371554719:AAGEGPfjdIFYMpEVJfZ68HR2KOV6CMVyALo"
        })
    except Exception:
        bot.sendMessage(chat_id=update.message.chat_id, text="Failed to send message to CI server\nTry run /settings to check... settings")

        return
        
    if (resp == None):
        text = "Check CI server API URL"
    else:
        if (resp.status_code == requests.codes.ok):
            text = "Successfully added"
        if (resp.status_code == requests.codes.not_found):
            text = "CI server not found on given url"
        if (resp.status_code == requests.codes.bad_request):
            text = "CI server respond with an error: %s" % resp.json()['message']
   
    bot.sendMessage(chat_id=update.message.chat_id, text=text) 

def update_settings(bot, update, args):
    if len(args) == 0:
        bot.sendMessage(chat_id=update.message.chat_id, text="Settings are:\nAPI url - %s\nChat ID - %s" % (config['ciUrl'], update.message.chat_id))

        return

    config['ciUrl'] = args[0]
    bot.sendMessage(chat_id=update.message.chat_id, text="Ok, CI API url changed to %s" % args[0])

def run():
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('help', help))
    dispatcher.add_handler(CommandHandler('addRepo', add_repo, pass_args=True))
    dispatcher.add_handler(CommandHandler('settings', update_settings, pass_args=True))
    dispatcher.add_handler(MessageHandler(Filters.command, help))

    logging.info('Bot deamon started')
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    run()
