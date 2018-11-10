import logging
import locale
from datetime import datetime as d

from telegram.ext import run_async

from commands.retro.models import RetroItem, Session
from utils.decorators import send_typing_action, log_time, private, admin_only

logger = logging.getLogger(__name__)

locale.setlocale(locale.LC_TIME, "es_AR.utf8")


@log_time
@send_typing_action
@run_async
@private
def retro_add(bot, update, args):
    if not args:
        update.message.reply_text('Tenes que agregar algo al retro bucket. `/retro mas recursos`',
                                  parse_mode='markdown')
        return
    retro_item = ' '.join(args)
    user = update.effective_user.first_name
    save_retro_item(retro_item, user, d.now())
    update.message.reply_text(
        '✅ Listo. Tu mensaje fue guardado para la retro.\n'
        'Para recordarlo en la retro escribí `/retroitems`',
        parse_mode='markdown'
    )


@log_time
@send_typing_action
@run_async
@private
def show_retro_items(bot, update):
    items = get_retro_items()
    if items:
        update.message.reply_text(
            '\n'.join(
                f"{item.user} | {item.text.capitalize()} | {item.datetime.strftime('%A %d/%m %H:%M').capitalize()}"
                for item in items
            )
        )
    else:
        update.message.reply_text('📋 No hay ningún retroitem guardado todavía')


@log_time
@admin_only
def expire_retro(bot, update):
    session = Session()
    for item in session.query(RetroItem):
        item.expired = True
    session.commit()
    update.message.reply_text(
        '✅ Listo. El registro de retroitems fue reseteado.'
    )


@log_time
def save_retro_item(retro_item, user, date_time):
    session = Session()
    item = RetroItem(user=user, text=retro_item, datetime=date_time)
    session.add(item)
    session.commit()


@log_time
def get_retro_items():
    session = Session()
    return session.query(RetroItem).filter_by(expired=False).all()
