from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QLabel,
    QTableWidget,
    QTableWidgetItem
)

from database.schema_inspector import SchemaInspector


class UI_table_manager(QMainWindow):

    def __init__(self, table_name):
        super().__init__()

        self.table_name = table_name

        self.setWindowTitle(f"Tabela: {table_name}")

        # ---------- CENTRAL WIDGET ----------

        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout(central)

        # ---------- LABEL ----------

        lbl_table = QLabel(f"Tabela: {table_name}")
        layout.addWidget(lbl_table)

        # ---------- GRID ----------

        self.grid = QTableWidget()
        layout.addWidget(self.grid)

        self.load_table()

    def load_table(self):

        columns = SchemaInspector.get_columns(
            self.table_name
        )

        rows = SchemaInspector.get_rows(
            self.table_name
        )

        # Cabeçalho

        self.grid.setColumnCount(
            len(columns)
        )

        self.grid.setHorizontalHeaderLabels(
            columns
        )

        # Dados

        self.grid.setRowCount(
            len(rows)
        )

        for row_idx, row in enumerate(rows):

            for col_idx, column_name in enumerate(columns):

                value = row[column_name]

                if value is None:
                    value = ""

                self.grid.setItem(
                    row_idx,
                    col_idx,
                    QTableWidgetItem(str(value))
                )

    @classmethod
    def load(cls, table_name):
        cls._janela = cls(table_name)
        cls._janela.resize(1000, 600)
        cls._janela.show()
        return cls._janela