import re

import random

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.types.message import ContentType
from aiogram.types import InputFile

from db import Database
import config
import keyboard 

import datetime

from aiogram.contrib.fsm_storage.memory import MemoryStorage


from aiogram.dispatcher import FSMContext

from aiogram.dispatcher.filters.state import StatesGroup, State

from utils import get_investment_text

from datetime import timedelta


bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
db = Database("database.db")
now = datetime.datetime.now()

class Form(StatesGroup):
    vivod = State()
    menu = State()
    popol = State()
    invest = State()
    calc = State()
    addb = State()
    admPass = State()
    oplata = State()

async def on_startup(_):
    print('bot online')

Binance = '555137128' #Payment key

async def check_sub_channels(channels, user_id):
    for channel in channels:
        chat_member = await bot.get_chat_member(chat_id=channel[1], user_id=user_id)
        if chat_member['status'] == 'left':
            return False
    return True

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if message.chat.type != 'private':
        return
    if not db.user_exists(message.from_user.id):
        start_command = message.text 
        referrer_id = str(start_command[7:])
        if str(referrer_id) != "":
            if str(referrer_id) != str(message.from_user.id):
                db.add_user(message.from_user.id, referrer_id)
                try:
                    await bot.send_message(referrer_id, "A new user has registered using your link!")
                except:
                    pass
            else:
                await bot.send_message(message.from_user.id, "You registered using the link!")
        else:
            db.add_user(message.from_user.id)
        if await check_sub_channels(config.CHANNELS, message.from_user.id):
            await bot.send_message(message.from_user.id, "| Welcome to CRYPTMINO |, select the button from the menu", reply_markup=keyboard.main)
        else:
            await bot.delete_message(message.from_user.id)
            await bot.send_message(message.from_user.id, config.NOT_SUB_MESSAGE, reply_markup=keyboard.showKanal())

@dp.callback_query_handler(text='subchanneldone')
async def subchanneldone(message : types.Message):
    await bot.delete_message(message.from_user.id, message.message.message_id)
    if await check_sub_channels(config.CHANNELS, message.from_user.id):
        await bot.send_message(message.from_user.id, f"| Welcome to CRYPTMINO |, select the button from the menu", reply_markup=keyboard.main)
    else:
            await bot.send_message(message.from_user.id, config.NOT_SUB_MESSAGE, reply_markup=keyboard.showKanal())

#User Status

@dp.message_handler(Text("👤 Profile"))
async def profile(message: types.Message, state: FSMContext):
    if db.check_vip(message.from_user.id):
         await bot.send_message(message.from_user.id,text=f"🤖 Your ID: {message.from_user.id}\n🌟 Status: VIP user\n💳 Your Balance: {db.user_balance(message.from_user.id)}$\n👥 Partners: {db.count_reeferals(message.from_user.id)} people.", reply_markup=keyboard.main)
    else:
        await bot.send_message(message.from_user.id,text=f"🤖 Your ID: {message.from_user.id}\n💳 Your Balance: {db.user_balance(message.from_user.id)}$\n👥 Partners: {db.count_reeferals(message.from_user.id)} people.", reply_markup=keyboard.main)
  
@dp.message_handler(Text("🗒 Training"))
async def profile(message: types.Message):
    await bot.send_message(message.from_user.id,text=f"🗒 By clicking on this link, you can find information about working with our service.\n\n----", reply_markup=keyboard.main)

#Investment calculator

@dp.message_handler(Text("🖨 Calculator"))
async def profiler(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id,text=f"💱 Enter investments to calculate your profit.", reply_markup=keyboard.gm)
    await state.set_state(Form.calc)


@dp.message_handler(state=Form.calc)
async def profile(message: types.Message, state: FSMContext):
    money = message.text
    if money.isdigit():
        if round(int(money)) < 50001:
            day = round((int(money) / 100) * 100)
            month = round((int(money) / 100) * 100 * 30)
            year = round((int(money) / 100) * 100 * 365)
            await state.finish()
            await bot.send_message(message.from_user.id,text=f"💱 In this section you will be able to calculate your profit, from the amount of your investment in our project:\n\n💵 Your investment: {money}$\n\n◼️ Profit per day: {day}$\n◼️ Profit per month: {month}$\n◼️ Profit per year: {year}$", reply_markup=keyboard.main)
        else:
            await bot.send_message(message.from_user.id,text=f"⛔ You have exceeded the maximum investment amount of $50,000", reply_markup=keyboard.gm)
    else:
        if message.text == "⏪ Main menu":
            await state.finish()
            await bot.send_message(message.from_user.id,text=f"⏪ You are back to the main menu.", reply_markup=keyboard.main)
        else:
            await bot.send_message(message.from_user.id,text=f"⛔ You entered an incorrect value.", reply_markup=keyboard.gm)

#User financial statistics

@dp.message_handler(Text("💳 Кошелёк"))
async def balance(message: types.Message):
    await bot.send_message(message.from_user.id, f"🤖 Your ID: {message.from_user.id}\n💳 Your Balance: {db.user_balance(message.from_user.id)}$\n\n🔔 Below you can manipulate your wallet", reply_markup=keyboard.currency)

@dp.message_handler(Text("➕ Top up"))
async def balancer(message: types.Message, state=FSMContext):
    await bot.send_message(message.from_user.id, text=f"Select the button with the amount", reply_markup=keyboard.oplata)

#Top up your balance

@dp.callback_query_handler(text='deposit')
async def lol(message: types.Message, state: FSMContext):
    await state.set_state(Form.vivod)
    await bot.send_message(chat_id=call.from_user.id, text='Deposit details balance', description="100", payload="fivehundred", provider_token=Binance, currency='USDT', start_parameter= "balance", prices=[{"label": "$", "amount": 50000}])

@dp.pre_checkout_query_handler()
async def oplataaa(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def oplataqweqwe(message: types.Message):
    if message.successful_payment.invoice_payload == 'fivehundret':
        await bot.send_message(message.from_user.id, f"Payment was successful!")
        db.set_balance(message.from_user.id, balance =+ 500)

#Request for withdrawal

@dp.message_handler(Text("➖ Withdraw"))
async def lol(message: types.Message, state: FSMContext):
    await state.set_state(Form.vivod)
    await bot.send_message(message.from_user.id, text=f"◼️ Enter the amount you want to withdraw from your balance.", reply_markup=keyboard.gm)


@dp.message_handler(state=Form.vivod)
async def get_addrebar(message: types.Message, state: FSMContext):
    user_balance = db.user_balance(message.from_user.id)
    if message.text.isdigit(): 
        if int(message.text) < 100:
             await bot.send_message(message.from_user.id,text=f"⛔ The minimum amount for withdrawal is $100.", reply_markup=keyboard.gm)
        else:
            if user_balance < int(message.text):
                await bot.send_message(message.from_user.id,text=f"⛔ There are insufficient funds in your account", reply_markup=keyboard.gm)
                return
            if db.check_vip(message.from_user.id):
                await bot.send_message(message.from_user.id, f"A withdrawal request has been created, its number: {random.randint(1,1000)}, send this number to the support agent: @keyurohit")
                await state.finish()
            else:
                await bot.send_message(message.from_user.id,text=f"⛔ To withdraw funds, contact the support agent: @keyurohit", reply_markup=keyboard.main)
                await state.finish()
                
    else: 
        if message.text == "⏪ Главное меню":
            await bot.send_message(message.from_user.id,text=f"⏪ You are back to the main menu.", reply_markup=keyboard.main)
            await state.finish()
        if message.text != "⏪ Главное меню":
            await bot.send_message(message.from_user.id,text=f"⛔ You entered an incorrect value.", reply_markup=keyboard.gm)


#Investments

@dp.message_handler(Text("➕ Invest"))
async def balance(message: types.Message, state: FSMContext):
    await state.set_state(Form.invest)
    await bot.send_message(message.from_user.id, text=f"◼️ Enter the amount you want to invest.", reply_markup=keyboard.gm)

#Link to affiliate

@dp.message_handler(Text("👥 affiliate program"))
async def balfdsnce(message: types.Message):
    await bot.send_message(message.from_user.id, text=f"В In this segment of CRYPTMINO we will raise the topic of earning money without investments.\n\n👥 At the moment there is an affiliate program 'CRYPTMINO FRIENDS' - bring your friends, or simply advertise our project on various platforms and receive 10% of the partners' deposit to your account for withdrawal!  \n\nAfter your partner follows your link or tops up your investment account, you will receive a notification.\n\nIn order for your partner to be counted, he needs to follow your affiliate link - https://t.me/{config.BOT_NICKNAME}?start={message.from_user.id}", reply_markup=keyboard.main)

@dp.message_handler(state=Form.invest)
async def get_addrefdsfds(message: types.Message, state: FSMContext):
    user_balance = db.user_balance(message.from_user.id)
    if message.text.isdigit(): 
        if int(message.text) < 100:
             await bot.send_message(message.from_user.id,text=f"⛔ The minimum amount for investment is $10.", reply_markup=keyboard.gm)
        else:
            if user_balance < int(message.text):
                await bot.send_message(message.from_user.id,text=f"⛔ There are insufficient funds in your account", reply_markup=keyboard.gm)
                return

            await state.finish()
            await bot.send_message(message.from_user.id,text=f"✅ You have successfully invested{int(message.text)} рублей", reply_markup=keyboard.main)
            db.add_invest(message.from_user.id, int(message.text))
            db.set_balance(message.from_user.id, int(message.text))
    else: 
        if message.text == "⏪ Main menu":
            await bot.send_message(message.from_user.id,text=f"⏪ You are back to the main menu.", reply_markup=keyboard.main)
            await state.finish()
        if message.text != "⏪ Главное меню":
            await bot.send_message(message.from_user.id,text=f"⛔ You entered an incorrect value.", reply_markup=keyboard.gm)

#Balancing the investment

@dp.message_handler(Text("➖ Collect"))
async def balance(message: types.Message):
    all_cash, investment_text = get_investment_text(db.user_invests(message.from_user.id))
    money = db.all_invests(message.from_user.id)
    user_balance = db.user_balance(message.from_user.id)

    if money > 0:
        await bot.send_message(message.from_user.id, text=f"✅ You have successfully received to your account ${money + all_cash}", reply_markup=keyboard.investment)
    else:
        return await bot.send_message(message.from_user.id, text=f"⛔ There are not enough funds in your investment account", reply_markup=keyboard.investment)

    db.set_balance(message.from_user.id, money+all_cash)
    db.dell_invests(message.from_id)

#Investment Stat (User)

@dp.message_handler(Text("🖥 Investments"))
async def investments(message: types.Message):
    all_cash, investment_text = get_investment_text(db.user_invests(message.from_user.id))
    cash = round(all_cash)
    money = round(db.all_invests(message.from_user.id))
    if money == 'NULL':
        money = 0
    await bot.send_message(message.from_user.id, f"Open your deposit below, and then receive profit from it and collect it in this section: \n\n🖨 Percentage of deposit: 100%\n⏱ Profitability time: 24 hours\n📅 Deposit term: Lifetime\n\n💳 Yours  deposit: ${money}\n💵 Accumulation: ${cash}\n\n⏱ Time before fundraising: 0:00:00", reply_markup=keyboard.investment)


@dp.message_handler(Text("🏦 Transfer to the balance"))
async def to_balance(message: types.Message):
    all_cash, investment_text = get_investment_text(db.user_invests(message.from_user.id))
    await message.reply(f"Your investment income: ${all_cash}.\n\n", reply_markup=keyboard.investment_to_balance)


@dp.message_handler(regexp=r"^💸\d+$")
async def invest_sum(message: types.Message):
    cash = int(re.findall(r"(\d+)", message.text)[0])
    investment_sum, invest_text = get_investment_text(db.user_invests(message.from_user.id))

    if cash > investment_sum:
        return await message.reply(f"You haven't earned this amount yet.  Available for translation: ${investment_sum}.")
    
    db.add_invest(message.from_user.id, "-" + cash)

    await message.reply(f"you translated ${cash}. to the main balance."
                        f"Remaining on your investment balance: {investment_sum - cash}")


@dp.message_handler(Text("📈 Invest"))
async def invest(message: types.Message):
    await message.reply("💵 Select amount", reply_markup=keyboard.investment_money)


@dp.message_handler(regexp=r"^📈\d+$")
async def invest_sum(message: types.Message):
    cash = int(re.findall(r"(\d+)", message.text)[0])
    user_balance = db.user_balance(message.from_user.id)

    if cash > user_balance:
        return await message.reply(f"There is not enough money on the balance sheet.  Top up your balance with {cash - user_balance} usdt.")
    
    db.set_balance(message.from_user.id, user_balance=user_balance-cash)
    db.add_invest(message.from_user.id, cash)

    await message.reply(f"You have invested {cash} usdt. Remaining on your balance: {user_balance - cash}")


@dp.message_handler(Text("💸 Conclusion"))
async def withdraw(message: types.Message):
    await message.reply("💸 Withdrawal of funds", reply_markup=keyboard.withdraw)


@dp.message_handler(Text("⏪ Main menu"))
async def to_main(message: types.Message, state: FSMContext):
   await bot.send_message(message.from_user.id,text=f"⏪ You have successfully returned to the main menu.", reply_markup=keyboard.main)
   await state.finish()
        
#Admin commands

@dp.message_handler(commands="addbalance")
async def addbalance(message: types.Message):
    if db.check_adm(message.from_user.id):
        args = message.text.split()
        db.set_balance(args[1], args[2]) # user id, money
        await bot.send_message(message.from_user.id, text=f"✅ You have successfully topped up your balance.\nUID » {args[1]}\nReplenishment » {args[2]}", reply_markup=keyboard.gm)
    else:
        await bot.send_message(message.from_user.id, f"Only available to administrator.")

@dp.message_handler(commands='awaybalance')
async def awaybalance(message : types.Message):
    if db.check_adm(message.from_user.id):
        args = message.text.split()
        db.awaybalance(args[1], args[2])
        await bot.send_message(message.from_user.id, text=f"✅ You have successfully withdrawn your balance.\nUID » {args[1]}\n They took » {args[2]}", reply_markup=keyboard.gm)
    else:
        await bot.send_message(message.from_user.id, f"Only available to administrator.")

@dp.message_handler(commands="setbalance")
async def balancefdr(message: types.Message):
    if db.check_adm(message.from_user.id):
        args = message.text.split()
        db.set_balance(args[1], args[2])
        await bot.send_message(message.from_user.id, text=f"✅ You have successfully set a new balance value.\nUID » {args[1]}\nBalance » {args[2]}", reply_markup=keyboard.gm)
    else:
        await bot.send_message(message.from_user.id, f"Only available to administrator.")

@dp.message_handler(commands=['stats'])
async def stats(message : types.Message):
    if db.check_adm(message.from_user.id):
        args = message.text.split()
        db.user_balance(args[1])
        await bot.send_message(message.from_user.id, f"Balance: {db.user_balance(args[1])} usdt.")
    else:
        await bot.send_message(message.from_user.id, f"Only available to administrator.")

#instructions for the admin panel are password protected

@dp.message_handler(commands=['adm'])
async def admstart(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, 'Enter your admin password.')
    await state.set_state(Form.admPass)

@dp.message_handler(state = Form.admPass)
async def password(message: types.Message, state: FSMContext):
    if message.text.isdigit(): 
        if int(message.text) == 2002:
                if db.check_adm(message.from_user.id):
                    await bot.send_message(message.from_user.id,text=f"Authorized as an administrator\n\n To view the user's balance, enter /stats ID (/stats 4358734)\n\nTo display the balance, use: /setbalance User ID and amount of money (/setbalance 656545654 12000000).\n\n To  issue a balance to the user (with a referral) use /addbalance ID usera amount of money.  \n\n To withdraw money from the user, enter /awaybalance ID Amount of money.\n\n\n ATTENTION \n\n\n BEFORE WITHDRAWING MONEY FROM THE USER, LOOK AT THE BALANCE SO AS NOT TO CREATE PROBLEMS!  \n\nWe use all commands strictly according to form.  And outside of this guide. ", reply_markup=keyboard.gm)
                else:
                    await bot.send_message(message.from_user.id, f"Only available to administrator.  This is a directory, please notify your supervisor.")
                    await state.finish()
    else: 
        if message.text== "⏪ Главное меню":
            await state.finish()
            await bot.send_message(message.from_user.id,text=f"⏪ You are back to the main menu.", reply_markup=keyboard.main)

@dp.message_handler(Text('VIP status'))
async def vipMain(message: types.Message):
    await bot.send_message(message.from_user.id, f"🤩 VIP status includes:\n🕶 Unique prefix\n💰 Withdrawal faster than usual\n👫 VIP chat\n\n💸 Price 50 USDT.", reply_markup=keyboard.vip)

@dp.message_handler(Text('Купить вип статус'))
async def buyvip(message: types.Message):
    priceVip = 50
    if priceVip > db.user_balance(message.from_user.id):
        await bot.send_message(message.from_user.id, 'Insufficient funds on balance.', reply_markup=keyboard.main)
    elif db.check_vip(message.from_user.id) == 1:
        await bot.send_message(message.from_user.id, "You already have VIP status")
    else:
        await bot.send_message(message.from_user.id, f"You have been given a VIP card for your account, thank you.")
        db.awaybalance(message.from_user.id, 50)
        db.vip(message.from_user.id, +1)
    

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)