from utils.utils import returnOtherMessage, returnFailure
from webbridge import WebBridge


class WebService:

    def __init__(self, bridge: WebBridge):
        self.bridge = bridge
        self.func_init()

    def func_init(self):
        for each in filter(lambda m: not m.startswith("_") and
                                     not m.endswith("_") and
                                     callable(getattr(self, m)), dir(self)):  # callable 表示为可以被调用执行的对象
            self.bridge.func_dict[each] = getattr(self, each)

    def set_fail_message(self, message: str):
        self.bridge.sendJson.emit(returnFailure(message))

    def set_other_message(self, message: str, code: int):
        self.bridge.sendJson.emit(returnOtherMessage(message, code))
