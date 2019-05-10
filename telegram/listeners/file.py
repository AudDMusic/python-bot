from aiogram import types

from misc import disp
from ..bot import AuddBot, Buttons


onAudio = disp.message_handler(content_types=[types.ContentType.VOICE, types.ContentType.AUDIO])
onVideo = disp.message_handler(content_types=[types.ContentType.VIDEO, types.ContentType.VIDEO_NOTE])


@onAudio
async def file_comes(message: types.Message):
    await message.reply(
        await AuddBot.recognize_by_url(message),
        reply_markup=Buttons.get_lyrics_buttons(message)
    )


@onVideo
async def video_comes(message: types.Message):
    txt, markup = await AuddBot.extract_audio_recognize(message)
    await message.reply(txt, reply_markup=markup)
