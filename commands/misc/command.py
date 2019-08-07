import os
import re

from telegram.ext import run_async, Filters

from updater import elbot
from utils.utils import monospace
from utils.constants import TICKET_REGEX, CODE_PREFIX
from utils.decorators import send_typing_action, log_time


@elbot.regex(pattern=CODE_PREFIX, pass_groupdict=True)
@log_time
@send_typing_action
def format_code(bot, update, groupdict):
    """Format text as code if it starts with $, ~, \c or \code."""
    code = groupdict.get('code')
    if code:
        update.message.reply_text(
            monospace(code), parse_mode='markdown'
        )


@elbot.message(filters=Filters.regex(TICKET_REGEX))
@send_typing_action
@run_async
def link_ticket(bot, update):
    """Given a ticket id, return the url."""
    jira_base = os.environ['jira']
    ticket_links = '\n'.join(
        f"» {jira_base.format(match.group('ticket'))}"
        for match in re.finditer(TICKET_REGEX, update.message.text)
        )

    update.message.reply_text(ticket_links, quote=False)


@elbot.command(command='code')
@send_typing_action
@run_async
def code(bot, update):
    """If a user sends an unknown command, answer accordingly"""
    REPO = 'https://github.com/Ambro17/AmbroBot'
    msg = (
        f"Here you can see my internals: {REPO}\n"
        "Don't forget to give it a ⭐️ if you like it!"
    )
    update.message.reply_text(msg, disable_web_page_preview=True)