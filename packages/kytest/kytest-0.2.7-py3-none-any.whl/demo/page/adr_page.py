"""
@Author: kang.yang
@Date: 2024/9/14 09:44
"""
import kytest


class AdrPage(kytest.Page):
    ad_btn = kytest.AdrElem(resourceId='com.qizhidao.clientapp:id/bottom_btn')
    my_tab = kytest.AdrElem(xpath='//android.widget.FrameLayout[4]')
    space_tab = kytest.AdrElem(text='科创空间')
    set_btn = kytest.AdrElem(resourceId='com.qizhidao.clientapp:id/me_top_bar_setting_iv')
    title = kytest.AdrElem(resourceId='com.qizhidao.clientapp:id/tv_actionbar_title')
    agree_text = kytest.AdrElem(resourceId='com.qizhidao.clientapp:id/agreement_tv_2')
    more_service = kytest.AdrElem(xpath='//*[@resource-id="com.qizhidao.clientapp:id/layout_top_content"]'
                       '/android.view.ViewGroup[3]/android.view.View[10]')
    page_title = kytest.AdrElem(resourceId='com.qizhidao.clientapp:id/tv_actionbar_title')

