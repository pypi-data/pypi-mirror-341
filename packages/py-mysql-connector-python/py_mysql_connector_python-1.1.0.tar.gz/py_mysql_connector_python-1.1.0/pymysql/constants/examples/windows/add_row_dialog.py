from PyAbcd6.AbcdWidgets import QPushButton, QLineEdit, QVBoxLayout, QLabel, QWidget, QMainWindow, QMessageBox

from db.helpers import get_columns
from db.mysql_connection import update


class AddRowDialog(QMainWindow):
    def __init__(self, tablename: str, parent: QWidget = None):
        super().__init__(parent)
        self.tablename = tablename
        self.columns = get_columns(self.tablename)

        self.columns = list(filter(lambda c: "id" not in c, self.columns))

        self.setWindowTitle(f"Добавить {tablename}")
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        self.layout = QVBoxLayout(central_widget)

        self.fields = self.create_fields_for_columns(self.columns)

        self.add_btn = QPushButton("Добавить")
        self.add_btn.clicked.connect(self.save)
        self.layout.addWidget(self.add_btn)

        self.setLayout(self.layout)

    def save(self):
        columns = []
        values = []
        for field, value in self.fields.items():
            if value:
                columns.append(field)
                values.append(value.text())

        query = (f"INSERT INTO {self.tablename} ({', '.join(columns)}) "
                 f"VALUES ({', '.join(values)})")
        try:
            update(query)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка при попытке сохранения", str(e))
            return
        self.parent().load_data()
        self.close()

    def create_fields_for_columns(self, columns: list[str]) -> dict[str, QLineEdit]:
        line_edits = dict()

        for column in columns:
            self.layout.addWidget(QLabel(f"{column}:"))
            line_edits[column] = QLineEdit()
            self.layout.addWidget(line_edits[column])

        return line_edits
