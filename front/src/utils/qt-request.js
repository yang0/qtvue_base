import { QWebChannel } from './qwebchannel'
import { ElMessage, Notification } from 'element-plus'
import { getCurrentInstance, onMounted } from "vue";

export var callBackDict = {}

function qtCallBack(jsonString) {
  /*
  res: {
      code: 200/400 400就是后台有问题
      func: string 在mount中载入
      data: Dict 传入到view函数中
  }
  */
  // console.info(callBackDict)
  const res = JSON.parse(jsonString)
  // 根据code码 想要什么信息提示框就自己整合
  console.log("[qt-request][qtCallBack][res]", res)
  switch (res.code) {
    case 200:
      const func = res.data.func;
      const data = res.data.data;
      callBackDict[func](data);
      return;
    case 400:
      console.error(res.message || 'Error')
      ElMessage({
        message: res.message || 'Error',
        type: 'error',
        duration: 5 * 1000
      });
      return;
    case 201:
      console.warn(res.message || "Success")
      Notification({
        type: 'success',
        title: 'INFO',
        message: res.message || "Success",
        duration: 5 * 1000
      });
      return;
  }
}


export default {
  install: (app, options) => {
    // window.onload = function () {
    if (location.search != "")
      var baseUrl = (/[?&]webChannelBaseUrl=([A-Za-z0-9\-:/\.]+)/.exec(location.search)[1]);
    else
      var baseUrl = "ws://localhost:12345";

    console.warn("open websocket: " + baseUrl)

    var socket = new WebSocket(baseUrl);


    socket.onclose = function () {
      console.error("web channel closed");
    };
    socket.onerror = function (error) {
      console.error("web channel error: " + error);
    };
    socket.onopen = function () {
      new QWebChannel(socket, function (channel) {
        // console.warn("channel.objects.bridge:"+channel.objects.bridge)
        // app.config.globalProperties.$bridge = channel.objects.bridge
        app.config.globalProperties.$callbacks = callBackDict
        app.config.globalProperties.$request = (func, data = null, callBack = null) => {
          callBackDict[func] = callBack
          channel.objects.bridge.request(
            JSON.stringify({ func: func, data: data })
          )
        }

        channel.objects.bridge.sendJson.connect(qtCallBack)

        app.mount('#app')
      });
    }
  }
}

function qt_request(func, data = null, callBack = null) {
  const { proxy, ctx } = getCurrentInstance();
  proxy.$request(func, data, callBack)
}

export { qt_request }