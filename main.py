# МЕСЯЦ = 1 секунда
# Реализовать метод process
#   Записать транзакции в файл transactions.csv
#   user_id,monthly_fee,'add'
#   0,monthly_fee,'substract'
#   Уменьшить priods на 1
#   Если periods == 0 то closed = True
# Из базы данных credits_deposits.json получить данные
# На их основании создать объекты Кредитов и депозитов
# Каждый месяц вызывать у этих объектов метод process
# Если кредит, депозит закрыт удаляем его из списка и пишем в бд (файл credits_deposits.json)
from abc import abstractmethod, ABC
import csv
import json
import time
# Создать класс BankProduct
#   задать свойства entity_id, percent, term, sum
#   задать свойство end_sum Расчёт сложного процента (используя свойства объекта)
#   свойства эти должны быть только на чтение
#   создать метод process он должен быть абстрактным те никакой конкретной реализации не должно быть
class BankProduct:
    def __init__(self, entity_id, percent, term, a_sum):
        self.__entity_id = entity_id
        self.__percent = percent
        self.__term = term
        self.__a_sum = a_sum
        self.__end_sum = float('{:.2f}'.format(self.__a_sum*((1+self.__percent/100)**self.__term)))
    def entity_id(self):
        return self.__entity_id
    def percent(self):
        return self.__percent
    def term(self):
        return self.__term
    def a_sum(self):
        return self.__a_sum
    def end_sum(self):
        return self.__end_sum
    @abstractmethod
    def process(self):
        pass
# Создать класс Credit
#   Унаследоваться от BankProduct
#   Создать свойство только на чтение periods = term*12
#   Создать свойство только на чтение closed = False
#   Создать свойство monthly_fee = end_sum / term*12
class Credit(BankProduct, ABC):
    def __init__(self, entity_id, percent, term, a_sum):
        BankProduct.__init__(self, entity_id, percent, term, a_sum)
        self.__periods = self.term() * 12
        self.__closed = False
    def periods(self):
        return self.__periods
    def closed(self):
        return self.__closed
    def monthly_fee(self):
        return float('{:.2f}'.format(self.end_sum()/(self.term()*12)))
    # Реализовать метод process
    #   Записать транзакции в файл transactions.csv
    #   user_id,monthly_fee,'subtract'
    #   0,monthly_fee,'add'
    #   Уменьшить periods на 1
    #   Если periods == 0 то closed = True
    def process(self):
        if not self.__closed:
            if self.__periods != 0:
                with open('./data/transactions.csv', 'a') as open_trans:  # Запись изменений в transactions.csv
                    file_writer = csv.writer(open_trans, delimiter=",")
                    file_writer.writerow([self.entity_id(), self.monthly_fee(), 'sub'])
                    file_writer.writerow(['0', self.monthly_fee(), 'add'])
                self.__periods -= 1
            else:
                self.__closed = True
# Создать класс Deposit
#   Унаследоваться от BankProduct
#   Создать свойство только на чтение periods = term*12
#   Создать свойство только на чтение closed = False
#   Создать свойство monthly_fee = end_sum / term*12
class Deposit(BankProduct, ABC):
    def __init__(self, entity_id, percent, term, a_sum):
        BankProduct.__init__(self, entity_id, percent, term, a_sum)
        self.__periods = self.term() * 12
        self.__closed = False
    def periods(self):
        return self.__periods
    def closed(self):
        return self.__closed
    def monthly_fee(self):
        return float('{:.2f}'.format(self.end_sum()/(self.term()*12)))
    # Реализовать метод process
    #   Записать транзакции в файл transactions.csv
    #   user_id,monthly_fee,'subtract'
    #   0,monthly_fee,'add'
    #   Уменьшить periods на 1
    #   Если periods == 0 то closed = True
    def process(self):
        if not self.__closed:
            if self.__periods != 0:
                with open('./data/transactions.csv', 'a') as open_trans:  # Запись изменений в transactions.csv
                    file_writer = csv.writer(open_trans, delimiter=",")
                    file_writer.writerow(['0', self.monthly_fee(), 'add'])
                    file_writer.writerow([self.entity_id(), self.monthly_fee(), 'sub'])
                self.__periods -= 1
            else:
                self.__closed = True

def main():
    with open('./data/credits_deposits.json', 'r') as open_db:
        read_db = open_db.read()
        db_ds = json.loads(read_db)
    db_dc = sorted(db_ds['credit'], key=lambda dictionary_c: dictionary_c['entity_id'])
    db_dd = sorted(db_ds['deposit'], key=lambda dictionary_c: dictionary_c['entity_id'])
    print(db_dc)
    print(db_dd)
    bank_clients = []
    for credit_client in db_dc:
        credit = Credit(entity_id=credit_client['entity_id'], percent=credit_client['percent'],
                        term=credit_client['term'],  a_sum=credit_client['sum'])
        bank_clients.append(credit)
    for deposit_client in db_dd:
        deposit = Deposit(entity_id=deposit_client['entity_id'], percent=deposit_client['percent'],
                        term=deposit_client['term'],  a_sum=deposit_client['sum'])
        bank_clients.append(deposit)
    max_term = 0
    for clients in bank_clients:
        if int(clients.term()) > max_term:
            max_term = int(clients.term())
    #     for deposit in array_deposit:
    #         if deposit['term'] > max_term:
    #             max_term = int(deposit['term'])
    print('Period = '+str(max_term))
    with open('./data/transactions.csv', 'w') as open_trans:  # Создание файла transactions.csv
        header = ["user_id", "monthly_fee", "subtract/add"]
        file_writer = csv.writer(open_trans, delimiter=",", lineterminator="\r",)
        file_writer.writerow(header)
    for year in range(1, max_term):
        for month in range(1, 12):
            time.sleep(0.2)
            for clients in bank_clients:
                if clients.closed():
                    bank_clients.remove(clients)
                    print('Client '+str(clients.entity_id())+' was removed, cause client close his credit/deposit')
                else:
                    clients.process()



main()
