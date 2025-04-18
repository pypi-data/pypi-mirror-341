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
import builtins
import logging
class bstack11l1111l11_opy_:
    def __init__(self, handler):
        self._11lll11l1ll_opy_ = builtins.print
        self.handler = handler
        self._started = False
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self._11lll11l1l1_opy_ = {
            level: getattr(self.logger, level)
            for level in [bstack1l1ll11_opy_ (u"ࠨ࡫ࡱࡪࡴ࠭ᙘ"), bstack1l1ll11_opy_ (u"ࠩࡧࡩࡧࡻࡧࠨᙙ"), bstack1l1ll11_opy_ (u"ࠪࡻࡦࡸ࡮ࡪࡰࡪࠫᙚ"), bstack1l1ll11_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪᙛ")]
        }
    def start(self):
        if self._started:
            return
        self._started = True
        builtins.print = self._11lll11l11l_opy_
        self._11lll11l111_opy_()
    def _11lll11l11l_opy_(self, *args, **kwargs):
        self._11lll11l1ll_opy_(*args, **kwargs)
        message = bstack1l1ll11_opy_ (u"ࠬࠦࠧᙜ").join(map(str, args)) + bstack1l1ll11_opy_ (u"࠭࡜࡯ࠩᙝ")
        self._log_message(bstack1l1ll11_opy_ (u"ࠧࡊࡐࡉࡓࠬᙞ"), message)
    def _log_message(self, level, msg, *args, **kwargs):
        if self.handler:
            self.handler({bstack1l1ll11_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧᙟ"): level, bstack1l1ll11_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᙠ"): msg})
    def _11lll11l111_opy_(self):
        for level, bstack11lll11ll1l_opy_ in self._11lll11l1l1_opy_.items():
            setattr(logging, level, self._11lll11ll11_opy_(level, bstack11lll11ll1l_opy_))
    def _11lll11ll11_opy_(self, level, bstack11lll11ll1l_opy_):
        def wrapper(msg, *args, **kwargs):
            bstack11lll11ll1l_opy_(msg, *args, **kwargs)
            self._log_message(level.upper(), msg)
        return wrapper
    def reset(self):
        if not self._started:
            return
        self._started = False
        builtins.print = self._11lll11l1ll_opy_
        for level, bstack11lll11ll1l_opy_ in self._11lll11l1l1_opy_.items():
            setattr(logging, level, bstack11lll11ll1l_opy_)