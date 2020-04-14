#!/usr/bin/env python
import os
import time

import config
from datetime import time
import telegram
from telegram.ext import (Updater, CommandHandler)

# Enable logging
from parser import Parser

import logging

format = "%(asctime) %(message)s"
logging.basicConfig(format=format, level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger('main')


def get_message(name):
    logger.info("Getting message")
    if os.path.isfile(name) & time.time() - os.path.getmtime(name) < 7200:
        logger.info("Getting from file")
        return get_from_file(name)
    else:
        logger.info("Getting from web")
        message = construct_message(name)
        save_to_file(message, name)
        return message


def get_from_file(file):
    with open(file, 'r') as f:
        return f.read()


def save_to_file(data, name):
    logger.info("saving to file")
    with open(name, "w") as f:
        f.write(data)


def construct_message(name):
    message = ""
    parser = Parser()
    if name == "rbc":
        message += "Привет!\nПора читать новости!\n\n<b>РБК</b>\n"
        for k, v in parser.rbc.items():
            message += v + " (<a href='" + k + "'>Линк</a>)\n\n"
    if name == "vedomosti":
        message += "<b>Ведомости</b>\n"
        for k, v in parser.vedomosti.items():
            message += v + " (<a href='" + k + "'>Линк</a>)\n\n"
    if name == "kommersant":
        message += "<b>Коммерсант</b>\n"
        for k, v in parser.kommersant.items():
            message += v + " (<a href='" + k + "'>Линк</a>)\n\n"
    if name == "yandex":
        message += "<b>Яндекс</b>\n"
        for k, v in parser.yandex.items():
            message += v + " (<a href='" + k + "'>Линк</a>)\n\n"
    return message


def instant_send(bot, update):
    logger.info("Instant sending started to user " + update.message.chat_id)
    bot.send_message(chat_id=update.message.chat_id, text=get_message("rbc"), parse_mode=telegram.ParseMode.HTML)
    bot.send_message(chat_id=update.message.chat_id, text=get_message("vedomosti"), parse_mode=telegram.ParseMode.HTML)
    bot.send_message(chat_id=update.message.chat_id, text=get_message("kommersant"), parse_mode=telegram.ParseMode.HTML)
    bot.send_message(chat_id=update.message.chat_id, text=get_message("yandex"), parse_mode=telegram.ParseMode.HTML)
    logger.info("Instant sending ended to user " + update.message.chat_id)


def callback_alarm(bot, job):
    logger.info("Timer sending started to user " + job.context)
    bot.send_message(chat_id=job.context, text=get_message("rbc"), parse_mode=telegram.ParseMode.HTML)
    bot.send_message(chat_id=job.context, text=get_message("vedomosti"), parse_mode=telegram.ParseMode.HTML)
    bot.send_message(chat_id=job.context, text=get_message("kommersant"), parse_mode=telegram.ParseMode.HTML)
    bot.send_message(chat_id=job.context, text=get_message("yandex"), parse_mode=telegram.ParseMode.HTML)
    logger.info("Timer sending ended to user " + job.context)


def callback_timer(bot, update, job_queue):
    logger.info("Timer ticked")
    bot.send_message(chat_id=update.message.chat_id, text="Добро пожаловать! Ждите от нас новости в 20.00 по Москве!\n"
                                                          "Хотите раньше? Напишите нам /now")
    job_queue.run_daily(callback_alarm, context=update.message.chat_id,
                        time=time(hour=17, minute=00, second=00))
    logger.info("Message sent")


def Stop_timer(bot, update, job_queue):
    bot.send_message(chat_id=update.message.chat_id,
                     text='Спасибо за дружбу!')
    logger.info("User " + update.message.chat_id + " unsubscribed")
    job_queue.stop()


updater = Updater(config.token)
updater.dispatcher.add_handler(CommandHandler('now', instant_send))
updater.dispatcher.add_handler(CommandHandler('start', callback_timer, pass_job_queue=True))
updater.dispatcher.add_handler(CommandHandler('stop', Stop_timer, pass_job_queue=True))
updater.start_polling()
