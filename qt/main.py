#############################################################################
##
## Copyright (C) 2016 Klarälvdalens Datakonsult AB, a KDAB Group company, info@kdab.com, author Milian Wolff <milian.wolff@kdab.com>
## Copyright (C) 2021 The Qt Company Ltd.
## Contact: http://www.qt.io/licensing/
##
## This file is part of the Qt for Python examples of the Qt Toolkit.
##
## $QT_BEGIN_LICENSE:BSD$
## You may use this file under the terms of the BSD license as follows:
##
## "Redistribution and use in source and binary forms, with or without
## modification, are permitted provided that the following conditions are
## met:
##   * Redistributions of source code must retain the above copyright
##     notice, this list of conditions and the following disclaimer.
##   * Redistributions in binary form must reproduce the above copyright
##     notice, this list of conditions and the following disclaimer in
##     the documentation and/or other materials provided with the
##     distribution.
##   * Neither the name of The Qt Company Ltd nor the names of its
##     contributors may be used to endorse or promote products derived
##     from this software without specific prior written permission.
##
##
## THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
## "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
## LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
## A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
## OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
## SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
## LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
## DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
## THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
## (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
## OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
##
## $QT_END_LICENSE$
##
#############################################################################


import os
import sys

from PySide6.QtWidgets import QApplication, QDialog
from PySide6.QtGui import QDesktopServices
from PySide6.QtNetwork import QHostAddress, QSslSocket
from PySide6.QtCore import (QFile, QFileInfo, QObject, QUrl)
from PySide6.QtWebChannel import QWebChannel
from PySide6.QtWebSockets import QWebSocketServer

from websocketclientwrapper import WebSocketClientWrapper
from PySide6.QtWebEngineWidgets import QWebEngineView
from webbridge import WebBridge
from testservice import TestService

class Test(QObject):

    def __init__(self, parent=None):
        super().__init__(parent)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    socket_client = WebSocketClientWrapper(12345)
    bridge = WebBridge()
    bridge.bind_service(TestService)
    socket_client.register_obj("bridge", bridge)

    # open a browser window with the client HTML page
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    url = QUrl.fromLocalFile(f"{cur_dir}/index.html")
    wv = QWebEngineView()
    wv.load(url)
    wv.show()

    sys.exit(app.exec())
