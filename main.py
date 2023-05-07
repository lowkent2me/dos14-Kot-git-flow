# МЕСЯЦ = 1 секунда
# Создать класс BankProduct
# задать свойства entity_id, percent, term, sum
# задать свойство end_sum Расчёт сложного процента (используя свойства объекта)
# свойства эти должны быть только на чтение
# создать метод process он должен быть абстрактным те никакой конкретной реализации не должно быть
# Создать класс Credit
# Унаследоваться от BankProduct
# Создать свойство только на чтение periods = term*12
# Создать свойство только на чтение closed = False
# Создать свойство monthly_fee = end_sum / term*12
# Реализовать метод process
# Записать транзакции в файл transactions.csv
# user_id,monthly_fee,'substract'
# 0,monthly_fee,'add'
# Уменьшить priods на 1
# Если periods == 0 то closed = True
# Создать класс Deposit
# Унаследоваться от BankProduct
# Создать свойство только на чтение periods = term*12
# Создать свойство только на чтение closed = False
# Создать свойство monthly_fee = end_sum / term*12
# Реализовать метод process
# Записать транзакции в файл transactions.csv
# user_id,monthly_fee,'add'
# 0,monthly_fee,'substract'
# Уменьшить priods на 1
# Если periods == 0 то closed = True
# Из базы данных credits_deposits.json получить данные
# На их основании создать объекты Кредитов и депозитов
# Каждый месяц вызывать у этих объектов метод process
# Если кредит, депозит закрыт удаляем его из списка и пишем в бд (файл credits_deposits.json)
from abc import abstractmethod
class BankProduct():
    def __init__(self, entity_id, percent, term, a_sum):
        self.__entity_id = entity_id
        self.__percent = percent
        self.__term = term
        self.__a_sum = a_sum
        self.__end_sum = a_sum+((1+percent/100)**term)

    @abstractmethod
    def process(self):
        pass
# class Credit(BankProduct):
#     periods = term * 12
#     closed = False
#     monthly_fee = end_sum / (term*12)