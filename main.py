from abc import abstractmethod, ABC
import csv
import time
import yaml
import json


class BankProduct:  # Создание класса BankProduct
    def __init__(self, client_id, percent, term, a_sum):
        self.__client_id = client_id
        self.__percent = percent
        self.__term = term
        self.__a_sum = a_sum
        self.__end_sum = float('{:.2f}'.format(self.__a_sum*((1+self.__percent/100)**self.__term)))

    def client_id(self):
        return self.__client_id

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


class Credit(BankProduct, ABC):  # Создание класса Credit, наследник BankProduct
    def __init__(self, client_id, percent, term, a_sum):
        BankProduct.__init__(self, client_id, percent, term, a_sum)
        self.__periods = self.term() * 12
        self.__closed = False

    def periods(self):
        return self.__periods

    def closed(self):
        return self.__closed

    def monthly_fee(self):
        return float('{:.2f}'.format(self.end_sum()/(self.term()*12)))

    def process(self):  # Реализация метода process
        if not self.closed():
            self.__periods = self.__periods - 1  # Уменьшение periods на 1
            if self.__periods == 0:  # Если periods == 0 то closed = True
                self.__closed = True
            else:
                with open('./data/transactions.csv', 'a') as open_trans:  # Запись транзакции в файл transactions.csv
                    file_writer = csv.writer(open_trans, delimiter=",")
                    file_writer.writerow([self.client_id(), self.monthly_fee(),
                                          'sub'])  # user_id,monthly_fee,'subtract'
                    file_writer.writerow(['0', self.monthly_fee(), 'add'])  # 0,monthly_fee,'add'


class Deposit(BankProduct, ABC):  # Создать класс Deposit, наследник BankProduct
    def __init__(self, client_id, percent, term, a_sum):
        BankProduct.__init__(self, client_id, percent, term, a_sum)
        self.__periods = self.term() * 12
        self.__closed = False

    def periods(self):
        return self.__periods

    def closed(self):
        return self.__closed

    def monthly_fee(self):
        return float('{:.2f}'.format((self.end_sum()-self.a_sum())/(self.term()*12)))

    def process(self):  # Реализация метода process аналогична process Credit
        if not self.closed():
            self.__periods = self.__periods - 1
            if self.__periods == 0:
                self.__closed = True
            else:
                with open('./data/transactions.csv', 'a') as open_trans:  # Запись изменений в transactions.csv
                    file_writer = csv.writer(open_trans, delimiter=",")
                    file_writer.writerow(['0', self.monthly_fee(), 'add'])
                    file_writer.writerow([self.client_id(), self.monthly_fee(), 'sub'])


def main():
    with open('./data/credits_deposits.yaml', 'r') as open_db:
        read_db = open_db.read()
        db_ds = yaml.load(read_db, Loader=yaml.FullLoader)  # Из базы данных credits_deposits.yaml получаем данные
    db_dc = sorted(db_ds['credit'], key=lambda dictionary_c: dictionary_c['client_id'])  # Словарь клиентов кредита
    db_dd = sorted(db_ds['deposit'], key=lambda dictionary_c: dictionary_c['client_id'])  # Словарь клиентов депозита
    bank_clients = []  # На их основании создаём объекты Кредитов и депозитов
    for credit_client in db_dc:
        credit = Credit(client_id=credit_client['client_id'], percent=credit_client['percent'],
                        term=credit_client['term'],  a_sum=credit_client['sum'])
        bank_clients.append(credit)
    for deposit_client in db_dd:
        deposit = Deposit(client_id=deposit_client['client_id'], percent=deposit_client['percent'],
                          term=deposit_client['term'],  a_sum=deposit_client['sum'])
        bank_clients.append(deposit)
    max_term = 0
    for clients in bank_clients:
        if int(clients.term()) > max_term:
            max_term = int(clients.term())
    print('Period = '+str(max_term)+' year(s)')
    with open('./data/transactions.csv', 'w') as open_trans:  # Создание файла transactions.csv
        header = ["user_id", "monthly_fee", "subtract/add"]
        file_writer = csv.writer(open_trans, delimiter=",", lineterminator="\r",)
        file_writer.writerow(header)
    for month in range(max_term*12):
        time.sleep(1)  # МЕСЯЦ = 1 секунда
        for clients in bank_clients:  # Каждый месяц вызываем у этих объектов метод process
            print('Monthly fee for client '+str(clients.client_id())+' ='+str(clients.monthly_fee()))
            clients.process()
            if clients.closed():  # Если кредит, депозит закрыт
                if isinstance(clients, Credit):
                    for c in db_dc:
                        if c['client_id'] == clients.client_id():
                            db_dc.remove(c)  # удаляем его из списка
                            to_yaml = {"credit": db_dc, "deposit": db_dd}
                            with open('./data/credits_deposits.yaml', 'w') as f:
                                yaml.dump(to_yaml, f)  # пишем в бд (файл credits_deposits.yaml)
                            print('Client '+str(clients.client_id())+' close his credit')
                elif isinstance(clients, Deposit):
                    for d in db_dd:
                        if d['client_id'] == clients.client_id():
                            db_dd.remove(d)
                            to_yaml = {"credit": db_dc, "deposit": db_dd}
                            with open('./data/credits_deposits.yaml', 'w') as f:
                                yaml.dump(to_yaml, f)
                            print('Client '+str(clients.client_id())+' close his deposit')


main()
