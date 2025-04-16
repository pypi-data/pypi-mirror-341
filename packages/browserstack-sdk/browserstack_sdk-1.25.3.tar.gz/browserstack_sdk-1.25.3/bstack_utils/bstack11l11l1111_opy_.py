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
import threading
from bstack_utils.helper import bstack111llll11_opy_
from bstack_utils.constants import bstack11lll111111_opy_, EVENTS, STAGE
from bstack_utils.bstack1l11l11lll_opy_ import get_logger
logger = get_logger(__name__)
class bstack11llll111l_opy_:
    bstack111l1l111ll_opy_ = None
    @classmethod
    def bstack1lllll11l1_opy_(cls):
        if cls.on() and os.getenv(bstack1l1_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉࠨ἟")):
            logger.info(
                bstack1l1_opy_ (u"࡙ࠩ࡭ࡸ࡯ࡴࠡࡪࡷࡸࡵࡹ࠺࠰࠱ࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡨࡵࡪ࡮ࡧࡷ࠴ࢁࡽࠡࡶࡲࠤࡻ࡯ࡥࡸࠢࡥࡹ࡮ࡲࡤࠡࡴࡨࡴࡴࡸࡴ࠭ࠢ࡬ࡲࡸ࡯ࡧࡩࡶࡶ࠰ࠥࡧ࡮ࡥࠢࡰࡥࡳࡿࠠ࡮ࡱࡵࡩࠥࡪࡥࡣࡷࡪ࡫࡮ࡴࡧࠡ࡫ࡱࡪࡴࡸ࡭ࡢࡶ࡬ࡳࡳࠦࡡ࡭࡮ࠣࡥࡹࠦ࡯࡯ࡧࠣࡴࡱࡧࡣࡦࠣ࡟ࡲࠬἠ").format(os.getenv(bstack1l1_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠣἡ"))))
    @classmethod
    def on(cls):
        if os.environ.get(bstack1l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨἢ"), None) is None or os.environ[bstack1l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩἣ")] == bstack1l1_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦἤ"):
            return False
        return True
    @classmethod
    def bstack1111l1ll1ll_opy_(cls, bs_config, framework=bstack1l1_opy_ (u"ࠢࠣἥ")):
        bstack11lll111lll_opy_ = False
        for fw in bstack11lll111111_opy_:
            if fw in framework:
                bstack11lll111lll_opy_ = True
        return bstack111llll11_opy_(bs_config.get(bstack1l1_opy_ (u"ࠨࡶࡨࡷࡹࡕࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬἦ"), bstack11lll111lll_opy_))
    @classmethod
    def bstack1111l1l11l1_opy_(cls, framework):
        return framework in bstack11lll111111_opy_
    @classmethod
    def bstack1111ll1lll1_opy_(cls, bs_config, framework):
        return cls.bstack1111l1ll1ll_opy_(bs_config, framework) is True and cls.bstack1111l1l11l1_opy_(framework)
    @staticmethod
    def current_hook_uuid():
        return getattr(threading.current_thread(), bstack1l1_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭ἧ"), None)
    @staticmethod
    def bstack11l1111l11_opy_():
        if getattr(threading.current_thread(), bstack1l1_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧἨ"), None):
            return {
                bstack1l1_opy_ (u"ࠫࡹࡿࡰࡦࠩἩ"): bstack1l1_opy_ (u"ࠬࡺࡥࡴࡶࠪἪ"),
                bstack1l1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭Ἣ"): getattr(threading.current_thread(), bstack1l1_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫἬ"), None)
            }
        if getattr(threading.current_thread(), bstack1l1_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬἭ"), None):
            return {
                bstack1l1_opy_ (u"ࠩࡷࡽࡵ࡫ࠧἮ"): bstack1l1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࠨἯ"),
                bstack1l1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫἰ"): getattr(threading.current_thread(), bstack1l1_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩἱ"), None)
            }
        return None
    @staticmethod
    def bstack1111l1l1111_opy_(func):
        def wrap(*args, **kwargs):
            if bstack11llll111l_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def bstack111lll11ll_opy_(test, hook_name=None):
        bstack1111l11llll_opy_ = test.parent
        if hook_name in [bstack1l1_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡩ࡬ࡢࡵࡶࠫἲ"), bstack1l1_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡦࡰࡦࡹࡳࠨἳ"), bstack1l1_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟࡮ࡱࡧࡹࡱ࡫ࠧἴ"), bstack1l1_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲࡵࡤࡶ࡮ࡨࠫἵ")]:
            bstack1111l11llll_opy_ = test
        scope = []
        while bstack1111l11llll_opy_ is not None:
            scope.append(bstack1111l11llll_opy_.name)
            bstack1111l11llll_opy_ = bstack1111l11llll_opy_.parent
        scope.reverse()
        return scope[2:]
    @staticmethod
    def bstack1111l1l11ll_opy_(hook_type):
        if hook_type == bstack1l1_opy_ (u"ࠥࡆࡊࡌࡏࡓࡇࡢࡉࡆࡉࡈࠣἶ"):
            return bstack1l1_opy_ (u"ࠦࡘ࡫ࡴࡶࡲࠣ࡬ࡴࡵ࡫ࠣἷ")
        elif hook_type == bstack1l1_opy_ (u"ࠧࡇࡆࡕࡇࡕࡣࡊࡇࡃࡉࠤἸ"):
            return bstack1l1_opy_ (u"ࠨࡔࡦࡣࡵࡨࡴࡽ࡮ࠡࡪࡲࡳࡰࠨἹ")
    @staticmethod
    def bstack1111l1l111l_opy_(bstack11l1ll11l1_opy_):
        try:
            if not bstack11llll111l_opy_.on():
                return bstack11l1ll11l1_opy_
            if os.environ.get(bstack1l1_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡒࡆࡔࡘࡒࠧἺ"), None) == bstack1l1_opy_ (u"ࠣࡶࡵࡹࡪࠨἻ"):
                tests = os.environ.get(bstack1l1_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡔࡈࡖ࡚ࡔ࡟ࡕࡇࡖࡘࡘࠨἼ"), None)
                if tests is None or tests == bstack1l1_opy_ (u"ࠥࡲࡺࡲ࡬ࠣἽ"):
                    return bstack11l1ll11l1_opy_
                bstack11l1ll11l1_opy_ = tests.split(bstack1l1_opy_ (u"ࠫ࠱࠭Ἶ"))
                return bstack11l1ll11l1_opy_
        except Exception as exc:
            logger.debug(bstack1l1_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡷ࡫ࡲࡶࡰࠣ࡬ࡦࡴࡤ࡭ࡧࡵ࠾ࠥࠨἿ") + str(str(exc)) + bstack1l1_opy_ (u"ࠨࠢὀ"))
        return bstack11l1ll11l1_opy_