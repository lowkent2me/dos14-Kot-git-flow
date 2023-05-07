# Lesson17
import json
import yaml
import csv
import time

"""БЛОК ОПРЕДЕЛЕНИЯ ФУНКЦИЙ"""


def straight_perc(s, p, t: int):
    """Функция производит расчёт сложного процента и выводит итоговую сумму
    s - сумма кредита
    p - ставка
    t - срок кредита
    """
    perc = 1 + p / 100
    prof = perc ** t
    raw_sum = s * prof
    end_sum = float('{:.2f}'.format(raw_sum))
    return end_sum


def write_account():
    with open('./data/account.csv', 'w') as open_account:  # Запись изменений в account.csv
        write_account = csv.DictWriter(open_account, fieldnames=list(account_d[0].keys()))
        write_account.writeheader()
        for row in account_d:
            write_account.writerow(row)


def collector(term):
    """Функция списывает денежные средства со счёта клиента в течение года
    term - текущий год от 0"""
    for credit_client in cons_c:  # инициируем процедуру перечисления средств
        for credit_c in account_d:
            if int(credit_c['id']) == int(credit_client['id']):
                if float(credit_c['amount']) >= float(credit_client['month_pay']):
                    if credit_client['end_sum'] <= credit_client['month_pay']:
                        credit_client['end_sum'] = 0
                        print('\nаккаунт ', credit_c['id'], ' выполнил все обязательства по кредиту')
                    else:
                        credit_c['amount'] = float('{:.2f}'.format(credit_c['amount'] -
                                                                   float(credit_client['month_pay'])))

                        account_d[0]['amount'] = float('{:.2f}'.format(account_d[0]['amount']
                                                                       + float(credit_client['month_pay'])))

                        credit_client['end_sum'] = float('{:.2f}'.format(credit_client['end_sum']
                                                                         - float(credit_client['month_pay'])))
                        # print('аккаунт ', credit_c['id'], ' выполнил обязательства по кредиту за ', month + 1,
                        # ' месяц')
                        # print('остаток на счёте аккаунта', credit_c['id'],'=',credit_c['amount'])
                        if month + 1 == 12:
                            print('\nаккаунт ', credit_c['id'], ' выполнил обязательства по кредиту за ', term,
                                  ' год')
                        write_account()
                else:  # Здесь будет альтернативное сообщение по долгу клиента
                    if credit_client['end_sum'] <= credit_client['month_pay']:
                        credit_client['end_sum'] = 0
                        break
                    else:
                        # print('долг аккаунта', credit_c['id'], 'составляет',
                        #           credit_client['end_sum'], 'денег')
                        credit_c['amount'] = float('{:.2f}'.format(credit_c['amount']
                                                                   - float(credit_client['month_pay'])))
                        credit_client['end_sum'] = float('{:.2f}'.format(credit_client['end_sum']
                                                                         - float(credit_client['month_pay'])))
                        print('\nУважаемый клиент', credit_c['id'],
                              '! Рекомендуем немедленно погасить долг по кредиту!', credit_client['end_sum'], 'денег')
                        write_account()


def cashier(term):
    """Функция списывает денежные средства со счёта банка в течение года в пользу клиента по депозиту
    term - текущий год от 0"""
    for vip_client in cons_d:
        if vip_client['end_sum'] > vip_client['month_pay']:
            for vip_c in account_d:
                if int(vip_c['id']) == int(vip_client['id']):
                    if float(account_d[0]['amount']) >= float(vip_client['month_pay']):
                        vip_c['amount'] = float('{:.2f}'.format(float(vip_c['amount'])
                                                                + float(vip_client['month_pay'])))
                        account_d[0]['amount'] = float('{:.2f}'.format(float(account_d[0]['amount'])
                                                                       - float(vip_client['month_pay'])))
                        vip_client['end_sum'] = float('{:.2f}'.format(float(vip_client['end_sum'])
                                                                      - float(vip_client['month_pay'])))
                        # print('аккаунт ', vip_c['id'], ' получил выплаты по депозиту за ', month + 1, ' месяц')
                        # print('остаток на счёте аккаунта', vip_c['id'], '=', vip_c['amount'])
                        if month + 1 == 12:
                            print('\nбанк выполнил обязательства по депозиту за ', term,
                                  ' год в пользу аккаунта', vip_c['id'])
                        write_account()
                    else:
                        vip_c['amount'] = 0
                        write_account()
                        print('СООБЩЕНИЕ ДЛЯ КЛИЕНТА', vip_client['id'],
                              ': Уважаемый клиент! Мы с прискорбием сообщаем, что\n'
                              'ИнвМразьБанк больше не может исполнить обязательства по депозитному договору в связи'
                              ' с\nбанкротством. В связи с этим, согласно пункту 456-с депозитного договора, мы'
                              ' блокируем\nваши счета.\n\n\nДо свидания, мистер лох)\n\nНавеки твой, ИнвМразьБанк\n')
                        vip_client['id'] = -1
                        break
        else:
            for vip_c in account_d:
                if int(vip_c['id']) == int(vip_client['id']):
                    account_d[0]['amount'] = float(account_d[0]['amount']) - float(vip_client['end_sum'])
                    vip_c['amount'] = float(vip_c['amount']) + float(vip_client['end_sum'])
                    vip_client['end_sum'] = 0
                    vip_client['month_pay'] = 0
            continue


def attach_deposit(client):
    """Расчёт конечной суммы платежа в месяц (по депозиту/кредиту)"""
    s_sum = client['sum']
    perc = client['percent']
    term = client['term']
    e_sum = straight_perc(s_sum, perc, term)
    e_pay = float('{:.2f}'.format(((e_sum / 12) / term)))
    client.update(end_sum=float(e_sum), month_pay=float(e_pay))
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
cons_c = []  # заполняем список клиентов банка по кредиту
for cr in credit_d:  # находим запросы на получение кредита
    if cr['sum'] == 0:
        continue
    else:
        for cr_p in account_d:  # инициируем процедуру перечисления средств
            if int(cr['id']) == int(cr_p['id']):
                print('аккаунт ', cr_p['id'], ' взял кредит на сумму', cr['sum'])
                account_d[0]['amount'] = float('{:.2f}'.format(float(account_d[0]['amount']) - float(cr['sum'])))
                cr_p['amount'] = float('{:.2f}'.format(float(cr_p['amount']) + float(cr['sum'])))
                cons_c.append(cr)
write_account()
for cons_p in cons_c:  # расчёт списания средств в счёт кредита
    attach_deposit(cons_p)
    c_pay = cons_p['month_pay']
    if cons_p['term'] == 1:
        print('\nаккаунт ', cons_p['id'], ' должен выплатить ', cons_p['end_sum'], 'денег в течение ', cons_p['term'],
              ' года')
    else:
        print('\nаккаунт ', cons_p['id'], ' должен выплатить ', cons_p['end_sum'], 'денег в течение ', cons_p['term'],
              ' лет')
    print('ежемесячный платёж по кредиту составляет', c_pay, 'денег')
# Создаём функцию расчёта депозитов
cons_d = []  # формирование списка клиентов банка по депозиту
for dep in deposit_d:
    if dep['sum'] != 0:
        for dep_p in account_d:  # записываем клиентов по депозиту в отдельный массив
            if int(dep['id']) == int(dep_p['id']):
                cons_d.append(dep)
for vip in cons_d:  # расчёт зачисления средств по депозиту
    attach_deposit(vip)
    if vip['term'] == 1:
        print('\nаккаунт ', vip['id'], ' получит выплат на сумму', vip['end_sum'], 'денег в течение ', vip['term'],
              ' года')
    else:
        print('\nаккаунт ', vip['id'], ' получит выплат на сумму', vip['end_sum'], 'денег в течение ', vip['term'],
              ' лет')
    print('ежемесячный платёж по депозиту составит', vip['month_pay'], 'денег')

"""Вычисляем максимальный срок просмотра данных по клиентам (равняется максимальному сроку депозита или кредита"""
max_term = 0
for accounts_c in deposit_d:
    if accounts_c['term'] > max_term:
        max_term = int(accounts_c['term'])
    for accounts_d in credit_d:
        if accounts_d['term'] > max_term:
            max_term = int(accounts_d['term'])

print('\nРассматриваемый период:', max_term, 'года')

for i in range(max_term):
    print('\nГОД', i + 1, '\n')
    for month in range(12):
        time.sleep(1)
        cashier(i + 1)
        collector(i + 1)
