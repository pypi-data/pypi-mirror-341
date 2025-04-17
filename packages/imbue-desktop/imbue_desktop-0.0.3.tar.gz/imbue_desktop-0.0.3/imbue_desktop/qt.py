import signal
from collections.abc import Callable
from typing import List
from typing import Optional
from urllib.parse import urlparse

from PySide6.QtCore import QTimer
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from PySide6.QtWebEngineCore import QWebEnginePage
from PySide6.QtWebEngineCore import QWebEngineProfile
from PySide6.QtWebEngineCore import QWebEngineUrlRequestInfo
from PySide6.QtWebEngineCore import QWebEngineUrlRequestInterceptor
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QMainWindow
from PySide6.QtWidgets import QToolBar
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QWidget

IMBUE_FRONTEND_TITLE = "Imbue Desktop"


class ImbueApplication(QApplication):
    def __init__(self, sys_argv: List[str], server_url: str, api_key: str) -> None:
        super().__init__(sys_argv)
        self.timer: Optional[QTimer] = None
        self.main_window = ImbueWebWindow(server_url, api_key)
        self.main_window.show()

    def register_signal_handler(self, signal_number: int, handler: Callable) -> None:
        if self.timer is None:
            # Periodically yield control back to Python so that we stay responsive to signals like Ctrl+C.
            self.timer = QTimer(self)
            self.timer.timeout.connect(lambda: None)
            self.timer.start(100)
        signal.signal(signal_number, handler)


class HeaderInterceptor(QWebEngineUrlRequestInterceptor):
    """
    Add the API key to each request that goes to the Imbue server.

    """

    def __init__(self, api_key: str, domain: str) -> None:
        super().__init__()
        self.api_key = api_key
        self.domain = domain

    def interceptRequest(self, info: QWebEngineUrlRequestInfo) -> None:
        if _get_domain(info.requestUrl().toString()) == self.domain:
            info.setHttpHeader(b"Authorization", b"Bearer " + self.api_key.encode())


class ImbueWebWindow(QMainWindow):
    def __init__(self, imbue_frontend_url: str, api_key: str) -> None:
        super().__init__()
        self.imbue_frontend_url = imbue_frontend_url
        self.browser = QWebEngineView()

        self.profile = QWebEngineProfile("custom_profile", self)
        self.interceptor = HeaderInterceptor(api_key, _get_domain(imbue_frontend_url))
        self.profile.setUrlRequestInterceptor(self.interceptor)
        self.browser.setPage(QWebEnginePage(self.profile, self.browser))
        self.browser.setUrl(imbue_frontend_url)
        self.last_url = imbue_frontend_url

        self.browser.urlChanged.connect(self.validate_url_update)

        # Uncomment this once we have in-app routing.
        # self._addNavbar()

        central_widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)  # Remove margins
        layout.setSpacing(0)  # Remove spacing
        layout.addWidget(self.browser)
        central_widget.setLayout(layout)

        self.setCentralWidget(central_widget)
        self.setWindowFlags(Qt.Window)
        self.showMaximized()

    def _addNavbar(self) -> None:
        # Navigation Toolbar
        nav_bar = QToolBar("Navigation")
        nav_bar.setMovable(False)
        self.addToolBar(nav_bar)

        # Back Button
        back_action = QAction("Back", self)
        back_action.triggered.connect(self.browser.back)
        nav_bar.addAction(back_action)

        # Forward Button
        forward_action = QAction("Forward", self)
        forward_action.triggered.connect(self.browser.forward)
        nav_bar.addAction(forward_action)

    def validate_url_update(self, qurl) -> None:
        url = qurl.toString()
        if urlparse(url).netloc != _get_domain(self.imbue_frontend_url):
            self.browser.setUrl(self.last_url)
            return
        self.last_url = qurl


def _get_domain(url: str) -> str:
    return urlparse(url).netloc
