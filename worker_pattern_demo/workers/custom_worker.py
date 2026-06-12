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
import time

from .base_worker import BaseWorker

logger = logging.getLogger(__name__)


class CustomWorker(BaseWorker):

  def __init__(self, error_mode: bool = False) -> None:
    super().__init__()
    self.error_mode = error_mode

  def do_work(self) -> None:
    for i in range(100):
      if self.isInterruptionRequested():
        logger.debug("interrupted")
        self.result.emit("Stopping worker...")
        time.sleep(1)
        self.result.emit("Cancelled")
        return

      if self.error_mode and i == 50:
        raise RuntimeError("Error occurs")

      self.progress.emit(i + 1)
      time.sleep(0.05)

    self.result.emit("Completed")
