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
import logging
import datetime
import threading
from bstack_utils.helper import bstack11lll1lll1l_opy_, bstack11ll111111_opy_, get_host_info, bstack11ll111ll1l_opy_, \
 bstack1lll1lll1l_opy_, bstack1l1l11l1l_opy_, bstack111l1ll1l1_opy_, bstack11l1l111l11_opy_, bstack11l1l11ll1_opy_
import bstack_utils.accessibility as bstack1l1l11l11_opy_
from bstack_utils.bstack11l11l1111_opy_ import bstack11llll111l_opy_
from bstack_utils.percy import bstack1111ll11_opy_
from bstack_utils.config import Config
bstack11llllll1_opy_ = Config.bstack111111ll_opy_()
logger = logging.getLogger(__name__)
percy = bstack1111ll11_opy_()
@bstack111l1ll1l1_opy_(class_method=False)
def bstack1111lll11l1_opy_(bs_config, bstack1ll1111l11_opy_):
  try:
    data = {
        bstack1l1_opy_ (u"ࠩࡩࡳࡷࡳࡡࡵࠩỡ"): bstack1l1_opy_ (u"ࠪ࡮ࡸࡵ࡮ࠨỢ"),
        bstack1l1_opy_ (u"ࠫࡵࡸ࡯࡫ࡧࡦࡸࡤࡴࡡ࡮ࡧࠪợ"): bs_config.get(bstack1l1_opy_ (u"ࠬࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࠪỤ"), bstack1l1_opy_ (u"࠭ࠧụ")),
        bstack1l1_opy_ (u"ࠧ࡯ࡣࡰࡩࠬỦ"): bs_config.get(bstack1l1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫủ"), os.path.basename(os.path.abspath(os.getcwd()))),
        bstack1l1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠ࡫ࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬỨ"): bs_config.get(bstack1l1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬứ")),
        bstack1l1_opy_ (u"ࠫࡩ࡫ࡳࡤࡴ࡬ࡴࡹ࡯࡯࡯ࠩỪ"): bs_config.get(bstack1l1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡈࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮ࠨừ"), bstack1l1_opy_ (u"࠭ࠧỬ")),
        bstack1l1_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫử"): bstack11l1l11ll1_opy_(),
        bstack1l1_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭Ữ"): bstack11ll111ll1l_opy_(bs_config),
        bstack1l1_opy_ (u"ࠩ࡫ࡳࡸࡺ࡟ࡪࡰࡩࡳࠬữ"): get_host_info(),
        bstack1l1_opy_ (u"ࠪࡧ࡮ࡥࡩ࡯ࡨࡲࠫỰ"): bstack11ll111111_opy_(),
        bstack1l1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢࡶࡺࡴ࡟ࡪࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫự"): os.environ.get(bstack1l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡇ࡛ࡉࡍࡆࡢࡖ࡚ࡔ࡟ࡊࡆࡈࡒ࡙ࡏࡆࡊࡇࡕࠫỲ")),
        bstack1l1_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩࡥࡴࡦࡵࡷࡷࡤࡸࡥࡳࡷࡱࠫỳ"): os.environ.get(bstack1l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡒࡆࡔࡘࡒࠬỴ"), False),
        bstack1l1_opy_ (u"ࠨࡸࡨࡶࡸ࡯࡯࡯ࡡࡦࡳࡳࡺࡲࡰ࡮ࠪỵ"): bstack11lll1lll1l_opy_(),
        bstack1l1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩỶ"): bstack1111l1l1l11_opy_(),
        bstack1l1_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡤࡦࡶࡤ࡭ࡱࡹࠧỷ"): bstack1111l1ll11l_opy_(bstack1ll1111l11_opy_),
        bstack1l1_opy_ (u"ࠫࡵࡸ࡯ࡥࡷࡦࡸࡤࡳࡡࡱࠩỸ"): bstack1l1l111ll_opy_(bs_config, bstack1ll1111l11_opy_.get(bstack1l1_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡷࡶࡩࡩ࠭ỹ"), bstack1l1_opy_ (u"࠭ࠧỺ"))),
        bstack1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩỻ"): bstack1lll1lll1l_opy_(bs_config),
    }
    return data
  except Exception as error:
    logger.error(bstack1l1_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣࡧࡷ࡫ࡡࡵ࡫ࡱ࡫ࠥࡶࡡࡺ࡮ࡲࡥࡩࠦࡦࡰࡴࠣࡘࡪࡹࡴࡉࡷࡥ࠾ࠥࠦࡻࡾࠤỼ").format(str(error)))
    return None
def bstack1111l1ll11l_opy_(framework):
  return {
    bstack1l1_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡓࡧ࡭ࡦࠩỽ"): framework.get(bstack1l1_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࠫỾ"), bstack1l1_opy_ (u"ࠫࡕࡿࡴࡦࡵࡷࠫỿ")),
    bstack1l1_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡗࡧࡵࡷ࡮ࡵ࡮ࠨἀ"): framework.get(bstack1l1_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡹࡩࡷࡹࡩࡰࡰࠪἁ")),
    bstack1l1_opy_ (u"ࠧࡴࡦ࡮࡚ࡪࡸࡳࡪࡱࡱࠫἂ"): framework.get(bstack1l1_opy_ (u"ࠨࡵࡧ࡯ࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ἃ")),
    bstack1l1_opy_ (u"ࠩ࡯ࡥࡳ࡭ࡵࡢࡩࡨࠫἄ"): bstack1l1_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪἅ"),
    bstack1l1_opy_ (u"ࠫࡹ࡫ࡳࡵࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫἆ"): framework.get(bstack1l1_opy_ (u"ࠬࡺࡥࡴࡶࡉࡶࡦࡳࡥࡸࡱࡵ࡯ࠬἇ"))
  }
def bstack1l1l111ll_opy_(bs_config, framework):
  bstack11l1ll11ll_opy_ = False
  bstack111111111_opy_ = False
  bstack1111l1ll1l1_opy_ = False
  if bstack1l1_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪἈ") in bs_config:
    bstack1111l1ll1l1_opy_ = True
  elif bstack1l1_opy_ (u"ࠧࡢࡲࡳࠫἉ") in bs_config:
    bstack11l1ll11ll_opy_ = True
  else:
    bstack111111111_opy_ = True
  bstack1lll11l1ll_opy_ = {
    bstack1l1_opy_ (u"ࠨࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨἊ"): bstack11llll111l_opy_.bstack1111l1ll1ll_opy_(bs_config, framework),
    bstack1l1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩἋ"): bstack1l1l11l11_opy_.bstack11l11111l_opy_(bs_config),
    bstack1l1_opy_ (u"ࠪࡴࡪࡸࡣࡺࠩἌ"): bs_config.get(bstack1l1_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࠪἍ"), False),
    bstack1l1_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡫ࠧἎ"): bstack111111111_opy_,
    bstack1l1_opy_ (u"࠭ࡡࡱࡲࡢࡥࡺࡺ࡯࡮ࡣࡷࡩࠬἏ"): bstack11l1ll11ll_opy_,
    bstack1l1_opy_ (u"ࠧࡵࡷࡵࡦࡴࡹࡣࡢ࡮ࡨࠫἐ"): bstack1111l1ll1l1_opy_
  }
  return bstack1lll11l1ll_opy_
@bstack111l1ll1l1_opy_(class_method=False)
def bstack1111l1l1l11_opy_():
  try:
    bstack1111l1l1l1l_opy_ = json.loads(os.getenv(bstack1l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡤࡇࡃࡄࡇࡖࡗࡎࡈࡉࡍࡋࡗ࡝ࡤࡉࡏࡏࡈࡌࡋ࡚ࡘࡁࡕࡋࡒࡒࡤ࡟ࡍࡍࠩἑ"), bstack1l1_opy_ (u"ࠩࡾࢁࠬἒ")))
    return {
        bstack1l1_opy_ (u"ࠪࡷࡪࡺࡴࡪࡰࡪࡷࠬἓ"): bstack1111l1l1l1l_opy_
    }
  except Exception as error:
    logger.error(bstack1l1_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦࡣࡳࡧࡤࡸ࡮ࡴࡧࠡࡩࡨࡸࡤࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡤࡹࡥࡵࡶ࡬ࡲ࡬ࡹࠠࡧࡱࡵࠤ࡙࡫ࡳࡵࡊࡸࡦ࠿ࠦࠠࡼࡿࠥἔ").format(str(error)))
    return {}
def bstack1111ll111ll_opy_(array, bstack1111l1lll11_opy_, bstack1111l1l1lll_opy_):
  result = {}
  for o in array:
    key = o[bstack1111l1lll11_opy_]
    result[key] = o[bstack1111l1l1lll_opy_]
  return result
def bstack1111lll1111_opy_(bstack1lll1llll1_opy_=bstack1l1_opy_ (u"ࠬ࠭ἕ")):
  bstack1111l1ll111_opy_ = bstack1l1l11l11_opy_.on()
  bstack1111l1llll1_opy_ = bstack11llll111l_opy_.on()
  bstack1111l1l1ll1_opy_ = percy.bstack1l111l11_opy_()
  if bstack1111l1l1ll1_opy_ and not bstack1111l1llll1_opy_ and not bstack1111l1ll111_opy_:
    return bstack1lll1llll1_opy_ not in [bstack1l1_opy_ (u"࠭ࡃࡃࡖࡖࡩࡸࡹࡩࡰࡰࡆࡶࡪࡧࡴࡦࡦࠪ἖"), bstack1l1_opy_ (u"ࠧࡍࡱࡪࡇࡷ࡫ࡡࡵࡧࡧࠫ἗")]
  elif bstack1111l1ll111_opy_ and not bstack1111l1llll1_opy_:
    return bstack1lll1llll1_opy_ not in [bstack1l1_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩἘ"), bstack1l1_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫἙ"), bstack1l1_opy_ (u"ࠪࡐࡴ࡭ࡃࡳࡧࡤࡸࡪࡪࠧἚ")]
  return bstack1111l1ll111_opy_ or bstack1111l1llll1_opy_ or bstack1111l1l1ll1_opy_
@bstack111l1ll1l1_opy_(class_method=False)
def bstack1111ll11ll1_opy_(bstack1lll1llll1_opy_, test=None):
  bstack1111l1lll1l_opy_ = bstack1l1l11l11_opy_.on()
  if not bstack1111l1lll1l_opy_ or bstack1lll1llll1_opy_ not in [bstack1l1_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭Ἓ")] or test == None:
    return None
  return {
    bstack1l1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬἜ"): bstack1111l1lll1l_opy_ and bstack1l1l11l1l_opy_(threading.current_thread(), bstack1l1_opy_ (u"࠭ࡡ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬἝ"), None) == True and bstack1l1l11l11_opy_.bstack1l1ll1l1_opy_(test[bstack1l1_opy_ (u"ࠧࡵࡣࡪࡷࠬ἞")])
  }