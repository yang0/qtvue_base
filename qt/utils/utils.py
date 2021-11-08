#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : utils.py
@Author  : Link
@Time    : 2021/4/17 12:48
"""
from logger_moudle import logger

import json


def returnSuccess(message, **kwargs):
    return json.dumps({"data": kwargs, "message": message, 'code': 200})


def returnFailure(message, **kwargs):
    return json.dumps({"data": kwargs, "message": message, 'code': 400})


def returnOtherMessage(message, code):
    if code == 200:
        raise Exception("other message cannot use 200 see in js qt-request ChannelCallBack")
    return json.dumps({"message": message, 'code': code})


def exec_web_request(func):
    def wrapper(ctx, kwargs: dict):
        # ctx.app.statusbar.clearMessage()
        try:
            func_name = kwargs["func"]
            if func.__name__ != func_name:
                raise Exception(f"error func: {func.__name__}, vue_func: {func_name}")
            data = kwargs.get("data", None)

            if data is None:
                return_data = func(ctx)
            else:
                return_data = func(ctx, data)
            if return_data is None:
                logger.info("func: {} done. no data emit.".format(func.__name__))
                return
            logger.info("func: {} emit: {}".format(func.__name__, return_data))
            return returnSuccess("success", func=func.__name__, data=return_data)
        except Exception as err:

            ctx.vue_obj.append_status_message.emit(str(err))  # QT

            logger.error(err)
            return returnFailure(str(err))

    return wrapper


def return_web_data(func):
    def wrapper(ctx, *args, **kwargs):
        # ctx.app.statusbar.clearMessage()
        try:
            return_data = func(ctx, *args, **kwargs)

            if return_data is None:
                logger.info("func: {} done. no data emit.".format(func.__name__))
                return
            logger.info("func: {} emit: {}".format(func.__name__, return_data))
            return ctx.vue_obj.connectSignal.emit(returnSuccess("success", func=func.__name__, data=return_data))
        except Exception as err:

            ctx.vue_obj.append_status_message.emit(str(err))  # QT

            logger.error(err)
            return ctx.vue_obj.connectSignal.emit(returnFailure(str(err)))

    return wrapper
