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
import os
import json
from bstack_utils.bstack1l11l11lll_opy_ import get_logger
logger = get_logger(__name__)
class bstack11lll1ll111_opy_(object):
  bstack1llll111l1_opy_ = os.path.join(os.path.expanduser(bstack1l1_opy_ (u"ࠫࢃ࠭ᘪ")), bstack1l1_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬᘫ"))
  bstack11lll1l1lll_opy_ = os.path.join(bstack1llll111l1_opy_, bstack1l1_opy_ (u"࠭ࡣࡰ࡯ࡰࡥࡳࡪࡳ࠯࡬ࡶࡳࡳ࠭ᘬ"))
  commands_to_wrap = None
  perform_scan = None
  bstack1l1l1l1ll_opy_ = None
  bstack1ll11l1ll1_opy_ = None
  bstack11llll111ll_opy_ = None
  def __new__(cls):
    if not hasattr(cls, bstack1l1_opy_ (u"ࠧࡪࡰࡶࡸࡦࡴࡣࡦࠩᘭ")):
      cls.instance = super(bstack11lll1ll111_opy_, cls).__new__(cls)
      cls.instance.bstack11lll1ll1l1_opy_()
    return cls.instance
  def bstack11lll1ll1l1_opy_(self):
    try:
      with open(self.bstack11lll1l1lll_opy_, bstack1l1_opy_ (u"ࠨࡴࠪᘮ")) as bstack1l1l111lll_opy_:
        bstack11lll1ll11l_opy_ = bstack1l1l111lll_opy_.read()
        data = json.loads(bstack11lll1ll11l_opy_)
        if bstack1l1_opy_ (u"ࠩࡦࡳࡲࡳࡡ࡯ࡦࡶࠫᘯ") in data:
          self.bstack11llll1llll_opy_(data[bstack1l1_opy_ (u"ࠪࡧࡴࡳ࡭ࡢࡰࡧࡷࠬᘰ")])
        if bstack1l1_opy_ (u"ࠫࡸࡩࡲࡪࡲࡷࡷࠬᘱ") in data:
          self.bstack1l111l1ll1_opy_(data[bstack1l1_opy_ (u"ࠬࡹࡣࡳ࡫ࡳࡸࡸ࠭ᘲ")])
    except:
      pass
  def bstack1l111l1ll1_opy_(self, scripts):
    if scripts != None:
      self.perform_scan = scripts.get(bstack1l1_opy_ (u"࠭ࡳࡤࡣࡱࠫᘳ"),bstack1l1_opy_ (u"ࠧࠨᘴ"))
      self.bstack1l1l1l1ll_opy_ = scripts.get(bstack1l1_opy_ (u"ࠨࡩࡨࡸࡗ࡫ࡳࡶ࡮ࡷࡷࠬᘵ"),bstack1l1_opy_ (u"ࠩࠪᘶ"))
      self.bstack1ll11l1ll1_opy_ = scripts.get(bstack1l1_opy_ (u"ࠪ࡫ࡪࡺࡒࡦࡵࡸࡰࡹࡹࡓࡶ࡯ࡰࡥࡷࡿࠧᘷ"),bstack1l1_opy_ (u"ࠫࠬᘸ"))
      self.bstack11llll111ll_opy_ = scripts.get(bstack1l1_opy_ (u"ࠬࡹࡡࡷࡧࡕࡩࡸࡻ࡬ࡵࡵࠪᘹ"),bstack1l1_opy_ (u"࠭ࠧᘺ"))
  def bstack11llll1llll_opy_(self, commands_to_wrap):
    if commands_to_wrap != None and len(commands_to_wrap) != 0:
      self.commands_to_wrap = commands_to_wrap
  def store(self):
    try:
      with open(self.bstack11lll1l1lll_opy_, bstack1l1_opy_ (u"ࠧࡸࠩᘻ")) as file:
        json.dump({
          bstack1l1_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࡵࠥᘼ"): self.commands_to_wrap,
          bstack1l1_opy_ (u"ࠤࡶࡧࡷ࡯ࡰࡵࡵࠥᘽ"): {
            bstack1l1_opy_ (u"ࠥࡷࡨࡧ࡮ࠣᘾ"): self.perform_scan,
            bstack1l1_opy_ (u"ࠦ࡬࡫ࡴࡓࡧࡶࡹࡱࡺࡳࠣᘿ"): self.bstack1l1l1l1ll_opy_,
            bstack1l1_opy_ (u"ࠧ࡭ࡥࡵࡔࡨࡷࡺࡲࡴࡴࡕࡸࡱࡲࡧࡲࡺࠤᙀ"): self.bstack1ll11l1ll1_opy_,
            bstack1l1_opy_ (u"ࠨࡳࡢࡸࡨࡖࡪࡹࡵ࡭ࡶࡶࠦᙁ"): self.bstack11llll111ll_opy_
          }
        }, file)
    except Exception as e:
      logger.error(bstack1l1_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡹࡴࡰࡴ࡬ࡲ࡬ࠦࡣࡰ࡯ࡰࡥࡳࡪࡳ࠻ࠢࡾࢁࠧᙂ").format(e))
      pass
  def bstack111l1ll1_opy_(self, bstack1ll1l111ll1_opy_):
    try:
      return any(command.get(bstack1l1_opy_ (u"ࠨࡰࡤࡱࡪ࠭ᙃ")) == bstack1ll1l111ll1_opy_ for command in self.commands_to_wrap)
    except:
      return False
bstack11ll111l1_opy_ = bstack11lll1ll111_opy_()