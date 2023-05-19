import sys
import sqlite3

from PyQt5.QtWidgets import QApplication, QWidget, QTableWidgetItem
# from dogovorbl1 import Ui_Form
from PyQt5.uic import loadUi

#STAFF_POSTS = ['бухгалтер', 'менеджер', 'программист']

class Scheta(QWidget):
    def __init__(self):#подключение функции к форме ui
        super(Scheta, self).__init__()
        loadUi("scheta.ui", self)
        self.pbOpen.clicked.connect(self.open)#присвоение кнопкам к их функциям
        self.pbInsert.clicked.connect(self.insert)
        self.pbDelete.clicked.connect(self.delete)
        # self.pbBack.clicked.connect(self.back)
        self.pbOplata.clicked.connect(self.oplata)
        self.pbNOplata.clicked.connect(self.noplata)
        self.pbReset.clicked.connect(self.reset)

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
        
    # def back(self):
    #     self.login = vblbor()
    #     self.login.show()
    #     self.hide()
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Scheta()
    ex.show()
    sys.exit(app.exec_())