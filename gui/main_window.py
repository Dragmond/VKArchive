from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
)


class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()

        self.setWindowTitle("VK Archive")
        self.resize(900, 700)

        central = QWidget()

        self.setCentralWidget(central)

        layout = QVBoxLayout(central)

        title = QLabel("VK Archive")

        title.setStyleSheet("""
            font-size:26px;
            font-weight:bold;
        """)

        layout.addWidget(title)

        self.loginButton = QPushButton("Войти в VK")

        layout.addWidget(self.loginButton)

        layout.addStretch()