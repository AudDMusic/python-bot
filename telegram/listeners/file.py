from aiogram import types

from misc import disp

from ..bot import AudDBot

onAudio = disp.message_handler(content_types=[types.ContentType.VOICE, types.ContentType.AUDIO])
onVideo = disp.message_handler(content_types=[types.ContentType.VIDEO, types.ContentType.VIDEO_NOTE])


@onAudio
async def voice_comes(message: types.Message):
    txt, markup = await AudDBot.ByUrl.song(message)
    await message.reply(
        text=txt,
        reply_markup=markup
    )


@onVideo
async def video_comes(message: types.Message):
    txt, markup = await AudDBot.Video.extract_audio_recognize(message)
    await message.reply(txt, reply_markup=markup)
