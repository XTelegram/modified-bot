from threading import Thread
from telegram import InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackQueryHandler

from bot import LOGGER, dispatcher
from bot.helper.mirror_utils.upload_utils.gdriveTools import GoogleDriveHelper
from bot.helper.telegram_helper.message_utils import sendMessage, editMessage, sendMarkup, auto_delete_message
from bot.helper.telegram_helper.filters import CustomFilters
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.telegram_helper import button_build

def list_drives(update, context):
    try:
        key = update.message.text.split(" ", maxsplit=1)[1]
        LOGGER.info(f"mencari: {key}")
        smsg = sendMessage(f"🔎 <b>Sedang Mencari</b> <code><i>{key}</i></code>", context.bot, update.message)
        gdrive = GoogleDriveHelper()
        msg, button = gdrive.drive_list(key, isRecursive=True, itemType="both")
        if button:
            editMessage(msg, smsg, button)
        else:
            editMessage(f'<b>📝 Tidak menemukan hasil dari:</b> <code><i>{key}</i></code>', smsg)
    except Exception as err:
        LOGGER.error(f"listing error: {err}")
        smsg = sendMessage('Gunakan cara dibawah\n\n<b>Ketik: </b><code>/search NamaFile</code>\n\n<b>Contoh: </b><code>/search GTA</code>', context.bot, update.message)
        Thread(target=auto_delete_message, args=(context.bot, update.message, smsg)).start()

list_handler = CommandHandler(BotCommands.ListCommand, list_drives, filters=CustomFilters.authorized_chat | CustomFilters.authorized_user, run_async=True)
dispatcher.add_handler(list_handler)
