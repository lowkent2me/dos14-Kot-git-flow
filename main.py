# Lesson17
import json
import yaml
import csv
import time

"""БЛОК ОПРЕДЕЛЕНИЯ ФУНКЦИЙ"""
# расчёт сложного процента
def pow(x,y):
    """функция считает значение x в степени y"""
    power = 1
    for i in range(y):
        power = power * x
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

pay = lambda end_sum, term : float('{:.2f}'.format((end_sum / 12)/term)) # расчёт ежемесячного платежа

def write_account():
    with open('./data/account.csv', 'w') as open_account: # Запись зменений в account.csv
        write_account = csv.DictWriter(open_account, fieldnames=list(account_d[0].keys()))
        write_account.writeheader()
        for row in account_d:
            write_account.writerow(row)

# def collector(cons_id, dict_c, term):
#     """Функция списывает денежные средства со счёта клиента в течение года
#     term - текущий год от 0"""
#     for month in range(12):
#         for cr_p in account_d: #инициируем процедуру перечисления средств
#             if int(cr_p['id']) == int(cons_id):
#                 if float(cr_p['amount']) >= float(dict_c['month_pay']):
#                     cr_p['amount'] = int(cr_p['amount']) - int(dict_c['month_pay'])
#                     account_d[0]['amount'] = int(account_d[0]['amount']) + int(dict_c['month_pay'])
#                     dict_c['end_sum'] = int(dict_c['end_sum']) - int(dict_c['month_pay'])
#                     # print('аккаунт ', cr_p['id'], ' выполнил обязательства по кредиту за ', month + 1, ' месяц')
#                     # print('остаток на счёте аккаунта', cr_p['id'],'=',cr_p['amount'])
#                     if month + 1 == 12:
#                         print('аккаунт ', cr_p['id'], ' выполнил обязательства по кредиту за ', term, ' год')
#                     write_account()
#                 else: # Здесь будет альтернативное сообщение по долгу клиента
#                     cr_p['amount'] = 0-dict_c['end_sum']
#                     write_account()
#                     print('у аккаунта', cr_p['id'], 'недостаточно средств для обеспечения обязательств по кредиту за '
#                           , month + 1, ' месяц', term, 'года')
#                     print('долг аккаунта', cr_p['id'], 'составляет', dict_c['end_sum'], 'денег')
#                     cons_id = -1
#                     break

def cashier(term):
    """Функция списывает денежные средства со счёта банка в течение года в пользу клиента по депозиту
    term - текущий год от 0"""
    for month in range(12):
        time.sleep(1)
        for vip_client in cons_d:
            if vip_client['end_sum'] > vip_client['month_pay']:
                for vip_c in account_d:
                    if int(vip_c['id']) == int(vip_client['id']):
                        if float(account_d[0]['amount']) >= float(vip_client['month_pay']):
                            vip_c['amount'] = int(vip_c['amount']) + int(vip_client['month_pay'])
                            account_d[0]['amount'] = int(account_d[0]['amount']) - int(vip_client['month_pay'])
                            vip_client['end_sum'] = int(vip_client['end_sum']) - int(vip_client['month_pay'])
                            # print('аккаунт ', vip_c['id'], ' получил выплаты по депозиту за ', month + 1, ' месяц')
                            # print('остаток на счёте аккаунта', vip_c['id'], '=', vip_c['amount'])
                            if month + 1 == 12:
                                print('банк выполнил обязательства по депозиту за ', term,
                                      ' год в пользу аккаунта', vip_c['id'])
                            write_account()
                        else:
                            vip_c['amount'] = 0
                            write_account()
                            print('СООБЩЕНИЕ ДЛЯ КЛИЕНТА', vip_client['id'],
                                  ': Уважаемый клиент! Мы с прискорбием собщаем, что\n'
                                  'ИнвМразьБанк больше не может исполнить обязательства по депозитному договору в связи'
                                  ' с\nбанкротством. В связи с этим, согласно пункту 456-с депозитного договора, мы'
                                  ' блокируем\nваши счета.\n\n\nДосведания, мистер лох)\n\nНавеки твой, ИнвМразьБанк\n')
                            vip_client['id'] = -1
                            break
            else:
                for vip_c in account_d:
                    if int(vip_c['id']) == int(vip_client['id']):
                        account_d[0]['amount'] = int(account_d[0]['amount']) - int(vip_client['end_sum'])
                        vip_c['amount'] = int(vip_c['amount']) + int(vip_client['end_sum'])
                        vip_client['end_sum'] = 0
                        vip_client['month_pay'] = 0
                continue

def attach_deposit(client):
    """Расчёт конечной суммы платежа в месяц (по депозиту/кредиту)"""
    sum = client['sum']
    perc = client['percent']
    term = client['term']
    esum = straight_perc(sum, perc, term)
    epay = float('{:.2f}'.format(pay(esum, term)))
    client.update(end_sum=float(esum), month_pay=float(epay))
    return client
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
# write_account()
for cons_p in cons_c: # расчёт списания средств в счёт кредита
    attach_deposit(cons_p)
    c_pay = cons_p['month_pay']
    if cons_p['term'] == 1:
        print('\nаккаунт ', cons_p['id'], ' должен выплатить ', cons_p['end_sum'], 'денег в течение ', cons_p['term'],
              ' года')
    else:
        print('\nаккаунт ', cons_p['id'], ' должен выплатить ', cons_p['end_sum'], 'денег в течение ', cons_p['term'],
              ' лет')
    print('ежемесячный платёж по кредиту составляет', c_pay, 'денег')
    # for n in range(c_term):
    #     collector(cons_p['id'], cons_p, n+1)
# Создаём функцию расчёта депозитов
cons_d = [] # формирование списка клиентов банка по депозиту
for dep in deposit_d:
    if dep['sum'] != 0:
        for dep_p in account_d: # записываем клиентов по депозиту в отдельный массив
            if int(dep['id']) == int(dep_p['id']):
                cons_d.append(dep)
for vip in cons_d: # расчёт зачисления средств по депозиту
    attach_deposit(vip)
    if vip['term'] == 1:
        print('\nаккаунт ', vip['id'], ' получит выпллат на сумму', vip['end_sum'], 'денег в течение ', vip['term'],
              ' года')
    else:
        print('\nаккаунт ', vip['id'], ' получит выпллат на сумму', vip['end_sum'], 'денег в течение ', vip['term'],
              ' лет')
    print('ежемесячный платёж по депозиту составит', vip['month_pay'], 'денег')
for i in range(5):
    cashier(i+1)
