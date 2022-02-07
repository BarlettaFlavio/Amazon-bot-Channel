# -*- coding: utf-8 -*-
"""
Created on Sun Jul 26 18:04:17 2020

@author: Flavio
"""
import telebot

API_TOKEN = '1338925720:AAGTfxJbjRM7QXEImJYzreJKws5qh-YIKsk'

bot = telebot.TeleBot(API_TOKEN)


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, """\
Hi there, I am EchoBot.
I am here to echo your kind words back to you. Just say anything nice and I'll say the exact same thing to you!\
""")


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, message.chat)


bot.polling()