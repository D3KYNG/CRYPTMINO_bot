from aiogram.types import KeyboardButton, InlineKeyboardButton, ReplyKeyboardMarkup

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

from config import CHANNELS

main_buttons = [
    [
        KeyboardButton(text='👤 Profile', callback_data='profile'),
    ],
    [
        KeyboardButton(text='💳 Currency', callback_data='currency'),
        KeyboardButton(text='🖥 Investments', callback_data='investments'),
    ],
    [
        KeyboardButton(text='🖨 Calculator', callback_data='calc'),
        KeyboardButton(text='🗒 Guide', callback_data='gide'),
        KeyboardButton(text='VIP status', callback_data='vipMain'),
    ],
    [
        KeyboardButton(text='👥 Affiliate Program', callback_data='part')
    ]
]
main = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=main_buttons)

go_main = [
    [
         KeyboardButton(text='⏪ Main Menu', callback_data='to_main')
    ]
]
gm = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=go_main)


stcheck = [
    [
         KeyboardButton(text='⏪ Main menu', callback_data='to_main')
    ],
    [
        KeyboardButton(text='🔔 Check payment', callback_data='to_main')
    ]
]
st = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=stcheck)

investment_buttons = [
    [
        KeyboardButton(text='➕ Invest', callback_data='balance'),
        KeyboardButton(text='➖ Collect', callback_data='to_balance'),
    ],
    [
        KeyboardButton(text='⏪ Main Menu', callback_data='to_main')
    ]
]
investment = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=investment_buttons)

currency_buttons = [
    [
        InlineKeyboardButton(text='➕ Top Up', callback_data='popol'),
        InlineKeyboardButton(text='➖ Withdraw', callback_data='vivod'),
    ],
    [
        InlineKeyboardButton(text='⏪ Main Menu', callback_data='to_main'),
    ]
]
currency = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=currency_buttons)

investment_money_buttons = [
    [
        KeyboardButton(text='📈5', callback_data='balance'),
        KeyboardButton(text='📈10', callback_data='balance'),
        KeyboardButton(text='📈50', callback_data='balance'),
    ],
    [
        KeyboardButton(text='📈100', callback_data='balance'),
        KeyboardButton(text='📈250', callback_data='balance'),
        KeyboardButton(text='📈500', callback_data='balance'),
    ],
    [
        KeyboardButton(text='📈1000', callback_data='balance'),
        KeyboardButton(text='📈2500', callback_data='balance'),
        KeyboardButton(text='📈5000', callback_data='balance'),
    ],
    [
        KeyboardButton(text='⏪ Main Menu', callback_data='to_main')
    ]
]
investment_money = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=investment_money_buttons)


investment_to_balance_buttons = [
    [
        KeyboardButton(text='💸5', callback_data='balance'),
        KeyboardButton(text='💸10', callback_data='balance'),
        KeyboardButton(text='💸50', callback_data='balance'),
    ],
    [
        KeyboardButton(text='💸100', callback_data='balance'),
        KeyboardButton(text='💸250', callback_data='balance'),
        KeyboardButton(text='💸500', callback_data='balance'),
    ],
    [
        KeyboardButton(text='💸1000', callback_data='balance'),
        KeyboardButton(text='💸2500', callback_data='balance'),
        KeyboardButton(text='💸5000', callback_data='balance'),
    ],
    [
        KeyboardButton(text='⏪ Main Menu', callback_data='to_main')
    ]
]
investment_to_balance = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=investment_to_balance_buttons)


withdraw_buttons = [
    [
        KeyboardButton(text='💳 To Binance', callback_data='to_binance'),
        KeyboardButton(text='🤖 To Cryptoaddress', callback_data='to_crypto'),
    ],
    [
        KeyboardButton(text='⏪ Main Menu', callback_data='to_main')
    ]
]
withdraw = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=withdraw_buttons)

adm_button = [
    [
        KeyboardButton(text='Issue balance', callback_data='setbalance'),
        KeyboardButton(text='Take away balance', callback_data = 'deletebal'),
    ],
    [
        KeyboardButton(text='⏪ Main Menu', callback_data='to_main')
    ]
]

admBtn = ReplyKeyboardMarkup(resize_keyboard=False, keyboard=adm_button)

oplata = InlineKeyboardMarkup(row_width=1)

oplataBtnfive = InlineKeyboardButton(text='500hundred', callback_data='fivehundred')

oplata.insert(oplataBtnfive)

vipBtn = [
    [
        KeyboardButton(text='Buy VIP status', callback_data='vip')
    ],
    [
        KeyboardButton(text='⏪ Main Menu', callback_data='to_main')
    ]
]

vip = ReplyKeyboardMarkup(resize_keyboard=False, keyboard=vipBtn)

def showKanal():
    keyboard = InlineKeyboardMarkup(row_width=1)

    for channel in CHANNELS:
        btn = InlineKeyboardButton(text=channel[0], url=channel[2])
        keyboard.insert(btn)

    btnDoneSub = InlineKeyboardButton(text='Check subscription', callback_data='subchanneldone')
    keyboard.insert(btnDoneSub)
    return keyboard