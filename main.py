# Lesson17
import json
import yaml
import csv
import time

"""БЛОК ОПРЕДЕЛЕНИЯ ФУНКЦИЙ"""
# расчёт сложного процента
def pow(x,y):
    """функция считает значение x в степени y"""
    i = 1
    power = 1
    for i in range(y):
        power = power * x
        i += i
    return power

percent = lambda f_sum, f_perc: f_sum * f_perc # функция считает итоговую сумму сложного процента

def straight_perc(s,p,t: int):
    """функция производит расчёт сложного процента и выводит итоговую сумму
    s - сумма кредита
    p - ставка
    t - срок кредита
    """
    perc = 1 + p / 100
    prof = pow(perc, t)
    raw_sum = percent(s, prof)
    end_sum = float('{:.2f}'.format(raw_sum))
    return end_sum

pay = lambda end_sum : float('{:.2f}'.format(end_sum / 12)) # расчёт ежемесячного платежа

def write_account():
    with open('./data/account.csv', 'w') as open_account: # Запись зменений в account.csv
        write_account = csv.DictWriter(open_account, fieldnames=list(account_d[0].keys()))
        write_account.writeheader()
        for row in account_d:
            write_account.writerow(row)

def collector(cons_id, dict, term):
    """Функция списывает денежные средства со счёта клиента в течение года
    cons_id - id аккаунта с кредитной задолженностью"""
    for month in range(12):
        time.sleep(1)
        for cr_p in account_d: #инициируем процедуру перечисления средств
            if int(cr_p['id']) == int(cons_id):
                if float(cr_p['amount']) >= float(dict['month_pay']):
                    cr_p['amount'] = int(cr_p['amount']) - int(dict['month_pay'])
                    account_d[0]['amount'] = int(account_d[0]['amount']) + int(dict['month_pay'])
                    dict['end_sum'] = int(dict['end_sum']) - int(dict['month_pay'])
                    # print('аккаунт ', cr_p['id'], ' выполнил обязательства по кредиту за ', month + 1, ' месяц')
                    # print('остаток на счёте аккаунта', cr_p['id'],'=',cr_p['amount'])
                    if month + 1 == 12:
                        print('аккаунт ', cr_p['id'], ' выполнил обязательства по кредиту за ', term, ' год')
                    write_account()
                else: # Здесь будет альтернативное сообщение по долгу клиента
                    cr_p['amount'] = 0
                    write_account()
                    print('у аккаунта', cr_p['id'], 'недостаточно средств для обеспечения обязательств по кредиту за '
                          , month + 1, ' месяц', term, 'года')
                    print('долг аккаунта', cr_p['id'], 'составляет', dict['end_sum'], 'денег')
                    cons_id = -1
                    break
"""КОНЕЦ БЛОКА ОПРЕДЕЛЕНИЯ ФУНКЦИЙ"""

"""Переменные из main
    
"""

# Чтение файлов и составление словарей
with open('./data/credit.json', 'r') as open_credit:
    read_credit = open_credit.read()
    credit_d = json.loads(read_credit)
with open('./data/deposit.yaml', 'r') as open_deposit:
    read_deposit = open_deposit.read()
    deposit_d = yaml.load(read_deposit, Loader=yaml.FullLoader)
with open('./data/account.csv', 'r') as open_account:
    reader_account = csv.DictReader(open_account, delimiter=',')
    account_d = []
    for row in reader_account:
        account_d.append(row)
cons_c = [] # заполняем список клиентов банка по кредиту
for cr in credit_d: #находим запросы на получение кредита
    if cr['sum'] == 0:
        continue
    else:
        for cr_p in account_d: #инициируем процедуру перечисления средств
            if int(cr['id']) == int(cr_p['id']):
                print('аккаунт ', cr_p['id'], ' взял кредит на сумму', cr['sum'])
                account_d[0]['amount'] = int(account_d[0]['amount']) - int(cr['sum'])
                cr_p['amount'] = int(cr_p['amount']) + int(cr['sum'])
                cons_c.append(cr)
write_account()
for cons_p in cons_c: # расчёт списания средств в счёт кредита
    c_sum = int(cons_p['sum'])
    c_perc = int(cons_p['percent'])
    c_term = int(cons_p['term'])
    c_esum = straight_perc(c_sum, c_perc, c_term)
    c_pay = float('{:.2f}'.format(pay(c_esum) / c_term))
    cons_p.update(end_sum=float(c_esum), month_pay=float(c_pay))
    if c_term == 1:
        print('аккаунт ', cons_p['id'], ' должен выплатить ', c_esum, 'денег в течение ', c_term, ' года')
    else:
        print('аккаунт ', cons_p['id'], ' должен выплатить ', c_esum, 'денег в течение ', c_term, ' лет')
    print('ежемесячный платёж по кредиту составляет', c_pay, 'денег')
    for n in range(c_term):
        collector(cons_p['id'], cons_p, n+1)