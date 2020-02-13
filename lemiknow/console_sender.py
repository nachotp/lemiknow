import os
import datetime
import traceback
import socket
import functools

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def console_sender(message: str = None, notify_end: bool = True, include_details: bool = True):
    """
    Console sender wrapper: execute func, print on console with the end status
    (sucessfully finished or crashed) at the end. Also print on console before
    executing func.

    `message`: str
        Optional message to include when notifying the function call.
        default: None
    `notify_end`: bool
        Send a notification when the function finishes (not recommended for short calls).
        default: True
    `include_details`: bool
        Adds extra information on notifications like hostname, start time, etc.
        Can't be False if message is None.
        default: true
    `debug`: bool
        Prints debug information on console
        default: False
    """

    def decorator_sender(func):
        def send_message(text):
            print(f"Lemiknow: {text}")

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
