import datetime

DAY_PERCENT = 100


def calculate_investment_cash(investment_money, days):
    investment_money = ((investment_money / 100) * DAY_PERCENT) * days
    return round(investment_money)


def get_investment_text(investments):
    money = ""
    all_cash = 0
    cash_withdraw = 0
    if investments == 'NoneType':
        return
    for investment in investments:
        if investment[1] < 0:
            cash_withdraw += investment[1]
            money += f"You transferred to your main account {-investment[1]} USDT.\n"
            continue

        investment_date = datetime.datetime.fromisoformat(investment[2])
        investment_cash = calculate_investment_cash(investment[1], (datetime.datetime.now() - investment_date).days)
        all_cash += investment_cash
        money += f"Income from investment in the amount {investment[1]} руб.: " \
                 f"{investment_cash} руб.\n"
    return all_cash+cash_withdraw, money