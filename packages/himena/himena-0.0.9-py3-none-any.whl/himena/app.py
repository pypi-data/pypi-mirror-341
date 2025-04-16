from __future__ import annotations

import sys
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Generic, TypeVar
from psygnal import Signal
from himena.exceptions import ExceptionHandler

if TYPE_CHECKING:
    from IPython import InteractiveShell
    from qtpy.QtWidgets import QApplication
    from warnings import WarningMessage

_A = TypeVar("_A")  # the backend application type


class EventLoopHandler(ABC, Generic[_A]):
    errored = Signal(Exception)
    warned = Signal(object)
    _instances: dict[str, QtEventLoopHandler] = {}

    def __init__(self, name: str):
        self._name = name
        self._instances[name] = self

    @classmethod
    def create(cls, name: str):
        if name not in cls._instances:
            cls._instances[name] = QtEventLoopHandler(name)
        return cls._instances[name]

    @abstractmethod
    def get_app(self) -> _A:
        """Get Application instance."""

    @abstractmethod
    def run_app(self):
        """Start the event loop."""


def gui_is_active(event_loop: str) -> bool:
    """True only if "%gui **" magic is called in ipython kernel."""
    shell = get_ipython_shell()
    return shell and shell.active_eventloop == event_loop


class QtEventLoopHandler(EventLoopHandler["QApplication"]):
    _APP: QApplication | None = None

    def get_app(self):
        """Get QApplication."""
        self.gui_qt()
        app = self.instance()
        if app is None:
            app = self.create_application()
        self._APP = app
        return app

    def create_application(self) -> QApplication:
        from qtpy.QtCore import Qt
        from qtpy.QtWidgets import QApplication
        from qtpy import QT6

        if not QT6:
            QApplication.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling)
        return QApplication([])

    def run_app(self):
        """Start the event loop."""
        if not gui_is_active("qt"):
            with ExceptionHandler(
                hook=self._except_hook,
                warning_hook=self._warn_hook,
            ) as _:
                self.get_app().exec()
            return None

        return self.get_app().exec()

    def instance(self) -> QApplication | None:
        """Get QApplication instance or None if it does not exist."""
        from qtpy.QtWidgets import QApplication

        return QApplication.instance()

    def gui_qt(self) -> None:
        """Call "%gui qt" magic."""
        if not gui_is_active("qt"):
            shell = get_ipython_shell()
            if shell and shell.active_eventloop != "qt":
                shell.enable_gui("qt")
        return None

    def _except_hook(self, exc_type: type[Exception], exc_value: Exception, exc_tb):
        """Exception hook used during application execution."""
        return self.errored.emit(exc_value)

    def _warn_hook(self, warning: WarningMessage):
        """Warning hook used during application execution."""
        return self.warned.emit(warning)


class EmptyEventLoopHandler(EventLoopHandler):
    def get_app(self):
        return None

    def run_app(self):
        return None


def get_event_loop_handler(backend: str, app_name: str) -> EventLoopHandler:
    if backend == "qt":
        return QtEventLoopHandler.create(app_name)
    else:
        return EmptyEventLoopHandler.create(app_name)


def get_ipython_shell() -> InteractiveShell | None:
    """Get ipython shell if available."""
    if "IPython" in sys.modules:
        from IPython import get_ipython

        return get_ipython()
    else:
        return None
