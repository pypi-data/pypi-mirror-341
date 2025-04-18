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
import logging
import datetime
import threading
from bstack_utils.helper import bstack11llll11l11_opy_, bstack11111ll1_opy_, get_host_info, bstack11l1ll1llll_opy_, \
 bstack11l1l1l1_opy_, bstack1lllll11_opy_, bstack111l11ll1l_opy_, bstack11l1lllll1l_opy_, bstack1l11111ll_opy_
import bstack_utils.accessibility as bstack1ll11llll1_opy_
from bstack_utils.bstack11l111ll1l_opy_ import bstack1l1llll11_opy_
from bstack_utils.percy import bstack11ll111ll1_opy_
from bstack_utils.config import Config
bstack11llllllll_opy_ = Config.bstack1l1111llll_opy_()
logger = logging.getLogger(__name__)
percy = bstack11ll111ll1_opy_()
@bstack111l11ll1l_opy_(class_method=False)
def bstack1111ll11lll_opy_(bs_config, bstack1l1llllll1_opy_):
  try:
    data = {
        bstack1l1ll11_opy_ (u"ࠪࡪࡴࡸ࡭ࡢࡶࠪỢ"): bstack1l1ll11_opy_ (u"ࠫ࡯ࡹ࡯࡯ࠩợ"),
        bstack1l1ll11_opy_ (u"ࠬࡶࡲࡰ࡬ࡨࡧࡹࡥ࡮ࡢ࡯ࡨࠫỤ"): bs_config.get(bstack1l1ll11_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠫụ"), bstack1l1ll11_opy_ (u"ࠧࠨỦ")),
        bstack1l1ll11_opy_ (u"ࠨࡰࡤࡱࡪ࠭ủ"): bs_config.get(bstack1l1ll11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬỨ"), os.path.basename(os.path.abspath(os.getcwd()))),
        bstack1l1ll11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ứ"): bs_config.get(bstack1l1ll11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭Ừ")),
        bstack1l1ll11_opy_ (u"ࠬࡪࡥࡴࡥࡵ࡭ࡵࡺࡩࡰࡰࠪừ"): bs_config.get(bstack1l1ll11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡉ࡫ࡳࡤࡴ࡬ࡴࡹ࡯࡯࡯ࠩỬ"), bstack1l1ll11_opy_ (u"ࠧࠨử")),
        bstack1l1ll11_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬỮ"): bstack1l11111ll_opy_(),
        bstack1l1ll11_opy_ (u"ࠩࡷࡥ࡬ࡹࠧữ"): bstack11l1ll1llll_opy_(bs_config),
        bstack1l1ll11_opy_ (u"ࠪ࡬ࡴࡹࡴࡠ࡫ࡱࡪࡴ࠭Ự"): get_host_info(),
        bstack1l1ll11_opy_ (u"ࠫࡨ࡯࡟ࡪࡰࡩࡳࠬự"): bstack11111ll1_opy_(),
        bstack1l1ll11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣࡷࡻ࡮ࡠ࡫ࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬỲ"): os.environ.get(bstack1l1ll11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡈࡕࡊࡎࡇࡣࡗ࡛ࡎࡠࡋࡇࡉࡓ࡚ࡉࡇࡋࡈࡖࠬỳ")),
        bstack1l1ll11_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪ࡟ࡵࡧࡶࡸࡸࡥࡲࡦࡴࡸࡲࠬỴ"): os.environ.get(bstack1l1ll11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡓࡇࡕ࡙ࡓ࠭ỵ"), False),
        bstack1l1ll11_opy_ (u"ࠩࡹࡩࡷࡹࡩࡰࡰࡢࡧࡴࡴࡴࡳࡱ࡯ࠫỶ"): bstack11llll11l11_opy_(),
        bstack1l1ll11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪỷ"): bstack1111l1l1ll1_opy_(),
        bstack1l1ll11_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡥࡧࡷࡥ࡮ࡲࡳࠨỸ"): bstack1111l1llll1_opy_(bstack1l1llllll1_opy_),
        bstack1l1ll11_opy_ (u"ࠬࡶࡲࡰࡦࡸࡧࡹࡥ࡭ࡢࡲࠪỹ"): bstack1ll1111l1_opy_(bs_config, bstack1l1llllll1_opy_.get(bstack1l1ll11_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡸࡷࡪࡪࠧỺ"), bstack1l1ll11_opy_ (u"ࠧࠨỻ"))),
        bstack1l1ll11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪỼ"): bstack11l1l1l1_opy_(bs_config),
    }
    return data
  except Exception as error:
    logger.error(bstack1l1ll11_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡽࡨࡪ࡮ࡨࠤࡨࡸࡥࡢࡶ࡬ࡲ࡬ࠦࡰࡢࡻ࡯ࡳࡦࡪࠠࡧࡱࡵࠤ࡙࡫ࡳࡵࡊࡸࡦ࠿ࠦࠠࡼࡿࠥỽ").format(str(error)))
    return None
def bstack1111l1llll1_opy_(framework):
  return {
    bstack1l1ll11_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡔࡡ࡮ࡧࠪỾ"): framework.get(bstack1l1ll11_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࠬỿ"), bstack1l1ll11_opy_ (u"ࠬࡖࡹࡵࡧࡶࡸࠬἀ")),
    bstack1l1ll11_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡘࡨࡶࡸ࡯࡯࡯ࠩἁ"): framework.get(bstack1l1ll11_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡺࡪࡸࡳࡪࡱࡱࠫἂ")),
    bstack1l1ll11_opy_ (u"ࠨࡵࡧ࡯࡛࡫ࡲࡴ࡫ࡲࡲࠬἃ"): framework.get(bstack1l1ll11_opy_ (u"ࠩࡶࡨࡰࡥࡶࡦࡴࡶ࡭ࡴࡴࠧἄ")),
    bstack1l1ll11_opy_ (u"ࠪࡰࡦࡴࡧࡶࡣࡪࡩࠬἅ"): bstack1l1ll11_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫἆ"),
    bstack1l1ll11_opy_ (u"ࠬࡺࡥࡴࡶࡉࡶࡦࡳࡥࡸࡱࡵ࡯ࠬἇ"): framework.get(bstack1l1ll11_opy_ (u"࠭ࡴࡦࡵࡷࡊࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭Ἀ"))
  }
def bstack1ll1111l1_opy_(bs_config, framework):
  bstack11l11111l_opy_ = False
  bstack1llll11l1_opy_ = False
  bstack1111l1l1lll_opy_ = False
  if bstack1l1ll11_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫἉ") in bs_config:
    bstack1111l1l1lll_opy_ = True
  elif bstack1l1ll11_opy_ (u"ࠨࡣࡳࡴࠬἊ") in bs_config:
    bstack11l11111l_opy_ = True
  else:
    bstack1llll11l1_opy_ = True
  bstack1ll11ll11_opy_ = {
    bstack1l1ll11_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩἋ"): bstack1l1llll11_opy_.bstack1111l1ll111_opy_(bs_config, framework),
    bstack1l1ll11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪἌ"): bstack1ll11llll1_opy_.bstack1l111l1111_opy_(bs_config),
    bstack1l1ll11_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࠪἍ"): bs_config.get(bstack1l1ll11_opy_ (u"ࠬࡶࡥࡳࡥࡼࠫἎ"), False),
    bstack1l1ll11_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡥࠨἏ"): bstack1llll11l1_opy_,
    bstack1l1ll11_opy_ (u"ࠧࡢࡲࡳࡣࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭ἐ"): bstack11l11111l_opy_,
    bstack1l1ll11_opy_ (u"ࠨࡶࡸࡶࡧࡵࡳࡤࡣ࡯ࡩࠬἑ"): bstack1111l1l1lll_opy_
  }
  return bstack1ll11ll11_opy_
@bstack111l11ll1l_opy_(class_method=False)
def bstack1111l1l1ll1_opy_():
  try:
    bstack1111l1l1l11_opy_ = json.loads(os.getenv(bstack1l1ll11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪἒ"), bstack1l1ll11_opy_ (u"ࠪࡿࢂ࠭ἓ")))
    return {
        bstack1l1ll11_opy_ (u"ࠫࡸ࡫ࡴࡵ࡫ࡱ࡫ࡸ࠭ἔ"): bstack1111l1l1l11_opy_
    }
  except Exception as error:
    logger.error(bstack1l1ll11_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠࡤࡴࡨࡥࡹ࡯࡮ࡨࠢࡪࡩࡹࡥࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡥࡳࡦࡶࡷ࡭ࡳ࡭ࡳࠡࡨࡲࡶ࡚ࠥࡥࡴࡶࡋࡹࡧࡀࠠࠡࡽࢀࠦἕ").format(str(error)))
    return {}
def bstack1111llll111_opy_(array, bstack1111l1ll1ll_opy_, bstack1111l1ll11l_opy_):
  result = {}
  for o in array:
    key = o[bstack1111l1ll1ll_opy_]
    result[key] = o[bstack1111l1ll11l_opy_]
  return result
def bstack1111ll1l1ll_opy_(bstack1l11l11l1_opy_=bstack1l1ll11_opy_ (u"࠭ࠧ἖")):
  bstack1111l1lll11_opy_ = bstack1ll11llll1_opy_.on()
  bstack1111l1ll1l1_opy_ = bstack1l1llll11_opy_.on()
  bstack1111l1l1l1l_opy_ = percy.bstack1lll111111_opy_()
  if bstack1111l1l1l1l_opy_ and not bstack1111l1ll1l1_opy_ and not bstack1111l1lll11_opy_:
    return bstack1l11l11l1_opy_ not in [bstack1l1ll11_opy_ (u"ࠧࡄࡄࡗࡗࡪࡹࡳࡪࡱࡱࡇࡷ࡫ࡡࡵࡧࡧࠫ἗"), bstack1l1ll11_opy_ (u"ࠨࡎࡲ࡫ࡈࡸࡥࡢࡶࡨࡨࠬἘ")]
  elif bstack1111l1lll11_opy_ and not bstack1111l1ll1l1_opy_:
    return bstack1l11l11l1_opy_ not in [bstack1l1ll11_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪἙ"), bstack1l1ll11_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬἚ"), bstack1l1ll11_opy_ (u"ࠫࡑࡵࡧࡄࡴࡨࡥࡹ࡫ࡤࠨἛ")]
  return bstack1111l1lll11_opy_ or bstack1111l1ll1l1_opy_ or bstack1111l1l1l1l_opy_
@bstack111l11ll1l_opy_(class_method=False)
def bstack1111lll1ll1_opy_(bstack1l11l11l1_opy_, test=None):
  bstack1111l1lll1l_opy_ = bstack1ll11llll1_opy_.on()
  if not bstack1111l1lll1l_opy_ or bstack1l11l11l1_opy_ not in [bstack1l1ll11_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧἜ")] or test == None:
    return None
  return {
    bstack1l1ll11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭Ἕ"): bstack1111l1lll1l_opy_ and bstack1lllll11_opy_(threading.current_thread(), bstack1l1ll11_opy_ (u"ࠧࡢ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭἞"), None) == True and bstack1ll11llll1_opy_.bstack1ll11l11_opy_(test[bstack1l1ll11_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭἟")])
  }