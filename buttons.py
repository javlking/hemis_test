from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def questions_button():
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='1', callback_data='0'),
                InlineKeyboardButton(text='2', callback_data='1'),
                InlineKeyboardButton(text='3', callback_data='2'),
                InlineKeyboardButton(text='4', callback_data='3'),
            ],
            [InlineKeyboardButton(text='Next', callback_data='next')]
        ]

    )

    return kb
