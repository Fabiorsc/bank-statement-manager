from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QLabel,
    QPushButton,
)


class ClickableLabel(QLabel):
    """
    Label clicável para permitir edição do filtro.
    """

    clicked = Signal()

    def mousePressEvent(self, event):

        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()

        super().mousePressEvent(event)


class UI_filter_chip(QWidget):
    """
    Chip visual de filtro.

    Exemplo:

        [Data: 01/06/2026 a 30/06/2026  ✕]

    Regras:

        - Clique no texto -> editar
        - Clique no X     -> remover
    """

    edit_requested = Signal()
    remove_requested = Signal()

    def __init__(self, texto):
        super().__init__()

        layout = QHBoxLayout(self)

        layout.setContentsMargins(8, 2, 4, 2)
        layout.setSpacing(4)

        self.setStyleSheet(
            """
            UI_filter_chip {
                border: 1px solid #999;
                border-radius: 10px;
                background-color: #f5f5f5;
            }
            """
        )

        self.lbl_texto = ClickableLabel(texto)

        self.btn_remover = QPushButton("✕")
        self.btn_remover.setFixedWidth(20)

        layout.addWidget(self.lbl_texto)
        layout.addWidget(self.btn_remover)

        self.lbl_texto.clicked.connect(
            self.edit_requested.emit
        )

        self.btn_remover.clicked.connect(
            self.remove_requested.emit
        )

    def set_text(self, texto):
        self.lbl_texto.setText(texto)

    def get_text(self):
        return self.lbl_texto.text()