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
import json
import multiprocessing
import os
from bstack_utils.config import Config
class bstack1l111l1l1_opy_():
  def __init__(self, args, logger, bstack111l11111l_opy_, bstack1111lll111_opy_, bstack1111ll1l1l_opy_):
    self.args = args
    self.logger = logger
    self.bstack111l11111l_opy_ = bstack111l11111l_opy_
    self.bstack1111lll111_opy_ = bstack1111lll111_opy_
    self.bstack1111ll1l1l_opy_ = bstack1111ll1l1l_opy_
  def bstack1lllllllll_opy_(self, bstack111l111l1l_opy_, bstack1lllll1ll1_opy_, bstack1111ll1ll1_opy_=False):
    bstack1l11ll1ll1_opy_ = []
    manager = multiprocessing.Manager()
    bstack1111lll1ll_opy_ = manager.list()
    bstack11llllllll_opy_ = Config.bstack1l1111llll_opy_()
    if bstack1111ll1ll1_opy_:
      for index, platform in enumerate(self.bstack111l11111l_opy_[bstack1l1ll11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩစ")]):
        if index == 0:
          bstack1lllll1ll1_opy_[bstack1l1ll11_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪဆ")] = self.args
        bstack1l11ll1ll1_opy_.append(multiprocessing.Process(name=str(index),
                                                    target=bstack111l111l1l_opy_,
                                                    args=(bstack1lllll1ll1_opy_, bstack1111lll1ll_opy_)))
    else:
      for index, platform in enumerate(self.bstack111l11111l_opy_[bstack1l1ll11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫဇ")]):
        bstack1l11ll1ll1_opy_.append(multiprocessing.Process(name=str(index),
                                                    target=bstack111l111l1l_opy_,
                                                    args=(bstack1lllll1ll1_opy_, bstack1111lll1ll_opy_)))
    i = 0
    for t in bstack1l11ll1ll1_opy_:
      try:
        if bstack11llllllll_opy_.get_property(bstack1l1ll11_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡶࡩࡸࡹࡩࡰࡰࠪဈ")):
          os.environ[bstack1l1ll11_opy_ (u"ࠪࡇ࡚ࡘࡒࡆࡐࡗࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡄࡂࡖࡄࠫဉ")] = json.dumps(self.bstack111l11111l_opy_[bstack1l1ll11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧည")][i % self.bstack1111ll1l1l_opy_])
      except Exception as e:
        self.logger.debug(bstack1l1ll11_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡷࡹࡵࡲࡪࡰࡪࠤࡨࡻࡲࡳࡧࡱࡸࠥࡶ࡬ࡢࡶࡩࡳࡷࡳࠠࡥࡧࡷࡥ࡮ࡲࡳ࠻ࠢࡾࢁࠧဋ").format(str(e)))
      i += 1
      t.start()
    for t in bstack1l11ll1ll1_opy_:
      t.join()
    return list(bstack1111lll1ll_opy_)