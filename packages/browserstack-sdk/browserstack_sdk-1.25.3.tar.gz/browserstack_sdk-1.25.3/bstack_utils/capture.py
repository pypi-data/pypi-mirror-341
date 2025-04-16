# coding: UTF-8
import sys
bstack1lllll1_opy_ = sys.version_info [0] == 2
bstack11l1111_opy_ = 2048
bstack11ll11_opy_ = 7
def bstack1l1_opy_ (bstack11l1_opy_):
    global bstack11lll_opy_
    bstack11111_opy_ = ord (bstack11l1_opy_ [-1])
    bstack11llll_opy_ = bstack11l1_opy_ [:-1]
    bstack1111ll_opy_ = bstack11111_opy_ % len (bstack11llll_opy_)
    bstack1l1l_opy_ = bstack11llll_opy_ [:bstack1111ll_opy_] + bstack11llll_opy_ [bstack1111ll_opy_:]
    if bstack1lllll1_opy_:
        bstack1l1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack11l1111_opy_ - (bstack1ll11ll_opy_ + bstack11111_opy_) % bstack11ll11_opy_) for bstack1ll11ll_opy_, char in enumerate (bstack1l1l_opy_)])
    else:
        bstack1l1lll_opy_ = str () .join ([chr (ord (char) - bstack11l1111_opy_ - (bstack1ll11ll_opy_ + bstack11111_opy_) % bstack11ll11_opy_) for bstack1ll11ll_opy_, char in enumerate (bstack1l1l_opy_)])
    return eval (bstack1l1lll_opy_)
import builtins
import logging
class bstack11l11l111l_opy_:
    def __init__(self, handler):
        self._11lll11l111_opy_ = builtins.print
        self.handler = handler
        self._started = False
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self._11lll11ll1l_opy_ = {
            level: getattr(self.logger, level)
            for level in [bstack1l1_opy_ (u"ࠧࡪࡰࡩࡳࠬᙗ"), bstack1l1_opy_ (u"ࠨࡦࡨࡦࡺ࡭ࠧᙘ"), bstack1l1_opy_ (u"ࠩࡺࡥࡷࡴࡩ࡯ࡩࠪᙙ"), bstack1l1_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩᙚ")]
        }
    def start(self):
        if self._started:
            return
        self._started = True
        builtins.print = self._11lll11l1ll_opy_
        self._11lll11l11l_opy_()
    def _11lll11l1ll_opy_(self, *args, **kwargs):
        self._11lll11l111_opy_(*args, **kwargs)
        message = bstack1l1_opy_ (u"ࠫࠥ࠭ᙛ").join(map(str, args)) + bstack1l1_opy_ (u"ࠬࡢ࡮ࠨᙜ")
        self._log_message(bstack1l1_opy_ (u"࠭ࡉࡏࡈࡒࠫᙝ"), message)
    def _log_message(self, level, msg, *args, **kwargs):
        if self.handler:
            self.handler({bstack1l1_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ᙞ"): level, bstack1l1_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᙟ"): msg})
    def _11lll11l11l_opy_(self):
        for level, bstack11lll11l1l1_opy_ in self._11lll11ll1l_opy_.items():
            setattr(logging, level, self._11lll11ll11_opy_(level, bstack11lll11l1l1_opy_))
    def _11lll11ll11_opy_(self, level, bstack11lll11l1l1_opy_):
        def wrapper(msg, *args, **kwargs):
            bstack11lll11l1l1_opy_(msg, *args, **kwargs)
            self._log_message(level.upper(), msg)
        return wrapper
    def reset(self):
        if not self._started:
            return
        self._started = False
        builtins.print = self._11lll11l111_opy_
        for level, bstack11lll11l1l1_opy_ in self._11lll11ll1l_opy_.items():
            setattr(logging, level, bstack11lll11l1l1_opy_)