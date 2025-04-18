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
import threading
import logging
import bstack_utils.accessibility as bstack1ll11llll1_opy_
from bstack_utils.helper import bstack1lllll11_opy_
logger = logging.getLogger(__name__)
def bstack1ll1l1l11l_opy_(bstack111l1l1ll_opy_):
  return True if bstack111l1l1ll_opy_ in threading.current_thread().__dict__.keys() else False
def bstack11l1111l1_opy_(context, *args):
    tags = getattr(args[0], bstack1l1ll11_opy_ (u"࠭ࡴࡢࡩࡶࠫᙏ"), [])
    bstack1llll1l111_opy_ = bstack1ll11llll1_opy_.bstack1ll11l11_opy_(tags)
    threading.current_thread().isA11yTest = bstack1llll1l111_opy_
    try:
      bstack1l1l1lll1_opy_ = threading.current_thread().bstackSessionDriver if bstack1ll1l1l11l_opy_(bstack1l1ll11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭ᙐ")) else context.browser
      if bstack1l1l1lll1_opy_ and bstack1l1l1lll1_opy_.session_id and bstack1llll1l111_opy_ and bstack1lllll11_opy_(
              threading.current_thread(), bstack1l1ll11_opy_ (u"ࠨࡣ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧᙑ"), None):
          threading.current_thread().isA11yTest = bstack1ll11llll1_opy_.bstack11ll111l1l_opy_(bstack1l1l1lll1_opy_, bstack1llll1l111_opy_)
    except Exception as e:
       logger.debug(bstack1l1ll11_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡴࡢࡴࡷࠤࡦ࠷࠱ࡺࠢ࡬ࡲࠥࡨࡥࡩࡣࡹࡩ࠿ࠦࡻࡾࠩᙒ").format(str(e)))
def bstack11llll11l_opy_(bstack1l1l1lll1_opy_):
    if bstack1lllll11_opy_(threading.current_thread(), bstack1l1ll11_opy_ (u"ࠪ࡭ࡸࡇ࠱࠲ࡻࡗࡩࡸࡺࠧᙓ"), None) and bstack1lllll11_opy_(
      threading.current_thread(), bstack1l1ll11_opy_ (u"ࠫࡦ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪᙔ"), None) and not bstack1lllll11_opy_(threading.current_thread(), bstack1l1ll11_opy_ (u"ࠬࡧ࠱࠲ࡻࡢࡷࡹࡵࡰࠨᙕ"), False):
      threading.current_thread().a11y_stop = True
      bstack1ll11llll1_opy_.bstack1ll111111_opy_(bstack1l1l1lll1_opy_, name=bstack1l1ll11_opy_ (u"ࠨࠢᙖ"), path=bstack1l1ll11_opy_ (u"ࠢࠣᙗ"))