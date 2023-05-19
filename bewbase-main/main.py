import sys
import sqlite3
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QTableWidgetItem, QWidget
from PyQt5.uic import loadUi
#имортирвоанеи библиотек

#класс окна авторизации
class Login(QWidget):
    def __init__(self):#функция __init__ вызывается при вызове класса
        super(Login, self).__init__()
        loadUi("authorization.ui",self)#подключение к форме
        self.lePassword.setEchoMode(QtWidgets.QLineEdit.Password)#присвоение кнопкам к их функциям
        self.pbLogin.clicked.connect(self.loginfunction)
    
    def login(self): #показ класса логин (вход)
        self.login = vblbor()
        self.login.show()
        self.hide()

    def loginfunction(self):#проверка при входе на верные данные
        db = sqlite3.connect("zhkha.db")#подключение к базе данных
        sql = db.cursor()
        email= self.leLogin.text()
        password= self.lePassword.text()
        #запрос на проверку данных для входу в SQL
        if email == "admin" and password == "admin":
            print("Вы зашли как админ")
            self.login = vblbor()
            self.login.show()
            self.hide()
        #sql запрос
        sql.execute(f"SELECT * FROM admin WHERE login = '{email}' AND password = '{password}';")
        db.commit() 
#класс окна меню где выбирается нужная база таблица        
class vblbor(QWidget):
    def __init__(self):#функция __init__ вызывается при вызове класса
        super(vblbor, self).__init__()
        loadUi("vblbor.ui", self)#подключение функции к форме ui
        self.pbStatus.clicked.connect(self.gotostatus)#присвоение кнопкам к их функциям
        self.pbKvart.clicked.connect(self.gotokvartira)
        self.pbDogovor.clicked.connect(self.gotodogovor)
        self.pbPlat.clicked.connect(self.gotoplatezhi)
        self.pbSotryd.clicked.connect(self.gotosotrudniki)
        self.pbSchet.clicked.connect(self.gotoscheta)
        self.pbTarif.clicked.connect(self.gototarif)
        self.pbYslygi.clicked.connect(self.gotoyslygi)

    def gotostatus(self):#функция при нажатии определенной кнопки переключается на другой класс(форму)
        self.login = Status()
        self.login.show()
        self.hide()

    def gotokvartira(self):#функция при нажатии определенной кнопки переключается на другой класс(форму)
        self.login = Kvartira()
        self.login.show()
        self.hide()

    def gotodogovor(self):#функция при нажатии определенной кнопки переключается на другой класс(форму)
        self.login = Dogovorbl()
        self.login.show()
        self.hide()

    def gotoplatezhi(self):#функция при нажатии определенной кнопки переключается на другой класс(форму)
        self.login = Platezhi()
        self.login.show()
        self.hide()

    def gotosotrudniki(self):#функция при нажатии определенной кнопки переключается на другой класс(форму)
        self.login = Sotrudniki()
        self.login.show()
        self.hide()

    def gotoscheta(self):#функция при нажатии определенной кнопки переключается на другой класс(форму)
        self.login = Scheta()
        self.login.show()
        self.hide()

    def gototarif(self):#функция при нажатии определенной кнопки переключается на другой класс(форму)
        self.login = Tarif()
        self.login.show()
        self.hide()

    def gotoyslygi(self):#функция при нажатии определенной кнопки переключается на другой класс(форму)
        self.login = Yslygi()
        self.login.show()
        self.hide()
    #стандартный класс 
class Status(QWidget):
    def __init__(self):#функция __init__ вызывается при вызове класса
        super(Status, self).__init__()
        loadUi("status.ui", self)#подключение функции к форме ui
        self.pbOpen.clicked.connect(self.open)#присвоение кнопкам к их функциям
        self.pbInsert.clicked.connect(self.insert)
        self.pbDelete.clicked.connect(self.delete)
        self.pbBack.clicked.connect(self.back)

    def open(self):
        self.conn = sqlite3.connect('zhkha.db')#подключение к БД
        cur = self.conn.cursor()
        data = cur.execute("select * from Статус")
        col_name = [i[0] for i in data.description]
        #создание переменных и присвоение им определенных значений для проверки вывода
        data_rows = data.fetchall()
        self.tableWidget.setColumnCount(len(col_name))
        self.tableWidget.setHorizontalHeaderLabels(col_name)
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(data_rows):
            self.tableWidget.setRowCount(self.tableWidget.rowCount()+1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))
        self.tableWidget.resizeColumnsToContents()
    #функция которая вызывается всегда при нажатии других кнопок для вывода таблицы
    def update_twStaffs(self, query="select * from Статус"):
        try:
            cur = self.conn.cursor()
            data = cur.execute(query).fetchall()
        except Exception as e:
            print(f"Проблемы с подключением к БД. {e}")
            return e
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(data):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() +1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))
            self.tableWidget.resizeColumnsToContents()
    #функция для добавения данных в таблицу
    def insert(self):
        row = [self.leID.text(), self.leName.text()]
        try:
            cur = self.conn.cursor()
            cur.execute(f"""insert into Статус (IDstat, Name)
            values('{row[0]}', '{row[1]}')""")
            self.conn.commit()
            cur.close()
        except Exception as e:
            print("Не смогли добавить запись.")
            return e
        self.update_twStaffs()
    #функция для удаления определеной строчки из таблицы
    def delete(self):
        row = self.tableWidget.currentRow()
        num = self.tableWidget.item(row, 0).text()
        try:
            cur = self.conn.cursor()
            cur.execute(f"delete from Статус where IDstat = {num}")
            self.conn.commit()
            cur.close()
        except Exception as e:
            print(f"Исключение: {e}")
            return e
        self.update_twStaffs()
    #фунция для переключения на другую форму
    def back(self):
        self.login = vblbor()
        self.login.show()
        self.hide()

class Kvartira(QWidget):
    def __init__(self):#подключение функции к форме ui
        super(Kvartira, self).__init__()
        loadUi("kvartira.ui", self)
        self.pbOpen.clicked.connect(self.open)#присвоение кнопкам к их функциям
        self.pbInsert.clicked.connect(self.insert)
        self.pbDelete.clicked.connect(self.delete)
        self.pbBack.clicked.connect(self.back)
        self.pbSearch.clicked.connect(self.search)

    def open(self):
        self.conn = sqlite3.connect('zhkha.db')#подключение к БД
        cur = self.conn.cursor()
        data = cur.execute("select * from Квартиросъемщики")
        col_name = [i[0] for i in data.description]
        data_rows = data.fetchall()
        self.tableWidget.setColumnCount(len(col_name))
        self.tableWidget.setHorizontalHeaderLabels(col_name)
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(data_rows):
            self.tableWidget.setRowCount(self.tableWidget.rowCount()+1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))
        self.tableWidget.resizeColumnsToContents()

    def update_twStaffs(self, query="select * from Квартиросъемщики"):
        try:
            cur = self.conn.cursor()
            data = cur.execute(query).fetchall()
        except Exception as e:
            print(f"Проблемы с подключением к БД. {e}")
            return e
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(data):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() +1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))
            self.tableWidget.resizeColumnsToContents()

    def insert(self):
        row = [self.leIDkv.text(), self.leFIO.text(), self.leCity.text(), self.leStreet.text(), self.leHouse.text(), self.leFlat.text(), self.leTele.text(), self.leDate.text(), self.lePay.text()]
        try:
            cur = self.conn.cursor()
            cur.execute(f"""insert into Квартиросъемщики (IDkv, FIO, City, Street, House, Flat, Telephone, DateOrder, PayMount)
            values('{row[0]}', '{row[1]}', '{row[2]}','{row[3]}','{row[4]}','{row[5]}','{row[6]}','{row[7]}','{row[8]}')""")
            self.conn.commit()
            cur.close()
        except Exception as e:
            print("Не смогли добавить запись.")
            return e
        self.update_twStaffs()

    def delete(self):
        row = self.tableWidget.currentRow()
        num = self.tableWidget.item(row, 0).text()
        try:
            cur = self.conn.cursor()
            cur.execute(f"delete from Квартиросъемщики where IDkv = {num}")
            self.conn.commit()
            cur.close()
        except Exception as e:
            print(f"Исключение: {e}")
            return e
        self.update_twStaffs()

    def search(self):
        row = self.leIDkv.text()
        self.update_twStaffs(f"select * from Квартиросъемщики where IDkv = {row}")

    def back(self):
        self.login = vblbor()
        self.login.show()
        self.hide()

class Dogovorbl(QWidget):
    def __init__(self):#подключение функции к форме ui
        super(Dogovorbl, self).__init__()
        loadUi("dogovorbl.ui", self)
        self.pbOpen.clicked.connect(self.open)#присвоение кнопкам к их функциям
        self.pbInsert.clicked.connect(self.insert)
        self.pbDelete.clicked.connect(self.delete)
        self.pbBack.clicked.connect(self.back)
        self.pbSearch.clicked.connect(self.search)

    def open(self):
        self.conn = sqlite3.connect('zhkha.db')#подключение к БД
        cur = self.conn.cursor()
        data = cur.execute("select * from Договоры")
        col_name = [i[0] for i in data.description]
        data_rows = data.fetchall()
        self.tableWidget.setColumnCount(len(col_name))
        self.tableWidget.setHorizontalHeaderLabels(col_name)
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(data_rows):
            self.tableWidget.setRowCount(self.tableWidget.rowCount()+1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))
        self.tableWidget.resizeColumnsToContents()

    def update_twStaffs(self, query="select * from Договоры"):
        try:
            cur = self.conn.cursor()
            data = cur.execute(query).fetchall()
        except Exception as e:
            print(f"Проблемы с подключением к БД. {e}")
            return e
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(data):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() +1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))
            self.tableWidget.resizeColumnsToContents()

    def insert(self):
        row = [self.leIDdog.text(), self.leNumDog.text(), self.leIDkv.text(), self.leDate.text(), self.leRental.text()]
        try:
            cur = self.conn.cursor()
            cur.execute(f"""insert into Договоры (IDdog, NumDog, IDkv, DateCon, RentalPeriod)
            values('{row[0]}', '{row[1]}', '{row[2]}','{row[3]}','{row[4]}')""")
            self.conn.commit()
            cur.close()
        except Exception as e:
            print("Не смогли добавить запись.")
            return e
        self.update_twStaffs()

    def delete(self):
        row = self.tableWidget.currentRow()
        num = self.tableWidget.item(row, 0).text()
        try:
            cur = self.conn.cursor()
            cur.execute(f"delete from Договоры where IDdog = {num}")
            self.conn.commit()
            cur.close()
        except Exception as e:
            print(f"Исключение: {e}")
            return e
        self.update_twStaffs()

    def search(self):
        row = self.leIDdog.text()
        self.update_twStaffs(f"select * from Договоры where IDdog = {row}")

    def back(self):
        self.login = vblbor()
        self.login.show()
        self.hide()
#класс платежи
class Platezhi(QWidget):
    def __init__(self):#функция __init__ вызывается при вызове класса
        super(Platezhi, self).__init__()
        loadUi("platezhi.ui", self)#подключение функции к форме ui
        self.pbOpen.clicked.connect(self.open)#присвоение кнопкам к их функциям
        self.pbInsert.clicked.connect(self.insert)
        self.pbDelete.clicked.connect(self.delete)
        self.pbBack.clicked.connect(self.back)
        self.pbOplata.clicked.connect(self.oplata)
        self.pbNOplata.clicked.connect(self.noplata)
        self.pbReset.clicked.connect(self.reset)
        self.pbSearch.clicked.connect(self.search)
    #функция для открытия таблицы
    def open(self):
        self.conn = sqlite3.connect('zhkha.db')#подключение к БД
        cur = self.conn.cursor()
        data = cur.execute("select * from Платежи")
        col_name = [i[0] for i in data.description]
        data_rows = data.fetchall()
        self.tableWidget.setColumnCount(len(col_name))
        self.tableWidget.setHorizontalHeaderLabels(col_name)
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(data_rows):
            self.tableWidget.setRowCount(self.tableWidget.rowCount()+1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))
        self.tableWidget.resizeColumnsToContents()
    #функция для проверки ввода данных 
    def update_twStaffs(self, query="select * from Платежи"):
        try:
            cur = self.conn.cursor()
            data = cur.execute(query).fetchall()
        except Exception as e:
            print(f"Проблемы с подключением к БД. {e}")
            return e
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(data):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() +1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))
            self.tableWidget.resizeColumnsToContents()
    #функция для добавления новых данных
    def insert(self):
        row = [self.leIDpay.text(), self.leIDkv.text(), self.leDatePay.text(), self.leSumPay.text(), self.leNumKv.text(), self.leStatus.text()]
        try:
            cur = self.conn.cursor()
            cur.execute(f"""insert into Платежи (IDpay, Idkv, DatePay, SumPay, NumKvartira, StatusPay)
            values('{row[0]}', '{row[1]}', '{row[2]}','{row[3]}','{row[4]}','{row[5]}')""")
            self.conn.commit()
            cur.close()
        except Exception as e:
            print("Не смогли добавить запись.")
            return e
        self.update_twStaffs()
    #функция для обновления данных в таблице
    def reset(self):
        row = [self.leIDpay.text(), self.leDatePay.text(), self.leStatus.text()]
        try:
            cur = self.conn.cursor()
            cur.execute(f"""update Платежи set StatusPay = '{row[2]}', DatePay = '{row[1]}'  where IDpay = '{row[0]}'""")
            self.conn.commit()
            cur.close()
        except Exception as e:
            print("Не смогли добавить запись.")
            return e
        self.update_twStaffs()
    #функция для удаления данных из таблицы
    def delete(self):
        row = self.tableWidget.currentRow()
        num = self.tableWidget.item(row, 0).text()
        try:
            cur = self.conn.cursor()
            cur.execute(f"delete from Платежи where IDpay = {num}")
            self.conn.commit()
            cur.close()
        except Exception as e:
            print(f"Исключение: {e}")
            return e
        self.update_twStaffs()
    #функция для сортировки данных в таблице
    def oplata(self):
        self.conn = sqlite3.connect('zhkha.db')#подключение к БД
        cur = self.conn.cursor()#sql запрос для вывода определенных данных
        data = cur.execute("select * from Платежи where StatusPay = 1")
        col_name = [i[0] for i in data.description]
        data_rows = data.fetchall()
        self.tableWidget.setColumnCount(len(col_name))
        self.tableWidget.setHorizontalHeaderLabels(col_name)
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(data_rows):
            self.tableWidget.setRowCount(self.tableWidget.rowCount()+1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))
        self.tableWidget.resizeColumnsToContents()
    #функция для сортировки данных в таблице
    def noplata(self):
        self.conn = sqlite3.connect('zhkha.db')#подключение к БД
        cur = self.conn.cursor()#sql запрос для вывода определенных данных
        data = cur.execute("select * from Платежи where StatusPay = 2")
        col_name = [i[0] for i in data.description]
        data_rows = data.fetchall()
        self.tableWidget.setColumnCount(len(col_name))
        self.tableWidget.setHorizontalHeaderLabels(col_name)
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(data_rows):
            self.tableWidget.setRowCount(self.tableWidget.rowCount()+1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))
        self.tableWidget.resizeColumnsToContents()

    def search(self):
        row = self.leIDpay.text()
        self.update_twStaffs(f"select * from Платежи where IDpay = {row}")
    #функция для переключения между формами
    def back(self):
        self.login = vblbor()
        self.login.show()
        self.hide()

class Sotrudniki(QWidget):
    def __init__(self):#подключение функции к форме ui
        super(Sotrudniki, self).__init__()
        loadUi("sotrudniki.ui", self)
        self.pbOpen.clicked.connect(self.open)#присвоение кнопкам к их функциям
        self.pbInsert.clicked.connect(self.insert)
        self.pbDelete.clicked.connect(self.delete)
        self.pbBack.clicked.connect(self.back)
        self.pbSearch.clicked.connect(self.search)

    def open(self):
        self.conn = sqlite3.connect('zhkha.db')#подключение к БД
        cur = self.conn.cursor()
        data = cur.execute("select * from Сотрудники")
        col_name = [i[0] for i in data.description]
        data_rows = data.fetchall()
        self.tableWidget.setColumnCount(len(col_name))
        self.tableWidget.setHorizontalHeaderLabels(col_name)
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(data_rows):
            self.tableWidget.setRowCount(self.tableWidget.rowCount()+1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))
        self.tableWidget.resizeColumnsToContents()

    def update_twStaffs(self, query="select * from Сотрудники"):
        try:
            cur = self.conn.cursor()
            data = cur.execute(query).fetchall()
        except Exception as e:
            print(f"Проблемы с подключением к БД. {e}")
            return e
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(data):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() +1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))
            self.tableWidget.resizeColumnsToContents()

    def insert(self):
        row = [self.leID.text(), self.lineEdit_2.text()]
        try:
            cur = self.conn.cursor()
            cur.execute(f"""insert into Сотрудники (IDsotr, FIOsotr)
            values('{row[0]}', '{row[1]}')""")
            self.conn.commit()
            cur.close()
        except Exception as e:
            print("Не смогли добавить запись.")
            return e
        self.update_twStaffs()

    def delete(self):
        row = self.tableWidget.currentRow()
        num = self.tableWidget.item(row, 0).text()
        try:
            cur = self.conn.cursor()
            cur.execute(f"delete from Сотрудники where IDsotr = {num}")
            self.conn.commit()
            cur.close()
        except Exception as e:
            print(f"Исключение: {e}")
            return e
        self.update_twStaffs()

    def search(self):
        row = self.leID.text()
        self.update_twStaffs(f"select * from Сотрудники where IDsotr = {row}")

    def back(self):
        self.login = vblbor()
        self.login.show()
        self.hide()

class Scheta(QWidget):
    def __init__(self):#подключение функции к форме ui
        super(Scheta, self).__init__()
        loadUi("scheta.ui", self)
        self.pbOpen.clicked.connect(self.open)#присвоение кнопкам к их функциям
        self.pbInsert.clicked.connect(self.insert)
        self.pbDelete.clicked.connect(self.delete)
        self.pbBack.clicked.connect(self.back)
        self.pbOplata.clicked.connect(self.oplata)
        self.pbNOplata.clicked.connect(self.noplata)
        self.pbReset.clicked.connect(self.reset)
        self.pbSearch.clicked.connect(self.search)

    def open(self):
        self.conn = sqlite3.connect('zhkha.db')#подключение к БД
        cur = self.conn.cursor()
        data = cur.execute("select * from Счета")
        col_name = [i[0] for i in data.description]
        data_rows = data.fetchall()
        self.tableWidget.setColumnCount(len(col_name))
        self.tableWidget.setHorizontalHeaderLabels(col_name)
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(data_rows):
            self.tableWidget.setRowCount(self.tableWidget.rowCount()+1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))
        self.tableWidget.resizeColumnsToContents()

    def update_twStaffs(self, query="select * from Счета"):
        try:
            cur = self.conn.cursor()
            data = cur.execute(query).fetchall()
        except Exception as e:
            print(f"Проблемы с подключением к БД. {e}")
            return e
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(data):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() +1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))
            self.tableWidget.resizeColumnsToContents()

    def insert(self):
        row = [self.leIDschet.text(), self.leIdkv.text(), self.leDate.text(), self.leSumSchet.text(), self.leStatus.text(), self.leDatePay.text()]
        try:
            cur = self.conn.cursor()
            cur.execute(f"""insert into Счета (IDschet, IDkv, Date, SumSchet, Status, DatePay)
            values('{row[0]}', '{row[1]}', '{row[2]}','{row[3]}','{row[4]}','{row[5]}')""")
            self.conn.commit()
            cur.close()
        except Exception as e:
            print("Не смогли добавить запись.")
            return e
        self.update_twStaffs()

    def reset(self):
        row = [self.leIDschet.text(), self.leStatus.text(), self.leDatePay.text()]
        try:
            cur = self.conn.cursor()
            cur.execute(f"""update Счета set Status = '{row[1]}', DatePay = '{row[2]}' where IDschet = '{row[0]}'""")
            self.conn.commit()
            cur.close()
        except Exception as e:
            print("Не смогли добавить запись.")
            return e
        self.update_twStaffs()

    def search(self):
        row = self.leIDschet.text()
        self.update_twStaffs(f"select * from Счета where IDschet = {row}")
        
    def delete(self):
        row = self.tableWidget.currentRow()
        num = self.tableWidget.item(row, 0).text()
        try:
            cur = self.conn.cursor()
            cur.execute(f"delete from Счета where IDschet = {num}")
            self.conn.commit()
            cur.close()
        except Exception as e:
            print(f"Исключение: {e}")
            return e
        self.update_twStaffs()

    def oplata(self):
        self.conn = sqlite3.connect('zhkha.db')#подключение к БД
        cur = self.conn.cursor()
        data = cur.execute("select * from Платежи where StatusPay = 1")
        col_name = [i[0] for i in data.description]
        data_rows = data.fetchall()
        self.tableWidget.setColumnCount(len(col_name))
        self.tableWidget.setHorizontalHeaderLabels(col_name)
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(data_rows):
            self.tableWidget.setRowCount(self.tableWidget.rowCount()+1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))
        self.tableWidget.resizeColumnsToContents()

    def noplata(self):
        self.conn = sqlite3.connect('zhkha.db')#подключение к БД
        cur = self.conn.cursor()
        data = cur.execute("select * from Платежи where StatusPay = 2")
        col_name = [i[0] for i in data.description]
        data_rows = data.fetchall()
        self.tableWidget.setColumnCount(len(col_name))
        self.tableWidget.setHorizontalHeaderLabels(col_name)
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(data_rows):
            self.tableWidget.setRowCount(self.tableWidget.rowCount()+1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))
        self.tableWidget.resizeColumnsToContents()
        
    def back(self):
        self.login = vblbor()
        self.login.show()
        self.hide()

class Tarif(QWidget):
    def __init__(self):#подключение функции к форме ui
        super(Tarif, self).__init__()
        loadUi("tarif.ui", self)
        self.pbOpen.clicked.connect(self.open)#присвоение кнопкам к их функциям
        self.pbInsert.clicked.connect(self.insert)
        self.pbDelete.clicked.connect(self.delete)
        self.pbBack.clicked.connect(self.back)
        self.pbReset.clicked.connect(self.reset)
        self.pbSearch.clicked.connect(self.search)

    def open(self):
        self.conn = sqlite3.connect('zhkha.db')#подключение к БД
        cur = self.conn.cursor()
        data = cur.execute("select * from Тарифы")
        col_name = [i[0] for i in data.description]
        data_rows = data.fetchall()
        self.tableWidget.setColumnCount(len(col_name))
        self.tableWidget.setHorizontalHeaderLabels(col_name)
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(data_rows):
            self.tableWidget.setRowCount(self.tableWidget.rowCount()+1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))
        self.tableWidget.resizeColumnsToContents()

    def update_twStaffs(self, query="select * from Тарифы"):
        try:
            cur = self.conn.cursor()
            data = cur.execute(query).fetchall()
        except Exception as e:
            print(f"Проблемы с подключением к БД. {e}")
            return e
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(data):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() +1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))
            self.tableWidget.resizeColumnsToContents()

    def insert(self):
        row = [self.leIDtarif.text(), self.leIDyslygi.text(), self.leName.text(), self.lePrice.text()]
        try:
            cur = self.conn.cursor()
            cur.execute(f"""insert into Тарифы (IDtarif, IDyslygi, NameTarif, PriceTarif)
            values('{row[0]}', '{row[1]}', '{row[2]}', '{row[3]}')""")
            self.conn.commit()
            cur.close()
        except Exception as e:
            print("Не смогли добавить запись.")
            return e
        self.update_twStaffs()

    def search(self):
        row = self.leIDtarif.text()
        self.update_twStaffs(f"select * from Тарифы where IDtarif = {row}")

    def reset(self):
        row = [self.leIDtarif.text(), self.lePrice.text()]
        try:
            cur = self.conn.cursor()
            cur.execute(f"""update Тарифы set PriceTarif = '{row[1]}' where IDtarif = '{row[0]}'""")
            self.conn.commit()
            cur.close()
        except Exception as e:
            print("Не смогли добавить запись.")
            return e
        self.update_twStaffs()

    def delete(self):
        row = self.tableWidget.currentRow()
        num = self.tableWidget.item(row, 0).text()
        try:
            cur = self.conn.cursor()
            cur.execute(f"delete from Тарифы where IDtarif = {num}")
            self.conn.commit()
            cur.close()
        except Exception as e:
            print(f"Исключение: {e}")
            return e
        self.update_twStaffs()

    def back(self):
        self.login = vblbor()
        self.login.show()
        self.hide()

class Yslygi(QWidget):
    def __init__(self):#подключение функции к форме ui
        super(Yslygi, self).__init__()
        loadUi("yslygi.ui", self)
        self.pbOpen.clicked.connect(self.open)#присвоение кнопкам к их функциям
        self.pbInsert.clicked.connect(self.insert)
        self.pbDelete.clicked.connect(self.delete)
        self.pbBack.clicked.connect(self.back)
        self.pbSearch.clicked.connect(self.search)

    def open(self):
        self.conn = sqlite3.connect('zhkha.db')#подключение к БД
        cur = self.conn.cursor()
        data = cur.execute("select * from Услуги")
        col_name = [i[0] for i in data.description]
        data_rows = data.fetchall()
        self.tableWidget.setColumnCount(len(col_name))
        self.tableWidget.setHorizontalHeaderLabels(col_name)
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(data_rows):
            self.tableWidget.setRowCount(self.tableWidget.rowCount()+1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))
        self.tableWidget.resizeColumnsToContents()

    def update_twStaffs(self, query="select * from Услуги"):
        try:
            cur = self.conn.cursor()
            data = cur.execute(query).fetchall()
        except Exception as e:
            print(f"Проблемы с подключением к БД. {e}")
            return e
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(data):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() +1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))
            self.tableWidget.resizeColumnsToContents()

    def insert(self):
        row = [self.leID.text(), self.leName.text()]
        try:
            cur = self.conn.cursor()
            cur.execute(f"""insert into Услуги (IDyslygi, NameYslygi)
            values('{row[0]}', '{row[1]}')""")
            self.conn.commit()
            cur.close()
        except Exception as e:
            print("Не смогли добавить запись.")
            return e
        self.update_twStaffs()

    def search(self):
        row = self.leID.text()
        self.update_twStaffs(f"select * from Услуги where IDyslygi = {row}")

    def delete(self):
        row = self.tableWidget.currentRow()
        num = self.tableWidget.item(row, 0).text()
        try:
            cur = self.conn.cursor()
            cur.execute(f"delete from Услуги where Услуги = {num}")
            self.conn.commit()
            cur.close()
        except Exception as e:
            print(f"Исключение: {e}")
            return e
        self.update_twStaffs()

    def back(self):
        self.login = vblbor()
        self.login.show()
        self.hide()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Login()
    # w.addWidget(w)
    w.show()
    sys.exit(app.exec_())