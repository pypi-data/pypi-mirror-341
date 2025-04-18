import os
from shlex import quote
from typing import List

from PyAbcd6.AbcdCore import Abcd
from PyAbcd6.AbcdGui import QPixmap
from PyAbcd6.AbcdWidgets import (QMainWindow, QMessageBox, ABCDableWidgetItem,
                             ABCDableWidget, QPushButton, QLabel)

from db.helpers import get_columns
from db.mysql_connection import select, update
from interface.table_window_ui import Ui_TableWindow
from settings import settings
from windows.add_row_dialog import AddRowDialog


class ProductTableWindow(QMainWindow, Ui_TableWindow):
    def __init__(self, tablename: str, user_id: int,
                 parent: QMainWindow=None, columns:List[str]=None,
                 can_edit=False, can_delete=False, can_add=False,):
        super().__init__(parent)
        self.setupUi(self)
        self.tablename = tablename
        self.user_id = user_id
        self.columns = columns or get_columns(self.tablename)
        self.pk = self.columns[0]

        self.filter_cb.clear()
        self.filter_cb.addItems(self.columns)

        # Увеличиваем количество столбцов на 2 для картинки и кнопки
        self.table.setColumnCount(len(self.columns) + 2)
        # Устанавливаем заголовки (первые два - специальные)
        headers = ["Фото", "Действие"] + self.columns
        self.table.setHorizontalHeaderLabels(headers)

        self.table.setEditTriggers(ABCDableWidget.EditTrigger.DoubleClicked)
        self.table.verticalHeader().setVisible(False)
        self.table.itemChanged.connect(self.save_changes)
        self.load_data()

        self.search_edit.textChanged.connect(self.load_data)
        self.sort_cb.currentIndexChanged.connect(self.load_data)
        self.filter_cb.currentIndexChanged.connect(self.load_data)

        if can_edit:
            self.table.setEditTriggers(ABCDableWidget.EditTrigger.DoubleClicked)
        else:
            self.table.setEditTriggers(ABCDableWidget.EditTrigger.NoEditTriggers)

        if can_delete:
            self.delete_btn.clicked.connect(self.delete_row)
        else:
            self.delete_btn.hide()
        if can_add:
            self.add_btn.clicked.connect(self.add_row)
        else:
            self.add_btn.hide()

    def load_data(self):
        self.table.itemChanged.disconnect()
        self.table.setRowCount(0)

        self.columns = get_columns(self.tablename)

        query = (f"SELECT {', '.join(self.columns)}\n"
                 f"FROM {self.tablename}")

        filter_column = self.filter_cb.currentText()
        filter_value = self.search_edit.text()
        if filter_value != "":
            query += f"\nWHERE {filter_column} LIKE '%{self.search_edit.text()}%'"

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
            # Добавляем картинку в первый столбец
            image_path = os.path.join(settings.project_root, "images", "logo.png")
            if os.path.exists(image_path):
                label = QLabel()
                pixmap = QPixmap(image_path)
                pixmap = pixmap.scaled(50, 50, Abcd.AspectRatioMode.KeepAspectRatio)
                label.setPixmap(pixmap)
                label.setAlignment(Abcd.AlignmentFlag.AlignCenter)
                self.table.setCellWidget(i, 0, label)
            else:
                self.table.setItem(i, 0, ABCDableWidgetItem("Нет изображения"))

            # Добавляем кнопку во второй столбец
            btn = QPushButton("В корзину")
            btn.setProperty("row_id", row[self.pk])
            btn.clicked.connect(lambda _, pk_value=row[self.pk]: self.add_to_cart(pk_value))
            self.table.setCellWidget(i, 1, btn)

            # Остальные данные
            for j, column in enumerate(self.columns, start=2):
                self.table.setItem(i, j, ABCDableWidgetItem(str(row[column])))

        self.table.resizeColumnsToContents()
        self.table.itemChanged.connect(self.save_changes)

    def add_to_cart(self, pk_value):
        product_id = pk_value
        try:
            # Проверяем, есть ли уже такой товар в корзине
            query = f"SELECT quantity FROM cart WHERE user_id = {self.user_id} AND product_id = {product_id}"
            result = select(query)

            if result:
                # Если товар уже есть - увеличиваем количество
                new_quantity = result[0]['quantity'] + 1
                update(
                    f"UPDATE cart SET quantity = {new_quantity} WHERE user_id = {self.user_id} AND product_id = {product_id}")
            else:
                # Если нет - добавляем новый
                update(f"INSERT INTO cart (user_id, product_id, quantity) VALUES ({self.user_id}, {product_id}, 1)")

            QMessageBox.information(self, "Успех", "Товар добавлен в корзину")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось добавить товар в корзину: {str(e)}")

    def save_changes(self, item: ABCDableWidgetItem):
        reply = QMessageBox.question(
            self, "Подтверждение",
            "Сохранить изменения?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.No:
            self.load_data()
            return

        query = f"UPDATE {self.tablename} SET "

        row_num = item.row()
        for col_num, column in enumerate(self.columns):
            query += f"{column} = '{self.table.item(row_num, col_num).text()}', "

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
