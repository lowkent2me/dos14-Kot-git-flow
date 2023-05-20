# dos14-Kot-git-flow

Этот репозиторий был создан специально для выполнения домашних заданий по курсу TeachMeSkills DevOps.  
Владелец репозитория: Кот Виталий Сергеевич.  
Здесь будет описан процесс выполнения домашних заданий.  

# Lesson-14 (Git)  
1. Создать новый репозиторий dos14-family_name-git-flow - Выполнено  
2. Создать 2 ветки master develop - Выполнено  
3. Создать ветку feature-hw-14 - Выполнено  
4. Добавит информацию о репозитории в README.md - Выполнено  
5. Сделать pull request в develop (после подтверждения @ggramal выполнить слияние) - Выполнено  
5.1. *выполнить слияние всех веток в репозитории с предыдущими домашними работами - Выполнено  
6. Сделать из develop release-v0.0.1  - Выполнено  
7. Выполнить слияние develop с master и сделать тэг v0.0.1 - Выполнено  
8. Удалить release-v0.0.1 - Выполнено  
---

# Lesson-15 (Python 1)  
1. Установить python 3.11 через pyenv - Выполнено  
2. Создать проект с помощью poetry - Выполнено  
3. Добавить группу зависимостей dev, сделать её опциональной и добавить black пакет - Выполнено  
4. Создать main.py с кодом - если переменная среды 'SHELL' равна '/bin/bash', напечатать в консоль Greetings bash  
если другое значение, Hello <Значение переменной среды> - Выполнено  
5. Выполнить black ./ - Выполнено  
6. Commit все файлы в feature ветку, выполнить слияние с develop - Выполнено  
7. По готовности сделать PR в master с approver @ggramal, отписаться в групповом чате - Выполнено  
---

# Lesson-16 (Python 2)
## Расчёт сложного процента - Выполнено 
База данных отдаёт 3 массива строк: сумма, ставка, срок. Все строки имеют вид  
"<id>_<сумма|ставка|срок>".   
Используя эти данные рассчитать итоговую сумму и получить массив из словарей  
```
[  
{"id": <some_id>, "start_sum": <some_sum>, "rate": <some_rate>, "term": <some_term>, "end_sum":  
<calculated_end_sum>}  
....  
]  
sum ["1_1000","2_30000","3_100000","8_100","5_11111","9_14124124124","6_444","4_123456","7_100000000000","10_81214"]  
rate % ["1_10","2_11","3_8","4_13","5_11""6_6","7_9","8_11","9_13","10_12"]  
term-years ["1_1","2_2","3_2","4_6","5_8""6_20","7_9","8_11","9_13","10_12"]  
```
---

# Lesson-17 (Python 3)
* **МЕСЯЦ = 10 секунд**
* Прочитать информацию о кредитах из файла credit.json
    * создать список словарей с атрибутами кредитов
* Прочитать информацию о депозитах из файла deposit.yaml
    * создать список словарей с атрибутами депозитов
* Прочитать информацию о счетах клиентов из файла account.csv
    * создать список словарей с атрибутами счетов
* Создать функцию расчёта кредитов
    * Добавляем sum к сумме на счёте клиента. Вычитая со счёта банка (id=0)
    * Пишем новые суммы в файл account.csv
    * Рассчитываем сумму которую надо списывать в месяц
        * для этого итоговую сумму (сложный процент) делим на term*12
    * Каждый месяц списываем сумму со счёта. Добавляя на счёт банка (id=0)
    * Пишем новые суммы в файл account.csv
    * Если деньги закончились, пишем "Дорогой клиент, <id> погасите ваш кредит. Сумма задолженности
      <sum>"
* Создать функцию расчёта депозитов
    * Рассчитываем сумму которую надо добавлять в месяц
        * для этого итоговую сумму (сложный процент) делим на term*12
    * Каждый месяц добавляем сумму на счёт клиента. Списывая со счёта банка (id=0)
    * Каждый месяц пишем новые суммы в файл account.csv  
---


# Lesson-18 (Python 4)
* **МЕСЯЦ = 1 секунда**
* Создать класс BankProduct
  * задать свойства entity_id, percent, term, sum
  * задать свойство end_sum Расчёт сложного процента (используя свойства объекта)
  * свойства эти должны быть только на чтение
  * создать метод process он должен быть абстрактным те никакой конкретной реализации не должно быть
* Создать класс Credit
  * Потомок BankProduct
  * Создать свойство только на чтение periods = term*12
  * Создать свойство только на чтение closed = False
  * Создать свойство monthly_fee = end_sum / term*12
* Реализовать метод process
  * Записать транзакции в файл transactions.csv
  * user_id,monthly_fee,'subtract'
  * 0,monthly_fee,'add'
  * Уменьшить periods на 1
  * Если periods == 0 то closed = True
* Создать класс Deposit
  * Потомок BankProduct
  * Создать свойство только на чтение periods = term*12
  * Создать свойство только на чтение closed = False
  * Создать свойство monthly_fee = end_sum / term*12
  * Реализовать метод process
* Записать транзакции в файл transactions.csv
  * user_id,monthly_fee,'add'
  * 0,monthly_fee,'subtract'
  * Уменьшить periods на 1
  * Если periods == 0 то closed = True
* Из базы данных credits_deposits.json получить данные
* На их основании создать объекты Кредитов и депозитов
*              Каждый месяц вызывать у этих объектов метод process
* Если кредит, депозит закрыт удаляем его из списка и пишем в бд (файл credits_deposits.json)
---


# Lesson-19 (Python 5)
* **МЕСЯЦ = 1 секунда**
* Переименовываем entity_id в client_id во всех классах
* Исправляем баг в monthly_fee для Deposits он должен быть проценты_по_вкладу_за_весь_срок/(term*12)
* Устанавливаем Flask через poetry
* Добавляем  через poetry зависимость account
  * зависимость ссылается на git https://github.com/ggramal/dos14-gramovich-git-flow.git
  * from account_clients import AccountClient
* Метод process Deposit/Credit теперь не пишет в файл а создаёт объекты AccountClient для каждого client_id и использует метод transaction
* При инициализации Deposit создаём объект AccountClient и меняем в нём withdraw на False
* Добавляем логику для инициализации кредитов (первичное пополнение счёта клиента)
* Наш сервис должен иметь следующий http интерфейс
  * GET /api/v1/credits/<client_id> - получить данные о кредите клиента
    * Если нет клиента ответить 404 и {"status": "error", "message": f"Client {client_id} does not have active credits"}
  * GET /api/v1/deposits/<client_id> - получить данные о депозите клиента
    * Если нет клиента ответить 404 и {"status": "error", "message": f"Client {client_id} does not have active deposits"}
  * GET /api/v1/deposits - получить данные о всех депозитах
  * GET /api/v1/credits - получить данные о всех кредитах
  * PUT /api/v1/credits - создать кредит для клиента используя {"client_id": <client_id>, "percent": <percent>, "sum": <sum>, "term": <term>}
    * Пишем в файл credits_deposits.yaml
    * Если клиент есть ответить 400 и {"status": "error", "message": f"Credit for client {client_id} already exists"}
  * PUT /api/v1/deposits - создать deposit для клиента используя {"client_id": <client_id>, "percent": <percent>, "sum": <sum>, "term": <term>}
    * Пишем в файл credits_deposits.yaml
    * Если клиент есть ответить 400 и {"status": "error", "message": f"Deposit for client {client_id} already exists"
* В отдельном от flask потоке(thread) мы раз в месяц вызываем process кредитов и депозитов
  * сервис не должен хранить состояние (те быть stateless). Это значит, что при старте сервиса мы должны продолжить обрабатывать кредиты и депозиты с того момента где мы закончили
  ---