#  MIT License
#
#  Copyright (c) 2026 Oleksii Sylichenko
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.

import logging

from PySide6.QtCore import Signal, QMargins
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import (
  QLabel,
  QPushButton,
  QVBoxLayout,
  QWidget, QProgressBar,
)

logger = logging.getLogger(__name__)

from PySide6.QtWidgets import QMainWindow
from .props import Status


def set_status(widget: QWidget, status: Status) -> None:
  widget.setProperty("status", status.value)
  widget.style().unpolish(widget)
  widget.style().polish(widget)


class MainWindow(QMainWindow):
  close_event = Signal()

  def __init__(self) -> None:
    super().__init__()
    self._setup_ui()

  def _setup_ui(self) -> None:
    self.setWindowTitle("Worker Example")
    self.resize(320, 320)

    self.label = QLabel("Ready")
    self.progress_bar = QProgressBar()
    self.start_button = QPushButton("Start")
    self.start_err_button = QPushButton("Start with error")
    self.stop_button = QPushButton("Stop")

    self.label.setObjectName("status_label")
    self.start_button.setObjectName("start_button")
    self.start_err_button.setObjectName("start_err_button")
    self.stop_button.setObjectName("stop_button")

    main_layout = QVBoxLayout()

    main_layout.setSpacing(10)
    main_layout.setContentsMargins(QMargins(24, 9, 24, 20))

    main_layout.addWidget(self.label)
    main_layout.addWidget(self.progress_bar)

    btn_layout = QVBoxLayout()
    btn_layout.setSpacing(10)
    btn_layout.setContentsMargins(0, 20, 0, 0)

    btn_layout.addWidget(self.start_button)
    btn_layout.addWidget(self.start_err_button)
    btn_layout.addWidget(self.stop_button)

    main_layout.addLayout(btn_layout)

    w = QWidget()
    w.setLayout(main_layout)
    self.setCentralWidget(w)

  def set_status(self, text: str, status: Status = Status.DEFAULT) -> None:
    self.label.setText(text)
    set_status(self.label, status)

  def closeEvent(self, event: QCloseEvent) -> None:
    self.close_event.emit()
    super().closeEvent(event)
