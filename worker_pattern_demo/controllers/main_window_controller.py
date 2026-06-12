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

from PySide6.QtCore import Slot, QObject

from worker_pattern_demo.ui import MainWindow, Status
from worker_pattern_demo.workers import BaseWorker, CustomWorker

logger = logging.getLogger(__name__)


class MainWindowController(QObject):
  TIMEOUT: int = 3000

  def __init__(self, window: MainWindow) -> None:
    super().__init__(window)

    self.window: MainWindow = window
    self.worker: BaseWorker | None = None

    self.window.close_event.connect(self.on_window_closed)

    self.window.start_button.clicked.connect(self.on_start_clicked)
    self.window.start_err_button.clicked.connect(self.on_start_err_clicked)
    self.window.stop_button.clicked.connect(self.stop_worker)

  def show_window(self) -> None:
    self.window.show()

  @Slot()
  def on_window_closed(self) -> None:
    self.window.hide()
    if self.worker is not None:
      self.worker.requestInterruption()
      if not self.worker.wait(self.TIMEOUT):
        logger.warning("Worker did not stop in time")

  @Slot()
  def on_start_clicked(self) -> None:
    logger.info("start clicked")
    self.run_worker(CustomWorker())

  @Slot()
  def on_start_err_clicked(self) -> None:
    logger.info("start err clicked")
    self.run_worker(CustomWorker(error_mode=True))

  def run_worker(self, worker: BaseWorker) -> None:
    if self.worker is not None:
      logger.warning("Worker is already running")
      self.window.set_status("Worker is already running")
      return

    self.worker = worker

    worker.progress.connect(self.on_progress_updated)
    worker.result.connect(self.on_result_received)
    worker.error.connect(self.on_error_occurred)
    worker.finished.connect(worker.deleteLater)
    worker.finished.connect(self.remove_worker)

    try:
      worker.start()
      self.window.set_status("Worker started")
    except RuntimeError as ex:
      self.window.set_status(str(ex), Status.ERROR)
      logger.error("Could not start worker", exc_info=ex)

  @Slot()
  def remove_worker(self) -> None:
    self.worker = None
    logger.info("worker removed")

  @Slot()
  def stop_worker(self) -> None:
    logger.info("stop clicked")
    if self.worker is not None:
      self.worker.requestInterruption()

  @Slot(int)
  def on_progress_updated(self, value: int) -> None:
    logger.debug(f"handle: {value}")
    self.window.progress_bar.setValue(value)

  @Slot(str)
  def on_result_received(self, text: str) -> None:
    self.window.set_status(text, Status.COMPLETED if text == "Completed" else Status.DEFAULT)

  @Slot(str)
  def on_error_occurred(self, text: str) -> None:
    self.window.set_status("Error", Status.ERROR)
    logger.error(text)
