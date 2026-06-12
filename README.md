# Qt PySide6 Worker Pattern Demo

<img width="600" alt="title" src="https://github.com/user-attachments/assets/95a6669f-0723-4602-80f0-c0372c494833" />

Demonstrates the Qt Worker Thread pattern using QThread subclassing. A WorkerThread base class provides error handling and a do_work() hook for subclasses. The main window manages the worker lifecycle: start, stop, and cleanup on close.


## Run

```
python -m worker_pattern_demo
```

## License

MIT License © 2026 Oleksii Silichenko


# References

- Article on Medium: [Safe QThread Usage in PySide6: Signals, Cancellation, and Error Handling](https://medium.com/@asilichenko/safe-qthread-usage-in-pyside6-signals-cancellation-and-error-handling-bf1823d95354)
- [PySide6.QtCore.QThread](https://doc.qt.io/qtforpython-6/PySide6/QtCore/QThread.html)
- [Gist](https://gist.github.com/asilichenko/6392942d2256993287161cde9dbb9526)
