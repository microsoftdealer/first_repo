import sys

dino_park = {'din1': {'gemph': 30, 'cost': 500, 'quantity': 0},
             'din2': {'gemph': 220, 'cost': 3000, 'quantity': 0},
             'din3': {'gemph': 1700, 'cost': 20000, 'quantity': 0}}
bonus = 50
gem_salary = 0
balance = 500
real_balance = 0
gem_balance = 0
cash = {'USD': 0, 'RUR': 0}
period = int(sys.argv[1])

def buy_dino(dino_type):
    global dino_park
    global gem_salary
    global balance
    if dino_type == False:
        pass
    else:
        dino_park[dino_type]['quantity'] += 1
        gem_salary += dino_park[dino_type]['gemph']
        balance -= dino_park[dino_type]['cost']

def gem_exchange(num_of_gems):
    global gem_balance
    global real_balance
    global balance
    gem_balance -= num_of_gems
    real_balance += num_of_gems / 300
    balance += num_of_gems / 300 * 2

def count_cash(real_balance):
    global cash
    cash = {'USD': 0, 'RUR': 0}
    cash['USD'] = real_balance / 200
    cash['RUR'] = real_balance / 200 * 65
    print(f"You balance in RUR is equal to {cash['RUR']:04}")
    print(f"or in USD: {cash['USD']:04}")
    return cash

def return_best_offer(balance):
    global dino_park
    best = False
    for key, values in dino_park.items():
        if dino_park[key]['cost'] < balance:
            best = key
        else:
            return best

def count_for_period(days):
    global gem_balance
    global balance
    global bonus
    global gem_salary
    for day in range(days):
        balance += bonus
        gem_balance += 24 * gem_salary
        gem_exchange(gem_balance)
        while return_best_offer(balance):
            buy_dino(return_best_offer(balance))
    print(f'Results for {days} days:')
    count_cash(real_balance)
    print(f'Gem salary per hour: {gem_salary}')
    print('Balance daily growth: ' + str((gem_salary * 24 / 150)))

count_for_period(period)
