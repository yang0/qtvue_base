from webbridge import WebBridge
from webservice import WebService
from utils import exec_web_request, return_web_data

class TestService(WebService):

    def __init__(self, bridge: WebBridge):
        super().__init__(bridge)

    @exec_web_request
    def p(self):
        print("trigged by web")
        return "abcdefg"