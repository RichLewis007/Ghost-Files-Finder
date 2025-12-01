# Filename: status_bar.py
# Author: Rich Lewis @RichLewis007
# Description: Status bar widget displaying scan progress and statistics. Shows progress
#              indicators, match counts, and status messages at the bottom of the main window.

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QFontMetrics, QResizeEvent
from PySide6.QtWidgets import QLabel, QProgressBar, QSizePolicy, QStatusBar, QWidget


class AppStatusBar(QStatusBar):
    # Status bar showing scan progress and stats.

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._progress = QProgressBar(self)
        self._progress.setRange(0, 0)  # Indeterminate by default.
        self._progress.setVisible(False)

        self._stats = QLabel("Ready", self)
        # Configure label to prevent window resizing from long paths
        self._stats.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self._stats.setTextFormat(Qt.TextFormat.PlainText)
        self._stats.setWordWrap(False)
        # Prevent label from expanding beyond available space
        self._stats.setMinimumWidth(0)
        # Store full message for elision on resize
        self._full_message = "Ready"

        self.addWidget(self._stats, 1)
        self.addPermanentWidget(self._progress, 0)

    def set_message(self, message: str) -> None:
        # Display a textual status update, eliding text if necessary to prevent window resizing.
        self._full_message = message
        self._update_elided_text()

    def resizeEvent(self, event: QResizeEvent) -> None:  # pyright: ignore[reportIncompatibleMethodOverride]
        # Re-elide text when status bar is resized.
        super().resizeEvent(event)
        self._update_elided_text()

    def _update_elided_text(self) -> None:
        # Update the label text with proper elision based on available width.
        if not self._full_message:
            self._stats.setText("")
            return

        # Get available width for the stats label
        available_width = self._stats.width()
        if available_width > 0:
            metrics = QFontMetrics(self._stats.font())
            elided_text = metrics.elidedText(
                self._full_message, Qt.TextElideMode.ElideMiddle, available_width
            )
            self._stats.setText(elided_text)
        else:
            # If width not available yet, show full text (will be elided on resize)
            self._stats.setText(self._full_message)

    def set_progress(self, fraction: float | None) -> None:
        # Show progress in the range [0, 1] or hide when ``None``.
        if fraction is None:
            self._progress.setRange(0, 0)
            self._progress.setVisible(False)
        else:
            self._progress.setRange(0, 1000)
            self._progress.setValue(int(fraction * 1000))
            self._progress.setVisible(True)
