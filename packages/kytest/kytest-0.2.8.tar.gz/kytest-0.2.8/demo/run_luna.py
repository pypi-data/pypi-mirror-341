"""
@Author: kang.yang
@Date: 2025/4/14 09:45
"""
import kytest
from kytest import AppConfig


if __name__ == '__main__':
    AppConfig.did = 'FMR0223824022829'
    AppConfig.pkg = 'com.luna.music'

    kytest.main(path='tests/test_luna.py')

