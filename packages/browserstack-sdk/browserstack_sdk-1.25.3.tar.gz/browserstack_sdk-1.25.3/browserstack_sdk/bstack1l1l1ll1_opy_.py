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
import json
import multiprocessing
import os
from bstack_utils.config import Config
class bstack1l1ll1l1l_opy_():
  def __init__(self, args, logger, bstack1111lll1ll_opy_, bstack1111llll11_opy_, bstack1111ll1l1l_opy_):
    self.args = args
    self.logger = logger
    self.bstack1111lll1ll_opy_ = bstack1111lll1ll_opy_
    self.bstack1111llll11_opy_ = bstack1111llll11_opy_
    self.bstack1111ll1l1l_opy_ = bstack1111ll1l1l_opy_
  def bstack1ll1lllll1_opy_(self, bstack1111lll11l_opy_, bstack1llll11l1l_opy_, bstack1111ll1ll1_opy_=False):
    bstack1ll11ll111_opy_ = []
    manager = multiprocessing.Manager()
    bstack1111llllll_opy_ = manager.list()
    bstack11llllll1_opy_ = Config.bstack111111ll_opy_()
    if bstack1111ll1ll1_opy_:
      for index, platform in enumerate(self.bstack1111lll1ll_opy_[bstack1l1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩစ")]):
        if index == 0:
          bstack1llll11l1l_opy_[bstack1l1_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪဆ")] = self.args
        bstack1ll11ll111_opy_.append(multiprocessing.Process(name=str(index),
                                                    target=bstack1111lll11l_opy_,
                                                    args=(bstack1llll11l1l_opy_, bstack1111llllll_opy_)))
    else:
      for index, platform in enumerate(self.bstack1111lll1ll_opy_[bstack1l1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫဇ")]):
        bstack1ll11ll111_opy_.append(multiprocessing.Process(name=str(index),
                                                    target=bstack1111lll11l_opy_,
                                                    args=(bstack1llll11l1l_opy_, bstack1111llllll_opy_)))
    i = 0
    for t in bstack1ll11ll111_opy_:
      try:
        if bstack11llllll1_opy_.get_property(bstack1l1_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡶࡩࡸࡹࡩࡰࡰࠪဈ")):
          os.environ[bstack1l1_opy_ (u"ࠪࡇ࡚ࡘࡒࡆࡐࡗࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡄࡂࡖࡄࠫဉ")] = json.dumps(self.bstack1111lll1ll_opy_[bstack1l1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧည")][i % self.bstack1111ll1l1l_opy_])
      except Exception as e:
        self.logger.debug(bstack1l1_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡷࡹࡵࡲࡪࡰࡪࠤࡨࡻࡲࡳࡧࡱࡸࠥࡶ࡬ࡢࡶࡩࡳࡷࡳࠠࡥࡧࡷࡥ࡮ࡲࡳ࠻ࠢࡾࢁࠧဋ").format(str(e)))
      i += 1
      t.start()
    for t in bstack1ll11ll111_opy_:
      t.join()
    return list(bstack1111llllll_opy_)