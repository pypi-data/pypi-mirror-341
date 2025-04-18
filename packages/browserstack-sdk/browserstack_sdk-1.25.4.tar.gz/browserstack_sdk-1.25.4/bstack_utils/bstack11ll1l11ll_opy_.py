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
import os
import json
from bstack_utils.bstack111l1l111_opy_ import get_logger
logger = get_logger(__name__)
class bstack11lll1ll1l1_opy_(object):
  bstack1ll1l111ll_opy_ = os.path.join(os.path.expanduser(bstack1l1ll11_opy_ (u"ࠬࢄࠧᘫ")), bstack1l1ll11_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ᘬ"))
  bstack11lll1ll11l_opy_ = os.path.join(bstack1ll1l111ll_opy_, bstack1l1ll11_opy_ (u"ࠧࡤࡱࡰࡱࡦࡴࡤࡴ࠰࡭ࡷࡴࡴࠧᘭ"))
  commands_to_wrap = None
  perform_scan = None
  bstack1l1ll1l11l_opy_ = None
  bstack1l111lllll_opy_ = None
  bstack11llll11lll_opy_ = None
  def __new__(cls):
    if not hasattr(cls, bstack1l1ll11_opy_ (u"ࠨ࡫ࡱࡷࡹࡧ࡮ࡤࡧࠪᘮ")):
      cls.instance = super(bstack11lll1ll1l1_opy_, cls).__new__(cls)
      cls.instance.bstack11lll1l1lll_opy_()
    return cls.instance
  def bstack11lll1l1lll_opy_(self):
    try:
      with open(self.bstack11lll1ll11l_opy_, bstack1l1ll11_opy_ (u"ࠩࡵࠫᘯ")) as bstack1ll1ll11l1_opy_:
        bstack11lll1ll111_opy_ = bstack1ll1ll11l1_opy_.read()
        data = json.loads(bstack11lll1ll111_opy_)
        if bstack1l1ll11_opy_ (u"ࠪࡧࡴࡳ࡭ࡢࡰࡧࡷࠬᘰ") in data:
          self.bstack11llllll1ll_opy_(data[bstack1l1ll11_opy_ (u"ࠫࡨࡵ࡭࡮ࡣࡱࡨࡸ࠭ᘱ")])
        if bstack1l1ll11_opy_ (u"ࠬࡹࡣࡳ࡫ࡳࡸࡸ࠭ᘲ") in data:
          self.bstack111l11lll_opy_(data[bstack1l1ll11_opy_ (u"࠭ࡳࡤࡴ࡬ࡴࡹࡹࠧᘳ")])
    except:
      pass
  def bstack111l11lll_opy_(self, scripts):
    if scripts != None:
      self.perform_scan = scripts.get(bstack1l1ll11_opy_ (u"ࠧࡴࡥࡤࡲࠬᘴ"),bstack1l1ll11_opy_ (u"ࠨࠩᘵ"))
      self.bstack1l1ll1l11l_opy_ = scripts.get(bstack1l1ll11_opy_ (u"ࠩࡪࡩࡹࡘࡥࡴࡷ࡯ࡸࡸ࠭ᘶ"),bstack1l1ll11_opy_ (u"ࠪࠫᘷ"))
      self.bstack1l111lllll_opy_ = scripts.get(bstack1l1ll11_opy_ (u"ࠫ࡬࡫ࡴࡓࡧࡶࡹࡱࡺࡳࡔࡷࡰࡱࡦࡸࡹࠨᘸ"),bstack1l1ll11_opy_ (u"ࠬ࠭ᘹ"))
      self.bstack11llll11lll_opy_ = scripts.get(bstack1l1ll11_opy_ (u"࠭ࡳࡢࡸࡨࡖࡪࡹࡵ࡭ࡶࡶࠫᘺ"),bstack1l1ll11_opy_ (u"ࠧࠨᘻ"))
  def bstack11llllll1ll_opy_(self, commands_to_wrap):
    if commands_to_wrap != None and len(commands_to_wrap) != 0:
      self.commands_to_wrap = commands_to_wrap
  def store(self):
    try:
      with open(self.bstack11lll1ll11l_opy_, bstack1l1ll11_opy_ (u"ࠨࡹࠪᘼ")) as file:
        json.dump({
          bstack1l1ll11_opy_ (u"ࠤࡦࡳࡲࡳࡡ࡯ࡦࡶࠦᘽ"): self.commands_to_wrap,
          bstack1l1ll11_opy_ (u"ࠥࡷࡨࡸࡩࡱࡶࡶࠦᘾ"): {
            bstack1l1ll11_opy_ (u"ࠦࡸࡩࡡ࡯ࠤᘿ"): self.perform_scan,
            bstack1l1ll11_opy_ (u"ࠧ࡭ࡥࡵࡔࡨࡷࡺࡲࡴࡴࠤᙀ"): self.bstack1l1ll1l11l_opy_,
            bstack1l1ll11_opy_ (u"ࠨࡧࡦࡶࡕࡩࡸࡻ࡬ࡵࡵࡖࡹࡲࡳࡡࡳࡻࠥᙁ"): self.bstack1l111lllll_opy_,
            bstack1l1ll11_opy_ (u"ࠢࡴࡣࡹࡩࡗ࡫ࡳࡶ࡮ࡷࡷࠧᙂ"): self.bstack11llll11lll_opy_
          }
        }, file)
    except Exception as e:
      logger.error(bstack1l1ll11_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦࡳࡵࡱࡵ࡭ࡳ࡭ࠠࡤࡱࡰࡱࡦࡴࡤࡴ࠼ࠣࡿࢂࠨᙃ").format(e))
      pass
  def bstack1llll1ll11_opy_(self, bstack1ll1l11llll_opy_):
    try:
      return any(command.get(bstack1l1ll11_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᙄ")) == bstack1ll1l11llll_opy_ for command in self.commands_to_wrap)
    except:
      return False
bstack11ll1l11ll_opy_ = bstack11lll1ll1l1_opy_()