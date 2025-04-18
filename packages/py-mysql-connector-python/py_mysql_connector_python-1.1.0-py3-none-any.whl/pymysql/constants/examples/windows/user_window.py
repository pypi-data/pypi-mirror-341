import logging
import os

from PyAbcd6.AbcdGui import QPixmap
from PyAbcd6.AbcdWidgets import QMainWindow, QMessageBox

from interface.user_window_ui import Ui_UserWindow
from db.mysql_connection import select
from settings import settings
from windows.produtcs_table_window import ProductTableWindow
from windows.table_window import TableWindow


class UserWindow(QMainWindow, Ui_UserWindow):
    def __init__(self, user_id:int, parent: QMainWindow=None):
        super().__init__(parent)
        self.setupUi(self)
        self.user_id = user_id
        self.set_icon()
        self.set_avatar()
        self.set_labels()

        self.back_btn.clicked.connect(self.go_back)
        self.table_button_1.clicked.connect(self.open_cart_window)
        self.table_button_1.setText("Корзина")
        self.table_button_2.clicked.connect(self.open_products_window)
        self.table_button_2.setText("Продукты")

    def set_icon(self):
        try:
            pixmap = QPixmap(
                os.path.join(
                    settings.project_root, "images", "logo.png"
                )
            )
            if not pixmap.isNull():
                self.icon_label.setPixmap(pixmap)
                self.icon_label.setScaledContents(True)
        except Exception as e:
            print(f"Ошибка загрузки иконки: {e}")

    def set_avatar(self):
        try:
            pixmap = QPixmap(
                os.path.join(
                    settings.project_root, "images", "logo.png"
                )
            )
            if not pixmap.isNull():
                self.avatar_label.setPixmap(pixmap)
                self.avatar_label.setScaledContents(True)
        except Exception as e:
            print(f"Ошибка загрузки аватарки: {e}")

    def set_labels(self):
        username = select(
            f"SELECT login FROM users WHERE id = {self.user_id}"
        )[0].get("login", "Undefined")
        self.name_label.setText(username)
        self.role_label.setText("User")

    def go_back(self):
        self.parent().show()
        self.close()

    def open_cart_window(self):
        self.window = TableWindow(tablename="cart", user_id=self.user_id, parent=self,
                                  can_edit=False, can_add=False, can_delete=True)
        self.window.show()

    def open_products_window(self):
        self.window = ProductTableWindow(tablename="products", user_id=self.user_id, parent=self,
                                         can_edit=False, can_add=False, can_delete=False)
        self.window.show()
