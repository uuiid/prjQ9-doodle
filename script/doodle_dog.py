from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from PyQt5 import QtWidgets
import time


def doodle_syss_run(obj):
    my_event_handler = PatternMatchingEventHandler(obj.patterns,
                                                   obj.ignore_patterns,
                                                   obj.ignore_directories,
                                                   obj.case_sensitive)
    my_event_handler.on_any_event(QtWidgets.QMessageBox.about(None, "ok", 'ok'))
    my_observer = Observer()
    my_observer.schedule(my_event_handler,
                         obj.path,
                         recursive=obj.go_recursively)

    # my_observer.start()
    # try:
    #     while True:
    #         time.sleep(10)
    # except KeyboardInterrupt:
    #     my_observer.stop()
    # my_observer.join()
