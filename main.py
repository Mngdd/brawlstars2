import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QHeaderView
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
import sqlite3


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.con = None
        self.data = []
        uic.loadUi('lcl.ui', self)
        self.load_table()

    def load_table(self):
        if self.con is not None:
            self.con.close()
        self.tablo.setRowCount(0)
        self.con = sqlite3.connect('coffee.sqlite')
        cur = self.con.cursor()
        self.data = cur.execute(f"""SELECT * FROM cofe""").fetchall()  # в разы удобней
        # чем копаться в qtable
        # Получили результат запроса, который ввели в текстовое поле
        print(self.data)
        self.tablo.setRowCount(len(self.data))
        self.tablo.setColumnCount(len(self.data[0]))
        # self.titles = [description[0] for description in cur.description]
        for y in range(len(self.data)):
            for x in range(len(self.data[0])):
                self.tablo.setItem(y, x, QTableWidgetItem(str(self.data[y][x])))

    def update(self):
        if not self.data:
            return -1
        del_id = int(self.id_.text())
        print(del_id)
        try:
            if del_id <= 0:
                raise IndexError
            saved = self.data[del_id - 1]
            cur = self.con.cursor()
            cur.execute(f"""DELETE from films
            WHERE films.id = {del_id}""")
            cur.execute(f"""INSERT INTO films VALUES ({del_id}, '{saved[1][::-1]}', 
            {saved[2] + 1000}, {saved[3]}, {saved[-1] * 2})""")
            self.data = cur.execute(f"""SELECT * FROM films""").fetchall()
            result = cur.execute("SELECT * FROM films WHERE id=?",
                                 (item_id := self.id_.text(),)).fetchall()
            self.tablo.setRowCount(0)
            self.tablo.setRowCount(1)
            self.tablo.setColumnCount(len(result[0]))
            self.titles = [description[0] for description in cur.description]
            for x in range(len(self.data[del_id - 1])):
                self.tablo.setItem(0, x, QTableWidgetItem(str(self.data[del_id - 1][x])))
            self.con.commit()
        except IndexError:
            print('died from cringe')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())
