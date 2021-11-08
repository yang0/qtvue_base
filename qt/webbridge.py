from PySide6.QtCore import QObject, Signal, Slot
from logger_moudle import logger
from utils.utils import returnFailure
import json

class WebBridge(QObject):
    """web对后端所有方法都交给bridge来统一调用"""

    func_dict = {}
    sendJson = Signal(str)

    @Slot(str)
    def request(self, req: str):
        logger.info("vue request: {}".format(req))
        try:
            request_data = json.loads(req)
            func = request_data.get("func", None)
            if func is None:
                raise Exception("没有传入[func]函数名")
            qt_func = self.func_dict.get(func, None)
            if qt_func is None:
                raise Exception("QT中不存在此函数:{}用于调用".format(func))
            data = qt_func(request_data)
            # 如果返回了数据, 就通过信号返回给前端 否则结束流程
            if data is None:
                return
            if not isinstance(data, str):
                raise Exception("返回值必须是一个json字符串类型")
            logger.info("pyqt emit: {}".format(data))
            self.sendJson.emit(data)
        except Exception as err:
            logger.warning("pyqt error: {}".format(err))
            self.sendJson.emit(returnFailure(str(err)))

    def bind_service(self, service_clas):
        service_clas(self)