# cython: language_level=3
# #!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author: MaJian
@Time: 2024/1/17 9:28
@SoftWare: PyCharm
@Project: mortal
@File: __init__.py
"""
__all__ = ["MortalWork"]
from .work_main import MortalWorkMain


class MortalWork(MortalWorkMain):
    """
    MortalWork 类继承自 MortalWorkMain，提供了与 Bonade SaaS 签名相关的功能。
    """

    def bonade_saas_sign(self, data, env="", update_time=True):
        """
        对给定的数据进行 Bonade SaaS 签名操作。

        :param data: 需要进行签名的数据。
        :param env: 环境标识，默认为空字符串。
        :param update_time: 是否更新时间戳，默认为 True。
        """
        return self._bonade_saas_sign(data, env, update_time)

    def bonade_saas_sign_params(self, params, env="", update_time=True):
        """
        对给定的参数进行 Bonade SaaS 签名操作。

        :param params: 需要进行签名的参数。
        :param env: 环境标识，默认为空字符串。
        :param update_time: 是否更新时间戳，默认为 True。
        """
        return self._bonade_saas_sign_params(params, env, update_time)
