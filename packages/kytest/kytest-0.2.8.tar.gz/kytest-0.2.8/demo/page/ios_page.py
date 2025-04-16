"""
@Author: kang.yang
@Date: 2025/4/11 14:59
"""
import kytest


class IosPage(kytest.Page):
    music_tab = kytest.IosElem(label='儿童')
    gold_tab = kytest.IosElem(name='金币')
