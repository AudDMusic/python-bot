from aiogram import types

from misc import disp
from ..bot import AuddBot, Buttons


onAudio = disp.message_handler(content_types=[types.ContentType.VOICE, types.ContentType.AUDIO])
onVideo = disp.message_handler(content_types=[types.ContentType.VIDEO, types.ContentType.VIDEO_NOTE])


@onAudio
async def voice_comes(message: types.Message):
    await message.reply(
        await AuddBot.ByUrl.song(message),
        reply_markup=Buttons[message, 'get']
    )


@onVideo
async def video_comes(message: types.Message):
    txt, markup = await AuddBot.extract_audio_recognize(message)
    await message.reply(txt, reply_markup=markup)
