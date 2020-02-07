import os
import datetime
import traceback
import functools
import socket
from matrix_client.api import MatrixHttpApi

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def matrix_sender(homeserver: str, token: str, room: str):
    """
    Matrix sender wrapper: execute func, send a Matrix message with the end status
    (sucessfully finished or crashed) at the end. Also send a Matrix message before
    executing func.

    `homeserver`: str
        The homeserver address which was used to register the BOT.
        It is e.g. 'https://matrix-client.matrix.org'. It can be also looked up
        in Riot by looking in the riot settings, "Help & About" at the bottom.
        Specifying the schema (`http` or `https`) is required.
    `token`: str
        The access TOKEN of the user that will send the messages.
        It can be obtained in Riot by looking in the riot settings, "Help & About" ,
        down the bottom is: Access Token:<click to reveal>
    `room`: str
        The alias of the room to which messages will be send by the BOT.
        After creating a room, an alias can be set. In Riot, this can be done
        by opening the room settings under 'Room Addresses'.
    """

    matrix = MatrixHttpApi(homeserver, token=token)
    room_id = matrix.get_room_id(room)

    def decorator_sender(func):

        def send_message(text, room_id=room_id):
            matrix.send_message(room_id, text)

        @functools.wraps(func)
        def wrapper_sender(*args, **kwargs):

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
