import asyncio

from aiogram import types

from misc import disp

from ..bot import AudDBot


loop = asyncio.get_event_loop()

VIDEO_TYPES = [types.ContentType.VIDEO, types.ContentType.VIDEO_NOTE]
AUDIO_TYPES = [types.ContentType.VOICE, types.ContentType.AUDIO]
onFiles = disp.message_handler(content_types=[*AUDIO_TYPES, *VIDEO_TYPES])


def tasker(*coros):
    for coro in coros:
        loop.create_task(coro)


async def inner_coro(message, coro):
    txt, markup = await coro(message)
    await message.reply(text=txt, reply_markup=markup)


@onFiles
async def file_comes(message: types.Message):
    coro = (
        AudDBot.ByUrl.song
        if message.content_type in AUDIO_TYPES
        else AudDBot.Video.extract_audio_recognize
    )

    tasker(types.ChatActions.typing(), inner_coro(message, coro))
