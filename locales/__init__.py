import json
import os

from aiogram import types

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class UnsupportedLang(Exception):
    pass


langs = {
    "ru": json.load(open(f"{BASE_DIR}/locales/ru.json")),
    "en": json.load(open(f"{BASE_DIR}/locales/en.json")),
}


def _get_text(key, lang, default=None) -> str:
    string = langs.get(lang, {}).get(key, default)
    if not string and string != default:
        raise UnsupportedLang
    return string.__str__()


def _get_lang(event):
    lang = event.from_user.language_code[:2] or "en"
    if lang in langs:
        return lang
    return "en"


class Text:
    @staticmethod
    def __class_getitem__(items):
        """
        >>> Text['start', 'en']
        ... 'Hey send me anything listenable'
        :param items: Sequenced items _> langKey
        :return:
        """
        if len(items) in [2, 3]:
            key, lang, *default = items
            if isinstance(lang, (types.CallbackQuery, types.Message)):
                lang = _get_lang(lang)[:2]
            return _get_text(key, lang, default[0] if default else None)
        raise ValueError(f"Ensure you passed right args to Text class")

    loading = "<b>...</b>"
