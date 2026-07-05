from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QFileDialog,
    QFormLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from utils.config import config


class SettingsWidget(QWidget):

    settingsSaved = Signal()

    def __init__(self, parent=None):

        super().__init__(parent)

        layout = QVBoxLayout(self)

        form = QFormLayout()

        self.downloadPathEdit = QLineEdit()

        self.downloadPathEdit.setPlaceholderText(
            "Папка для архива"
        )

        browseLayout = QHBoxLayout()

        browseLayout.addWidget(self.downloadPathEdit)

        self.browseButton = QPushButton("Выбрать")

        self.browseButton.clicked.connect(
            self._select_download_path
        )

        browseLayout.addWidget(self.browseButton)

        form.addRow(
            "Папка",
            browseLayout,
        )

        self.threadsSpinBox = QSpinBox()

        self.threadsSpinBox.setRange(
            1,
            32,
        )

        form.addRow(
            "Потоки",
            self.threadsSpinBox,
        )

        self.themeComboBox = QComboBox()

        self.themeComboBox.addItem(
            "Тёмная",
            "dark",
        )

        self.themeComboBox.addItem(
            "Светлая",
            "light",
        )

        form.addRow(
            "Тема",
            self.themeComboBox,
        )

        self.continueDownloadCheckBox = QCheckBox(
            "Продолжать прерванные загрузки"
        )

        form.addRow(
            "",
            self.continueDownloadCheckBox,
        )

        self.maxQualityCheckBox = QCheckBox(
            "Скачивать максимальное качество"
        )

        form.addRow(
            "",
            self.maxQualityCheckBox,
        )

        self.writeExifCheckBox = QCheckBox(
            "Записывать EXIF"
        )

        form.addRow(
            "",
            self.writeExifCheckBox,
        )

        self.writeFileDateCheckBox = QCheckBox(
            "Сохранять дату файла"
        )

        form.addRow(
            "",
            self.writeFileDateCheckBox,
        )

        layout.addLayout(form)

        actions = QHBoxLayout()

        actions.addStretch()

        self.saveButton = QPushButton("Сохранить")

        self.saveButton.clicked.connect(
            self.save_settings
        )

        actions.addWidget(self.saveButton)

        layout.addLayout(actions)

        self.load_settings()

    def load_settings(self) -> None:

        settings = config.settings

        self.downloadPathEdit.setText(
            settings.download_path
        )

        self.threadsSpinBox.setValue(
            settings.threads
        )

        theme_index = self.themeComboBox.findData(
            settings.theme
        )

        if theme_index >= 0:

            self.themeComboBox.setCurrentIndex(
                theme_index
            )

        self.continueDownloadCheckBox.setChecked(
            settings.continue_download
        )

        self.maxQualityCheckBox.setChecked(
            settings.download_max_quality
        )

        self.writeExifCheckBox.setChecked(
            settings.write_exif
        )

        self.writeFileDateCheckBox.setChecked(
            settings.write_file_date
        )

    def save_settings(self) -> None:

        settings = config.settings

        settings.download_path = (
            self.downloadPathEdit.text().strip()
        )

        settings.threads = self.threadsSpinBox.value()

        settings.theme = self.themeComboBox.currentData()

        settings.continue_download = (
            self.continueDownloadCheckBox.isChecked()
        )

        settings.download_max_quality = (
            self.maxQualityCheckBox.isChecked()
        )

        settings.write_exif = (
            self.writeExifCheckBox.isChecked()
        )

        settings.write_file_date = (
            self.writeFileDateCheckBox.isChecked()
        )

        config.save()

        self.settingsSaved.emit()

    def _select_download_path(self) -> None:

        path = QFileDialog.getExistingDirectory(
            self,
            "Папка для архива",
            self.downloadPathEdit.text(),
        )

        if not path:
            return

        self.downloadPathEdit.setText(path)
