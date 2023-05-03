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

def collector(cons_id, dict_c, term):
    """Функция списывает денежные средства со счёта клиента в течение года
    cons_id - id аккаунта с кредитной задолженностью
    dict_c - словарь данных одного клиента
    term - срок кредита в годах"""
    for month in range(12):
        time.sleep(1)
        for cr_p in account_d: #инициируем процедуру перечисления средств
            if int(cr_p['id']) == int(cons_id):
                if float(cr_p['amount']) >= float(dict_c['month_pay']):
                    cr_p['amount'] = int(cr_p['amount']) - int(dict_c['month_pay'])
                    account_d[0]['amount'] = int(account_d[0]['amount']) + int(dict_c['month_pay'])
                    dict_c['end_sum'] = int(dict_c['end_sum']) - int(dict_c['month_pay'])
                    # print('аккаунт ', cr_p['id'], ' выполнил обязательства по кредиту за ', month + 1, ' месяц')
                    # print('остаток на счёте аккаунта', cr_p['id'],'=',cr_p['amount'])
                    if month + 1 == 12:
                        print('аккаунт ', cr_p['id'], ' выполнил обязательства по кредиту за ', term, ' год')
                    write_account()
                else: # Здесь будет альтернативное сообщение по долгу клиента
                    cr_p['amount'] = 0-dict_c['end_sum']
                    write_account()
                    print('у аккаунта', cr_p['id'], 'недостаточно средств для обеспечения обязательств по кредиту за '
                          , month + 1, ' месяц', term, 'года')
                    print('долг аккаунта', cr_p['id'], 'составляет', dict_c['end_sum'], 'денег')
                    cons_id = -1
                    break

def cashier(vip_id, dict_d, term):
    """Функция списывает денежные средства со счёта банка в течение года в пользу клиента по депозиту
    vip_id - id аккаунта с кредитной задолженностью
    dict_d - словарь данных одного клиента
    term - срок депозита в годах"""
    for month in range(12):
        time.sleep(1)
        for vip_c in account_d:
            if int(vip_c['id']) == int(vip_id):
                if float(account_d[0]['amount']) >= float(dict_d['month_pay']):
                    vip_c['amount'] = int(vip_c['amount']) + int(dict_d['month_pay'])
                    account_d[0]['amount'] = int(account_d[0]['amount']) - int(dict_d['month_pay'])
                    dict_d['capital'] = int(dict_d['capital']) - int(dict_d['month_pay'])
                    #print('аккаунт ', vip_c['id'], ' получил выплаты по депозиту за ', month + 1, ' месяц')
                    #print('остаток на счёте аккаунта', vip_c['id'], '=', vip_c['amount'])
                    if month + 1 == 12:
                        print('банк выполнил обязательства по депозиту за ', term, ' год в пользу аккаунта'
                              , vip_c['id'])
                    write_account()
                else:
                    vip_c['amount'] = 0
                    write_account()
                    print('СООБЩЕНИЕ ДЛЯ КЛИЕНТА', vip_id, ': Уважаемый клиент! Мы с прискорбием собщаем, что\n'
                          'ИнвМразьБанк больше не может исполнить обязательства по депозитному договору в связи с\n'
                          'банкротством. В связи с этим, согласно пункту 456-с депозитного договора, мы блокируем\n'
                          'ваши счета.\n\n\nДосведания, мистер лох)\n\nНавеки твой, ИнвМразьБанк\n')
                    vip_id = -1
                    break

"""КОНЕЦ БЛОКА ОПРЕДЕЛЕНИЯ ФУНКЦИЙ"""

# Чтение файлов и составление словарей
with open('./data/credit.json', 'r') as open_credit:
    read_credit = open_credit.read()
    credit_ds = json.loads(read_credit)
with open('./data/deposit.yaml', 'r') as open_deposit:
    read_deposit = open_deposit.read()
    deposit_ds = yaml.load(read_deposit, Loader=yaml.FullLoader)
with open('./data/account.csv', 'r') as open_account:
    reader_account = csv.DictReader(open_account, delimiter=',')
    account_ds = []
    for row in reader_account:
        account_ds.append(row)
"""сортировка словарей"""
account_d = sorted(account_ds, key=lambda dictionary_a: int(dictionary_a['id']))
deposit_d = sorted(deposit_ds, key=lambda dictionary_d: dictionary_d['id'])
credit_d = sorted(credit_ds, key=lambda dictionary_c: dictionary_c['id'])
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
# Создаём функцию расчёта депозитов
cons_d = [] # формирование списка клиентов банка по депозиту
for dep in deposit_d:
    if dep['sum'] != 0:
        for dep_p in account_d: # записываем клиентов по депозиту в отдельный массив
            if int(dep['id']) == int(dep_p['id']):
                cons_d.append(dep)
for vip in cons_d: # расчёт зачисления средств по депозиту
    d_sum = vip['sum']
    d_perc = vip['percent']
    d_term = vip['term']
    d_esum = straight_perc(d_sum, d_perc, d_term)
    d_pay = float('{:.2f}'.format(pay(d_esum) / d_term))
    vip.update(capital=float(d_esum), month_pay=float(d_pay))
    if d_term == 1:
        print('аккаунт ', vip['id'], ' получит выпллат на сумму', d_esum, 'денег в течение ', d_term, ' года')
    else:
        print('аккаунт ', vip['id'], ' получит выпллат на сумму', d_esum, 'денег в течение ', d_term, ' лет')
    print('ежемесячный платёж по депозиту составит', d_pay, 'денег')
    for n in range(d_term):
        cashier(vip['id'], vip, n+1)