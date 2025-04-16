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
import threading
import logging
import bstack_utils.accessibility as bstack1l1l11l11_opy_
from bstack_utils.helper import bstack1l1l11l1l_opy_
logger = logging.getLogger(__name__)
def bstack11lllll1ll_opy_(bstack11l111ll_opy_):
  return True if bstack11l111ll_opy_ in threading.current_thread().__dict__.keys() else False
def bstack111l1llll_opy_(context, *args):
    tags = getattr(args[0], bstack1l1_opy_ (u"ࠬࡺࡡࡨࡵࠪᙎ"), [])
    bstack1lll11111l_opy_ = bstack1l1l11l11_opy_.bstack1l1ll1l1_opy_(tags)
    threading.current_thread().isA11yTest = bstack1lll11111l_opy_
    try:
      bstack1l1lll11l_opy_ = threading.current_thread().bstackSessionDriver if bstack11lllll1ll_opy_(bstack1l1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬᙏ")) else context.browser
      if bstack1l1lll11l_opy_ and bstack1l1lll11l_opy_.session_id and bstack1lll11111l_opy_ and bstack1l1l11l1l_opy_(
              threading.current_thread(), bstack1l1_opy_ (u"ࠧࡢ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭ᙐ"), None):
          threading.current_thread().isA11yTest = bstack1l1l11l11_opy_.bstack1llll111_opy_(bstack1l1lll11l_opy_, bstack1lll11111l_opy_)
    except Exception as e:
       logger.debug(bstack1l1_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸࡺࡡࡳࡶࠣࡥ࠶࠷ࡹࠡ࡫ࡱࠤࡧ࡫ࡨࡢࡸࡨ࠾ࠥࢁࡽࠨᙑ").format(str(e)))
def bstack11lll111l_opy_(bstack1l1lll11l_opy_):
    if bstack1l1l11l1l_opy_(threading.current_thread(), bstack1l1_opy_ (u"ࠩ࡬ࡷࡆ࠷࠱ࡺࡖࡨࡷࡹ࠭ᙒ"), None) and bstack1l1l11l1l_opy_(
      threading.current_thread(), bstack1l1_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩᙓ"), None) and not bstack1l1l11l1l_opy_(threading.current_thread(), bstack1l1_opy_ (u"ࠫࡦ࠷࠱ࡺࡡࡶࡸࡴࡶࠧᙔ"), False):
      threading.current_thread().a11y_stop = True
      bstack1l1l11l11_opy_.bstack1l1l1ll111_opy_(bstack1l1lll11l_opy_, name=bstack1l1_opy_ (u"ࠧࠨᙕ"), path=bstack1l1_opy_ (u"ࠨࠢᙖ"))