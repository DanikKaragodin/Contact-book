import sqlite3
import argparse
import sys

# Проверка для выхода из программы


def check():
    print("Еще хотите что-то сделать?\n1.Да\n2.Нет")
    if (input("--> ") == "1"):
        print("Перечень комманд:\n1.Добавить\n2.Изменить существующий контакт\n3.Удалить\n4.Что-то найти\n5.Увидеть полную базу\n000. Выйти из программы")
        return False
    else:
        return True

# Вывод всей базы


def fullBase(c):
    for row in c.execute('SELECT * FROM book '):
        print(row)


def advancedFullBase(c):
    inputValue = input(
        "По какому виду сортировки вам надо показать базу?\n1.По ID(стандартная)\n2.По Имени\n3.По адресу\n4.По номеру\n5.По электронной почте\n--> ")
    if int(inputValue) == 1:
        for row in c.execute('SELECT * FROM book '):
            print(row)
    elif int(inputValue) == 2:
        for row in c.execute('SELECT * FROM book ORDER BY name'):
            print(row)
    elif int(inputValue) == 3:
        for row in c.execute('SELECT * FROM book ORDER BY adress'):
            print(row)
    elif int(inputValue) == 4:
        for row in c.execute('SELECT * FROM book ORDER BY number'):
            print(row)
    elif int(inputValue) == 5:
        for row in c.execute('SELECT * FROM book ORDER BY email'):
            print(row)
    else:
        print("Вы ввели неправльную цифру, из за этого вы ничего не увидели")


# Парсер
parser = argparse.ArgumentParser()

parser.add_argument('-log', '--logs', action="store_true",
                    help="Вывод данных для разработчика")
parser.add_argument('-add', '--adds', action="store_true",
                    help="Сразу проведение функции добавления")
parser.add_argument('-delete', '--deletes', action="store_true",
                    help="Сразу проведение функции удаления")
parser.add_argument('-change', '--changes', action="store_true",
                    help="Сразу проведение функции изменения")
parser.add_argument('-find', '--finds', action="store_true",
                    help="Сразу проведение функции нахождения")
parser.add_argument('-watch', '--watchs', action="store_true",
                    help="Сразу проведение функции просмотра всей базы")
parser.add_argument('-clear', '--clears', action="store_true",
                    help="Очистка всей базы")
args = parser.parse_args()

# Подключение базы
conn = sqlite3.connect('book.sqlite')
c = conn.cursor()

# Попытка создания таблицы
try:
    c.execute('''CREATE TABLE book(
        id INTEGER PRIMARY KEY,
        name text,
        adress text,
        number text,
        email text)''')
    if args.logs:
        print("#Автоматическое создание таблицы призошло успешно")
except(sqlite3.OperationalError):
    if args.logs:
        print("#Автоматическое создание таблицы призошло безуспешно(файл уже создан)")

# Переменная помогающая для выхода из программы
exitFromProgramm = False
# Подсчет последнего id в таблице
kolvoID = 0
for i in c.execute('SELECT * FROM book '):
    kolvoID += 1
if args.logs:
    print("# {} найденное количество id".format(kolvoID))
# Очистка всей базы
if args.clears:
    c.execute("DELETE FROM book ")
    print("Были удалены все данные с таблицы")
    sys.exit()
# Проверка был ли парсинг и надо ли исчезать строке команд

if args.adds or args.changes or args.deletes or args.finds or args.watchs:
    pass
else:
    print("Здравствуйте,что вы хотите сделать с базой данных?\n1.Добавить\n2.Изменить существующий контакт\n3.Удалить\n4.Что-то найти\n5.Увидеть полную базу\n000. Выйти из программы")
# Сам процесс программы
while exitFromProgramm == False:
    if args.adds:
        vibor = "1"
    elif args.changes:
        vibor = "2"
    elif args.deletes:
        vibor = "3"
    elif args.finds:
        vibor = "4"
    elif args.watchs:
        vibor = "5"
    else:
        vibor = input("--> ")
# Добавление
    if(vibor == "1"):
        kolvoID += 1
        name = input("Введите имя: ")
        adress = input("Введите адрес: ")
        number = input("Введите номер телефона: ")
        email = input("Введите адрес электронной почты: ")
        table = [(kolvoID, name, adress, number, email)]
        if name == "" or adress == "" or number == "" or email == "":
            pass
        else:
            c.executemany(
                ''' INSERT OR REPLACE INTO book VALUES (?,?,?,?,?)''', table)
            if args.logs:
                for i in c.execute('SELECT * FROM book WHERE id = ? ', (kolvoID,)):
                    print("#Была введена строка данных:", i)
            conn.commit()
            if args.adds:
                sys.exit()

        exitFromProgramm = check()
# обновления контактной информации
    elif(vibor == "2"):
        if(input("Нужно ли вам посмотреть полную Базу? \n 1. Да \n 0. Нет\n-->") == "1"):
            fullBase(c)
        print("Выберете id контакта, которого вы хотите изменить")
        idChoose = input("--> ")
        name = input("Введите имя(нажимайте Enter если не хотите менять): ")
        adress = input(
            "Введите адрес(нажимайте Enter если не хотите менять): ")
        number = input(
            "Введите номер телефона(нажимайте Enter если не хотите менять): ")
        email = input(
            "Введите адрес электронной почты(нажимайте Enter если не хотите менять): ")
        c.execute('SELECT * FROM book WHERE id = ? ', (idChoose))
        bufferbase = c.fetchone()
        bufferbase = list(bufferbase)
        print(bufferbase)
        if name != "":
            bufferbase[1] = name
        if adress != "":
            bufferbase[2] = adress
        if number != "":
            bufferbase[3] = number
        if email != "":
            bufferbase[4] = email
        if args.logs:
            for i in c.execute('SELECT * FROM book WHERE id = ? ', (idChoose)):
                print("#Была изменена эта строка: ", i)
        print(bufferbase)
        bufferbase = [tuple(bufferbase)]
        c.executemany(
            '''INSERT OR REPLACE INTO book VALUES (?,?,?,?,?)''', bufferbase)
        conn.commit()
        if args.changes:
            sys.exit()
        exitFromProgramm = check()
# Удаление
    elif (vibor == "3"):

        if(input("Нужно ли вам посмотреть полную Базу? \n 1. Да \n 0. Нет\n-->") == "1"):
            fullBase(c)
        print("Выберете id контакта, которого вы хотите удалить")
        idChoose = input("-->")
        if args.logs:
            for i in c.execute('SELECT * FROM book WHERE id = ? ', (idChoose)):
                print("#Была удалена эта строка: ", i)
        c.execute('DELETE FROM book WHERE id = ? ', (idChoose))
        c.execute('UPDATE book SET id = (id-1) WHERE id > ? ', (idChoose))
        conn.commit()
        kolvoID -= 1
        if args.deletes:
            sys.exit()
        exitFromProgramm = check()
# Нахождение
    elif (vibor == "4"):
        print("Какую информацию вы можете дать? Если вы не знаете что написать в одном из пунктов, то просто жмите ENTER")
        name = input("Введите имя: ")
        adress = input("Введите адрес: ")
        number = input("Введите номер телефона: ")
        email = input("Введите адрес электронной почты: ")
        findBase = []
        for row in c.execute('SELECT * FROM book'):
            findBase.append(list(row))
        index = 0
        if name != "":
            for i in range(len(findBase)):
                try:

                    bufferBase = findBase[index]
                    if bufferBase[1] != name:
                        findBase.pop(index)
                        index -= 1
                    index += 1
                except IndexError:
                    break
            index = 0
        if adress != "":
            for i in range(len(findBase)):
                try:
                    bufferBase = findBase[index]
                    if bufferBase[2] != adress:
                        findBase.pop(index)
                        index -= 1
                    index += 1
                except IndexError:
                    break
            index = 0
        if number != "":
            for i in range(len(findBase)):
                try:
                    bufferBase = findBase[index]
                    if bufferBase[3] != number:
                        findBase.pop(index)
                        index -= 1
                    index += 1
                except IndexError:
                    break
            index = 0
        if email != "":
            for i in range(len(findBase)):
                try:
                    bufferBase = findBase[index]
                    if bufferBase[4] != email:
                        findBase.pop(index)
                        index -= 1
                    index += 1
                except IndexError:
                    break
            index = 0
        print("Вот варианты:")
        for x in findBase:
            print(x)
        if args.finds:
            sys.exit()
        exitFromProgramm = check()
# Полная база
    elif (vibor == "5"):
        advancedFullBase(c)
        if args.watchs:
            sys.exit()
        exitFromProgramm = check()
# Выход + неправильный ввод
    elif (vibor == "000"):
        print("Завершение программы. Удачи!")
        exitFromProgramm = True
    else:
        print("Вы ввели неправильную команду")

conn.close()
