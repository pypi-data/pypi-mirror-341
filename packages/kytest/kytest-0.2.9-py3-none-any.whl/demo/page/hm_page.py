"""
@Author: kang.yang
@Date: 2024/10/8 15:04
"""
import kytest


class HmPage(kytest.Page):
    my_entry = kytest.HmElem(text='我的')
    login_entry = kytest.HmElem(text='登录/注册')
    pwd_login = kytest.HmElem(text='账号登录')
    forget_pwd = kytest.HmElem(text='忘记密码')

