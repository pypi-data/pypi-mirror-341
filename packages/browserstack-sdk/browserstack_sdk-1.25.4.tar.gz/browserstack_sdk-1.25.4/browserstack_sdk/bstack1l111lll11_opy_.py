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
import multiprocessing
import os
import json
from time import sleep
import bstack_utils.accessibility as bstack1ll11llll1_opy_
from browserstack_sdk.bstack11l1l111l_opy_ import *
from bstack_utils.config import Config
from bstack_utils.messages import bstack1l1l11l11_opy_
class bstack1l1l1l1ll1_opy_:
    def __init__(self, args, logger, bstack111l11111l_opy_, bstack1111lll111_opy_):
        self.args = args
        self.logger = logger
        self.bstack111l11111l_opy_ = bstack111l11111l_opy_
        self.bstack1111lll111_opy_ = bstack1111lll111_opy_
        self._prepareconfig = None
        self.Config = None
        self.runner = None
        self.bstack1l1l1l1l_opy_ = []
        self.bstack111l11l111_opy_ = None
        self.bstack1l11l1l1l1_opy_ = []
        self.bstack111l1111l1_opy_ = self.bstack11ll111ll_opy_()
        self.bstack111l1l1l_opy_ = -1
    def bstack1lllll1ll1_opy_(self, bstack111l111l11_opy_):
        self.parse_args()
        self.bstack1111lll11l_opy_()
        self.bstack1111ll1lll_opy_(bstack111l111l11_opy_)
    @staticmethod
    def version():
        import pytest
        return pytest.__version__
    @staticmethod
    def bstack1111lll1l1_opy_():
        import importlib
        if getattr(importlib, bstack1l1ll11_opy_ (u"ࠩࡩ࡭ࡳࡪ࡟࡭ࡱࡤࡨࡪࡸࠧ࿥"), False):
            bstack1111llll1l_opy_ = importlib.find_loader(bstack1l1ll11_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡢࡷࡪࡲࡥ࡯࡫ࡸࡱࠬ࿦"))
        else:
            bstack1111llll1l_opy_ = importlib.util.find_spec(bstack1l1ll11_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࡣࡸ࡫࡬ࡦࡰ࡬ࡹࡲ࠭࿧"))
    def bstack111l111lll_opy_(self, arg):
        if arg in self.args:
            i = self.args.index(arg)
            self.args.pop(i + 1)
            self.args.pop(i)
    def parse_args(self):
        self.bstack111l1l1l_opy_ = -1
        if self.bstack1111lll111_opy_ and bstack1l1ll11_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬ࿨") in self.bstack111l11111l_opy_:
            self.bstack111l1l1l_opy_ = int(self.bstack111l11111l_opy_[bstack1l1ll11_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭࿩")])
        try:
            bstack1111llllll_opy_ = [bstack1l1ll11_opy_ (u"ࠧ࠮࠯ࡧࡶ࡮ࡼࡥࡳࠩ࿪"), bstack1l1ll11_opy_ (u"ࠨ࠯࠰ࡴࡱࡻࡧࡪࡰࡶࠫ࿫"), bstack1l1ll11_opy_ (u"ࠩ࠰ࡴࠬ࿬")]
            if self.bstack111l1l1l_opy_ >= 0:
                bstack1111llllll_opy_.extend([bstack1l1ll11_opy_ (u"ࠪ࠱࠲ࡴࡵ࡮ࡲࡵࡳࡨ࡫ࡳࡴࡧࡶࠫ࿭"), bstack1l1ll11_opy_ (u"ࠫ࠲ࡴࠧ࿮")])
            for arg in bstack1111llllll_opy_:
                self.bstack111l111lll_opy_(arg)
        except Exception as exc:
            self.logger.error(str(exc))
    def get_args(self):
        return self.args
    def bstack1111lll11l_opy_(self):
        bstack111l11l111_opy_ = [os.path.normpath(item) for item in self.args]
        self.bstack111l11l111_opy_ = bstack111l11l111_opy_
        return bstack111l11l111_opy_
    def bstack11lll11ll1_opy_(self):
        try:
            from _pytest.config import _prepareconfig
            from _pytest.config import Config
            from _pytest import runner
            self.bstack1111lll1l1_opy_()
            self._prepareconfig = _prepareconfig
            self.Config = Config
            self.runner = runner
        except Exception as e:
            self.logger.warn(e, bstack1l1l11l11_opy_)
    def bstack1111ll1lll_opy_(self, bstack111l111l11_opy_):
        bstack11llllllll_opy_ = Config.bstack1l1111llll_opy_()
        if bstack111l111l11_opy_:
            self.bstack111l11l111_opy_.append(bstack1l1ll11_opy_ (u"ࠬ࠳࠭ࡴ࡭࡬ࡴࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ࿯"))
            self.bstack111l11l111_opy_.append(bstack1l1ll11_opy_ (u"࠭ࡔࡳࡷࡨࠫ࿰"))
        if bstack11llllllll_opy_.bstack1111lllll1_opy_():
            self.bstack111l11l111_opy_.append(bstack1l1ll11_opy_ (u"ࠧ࠮࠯ࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸ࠭࿱"))
            self.bstack111l11l111_opy_.append(bstack1l1ll11_opy_ (u"ࠨࡖࡵࡹࡪ࠭࿲"))
        self.bstack111l11l111_opy_.append(bstack1l1ll11_opy_ (u"ࠩ࠰ࡴࠬ࿳"))
        self.bstack111l11l111_opy_.append(bstack1l1ll11_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡢࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡲ࡯ࡹ࡬࡯࡮ࠨ࿴"))
        self.bstack111l11l111_opy_.append(bstack1l1ll11_opy_ (u"ࠫ࠲࠳ࡤࡳ࡫ࡹࡩࡷ࠭࿵"))
        self.bstack111l11l111_opy_.append(bstack1l1ll11_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࠬ࿶"))
        if self.bstack111l1l1l_opy_ > 1:
            self.bstack111l11l111_opy_.append(bstack1l1ll11_opy_ (u"࠭࠭࡯ࠩ࿷"))
            self.bstack111l11l111_opy_.append(str(self.bstack111l1l1l_opy_))
    def bstack1111llll11_opy_(self):
        bstack1l11l1l1l1_opy_ = []
        for spec in self.bstack1l1l1l1l_opy_:
            bstack1l111ll1_opy_ = [spec]
            bstack1l111ll1_opy_ += self.bstack111l11l111_opy_
            bstack1l11l1l1l1_opy_.append(bstack1l111ll1_opy_)
        self.bstack1l11l1l1l1_opy_ = bstack1l11l1l1l1_opy_
        return bstack1l11l1l1l1_opy_
    def bstack11ll111ll_opy_(self):
        try:
            from pytest_bdd import reporting
            self.bstack111l1111l1_opy_ = True
            return True
        except Exception as e:
            self.bstack111l1111l1_opy_ = False
        return self.bstack111l1111l1_opy_
    def bstack1lllllllll_opy_(self, bstack111l111l1l_opy_, bstack1lllll1ll1_opy_):
        bstack1lllll1ll1_opy_[bstack1l1ll11_opy_ (u"ࠧࡄࡑࡑࡊࡎࡍࠧ࿸")] = self.bstack111l11111l_opy_
        multiprocessing.set_start_method(bstack1l1ll11_opy_ (u"ࠨࡵࡳࡥࡼࡴࠧ࿹"))
        bstack1l11ll1ll1_opy_ = []
        manager = multiprocessing.Manager()
        bstack1111lll1ll_opy_ = manager.list()
        if bstack1l1ll11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ࿺") in self.bstack111l11111l_opy_:
            for index, platform in enumerate(self.bstack111l11111l_opy_[bstack1l1ll11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭࿻")]):
                bstack1l11ll1ll1_opy_.append(multiprocessing.Process(name=str(index),
                                                            target=bstack111l111l1l_opy_,
                                                            args=(self.bstack111l11l111_opy_, bstack1lllll1ll1_opy_, bstack1111lll1ll_opy_)))
            bstack111l111ll1_opy_ = len(self.bstack111l11111l_opy_[bstack1l1ll11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ࿼")])
        else:
            bstack1l11ll1ll1_opy_.append(multiprocessing.Process(name=str(0),
                                                        target=bstack111l111l1l_opy_,
                                                        args=(self.bstack111l11l111_opy_, bstack1lllll1ll1_opy_, bstack1111lll1ll_opy_)))
            bstack111l111ll1_opy_ = 1
        i = 0
        for t in bstack1l11ll1ll1_opy_:
            os.environ[bstack1l1ll11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬ࿽")] = str(i)
            if bstack1l1ll11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ࿾") in self.bstack111l11111l_opy_:
                os.environ[bstack1l1ll11_opy_ (u"ࠧࡄࡗࡕࡖࡊࡔࡔࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡈࡆ࡚ࡁࠨ࿿")] = json.dumps(self.bstack111l11111l_opy_[bstack1l1ll11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫက")][i % bstack111l111ll1_opy_])
            i += 1
            t.start()
        for t in bstack1l11ll1ll1_opy_:
            t.join()
        return list(bstack1111lll1ll_opy_)
    @staticmethod
    def bstack1ll111ll_opy_(driver, bstack111l111111_opy_, logger, item=None, wait=False):
        item = item or getattr(threading.current_thread(), bstack1l1ll11_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡷࡩࡲ࠭ခ"), None)
        if item and getattr(item, bstack1l1ll11_opy_ (u"ࠪࡣࡦ࠷࠱ࡺࡡࡷࡩࡸࡺ࡟ࡤࡣࡶࡩࠬဂ"), None) and not getattr(item, bstack1l1ll11_opy_ (u"ࠫࡤࡧ࠱࠲ࡻࡢࡷࡹࡵࡰࡠࡦࡲࡲࡪ࠭ဃ"), False):
            logger.info(
                bstack1l1ll11_opy_ (u"ࠧࡇࡵࡵࡱࡰࡥࡹ࡫ࠠࡵࡧࡶࡸࠥࡩࡡࡴࡧࠣࡩࡽ࡫ࡣࡶࡶ࡬ࡳࡳࠦࡨࡢࡵࠣࡩࡳࡪࡥࡥ࠰ࠣࡔࡷࡵࡣࡦࡵࡶ࡭ࡳ࡭ࠠࡧࡱࡵࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡹ࡫ࡳࡵ࡫ࡱ࡫ࠥ࡯ࡳࠡࡷࡱࡨࡪࡸࡷࡢࡻ࠱ࠦင"))
            bstack111l1111ll_opy_ = item.cls.__name__ if not item.cls is None else None
            bstack1ll11llll1_opy_.bstack1ll111111_opy_(driver, item.name, item.path)
            item._a11y_stop_done = True
            if wait:
                sleep(2)