import os.path
from telegram.ext import (
    Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler,
    messagequeue as mq, InlineQueryHandler, PollAnswerHandler,ConversationHandler
)
from telegram.utils.request import Request
from .head import MQBot, start


BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class Command(BaseCommand):
    help = 'Displays current time'
    print('hend')

    def handle(self, *args, **kwargs):
        q = mq.MessageQueue(all_burst_limit=3, all_time_limit_ms=3000)
        request = Request(con_pool_size=36)
        test_bot = MQBot('1634634823:AAE9ZwkCR1bZRkEljCqgAVO5GS2EDM7nrdY', request=request, mqueue=q)
        updater = Updater(bot=test_bot, use_context=True, workers=32)

        # Get the dispatcher to register handlers
        dispatcher = updater.dispatcher

        # on different commands - answer in Telegram
        # dispatcher.add_handler(CommandHandler("start", start))
        # dispatcher.add_handler(MessageHandler(Filters.text, received_message))
        # dispatcher.add_handler(MessageHandler(Filters.contact, get_contact_value))
        # dispatcher.add_handler(MessageHandler(Filters.photo, received_photo))
        # dispatcher.add_handler(MessageHandler(Filters.document, received_document))
        # dispatcher.add_handler(CallbackQueryHandler(inline_button))
        conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start),
        MessageHandler(Filters.regex('^(🛒 Buyurtma qilish)$'), buyurtma)],
        states={
            1: [MessageHandler(Filters.regex('^(🛒 Buyurtma qilish)$'), buyurtma),
                MessageHandler(Filters.regex('^(🛍 Buyurtmalarim)$'), buyurtmalarim)],
            2: [CallbackQueryHandler(menu),
                [MessageHandler(Filters.regex('^(🛒 Buyurtma qilish)$'), buyurtma)]]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    dispatcher.add_handler(conv_handler)

        updater.start_polling()
        updater.idle()
