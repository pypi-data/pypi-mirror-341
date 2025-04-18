# coding: UTF-8
import sys
bstack1l1llll_opy_ = sys.version_info [0] == 2
bstack11l111l_opy_ = 2048
bstack111l_opy_ = 7
def bstack1l1ll11_opy_ (bstack11111l1_opy_):
    global bstack1l11ll_opy_
    bstack1l111l1_opy_ = ord (bstack11111l1_opy_ [-1])
    bstack1llllll1_opy_ = bstack11111l1_opy_ [:-1]
    bstack1111l_opy_ = bstack1l111l1_opy_ % len (bstack1llllll1_opy_)
    bstack1ll111_opy_ = bstack1llllll1_opy_ [:bstack1111l_opy_] + bstack1llllll1_opy_ [bstack1111l_opy_:]
    if bstack1l1llll_opy_:
        bstack11lll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack11l111l_opy_ - (bstack1lllll1l_opy_ + bstack1l111l1_opy_) % bstack111l_opy_) for bstack1lllll1l_opy_, char in enumerate (bstack1ll111_opy_)])
    else:
        bstack11lll1l_opy_ = str () .join ([chr (ord (char) - bstack11l111l_opy_ - (bstack1lllll1l_opy_ + bstack1l111l1_opy_) % bstack111l_opy_) for bstack1lllll1l_opy_, char in enumerate (bstack1ll111_opy_)])
    return eval (bstack11lll1l_opy_)
class bstack11l1l111l1_opy_:
    def __init__(self, handler):
        self._111l11l11l1_opy_ = None
        self.handler = handler
        self._111l11l111l_opy_ = self.bstack111l11l1111_opy_()
        self.patch()
    def patch(self):
        self._111l11l11l1_opy_ = self._111l11l111l_opy_.execute
        self._111l11l111l_opy_.execute = self.bstack111l11l11ll_opy_()
    def bstack111l11l11ll_opy_(self):
        def execute(this, driver_command, *args, **kwargs):
            self.handler(bstack1l1ll11_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࠧᵱ"), driver_command, None, this, args)
            response = self._111l11l11l1_opy_(this, driver_command, *args, **kwargs)
            self.handler(bstack1l1ll11_opy_ (u"ࠨࡡࡧࡶࡨࡶࠧᵲ"), driver_command, response)
            return response
        return execute
    def reset(self):
        self._111l11l111l_opy_.execute = self._111l11l11l1_opy_
    @staticmethod
    def bstack111l11l1111_opy_():
        from selenium.webdriver.remote.webdriver import WebDriver
        return WebDriver