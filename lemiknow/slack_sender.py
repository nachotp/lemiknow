from typing import List
import os
import datetime
import traceback
import functools
import json
import socket
import requests

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def slack_sender(webhook_url: str, channel: str, user_mentions: List[str] = [], message: str = None, notify_end: bool = True, include_details: bool = True):
    """
    Slack sender wrapper: execute func, send a Slack notification with the end status
    (sucessfully finished or crashed) at the end. Also send a Slack notification before
    executing func.

    `webhook_url`: str
        The webhook URL to access your slack room.
        Visit https://api.slack.com/incoming-webhooks#create_a_webhook for more details.
    `channel`: str
        The slack room to log.
    `user_mentions`: List[str] (default=[])
        Optional users ids to notify.
        Visit https://api.slack.com/methods/users.identity for more details.
    """

    dump = {
        "username": "Le Mi Know",
        "channel": channel,
    }

    def decorator_sender(func):
        def send_message(text: str):
            dump["text"] = text
            requests.post(webhook_url, json.dumps(dump))

        @functools.wraps(func)
        def wrapper_sender(*args, **kwargs):
            if (not include_details and message == None) or (not include_details and message == ""):
                raise ValueError(
                    "Message cannot be empty if include_details is set to False")

            start_time = datetime.datetime.now()
            host_name = socket.gethostname()
            func_name = func.__name__
            text = ""
            if include_details:
                text += f'{func_name} called on {host_name} at {start_time.strftime(DATE_FORMAT)}'
            if message:
                text += f'{func_name}: {message}' if not include_details else f'\nMessage: {message}'
            if notify_end:
                text += '\nWe\'ll let you know when it\'s done.'

            send_message(text=text)

            try:
                value = func(*args, **kwargs)
                if notify_end:
                    end_time = datetime.datetime.now()
                    elapsed_time = end_time - start_time
                    text = ""
                    text += f'✅ {func_name} finished on {host_name} at {end_time.strftime(DATE_FORMAT)}'
                    text += f'\nDuration: {elapsed_time}'

                    try:
                        str_value = str(value)
                        text += f'\nReturned value: {str_value}'
                    except:
                        text += f'\nReturned value: ERROR - Couldn\'t parse the returned value.'

                    send_message(text=text)

                return value

            except Exception as ex:
                end_time = datetime.datetime.now()
                elapsed_time = end_time - start_time
                contents = [f"☠️ {func_name} has crashed on {host_name} at {end_time.strftime(DATE_FORMAT)}",
                            "Here's the error:",
                            '%s\n\n' % ex,
                            "Traceback:",
                            '%s' % traceback.format_exc()]
                text = '\n'.join(contents)
                send_message(text=text)
                raise ex

        return wrapper_sender

    return decorator_sender
