"""
@Author: kang.yang
@Date: 2025/4/14 09:45
"""
import kytest


class TestLunaMusic(kytest.AdrTC):
    """
    汽水音乐刷广告
    """

    def test_add(self):
        self.start_app(force=True)
        self.sleep(10)
        self.elem(resourceId='com.luna.music:id/kj').click()
        self.sleep(10)
        while True:
            self.sleep(10)
            self.dr.click(0.834, 0.065)
            self.elem(resourceId='com.luna.music:id/a7d').\
                click_exists(timeout=1)
            self.elem(text='继续观看').click_exists(timeout=1)
            self.elem(text='领取奖励').click_exists(timeout=1)






