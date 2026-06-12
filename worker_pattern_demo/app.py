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
import sys
from logging.handlers import RotatingFileHandler

from PySide6.QtWidgets import QApplication

from worker_pattern_demo.ui import MainWindow

from worker_pattern_demo.controllers import MainWindowController
from worker_pattern_demo.paths import LOGS

logger = logging.getLogger(__name__)

STYLE = """
QMainWindow, QWidget {
    background-color: #1c1c2e;
    color: #ffffff;
    font-family: "Tahoma", sans-serif;
}

QLabel {
    color: #ffffff;
    padding: 20px 0 0 0;
    font-size: 22px;
}

QLabel#status_label[status="completed"] {
    color: #4cd964;
}

QLabel#status_label[status="error"] {
    color: #ff3b30;
}

QProgressBar {
    background-color: #2c2c44;
    border: none;
    border-radius: 6px;
    height: 20px;
    text-align: right;
    padding-right: 6px;
    color: #ffffff;
    font-size: 12px;
}

QProgressBar::chunk {
    background-color: #2979ff;
    border-radius: 6px;
}

QPushButton {
    border: none;
    border-radius: 8px;
    padding: 12px 16px;
    font-size: 22px;
    color: #ffffff;
    min-height: 25px;
}

QPushButton#start_button {
    background-color: #084992;
}

QPushButton#start_button:hover {
    background-color: #2979ff;
}

QPushButton#start_button:pressed {
    background-color: #1565c0;
}

QPushButton#start_err_button {
    background-color: #2c2c44;
    color: #cccccc;
}

QPushButton#start_err_button:hover {
    background-color: #3a3a55;
}

QPushButton#start_err_button:pressed {
    background-color: #1e1e33;
}

QPushButton#stop_button {
    background-color: #bc3530;
}

QPushButton#stop_button:hover {
    background-color: #e53935;
}

QPushButton#stop_button:pressed {
    background-color: #b71c1c;
}

QPushButton:disabled {
    background-color: #2c2c44;
    color: #555577;
}
"""


def run() -> None:
  logging_config()
  logger.info("Starting")

  app = QApplication(sys.argv)
  app.aboutToQuit.connect(on_shutdown)

  app.setStyleSheet(STYLE)

  try:
    main_wnd = MainWindow()
    _ = MainWindowController(main_wnd)
  except Exception:
    logger.exception("Failed to start")  # auto add traceback
    raise

  main_wnd.show()
  sys.exit(app.exec())  # blocking, last line can be run


def on_shutdown() -> None:
  logger.info("Shutdown")


def logging_config(level=logging.DEBUG):
  root_logger = logging.getLogger()
  root_logger.setLevel(level)

  if root_logger.hasHandlers():
    root_logger.handlers.clear()

  date_format: str = '%Y-%m-%d %H:%M:%S'
  log_format: str = '%(asctime)s [%(levelname)s] %(name)s[%(funcName)s]: %(message)s'
  formatter = logging.Formatter(log_format, date_format)

  console_handler = logging.StreamHandler()
  console_handler.setFormatter(formatter)
  root_logger.addHandler(console_handler)

  LOGS.mkdir(exist_ok=True)

  err_log_handler: logging.FileHandler = RotatingFileHandler(LOGS / "error.log", maxBytes=1_000_000, backupCount=3)
  err_log_handler.setLevel(logging.ERROR)
  err_log_handler.setFormatter(formatter)
  root_logger.addHandler(err_log_handler)

  debug_log_handler: logging.FileHandler = RotatingFileHandler(LOGS / "debug.log", maxBytes=1_000_000, backupCount=3)
  debug_log_handler.setLevel(logging.DEBUG)
  debug_log_handler.setFormatter(formatter)
  root_logger.addHandler(debug_log_handler)

  info_log_handler: logging.FileHandler = RotatingFileHandler(LOGS / "info.log", maxBytes=1_000_000, backupCount=3)
  info_log_handler.setLevel(logging.INFO)
  info_log_handler.setFormatter(formatter)
  root_logger.addHandler(info_log_handler)


if __name__ == '__main__':
  run()
