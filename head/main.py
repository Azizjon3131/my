import os.path
import telegram
from queue import Queue
from threading import Thread
from telegram import (
    bot, KeyboardButton, ReplyKeyboardMarkup,InlineKeyboardMarkup,InlineKeyboardButton
)
from telegram.ext import (
    Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler,
    messagequeue as mq, InlineQueryHandler, PollAnswerHandler,ConversationHandler
)
from telegram.utils.request import Request
from telegram import Update
from telegram.ext import Dispatcher
from telegram.error import TelegramError
import logging
import json

# from django.http import JsonResponse
# from django.conf import settings

# wungacha
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MEDIA_DIR = os.path.join(BASE_DIR, '..', '..', '..', 'media')
logger = logging.getLogger(__name__)


class MQBot(bot.Bot):
    print('class MQBot 34-qator' )
    '''A subclass of Bot which delegates send method handling to MQ'''
    def __init__(self, *args, is_queued_def=True, mqueue=None, **kwargs):
        super(MQBot, self).__init__(*args, **kwargs)
        # below 2 attributes should be provided for decorator usage
        self._is_messages_queued_default = is_queued_def
        self._msg_queue = mqueue or mq.MessageQueue()

    def __del__(self):
        try:
            self._msg_queue.stop()
        except:
            pass

    @mq.queuedmessage
    def send_message(self, *args, **kwargs):
        '''Wrapped method would accept new `queued` and `isgroup`
        OPTIONAL arguments'''
        return super(MQBot, self).send_message(*args, **kwargs)

    @mq.queuedmessage
    def forward_message(self, *args, **kwargs):
        return super(MQBot, self).forward_message(*args, **kwargs)

    @mq.queuedmessage
    def delete_message(self, chat_id, message_id, timeout=None, **kwargs):
        return super(MQBot, self).delete_message(chat_id, message_id, timeout, **kwargs)

    @mq.queuedmessage
    def send_photo(self, *args, **kwargs):
        '''Wrapped method would accept new `queued` and `isgroup`
        OPTIONAL arguments'''
        return super(MQBot, self).send_photo(*args, **kwargs)

    @mq.queuedmessage
    def send_video(self, *args, **kwargs):
        '''Wrapped method would accept new `queued` and `isgroup`
        OPTIONAL arguments'''
        return super(MQBot, self).send_video(*args, **kwargs)

    @mq.queuedmessage
    def send_audio(self, *args, **kwargs):
        '''Wrapped method would accept new `queued` and `isgroup`
        OPTIONAL arguments'''
        return super(MQBot, self).send_audio(*args, **kwargs)

    @mq.queuedmessage
    def send_document(self, *args, **kwargs):
        '''Wrapped method would accept new `queued` and `isgroup`
        OPTIONAL arguments'''
        return super(MQBot, self).send_document(*args, **kwargs)

    @mq.queuedmessage
    def send_voice(self, *args, **kwargs):
        '''Wrapped method would accept new `queued` and `isgroup`
        OPTIONAL arguments'''
        return super(MQBot, self).send_voice(*args, **kwargs)


def text_translate(message):
    try:
        result = message.encode('utf-8')
    except AttributeError:
        result = message
    return result


def delete_message_user(context, chat_id, message_id):
    context.bot.delete_message(chat_id, message_id)


def go_message(context, user_id, message, reply_markup):
    context.bot.send_message(chat_id=user_id, text=message, reply_markup=reply_markup, parse_mode='HTML',
                             disable_web_page_preview=True)


def go_message_md(context, user_id, message, reply_markup, delete=True):

    context.bot.send_message(chat_id=user_id, text=message, reply_markup=reply_markup, parse_mode='Markdown',
                             disable_web_page_preview=True)


def go_reply(context, user_id, message, reply_id):
    context.bot.send_message(chat_id=user_id, text=message, reply_to_message_id=reply_id, parse_mode='HTML',
                             disable_web_page_preview=True)


def go_reply_video(context, user_id, message, reply_id):
    context.bot.send_video(chat_id=user_id, text=message, reply_to_message_id=reply_id, parse_mode='HTML')


def edit_message(context, chat_id, message_id, message, reply_markup):
    try:
        context.bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=message, reply_markup=reply_markup,
                                  parse_mode='HTML')
    except Exception as e:
        print('ERROR edit message: ', str(e))


def send_photo(context, user_id, photo, caption=None, reply_markup=None):
    return context.bot.send_photo(user_id, photo=photo, caption=caption, reply_markup=reply_markup, parse_mode='HTML')


# def send_document(context, user_id,phone_number):
#     return context.bot.send_photo(user_id,phone_number=phone_number)


def send_voice(context, user_id, voice, caption=None, reply_markup=None):
    context.bot.send_voice(user_id, voice=voice, caption=caption, reply_markup=reply_markup, parse_mode='HTML')


# @private_decorator_chat
def start(update, context):
    print(update)
    # bot = services.get_bot(f"@{context.bot.username}")
    print('dddddddddddddddd',bot)
    user = update.message.from_user
    # print(user.id)
    buttons = [['bir'],['ikki', 'uch']]
    go_message(context, user.id, 'sdeasdsd',ReplyKeyboardMarkup(buttons, one_time_keyboard=True, resize_keyboard=True))
    context.bot.send_document(chat_id=user.id, document='C:\Users\Admin\Desktop\javob.pdf')

    return 1


def keldi(update, context):
    user = update.message.from_user
    go_message(context, user.id, '11111',None)


def ketti(update, context):
    user = update.message.from_user
    go_message(context, user.id, '22222',None)



def cancel(update, context):
    go_message(context, user.id, 'cancellll',None)


def main():
    # Create the Updater and pass it your bot's token.
    # def handle(self, *args, **kwargs):
    q = mq.MessageQueue(all_burst_limit=3, all_time_limit_ms=3000)
    request = Request(con_pool_size=36)
    test_bot = MQBot('1755954911:AAHl7bMn7z6PGNJUjI-A4gOdJIixuEg7R7M', request=request, mqueue=q)
    updater =telegram.ext.updater.Updater(bot=test_bot, use_context=True, workers=32)


    dispatcher = updater.dispatcher

    # dispatcher.add_handler(CommandHandler("start", start))
    # dispatcher.add_handler(MessageHandler(Filters.text, received_message))
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            1: [MessageHandler(Filters.regex('^(bir)$'), keldi),
                MessageHandler(Filters.regex('^(ikki)$'), ketti)]
                },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    dispatcher.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
