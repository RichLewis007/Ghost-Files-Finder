# Filename: settings_dialog.py
# Author: Rich Lewis @RichLewis007
# Description: Settings dialog for application preferences. Allows users to configure
#              logging, UI sounds, completion sounds, and other application settings.

from __future__ import annotations

from PySide6.QtGui import QFont, QShowEvent
from PySide6.QtWidgets import (
    QCheckBox,
    QDialog,
    QDialogButtonBox,
    QLabel,
    QVBoxLayout,
    QWidget,
)

from rfe.services.config import SettingsStore


class SettingsDialog(QDialog):
    # Dialog for application settings and preferences.

    def __init__(self, settings_store: SettingsStore, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._settings_store = settings_store
        self.setWindowTitle("Settings")
        self.setMinimumWidth(400)
        self.setModal(True)

        # Create checkboxes
        self._debug_log_checkbox = QCheckBox("Enable Debug Log Level", self)
        self._ui_sounds_checkbox = QCheckBox("UI Sounds", self)
        self._completion_sound_checkbox = QCheckBox("Scan/Processing completed sound", self)

        # Load current settings
        self._debug_log_checkbox.setChecked(
            self._settings_store.load_debug_log_level(default=False)
        )
        self._ui_sounds_checkbox.setChecked(
            self._settings_store.load_ui_sounds_enabled(default=True)
        )
        self._completion_sound_checkbox.setChecked(
            self._settings_store.load_completion_sound_enabled(default=True)
        )

        # Create layout
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(20, 20, 20, 20)

        # Add title
        title_label = QLabel("Settings", self)
        title_font = QFont(title_label.font())
        title_font.setPointSize(title_font.pointSize() + 4)
        title_font.setBold(True)
        title_label.setFont(title_font)
        layout.addWidget(title_label)

        layout.addSpacing(10)

        # Logging section
        logging_label = QLabel("Logging", self)
        logging_font = QFont(logging_label.font())
        logging_font.setBold(True)
        logging_label.setFont(logging_font)
        layout.addWidget(logging_label)

        layout.addWidget(self._debug_log_checkbox)
        layout.addWidget(
            QLabel(
                "Enable detailed debug logging. Restart required for changes to take effect.",
                self,
            )
        )

        layout.addSpacing(16)

        # Sounds section
        sounds_label = QLabel("Sounds", self)
        sounds_font = QFont(sounds_label.font())
        sounds_font.setBold(True)
        sounds_label.setFont(sounds_font)
        layout.addWidget(sounds_label)

        layout.addWidget(self._ui_sounds_checkbox)
        layout.addWidget(
            QLabel(
                "Enable sound effects for UI interactions (buttons, clicks, etc.). "
                "Scan completion sound can still play when this is disabled.",
                self,
            )
        )

        layout.addSpacing(10)

        layout.addWidget(self._completion_sound_checkbox)
        layout.addWidget(
            QLabel(
                "Play a sound when scanning and processing are completed.",
                self,
            )
        )

        layout.addSpacing(16)

        # Other recommended settings section
        other_label = QLabel("Other", self)
        other_font = QFont(other_label.font())
        other_font.setBold(True)
        other_label.setFont(other_font)
        layout.addWidget(other_label)

        # Add helpful note about future settings
        info_label = QLabel(
            "Additional settings may be added in future versions.",
            self,
        )
        info_label.setStyleSheet("color: #666; font-style: italic;")
        layout.addWidget(info_label)

        layout.addStretch()

        # Dialog buttons
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel,
            self,
        )
        button_box.accepted.connect(self._on_ok)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def showEvent(self, event: QShowEvent) -> None:  # pyright: ignore[reportIncompatibleMethodOverride]
        # Position dialog centered on parent window.
        super().showEvent(event)
        parent = self.parentWidget()
        if parent is not None:
            parent_rect = parent.geometry()
            dialog_rect = self.frameGeometry()
            dialog_rect.moveCenter(parent_rect.center())
            self.move(dialog_rect.topLeft())

    def _on_ok(self) -> None:
        # Save settings and close dialog.
        self._settings_store.save_debug_log_level(self._debug_log_checkbox.isChecked())
        self._settings_store.save_ui_sounds_enabled(self._ui_sounds_checkbox.isChecked())
        self._settings_store.save_completion_sound_enabled(
            self._completion_sound_checkbox.isChecked()
        )
        self.accept()
