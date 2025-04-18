from shlex import quote
from typing import Union, List

from PyAbcd6.AbcdWidgets import QMainWindow, QMessageBox, ABCDableWidgetItem, ABCDableWidget, QApplication

from db.helpers import get_columns
from db.mysql_connection import select, update
from interface.table_window_ui import Ui_TableWindow
from windows.add_row_dialog import AddRowDialog


class TableWindow(QMainWindow, Ui_TableWindow):
    def __init__(self, tablename: str, user_id: int,
                 parent: QMainWindow=None, columns:List[str]=None,
                 can_edit=True, can_add=True, can_delete=True):
        """
        Шаблонный класс для CRUD-а с любой таблицей

        :param tablename: название таблицы
        :param user_id: ИД авторизованного пользователя
        :param parent: Родительское окно
        :param columns: Поля, которые нужно отображать в таблице. Если не передать - все
        :param can_edit: Возможность редактировать в таблице
        :param can_add: Возможность добавлять в таблице
        :param can_delete: Возможность удалять записи в таблице
        """
        super().__init__(parent)
        self.setupUi(self)
        self.tablename = tablename
        self.user_id = user_id
        self.columns = columns or get_columns(self.tablename)
        self.pk = self.columns[0]

        self.table.verticalHeader().setVisible(False)
        self.table.setColumnCount(len(self.columns))
        self.table.setHorizontalHeaderLabels(self.columns)
        self.table.itemChanged.connect(self.save_changes)

        self.filter_cb.clear()
        self.filter_cb.addItems(self.columns)

        self.search_edit.textChanged.connect(self.load_data)
        self.sort_cb.currentIndexChanged.connect(self.load_data)
        self.filter_cb.currentIndexChanged.connect(self.load_data)

        self.load_data()


        if can_edit:
            self.table.setEditTriggers(ABCDableWidget.EditTrigger.DoubleClicked)
        else:
            self.table.setEditTriggers(ABCDableWidget.EditTrigger.NoEditTriggers)

        if can_add:
            self.add_btn.clicked.connect(self.add_row)
        else:
            self.add_btn.hide()

        if can_delete:
            self.delete_btn.clicked.connect(self.delete_row)
        else:
            self.delete_btn.hide()

    def load_data(self):
        self.table.itemChanged.disconnect()
        self.table.setRowCount(0)

        filter_column = self.filter_cb.currentText()
        filter_value = self.search_edit.text()

        query = (f"SELECT {', '.join(self.columns)}\n"
                 f"FROM {self.tablename}\n")

        query += f"WHERE user_id = {self.user_id}"
        if filter_value != "":
            query += f"\nAND {filter_column} LIKE '%{self.search_edit.text()}%'"

        try:
            data = select(query)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка при загрузке данных", str(e))
            return

        if not data:
            self.table.setRowCount(0)
            self.table.itemChanged.connect(self.save_changes)
            return

        data = sorted(data,
                      key=lambda row: row[filter_column],
                      reverse=self.sort_cb.currentIndex())
        self.table.setRowCount(len(data))

        for i, row in enumerate(data):
            for j, column in enumerate(row.keys()):
                self.table.setItem(i, j, ABCDableWidgetItem(str(row[column])))

        self.table.resizeColumnsToContents()
        self.table.itemChanged.connect(self.save_changes)

    def save_changes(self, item:ABCDableWidgetItem):
        reply = QMessageBox.question(
            self, "Подтверждение",
            "Сохранить изменения?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.No:
            self.load_data()
            return

        query = f"UPDATE {self.tablename} SET\n"

        row_num = item.row()
        for col_num, column in enumerate(self.columns):
            query += f"{column} = '{self.table.item(row_num, col_num).text()}',\n"

        query = query.rstrip(", ")
        pk_value = self.table.item(row_num, 0).text()
        query += f"WHERE {self.pk} = '{pk_value}'"
        try:
            update(query)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка при попытке сохранения", str(e))

        self.load_data()

    def delete_row(self):
        current_row = self.table.currentRow()
        pk_value = self.table.item(current_row, 0).text()
        pk_value = pk_value if pk_value.isdigit() else quote(pk_value)
        try:
            update(f"DELETE FROM {self.tablename} WHERE {self.pk} = {pk_value}")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка при попытке удаления", str(e))
        self.load_data()

    def add_row(self):
        self.window = AddRowDialog(self.tablename, self)
        self.window.show()


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = TableWindow(tablename="cart", user_id=1,
                              can_edit=False, can_add=False, can_delete=True)
    window.show()
    sys.exit(app.exec())
