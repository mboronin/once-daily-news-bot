#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.
import logging
import secrets
from datetime import time

import telegram
from telegram.ext import Updater, CommandHandler

from parser import Parser

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def construct_message(name):
    message = ""
    parser = Parser()
    if name == "rbc":
        message += "Привет!\nПора читать новости!\n\n<b>РБК</b>\n"
        for k, v in parser.rbc.items():
            message += v + " (<a href='" + k + "'>Линк</a>)\n\n"
    if name == "vedomosti":
        message += "<b>Ведомости</b>\n\n"
        for k, v in parser.vedomosti.items():
            message += v + " (<a href='" + k + "'>Линк</a>)\n\n"
    if name == "kommersant":
        message += "<b>Коммерсант</b>\n\n"
        for k, v in parser.kommersant.items():
            message += v + " (<a href='" + k + "'>Линк</a>)\n\n"
    if name == "yandex":
        message += "<b>Яндекс</b>\n\n"
        for k, v in parser.yandex.items():
            message += v + " (<a href='" + k + "'>Линк</a>)\n\n"
    return message


def callback_alarm(bot, job):
    bot.send_message(chat_id=job.context, text=construct_message("rbc"), parse_mode=telegram.ParseMode.HTML)
    bot.send_message(chat_id=job.context, text=construct_message("vedomosti"), parse_mode=telegram.ParseMode.HTML)
    bot.send_message(chat_id=job.context, text=construct_message("kommersant"), parse_mode=telegram.ParseMode.HTML)
    bot.send_message(chat_id=job.context, text=construct_message("yandex"), parse_mode=telegram.ParseMode.HTML)


def callback_timer(bot, update, job_queue):
    bot.send_message(chat_id=update.message.chat_id, text="Добро пожаловать! Ждите от нас новости в 20.00 по Москве!")
    job_queue.run_daily(callback_alarm, context=update.message.chat_id,
                        time=time(hour=17, minute=00, second=00))


def Stop_timer(bot, update, job_queue):
    bot.send_message(chat_id=update.message.chat_id,
                     text='Спасибо за дружбу!')
    job_queue.stop()


updater = Updater(secrets.token)
updater.dispatcher.add_handler(CommandHandler('start', callback_timer, pass_job_queue=True))
updater.dispatcher.add_handler(CommandHandler('stop', Stop_timer, pass_job_queue=True))
updater.start_polling()
