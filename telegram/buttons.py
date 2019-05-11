from aiogram.types.inline_keyboard import InlineKeyboardButton as Button, InlineKeyboardMarkup as Markup

from locales import Text


class Buttons:
    @staticmethod
    def _get_copy(func):
        return {
            'callback_data': f'{func}:lyrics',
            'text': f'{func}Lyrics'  # text key
        }

    @staticmethod
    def __class_getitem__(items):
        """
        Magic markup creation.

        >>> Buttons['messageObject', 'close'] == Markup().add(Button(Text['close', 'messageObject']))

        :param items: event, 'close' or 'get', cache key
        :return:
        """
        kwargs = Buttons._get_copy(items[1])
        kwargs['text'] = Text[kwargs['text'], items[0]]

        if len(items) == 3:
            kwargs['callback_data'] = f'{items[1]}:cached:{items[2]}'

        return Markup().add(Button(**kwargs))


__all__ = ['Buttons', 'Markup', 'Button']

