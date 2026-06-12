# pyside6-worker-pattern-demo
Demonstrates the Qt Worker Thread pattern using QThread subclassing. A WorkerThread base class provides error handling and a do_work() hook for subclasses. The main window manages the worker lifecycle: start, stop, and cleanup on close. 
