import sys
import sqlite3

from PyQt5.QtWidgets import QApplication, QWidget, QTableWidgetItem
# from dogovorbl1 import Ui_Form
from PyQt5.uic import loadUi

#STAFF_POSTS = ['бухгалтер', 'менеджер', 'программист']

class Tarif(QWidget):
    def __init__(self):
        super(Tarif, self).__init__()
        loadUi("tarif.ui", self)
        # self.setupUi(self)
        #self.cbPost.addItems(STAFF_POSTS)
        self.pbOpen.clicked.connect(self.open)
        self.pbInsert.clicked.connect(self.insert)
        self.pbDelete.clicked.connect(self.delete)

    def open(self):
        #try:
        self.conn = sqlite3.connect('zhkha.db')
        cur = self.conn.cursor()
        data = cur.execute("select * from Тарифы")
        col_name = [i[0] for i in data.description]
        data_rows = data.fetchall()
        #except Exception as e:
            # print("Ошибка с подключением к базе данных")
            # return e
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
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Tarif()
    ex.show()
    sys.exit(app.exec_())