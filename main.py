# Lesson17
import json
import yaml
import csv
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
# Создать функцию расчёта кредитов
# Добавляем sum к сумме на счёте клиента. Вычитая со счёта банка (id=0)
# Пишем новые суммы в файл account.csv
# Расчитывем сумму которую надо списывать в месяц
# для этого итоговую сумму (сложный процент) делим на term*12
# Каждый месяц списываем сумму со счёта. Добавляя на счёт банка (id=0)
# Пишем новые суммы в файл account.csv
# Если деньги закончились пишем "Дорогой клиент, погасите ваш кредит. Сумма задолжености "
print(account_d)
for cr in credit_d: #находим запросы на получение кредита
    if cr['sum'] == 0:
        continue
    else:
        for cr_p in account_d: #инициируем процедуру перечисления средств
            if int(cr['id']) == int(cr_p['id']):
                print('аккаунт ', cr_p['id'], ' взял кредит на сумму', cr['sum'])
                account_d[0]['amount'] = int(account_d[0]['amount']) - int(cr['sum'])
                cr_p['amount'] = int(cr_p['amount']) + int(cr['sum'])
            else:
                continue
with open('./data/account.csv', 'w') as open_account: # Запись зменений в account.csv
    write_account = csv.DictWriter(open_account, fieldnames=list(account_d[0].keys()))
    write_account.writeheader()
    for row in account_d:
        write_account.writerow(row)
print(account_d)


