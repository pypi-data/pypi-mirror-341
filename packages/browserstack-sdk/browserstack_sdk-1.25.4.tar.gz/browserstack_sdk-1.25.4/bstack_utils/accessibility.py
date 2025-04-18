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
import requests
import logging
import threading
from urllib.parse import urlparse
from bstack_utils.constants import bstack11llllll11l_opy_ as bstack11lllll11ll_opy_, EVENTS
from bstack_utils.bstack11ll1l11ll_opy_ import bstack11ll1l11ll_opy_
from bstack_utils.helper import bstack1l11111ll_opy_, bstack111l11l11l_opy_, bstack11l1l1l1_opy_, bstack11llll11ll1_opy_, \
  bstack11lllll111l_opy_, bstack11111ll1_opy_, get_host_info, bstack11llll11l11_opy_, bstack1l1ll11lll_opy_, bstack111l11ll1l_opy_, bstack1lllll11_opy_
from browserstack_sdk._version import __version__
from bstack_utils.bstack111l1l111_opy_ import get_logger
from bstack_utils.bstack1lll111l_opy_ import bstack1ll1llllll1_opy_
from bstack_utils.constants import *
logger = get_logger(__name__)
bstack1lll111l_opy_ = bstack1ll1llllll1_opy_()
@bstack111l11ll1l_opy_(class_method=False)
def _11lll1lllll_opy_(driver, bstack111l111111_opy_):
  response = {}
  try:
    caps = driver.capabilities
    response = {
        bstack1l1ll11_opy_ (u"ࠨࡱࡶࡣࡳࡧ࡭ࡦࠩᕎ"): caps.get(bstack1l1ll11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡒࡦࡳࡥࠨᕏ"), None),
        bstack1l1ll11_opy_ (u"ࠪࡳࡸࡥࡶࡦࡴࡶ࡭ࡴࡴࠧᕐ"): bstack111l111111_opy_.get(bstack1l1ll11_opy_ (u"ࠫࡴࡹࡖࡦࡴࡶ࡭ࡴࡴࠧᕑ"), None),
        bstack1l1ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥ࡮ࡢ࡯ࡨࠫᕒ"): caps.get(bstack1l1ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫᕓ"), None),
        bstack1l1ll11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠩᕔ"): caps.get(bstack1l1ll11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩᕕ"), None)
    }
  except Exception as error:
    logger.debug(bstack1l1ll11_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡨࡨࡸࡨ࡮ࡩ࡯ࡩࠣࡴࡱࡧࡴࡧࡱࡵࡱࠥࡪࡥࡵࡣ࡬ࡰࡸࠦࡷࡪࡶ࡫ࠤࡪࡸࡲࡰࡴࠣ࠾ࠥ࠭ᕖ") + str(error))
  return response
def on():
    if os.environ.get(bstack1l1ll11_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨᕗ"), None) is None or os.environ[bstack1l1ll11_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩᕘ")] == bstack1l1ll11_opy_ (u"ࠧࡴࡵ࡭࡮ࠥᕙ"):
        return False
    return True
def bstack1l111l1111_opy_(config):
  return config.get(bstack1l1ll11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ᕚ"), False) or any([p.get(bstack1l1ll11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᕛ"), False) == True for p in config.get(bstack1l1ll11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫᕜ"), [])])
def bstack1l1llll1_opy_(config, bstack11111l11l_opy_):
  try:
    if not bstack11l1l1l1_opy_(config):
      return False
    bstack11lllll1l1l_opy_ = config.get(bstack1l1ll11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩᕝ"), False)
    if int(bstack11111l11l_opy_) < len(config.get(bstack1l1ll11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ᕞ"), [])) and config[bstack1l1ll11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧᕟ")][bstack11111l11l_opy_]:
      bstack11llll111ll_opy_ = config[bstack1l1ll11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨᕠ")][bstack11111l11l_opy_].get(bstack1l1ll11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ᕡ"), None)
    else:
      bstack11llll111ll_opy_ = config.get(bstack1l1ll11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᕢ"), None)
    if bstack11llll111ll_opy_ != None:
      bstack11lllll1l1l_opy_ = bstack11llll111ll_opy_
    bstack11llll1l1ll_opy_ = os.getenv(bstack1l1ll11_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭ᕣ")) is not None and len(os.getenv(bstack1l1ll11_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧᕤ"))) > 0 and os.getenv(bstack1l1ll11_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨᕥ")) != bstack1l1ll11_opy_ (u"ࠫࡳࡻ࡬࡭ࠩᕦ")
    return bstack11lllll1l1l_opy_ and bstack11llll1l1ll_opy_
  except Exception as error:
    logger.debug(bstack1l1ll11_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡻ࡫ࡲࡪࡨࡼ࡭ࡳ࡭ࠠࡵࡪࡨࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡽࡩࡵࡪࠣࡩࡷࡸ࡯ࡳࠢ࠽ࠤࠬᕧ") + str(error))
  return False
def bstack1ll11l11_opy_(test_tags):
  bstack1ll1l1l1ll1_opy_ = os.getenv(bstack1l1ll11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡢࡅࡈࡉࡅࡔࡕࡌࡆࡎࡒࡉࡕ࡛ࡢࡇࡔࡔࡆࡊࡉࡘࡖࡆ࡚ࡉࡐࡐࡢ࡝ࡒࡒࠧᕨ"))
  if bstack1ll1l1l1ll1_opy_ is None:
    return True
  bstack1ll1l1l1ll1_opy_ = json.loads(bstack1ll1l1l1ll1_opy_)
  try:
    include_tags = bstack1ll1l1l1ll1_opy_[bstack1l1ll11_opy_ (u"ࠧࡪࡰࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬᕩ")] if bstack1l1ll11_opy_ (u"ࠨ࡫ࡱࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭ᕪ") in bstack1ll1l1l1ll1_opy_ and isinstance(bstack1ll1l1l1ll1_opy_[bstack1l1ll11_opy_ (u"ࠩ࡬ࡲࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧᕫ")], list) else []
    exclude_tags = bstack1ll1l1l1ll1_opy_[bstack1l1ll11_opy_ (u"ࠪࡩࡽࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨᕬ")] if bstack1l1ll11_opy_ (u"ࠫࡪࡾࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩᕭ") in bstack1ll1l1l1ll1_opy_ and isinstance(bstack1ll1l1l1ll1_opy_[bstack1l1ll11_opy_ (u"ࠬ࡫ࡸࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪᕮ")], list) else []
    excluded = any(tag in exclude_tags for tag in test_tags)
    included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
    return not excluded and included
  except Exception as error:
    logger.debug(bstack1l1ll11_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤࡻࡧ࡬ࡪࡦࡤࡸ࡮ࡴࡧࠡࡶࡨࡷࡹࠦࡣࡢࡵࡨࠤ࡫ࡵࡲࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡤࡨࡪࡴࡸࡥࠡࡵࡦࡥࡳࡴࡩ࡯ࡩ࠱ࠤࡊࡸࡲࡰࡴࠣ࠾ࠥࠨᕯ") + str(error))
  return False
def bstack11lllll1l11_opy_(config, bstack11lllll1ll1_opy_, bstack11lllll1lll_opy_, bstack11llll1111l_opy_):
  bstack11llll111l1_opy_ = bstack11llll11ll1_opy_(config)
  bstack11lllll1111_opy_ = bstack11lllll111l_opy_(config)
  if bstack11llll111l1_opy_ is None or bstack11lllll1111_opy_ is None:
    logger.error(bstack1l1ll11_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡦࡶࡪࡧࡴࡪࡰࡪࠤࡹ࡫ࡳࡵࠢࡵࡹࡳࠦࡦࡰࡴࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡀࠠࡎ࡫ࡶࡷ࡮ࡴࡧࠡࡣࡸࡸ࡭࡫࡮ࡵ࡫ࡦࡥࡹ࡯࡯࡯ࠢࡷࡳࡰ࡫࡮ࠨᕰ"))
    return [None, None]
  try:
    settings = json.loads(os.getenv(bstack1l1ll11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡤࡇࡃࡄࡇࡖࡗࡎࡈࡉࡍࡋࡗ࡝ࡤࡉࡏࡏࡈࡌࡋ࡚ࡘࡁࡕࡋࡒࡒࡤ࡟ࡍࡍࠩᕱ"), bstack1l1ll11_opy_ (u"ࠩࡾࢁࠬᕲ")))
    data = {
        bstack1l1ll11_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨᕳ"): config[bstack1l1ll11_opy_ (u"ࠫࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦࠩᕴ")],
        bstack1l1ll11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨᕵ"): config.get(bstack1l1ll11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩᕶ"), os.path.basename(os.getcwd())),
        bstack1l1ll11_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡚ࡩ࡮ࡧࠪᕷ"): bstack1l11111ll_opy_(),
        bstack1l1ll11_opy_ (u"ࠨࡦࡨࡷࡨࡸࡩࡱࡶ࡬ࡳࡳ࠭ᕸ"): config.get(bstack1l1ll11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡅࡧࡶࡧࡷ࡯ࡰࡵ࡫ࡲࡲࠬᕹ"), bstack1l1ll11_opy_ (u"ࠪࠫᕺ")),
        bstack1l1ll11_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫᕻ"): {
            bstack1l1ll11_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡏࡣࡰࡩࠬᕼ"): bstack11lllll1ll1_opy_,
            bstack1l1ll11_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡘࡨࡶࡸ࡯࡯࡯ࠩᕽ"): bstack11lllll1lll_opy_,
            bstack1l1ll11_opy_ (u"ࠧࡴࡦ࡮࡚ࡪࡸࡳࡪࡱࡱࠫᕾ"): __version__,
            bstack1l1ll11_opy_ (u"ࠨ࡮ࡤࡲ࡬ࡻࡡࡨࡧࠪᕿ"): bstack1l1ll11_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩᖀ"),
            bstack1l1ll11_opy_ (u"ࠪࡸࡪࡹࡴࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪᖁ"): bstack1l1ll11_opy_ (u"ࠫࡸ࡫࡬ࡦࡰ࡬ࡹࡲ࠭ᖂ"),
            bstack1l1ll11_opy_ (u"ࠬࡺࡥࡴࡶࡉࡶࡦࡳࡥࡸࡱࡵ࡯࡛࡫ࡲࡴ࡫ࡲࡲࠬᖃ"): bstack11llll1111l_opy_
        },
        bstack1l1ll11_opy_ (u"࠭ࡳࡦࡶࡷ࡭ࡳ࡭ࡳࠨᖄ"): settings,
        bstack1l1ll11_opy_ (u"ࠧࡷࡧࡵࡷ࡮ࡵ࡮ࡄࡱࡱࡸࡷࡵ࡬ࠨᖅ"): bstack11llll11l11_opy_(),
        bstack1l1ll11_opy_ (u"ࠨࡥ࡬ࡍࡳ࡬࡯ࠨᖆ"): bstack11111ll1_opy_(),
        bstack1l1ll11_opy_ (u"ࠩ࡫ࡳࡸࡺࡉ࡯ࡨࡲࠫᖇ"): get_host_info(),
        bstack1l1ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬᖈ"): bstack11l1l1l1_opy_(config)
    }
    headers = {
        bstack1l1ll11_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲࡚ࡹࡱࡧࠪᖉ"): bstack1l1ll11_opy_ (u"ࠬࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠨᖊ"),
    }
    config = {
        bstack1l1ll11_opy_ (u"࠭ࡡࡶࡶ࡫ࠫᖋ"): (bstack11llll111l1_opy_, bstack11lllll1111_opy_),
        bstack1l1ll11_opy_ (u"ࠧࡩࡧࡤࡨࡪࡸࡳࠨᖌ"): headers
    }
    response = bstack1l1ll11lll_opy_(bstack1l1ll11_opy_ (u"ࠨࡒࡒࡗ࡙࠭ᖍ"), bstack11lllll11ll_opy_ + bstack1l1ll11_opy_ (u"ࠩ࠲ࡺ࠷࠵ࡴࡦࡵࡷࡣࡷࡻ࡮ࡴࠩᖎ"), data, config)
    bstack11llll1l111_opy_ = response.json()
    if bstack11llll1l111_opy_[bstack1l1ll11_opy_ (u"ࠪࡷࡺࡩࡣࡦࡵࡶࠫᖏ")]:
      parsed = json.loads(os.getenv(bstack1l1ll11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬᖐ"), bstack1l1ll11_opy_ (u"ࠬࢁࡽࠨᖑ")))
      parsed[bstack1l1ll11_opy_ (u"࠭ࡳࡤࡣࡱࡲࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧᖒ")] = bstack11llll1l111_opy_[bstack1l1ll11_opy_ (u"ࠧࡥࡣࡷࡥࠬᖓ")][bstack1l1ll11_opy_ (u"ࠨࡵࡦࡥࡳࡴࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩᖔ")]
      os.environ[bstack1l1ll11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪᖕ")] = json.dumps(parsed)
      bstack11ll1l11ll_opy_.bstack111l11lll_opy_(bstack11llll1l111_opy_[bstack1l1ll11_opy_ (u"ࠪࡨࡦࡺࡡࠨᖖ")][bstack1l1ll11_opy_ (u"ࠫࡸࡩࡲࡪࡲࡷࡷࠬᖗ")])
      bstack11ll1l11ll_opy_.bstack11llllll1ll_opy_(bstack11llll1l111_opy_[bstack1l1ll11_opy_ (u"ࠬࡪࡡࡵࡣࠪᖘ")][bstack1l1ll11_opy_ (u"࠭ࡣࡰ࡯ࡰࡥࡳࡪࡳࠨᖙ")])
      bstack11ll1l11ll_opy_.store()
      return bstack11llll1l111_opy_[bstack1l1ll11_opy_ (u"ࠧࡥࡣࡷࡥࠬᖚ")][bstack1l1ll11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡕࡱ࡮ࡩࡳ࠭ᖛ")], bstack11llll1l111_opy_[bstack1l1ll11_opy_ (u"ࠩࡧࡥࡹࡧࠧᖜ")][bstack1l1ll11_opy_ (u"ࠪ࡭ࡩ࠭ᖝ")]
    else:
      logger.error(bstack1l1ll11_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦࡲࡶࡰࡱ࡭ࡳ࡭ࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰ࠽ࠤࠬᖞ") + bstack11llll1l111_opy_[bstack1l1ll11_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᖟ")])
      if bstack11llll1l111_opy_[bstack1l1ll11_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᖠ")] == bstack1l1ll11_opy_ (u"ࠧࡊࡰࡹࡥࡱ࡯ࡤࠡࡥࡲࡲ࡫࡯ࡧࡶࡴࡤࡸ࡮ࡵ࡮ࠡࡲࡤࡷࡸ࡫ࡤ࠯ࠩᖡ"):
        for bstack11lll1lll11_opy_ in bstack11llll1l111_opy_[bstack1l1ll11_opy_ (u"ࠨࡧࡵࡶࡴࡸࡳࠨᖢ")]:
          logger.error(bstack11lll1lll11_opy_[bstack1l1ll11_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᖣ")])
      return None, None
  except Exception as error:
    logger.error(bstack1l1ll11_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡷࡩ࡫࡯ࡩࠥࡩࡲࡦࡣࡷ࡭ࡳ࡭ࠠࡵࡧࡶࡸࠥࡸࡵ࡯ࠢࡩࡳࡷࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯࠼ࠣࠦᖤ") +  str(error))
    return None, None
def bstack11llll1llll_opy_():
  if os.getenv(bstack1l1ll11_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩᖥ")) is None:
    return {
        bstack1l1ll11_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬᖦ"): bstack1l1ll11_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬᖧ"),
        bstack1l1ll11_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨᖨ"): bstack1l1ll11_opy_ (u"ࠨࡄࡸ࡭ࡱࡪࠠࡤࡴࡨࡥࡹ࡯࡯࡯ࠢ࡫ࡥࡩࠦࡦࡢ࡫࡯ࡩࡩ࠴ࠧᖩ")
    }
  data = {bstack1l1ll11_opy_ (u"ࠩࡨࡲࡩ࡚ࡩ࡮ࡧࠪᖪ"): bstack1l11111ll_opy_()}
  headers = {
      bstack1l1ll11_opy_ (u"ࠪࡅࡺࡺࡨࡰࡴ࡬ࡾࡦࡺࡩࡰࡰࠪᖫ"): bstack1l1ll11_opy_ (u"ࠫࡇ࡫ࡡࡳࡧࡵࠤࠬᖬ") + os.getenv(bstack1l1ll11_opy_ (u"ࠧࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠥᖭ")),
      bstack1l1ll11_opy_ (u"࠭ࡃࡰࡰࡷࡩࡳࡺ࠭ࡕࡻࡳࡩࠬᖮ"): bstack1l1ll11_opy_ (u"ࠧࡢࡲࡳࡰ࡮ࡩࡡࡵ࡫ࡲࡲ࠴ࡰࡳࡰࡰࠪᖯ")
  }
  response = bstack1l1ll11lll_opy_(bstack1l1ll11_opy_ (u"ࠨࡒࡘࡘࠬᖰ"), bstack11lllll11ll_opy_ + bstack1l1ll11_opy_ (u"ࠩ࠲ࡸࡪࡹࡴࡠࡴࡸࡲࡸ࠵ࡳࡵࡱࡳࠫᖱ"), data, { bstack1l1ll11_opy_ (u"ࠪ࡬ࡪࡧࡤࡦࡴࡶࠫᖲ"): headers })
  try:
    if response.status_code == 200:
      logger.info(bstack1l1ll11_opy_ (u"ࠦࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡕࡧࡶࡸࠥࡘࡵ࡯ࠢࡰࡥࡷࡱࡥࡥࠢࡤࡷࠥࡩ࡯࡮ࡲ࡯ࡩࡹ࡫ࡤࠡࡣࡷࠤࠧᖳ") + bstack111l11l11l_opy_().isoformat() + bstack1l1ll11_opy_ (u"ࠬࡠࠧᖴ"))
      return {bstack1l1ll11_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ᖵ"): bstack1l1ll11_opy_ (u"ࠧࡴࡷࡦࡧࡪࡹࡳࠨᖶ"), bstack1l1ll11_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᖷ"): bstack1l1ll11_opy_ (u"ࠩࠪᖸ")}
    else:
      response.raise_for_status()
  except requests.RequestException as error:
    logger.error(bstack1l1ll11_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡷࡩ࡫࡯ࡩࠥࡳࡡࡳ࡭࡬ࡲ࡬ࠦࡣࡰ࡯ࡳࡰࡪࡺࡩࡰࡰࠣࡳ࡫ࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡗࡩࡸࡺࠠࡓࡷࡱ࠾ࠥࠨᖹ") + str(error))
    return {
        bstack1l1ll11_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫᖺ"): bstack1l1ll11_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫᖻ"),
        bstack1l1ll11_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᖼ"): str(error)
    }
def bstack11llll11111_opy_(bstack11lll1llll1_opy_):
    return re.match(bstack1l1ll11_opy_ (u"ࡲࠨࡠ࡟ࡨ࠰࠮࡜࠯࡞ࡧ࠯࠮ࡅࠤࠨᖽ"), bstack11lll1llll1_opy_.strip()) is not None
def bstack11lll1lll1_opy_(caps, options, desired_capabilities={}):
    try:
        if options:
          bstack11llllll1l1_opy_ = options.to_capabilities()
        elif desired_capabilities:
          bstack11llllll1l1_opy_ = desired_capabilities
        else:
          bstack11llllll1l1_opy_ = {}
        bstack11llll11l1l_opy_ = (bstack11llllll1l1_opy_.get(bstack1l1ll11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡑࡥࡲ࡫ࠧᖾ"), bstack1l1ll11_opy_ (u"ࠩࠪᖿ")).lower() or caps.get(bstack1l1ll11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡓࡧ࡭ࡦࠩᗀ"), bstack1l1ll11_opy_ (u"ࠫࠬᗁ")).lower())
        if bstack11llll11l1l_opy_ == bstack1l1ll11_opy_ (u"ࠬ࡯࡯ࡴࠩᗂ"):
            return True
        if bstack11llll11l1l_opy_ == bstack1l1ll11_opy_ (u"࠭ࡡ࡯ࡦࡵࡳ࡮ࡪࠧᗃ"):
            bstack11llll1ll11_opy_ = str(float(caps.get(bstack1l1ll11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩᗄ")) or bstack11llllll1l1_opy_.get(bstack1l1ll11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩᗅ"), {}).get(bstack1l1ll11_opy_ (u"ࠩࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠬᗆ"),bstack1l1ll11_opy_ (u"ࠪࠫᗇ"))))
            if bstack11llll11l1l_opy_ == bstack1l1ll11_opy_ (u"ࠫࡦࡴࡤࡳࡱ࡬ࡨࠬᗈ") and int(bstack11llll1ll11_opy_.split(bstack1l1ll11_opy_ (u"ࠬ࠴ࠧᗉ"))[0]) < float(bstack11llll1lll1_opy_):
                logger.warning(str(bstack11lllll11l1_opy_))
                return False
            return True
        bstack1ll1ll1lll1_opy_ = caps.get(bstack1l1ll11_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧᗊ"), {}).get(bstack1l1ll11_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡎࡢ࡯ࡨࠫᗋ"), caps.get(bstack1l1ll11_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࠨᗌ"), bstack1l1ll11_opy_ (u"ࠩࠪᗍ")))
        if bstack1ll1ll1lll1_opy_:
            logger.warn(bstack1l1ll11_opy_ (u"ࠥࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡸ࡫࡯ࡰࠥࡸࡵ࡯ࠢࡲࡲࡱࡿࠠࡰࡰࠣࡈࡪࡹ࡫ࡵࡱࡳࠤࡧࡸ࡯ࡸࡵࡨࡶࡸ࠴ࠢᗎ"))
            return False
        browser = caps.get(bstack1l1ll11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩᗏ"), bstack1l1ll11_opy_ (u"ࠬ࠭ᗐ")).lower() or bstack11llllll1l1_opy_.get(bstack1l1ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫᗑ"), bstack1l1ll11_opy_ (u"ࠧࠨᗒ")).lower()
        if browser != bstack1l1ll11_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࠨᗓ"):
            logger.warning(bstack1l1ll11_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡷࡪ࡮࡯ࠤࡷࡻ࡮ࠡࡱࡱࡰࡾࠦ࡯࡯ࠢࡆ࡬ࡷࡵ࡭ࡦࠢࡥࡶࡴࡽࡳࡦࡴࡶ࠲ࠧᗔ"))
            return False
        browser_version = caps.get(bstack1l1ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫᗕ")) or caps.get(bstack1l1ll11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ᗖ")) or bstack11llllll1l1_opy_.get(bstack1l1ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᗗ")) or bstack11llllll1l1_opy_.get(bstack1l1ll11_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧᗘ"), {}).get(bstack1l1ll11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨᗙ")) or bstack11llllll1l1_opy_.get(bstack1l1ll11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩᗚ"), {}).get(bstack1l1ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡢࡺࡪࡸࡳࡪࡱࡱࠫᗛ"))
        if browser_version and browser_version != bstack1l1ll11_opy_ (u"ࠪࡰࡦࡺࡥࡴࡶࠪᗜ") and int(browser_version.split(bstack1l1ll11_opy_ (u"ࠫ࠳࠭ᗝ"))[0]) <= 98:
            logger.warning(bstack1l1ll11_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡺ࡭ࡱࡲࠠࡳࡷࡱࠤࡴࡴ࡬ࡺࠢࡲࡲࠥࡉࡨࡳࡱࡰࡩࠥࡨࡲࡰࡹࡶࡩࡷࠦࡶࡦࡴࡶ࡭ࡴࡴࠠࡨࡴࡨࡥࡹ࡫ࡲࠡࡶ࡫ࡥࡳࠦ࠹࠹࠰ࠥᗞ"))
            return False
        if not options:
            bstack1ll1ll11l11_opy_ = caps.get(bstack1l1ll11_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫᗟ")) or bstack11llllll1l1_opy_.get(bstack1l1ll11_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬᗠ"), {})
            if bstack1l1ll11_opy_ (u"ࠨ࠯࠰࡬ࡪࡧࡤ࡭ࡧࡶࡷࠬᗡ") in bstack1ll1ll11l11_opy_.get(bstack1l1ll11_opy_ (u"ࠩࡤࡶ࡬ࡹࠧᗢ"), []):
                logger.warn(bstack1l1ll11_opy_ (u"ࠥࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡸ࡫࡯ࡰࠥࡴ࡯ࡵࠢࡵࡹࡳࠦ࡯࡯ࠢ࡯ࡩ࡬ࡧࡣࡺࠢ࡫ࡩࡦࡪ࡬ࡦࡵࡶࠤࡲࡵࡤࡦ࠰ࠣࡗࡼ࡯ࡴࡤࡪࠣࡸࡴࠦ࡮ࡦࡹࠣ࡬ࡪࡧࡤ࡭ࡧࡶࡷࠥࡳ࡯ࡥࡧࠣࡳࡷࠦࡡࡷࡱ࡬ࡨࠥࡻࡳࡪࡰࡪࠤ࡭࡫ࡡࡥ࡮ࡨࡷࡸࠦ࡭ࡰࡦࡨ࠲ࠧᗣ"))
                return False
        return True
    except Exception as error:
        logger.debug(bstack1l1ll11_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡺࡦࡲࡩࡥࡣࡷࡩࠥࡧ࠱࠲ࡻࠣࡷࡺࡶࡰࡰࡴࡷࠤ࠿ࠨᗤ") + str(error))
        return False
def set_capabilities(caps, config):
  try:
    bstack1llll111111_opy_ = config.get(bstack1l1ll11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬᗥ"), {})
    bstack1llll111111_opy_[bstack1l1ll11_opy_ (u"࠭ࡡࡶࡶ࡫ࡘࡴࡱࡥ࡯ࠩᗦ")] = os.getenv(bstack1l1ll11_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬᗧ"))
    bstack11llllll111_opy_ = json.loads(os.getenv(bstack1l1ll11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡤࡇࡃࡄࡇࡖࡗࡎࡈࡉࡍࡋࡗ࡝ࡤࡉࡏࡏࡈࡌࡋ࡚ࡘࡁࡕࡋࡒࡒࡤ࡟ࡍࡍࠩᗨ"), bstack1l1ll11_opy_ (u"ࠩࡾࢁࠬᗩ"))).get(bstack1l1ll11_opy_ (u"ࠪࡷࡨࡧ࡮࡯ࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫᗪ"))
    caps[bstack1l1ll11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᗫ")] = True
    if not config[bstack1l1ll11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡔࡷࡵࡤࡶࡥࡷࡑࡦࡶࠧᗬ")].get(bstack1l1ll11_opy_ (u"ࠨࡡࡱࡲࡢࡥࡺࡺ࡯࡮ࡣࡷࡩࠧᗭ")):
      if bstack1l1ll11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᗮ") in caps:
        caps[bstack1l1ll11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩᗯ")][bstack1l1ll11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩᗰ")] = bstack1llll111111_opy_
        caps[bstack1l1ll11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫᗱ")][bstack1l1ll11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫᗲ")][bstack1l1ll11_opy_ (u"ࠬࡹࡣࡢࡰࡱࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᗳ")] = bstack11llllll111_opy_
      else:
        caps[bstack1l1ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬᗴ")] = bstack1llll111111_opy_
        caps[bstack1l1ll11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ᗵ")][bstack1l1ll11_opy_ (u"ࠨࡵࡦࡥࡳࡴࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩᗶ")] = bstack11llllll111_opy_
  except Exception as error:
    logger.debug(bstack1l1ll11_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡽࡨࡪ࡮ࡨࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳ࠯ࠢࡈࡶࡷࡵࡲ࠻ࠢࠥᗷ") +  str(error))
def bstack11ll111l1l_opy_(driver, bstack11llll1ll1l_opy_):
  try:
    setattr(driver, bstack1l1ll11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡄ࠵࠶ࡿࡓࡩࡱࡸࡰࡩ࡙ࡣࡢࡰࠪᗸ"), True)
    session = driver.session_id
    if session:
      bstack11lll1ll1ll_opy_ = True
      current_url = driver.current_url
      try:
        url = urlparse(current_url)
      except Exception as e:
        bstack11lll1ll1ll_opy_ = False
      bstack11lll1ll1ll_opy_ = url.scheme in [bstack1l1ll11_opy_ (u"ࠦ࡭ࡺࡴࡱࠤᗹ"), bstack1l1ll11_opy_ (u"ࠧ࡮ࡴࡵࡲࡶࠦᗺ")]
      if bstack11lll1ll1ll_opy_:
        if bstack11llll1ll1l_opy_:
          logger.info(bstack1l1ll11_opy_ (u"ࠨࡓࡦࡶࡸࡴࠥ࡬࡯ࡳࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡷࡩࡸࡺࡩ࡯ࡩࠣ࡬ࡦࡹࠠࡴࡶࡤࡶࡹ࡫ࡤ࠯ࠢࡄࡹࡹࡵ࡭ࡢࡶࡨࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫ࠠࡦࡺࡨࡧࡺࡺࡩࡰࡰࠣࡻ࡮ࡲ࡬ࠡࡤࡨ࡫࡮ࡴࠠ࡮ࡱࡰࡩࡳࡺࡡࡳ࡫࡯ࡽ࠳ࠨᗻ"))
      return bstack11llll1ll1l_opy_
  except Exception as e:
    logger.error(bstack1l1ll11_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡳࡵࡣࡵࡸ࡮ࡴࡧࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡹࡣࡢࡰࠣࡪࡴࡸࠠࡵࡪ࡬ࡷࠥࡺࡥࡴࡶࠣࡧࡦࡹࡥ࠻ࠢࠥᗼ") + str(e))
    return False
def bstack1ll111111_opy_(driver, name, path):
  try:
    bstack1ll1l1111ll_opy_ = {
        bstack1l1ll11_opy_ (u"ࠨࡶ࡫ࡘࡪࡹࡴࡓࡷࡱ࡙ࡺ࡯ࡤࠨᗽ"): threading.current_thread().current_test_uuid,
        bstack1l1ll11_opy_ (u"ࠩࡷ࡬ࡇࡻࡩ࡭ࡦࡘࡹ࡮ࡪࠧᗾ"): os.environ.get(bstack1l1ll11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨᗿ"), bstack1l1ll11_opy_ (u"ࠫࠬᘀ")),
        bstack1l1ll11_opy_ (u"ࠬࡺࡨࡋࡹࡷࡘࡴࡱࡥ࡯ࠩᘁ"): os.environ.get(bstack1l1ll11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪᘂ"), bstack1l1ll11_opy_ (u"ࠧࠨᘃ"))
    }
    bstack1ll1ll11l1l_opy_ = bstack1lll111l_opy_.bstack1ll1ll1l11l_opy_(EVENTS.bstack111lll11l_opy_.value)
    logger.debug(bstack1l1ll11_opy_ (u"ࠨࡒࡨࡶ࡫ࡵࡲ࡮࡫ࡱ࡫ࠥࡹࡣࡢࡰࠣࡦࡪ࡬࡯ࡳࡧࠣࡷࡦࡼࡩ࡯ࡩࠣࡶࡪࡹࡵ࡭ࡶࡶࠫᘄ"))
    try:
      if (bstack1lllll11_opy_(threading.current_thread(), bstack1l1ll11_opy_ (u"ࠩ࡬ࡷࡆࡶࡰࡂ࠳࠴ࡽ࡙࡫ࡳࡵࠩᘅ"), None) and bstack1lllll11_opy_(threading.current_thread(), bstack1l1ll11_opy_ (u"ࠪࡥࡵࡶࡁ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬᘆ"), None)):
        scripts = {bstack1l1ll11_opy_ (u"ࠫࡸࡩࡡ࡯ࠩᘇ"): bstack11ll1l11ll_opy_.perform_scan}
        bstack11llll1l11l_opy_ = json.loads(scripts[bstack1l1ll11_opy_ (u"ࠧࡹࡣࡢࡰࠥᘈ")].replace(bstack1l1ll11_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࠤᘉ"), bstack1l1ll11_opy_ (u"ࠢࠣᘊ")))
        bstack11llll1l11l_opy_[bstack1l1ll11_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫᘋ")][bstack1l1ll11_opy_ (u"ࠩࡰࡩࡹ࡮࡯ࡥࠩᘌ")] = None
        scripts[bstack1l1ll11_opy_ (u"ࠥࡷࡨࡧ࡮ࠣᘍ")] = bstack1l1ll11_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࠢᘎ") + json.dumps(bstack11llll1l11l_opy_)
        bstack11ll1l11ll_opy_.bstack111l11lll_opy_(scripts)
        bstack11ll1l11ll_opy_.store()
        logger.debug(driver.execute_script(bstack11ll1l11ll_opy_.perform_scan))
      else:
        logger.debug(driver.execute_async_script(bstack11ll1l11ll_opy_.perform_scan, {bstack1l1ll11_opy_ (u"ࠧࡳࡥࡵࡪࡲࡨࠧᘏ"): name}))
      bstack1lll111l_opy_.end(EVENTS.bstack111lll11l_opy_.value, bstack1ll1ll11l1l_opy_ + bstack1l1ll11_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨᘐ"), bstack1ll1ll11l1l_opy_ + bstack1l1ll11_opy_ (u"ࠢ࠻ࡧࡱࡨࠧᘑ"), True, None)
    except Exception as error:
      bstack1lll111l_opy_.end(EVENTS.bstack111lll11l_opy_.value, bstack1ll1ll11l1l_opy_ + bstack1l1ll11_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣᘒ"), bstack1ll1ll11l1l_opy_ + bstack1l1ll11_opy_ (u"ࠤ࠽ࡩࡳࡪࠢᘓ"), False, str(error))
    bstack1ll1ll11l1l_opy_ = bstack1lll111l_opy_.bstack11lll1lll1l_opy_(EVENTS.bstack1ll1l11111l_opy_.value)
    bstack1lll111l_opy_.mark(bstack1ll1ll11l1l_opy_ + bstack1l1ll11_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥᘔ"))
    try:
      if (bstack1lllll11_opy_(threading.current_thread(), bstack1l1ll11_opy_ (u"ࠫ࡮ࡹࡁࡱࡲࡄ࠵࠶ࡿࡔࡦࡵࡷࠫᘕ"), None) and bstack1lllll11_opy_(threading.current_thread(), bstack1l1ll11_opy_ (u"ࠬࡧࡰࡱࡃ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧᘖ"), None)):
        scripts = {bstack1l1ll11_opy_ (u"࠭ࡳࡤࡣࡱࠫᘗ"): bstack11ll1l11ll_opy_.perform_scan}
        bstack11llll1l11l_opy_ = json.loads(scripts[bstack1l1ll11_opy_ (u"ࠢࡴࡥࡤࡲࠧᘘ")].replace(bstack1l1ll11_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࠦᘙ"), bstack1l1ll11_opy_ (u"ࠤࠥᘚ")))
        bstack11llll1l11l_opy_[bstack1l1ll11_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ᘛ")][bstack1l1ll11_opy_ (u"ࠫࡲ࡫ࡴࡩࡱࡧࠫᘜ")] = None
        scripts[bstack1l1ll11_opy_ (u"ࠧࡹࡣࡢࡰࠥᘝ")] = bstack1l1ll11_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࠤᘞ") + json.dumps(bstack11llll1l11l_opy_)
        bstack11ll1l11ll_opy_.bstack111l11lll_opy_(scripts)
        bstack11ll1l11ll_opy_.store()
        logger.debug(driver.execute_script(bstack11ll1l11ll_opy_.perform_scan))
      else:
        logger.debug(driver.execute_async_script(bstack11ll1l11ll_opy_.bstack11llll11lll_opy_, bstack1ll1l1111ll_opy_))
      bstack1lll111l_opy_.end(bstack1ll1ll11l1l_opy_, bstack1ll1ll11l1l_opy_ + bstack1l1ll11_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢᘟ"), bstack1ll1ll11l1l_opy_ + bstack1l1ll11_opy_ (u"ࠣ࠼ࡨࡲࡩࠨᘠ"),True, None)
    except Exception as error:
      bstack1lll111l_opy_.end(bstack1ll1ll11l1l_opy_, bstack1ll1ll11l1l_opy_ + bstack1l1ll11_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤᘡ"), bstack1ll1ll11l1l_opy_ + bstack1l1ll11_opy_ (u"ࠥ࠾ࡪࡴࡤࠣᘢ"),False, str(error))
    logger.info(bstack1l1ll11_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡹ࡫ࡳࡵ࡫ࡱ࡫ࠥ࡬࡯ࡳࠢࡷ࡬࡮ࡹࠠࡵࡧࡶࡸࠥࡩࡡࡴࡧࠣ࡬ࡦࡹࠠࡦࡰࡧࡩࡩ࠴ࠢᘣ"))
  except Exception as bstack1ll1l11lll1_opy_:
    logger.error(bstack1l1ll11_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡸࡥࡴࡷ࡯ࡸࡸࠦࡣࡰࡷ࡯ࡨࠥࡴ࡯ࡵࠢࡥࡩࠥࡶࡲࡰࡥࡨࡷࡸ࡫ࡤࠡࡨࡲࡶࠥࡺࡨࡦࠢࡷࡩࡸࡺࠠࡤࡣࡶࡩ࠿ࠦࠢᘤ") + str(path) + bstack1l1ll11_opy_ (u"ࠨࠠࡆࡴࡵࡳࡷࠦ࠺ࠣᘥ") + str(bstack1ll1l11lll1_opy_))
def bstack11llll1l1l1_opy_(driver):
    caps = driver.capabilities
    if caps.get(bstack1l1ll11_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪࠨᘦ")) and str(caps.get(bstack1l1ll11_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡑࡥࡲ࡫ࠢᘧ"))).lower() == bstack1l1ll11_opy_ (u"ࠤࡤࡲࡩࡸ࡯ࡪࡦࠥᘨ"):
        bstack11llll1ll11_opy_ = caps.get(bstack1l1ll11_opy_ (u"ࠥࡥࡵࡶࡩࡶ࡯࠽ࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠧᘩ")) or caps.get(bstack1l1ll11_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳࠨᘪ"))
        if bstack11llll1ll11_opy_ and int(str(bstack11llll1ll11_opy_)) < bstack11llll1lll1_opy_:
            return False
    return True