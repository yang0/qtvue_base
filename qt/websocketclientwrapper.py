#############################################################################
##
## Copyright (C) 2017 Klarälvdalens Datakonsult AB, a KDAB Group company, info@kdab.com, author Milian Wolff <milian.wolff@kdab.com>
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

import sys
from PySide6.QtWebChannel import QWebChannel
from PySide6.QtCore import QObject, Signal, Slot
from PySide6.QtNetwork import QHostAddress, QSslSocket
from PySide6.QtWebSockets import QWebSocketServer
from PySide6.QtWidgets import QApplication
from webbridge import WebBridge
from websockettransport import WebSocketTransport
from webservice_config import services


class WebSocketClientWrapper(QObject):
   """Wraps connected QWebSockets clients in WebSocketTransport objects.

      This code is all that is required to connect incoming WebSockets to
      the WebChannel. Any kind of remote JavaScript client that supports
      WebSockets can thus receive messages and access the published objects.
   """
   client_connected = Signal(WebSocketTransport)

   def __init__(self, app:QApplication,  port, parent=None):
      """Construct the client wrapper with the given parent. All clients
         connecting to the QWebSocketServer will be automatically wrapped
         in WebSocketTransport objects."""
      super().__init__(parent)
      self._server = self._create_server(port)
      self._server.newConnection.connect(self.handle_new_connection)
      self._transports = []
      self.channel = QWebChannel()
      self.client_connected.connect(self.channel.connectTo)
      self.bridge = WebBridge()
      self.register_obj("bridge", self.bridge)
      self.bind_services()

      app.web_socket = self

   def _create_server(self, port):
      if not QSslSocket.supportsSsl():
         print('The example requires SSL support.')
         sys.exit(-1)

      server = QWebSocketServer("QWebChannel Standalone Example Server",
                           QWebSocketServer.NonSecureMode)
      if not server.listen(QHostAddress.LocalHost, port):
         print("Failed to open web socket server.")
         sys.exit(-1)

      return server


   @Slot()
   def handle_new_connection(self):
      """Wrap an incoming WebSocket connection in a WebSocketTransport
         object."""
      socket = self._server.nextPendingConnection()
      transport = WebSocketTransport(socket)
      self._transports.append(transport)
      self.client_connected.emit(transport)


   def register_obj(self, obj_name: str, obj:QObject):
      self.channel.registerObject(obj_name, obj)

   def bind_service(self, service_cls):
      self.bridge.bind_service(service_cls)

   def bind_services(self):
      for service_cls in services:
         self.bind_service(service_cls)
          


          
