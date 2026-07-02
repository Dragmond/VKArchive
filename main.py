import sys

from PySide6.QtWidgets import QApplication

from gui.main_window import MainWindow

from utils.logger import logger

from utils.constants import APP_NAME


def main():

    logger.info("Application started")

    app = QApplication(sys.argv)

    app.setApplicationName(APP_NAME)

    window = MainWindow()

    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
