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
import threading
from bstack_utils.helper import bstack11111ll1l_opy_
from bstack_utils.constants import bstack11ll1llllll_opy_, EVENTS, STAGE
from bstack_utils.bstack111l1l111_opy_ import get_logger
logger = get_logger(__name__)
class bstack1l1llll11_opy_:
    bstack111l11lll1l_opy_ = None
    @classmethod
    def bstack1llll1l1_opy_(cls):
        if cls.on() and os.getenv(bstack1l1ll11_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠢἠ")):
            logger.info(
                bstack1l1ll11_opy_ (u"࡚ࠪ࡮ࡹࡩࡵࠢ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡢࡶ࡫࡯ࡨࡸ࠵ࡻࡾࠢࡷࡳࠥࡼࡩࡦࡹࠣࡦࡺ࡯࡬ࡥࠢࡵࡩࡵࡵࡲࡵ࠮ࠣ࡭ࡳࡹࡩࡨࡪࡷࡷ࠱ࠦࡡ࡯ࡦࠣࡱࡦࡴࡹࠡ࡯ࡲࡶࡪࠦࡤࡦࡤࡸ࡫࡬࡯࡮ࡨࠢ࡬ࡲ࡫ࡵࡲ࡮ࡣࡷ࡭ࡴࡴࠠࡢ࡮࡯ࠤࡦࡺࠠࡰࡰࡨࠤࡵࡲࡡࡤࡧࠤࡠࡳ࠭ἡ").format(os.getenv(bstack1l1ll11_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠤἢ"))))
    @classmethod
    def on(cls):
        if os.environ.get(bstack1l1ll11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩἣ"), None) is None or os.environ[bstack1l1ll11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪἤ")] == bstack1l1ll11_opy_ (u"ࠢ࡯ࡷ࡯ࡰࠧἥ"):
            return False
        return True
    @classmethod
    def bstack1111l1ll111_opy_(cls, bs_config, framework=bstack1l1ll11_opy_ (u"ࠣࠤἦ")):
        bstack11lll111ll1_opy_ = False
        for fw in bstack11ll1llllll_opy_:
            if fw in framework:
                bstack11lll111ll1_opy_ = True
        return bstack11111ll1l_opy_(bs_config.get(bstack1l1ll11_opy_ (u"ࠩࡷࡩࡸࡺࡏࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭ἧ"), bstack11lll111ll1_opy_))
    @classmethod
    def bstack1111l1l11ll_opy_(cls, framework):
        return framework in bstack11ll1llllll_opy_
    @classmethod
    def bstack1111lll1l11_opy_(cls, bs_config, framework):
        return cls.bstack1111l1ll111_opy_(bs_config, framework) is True and cls.bstack1111l1l11ll_opy_(framework)
    @staticmethod
    def current_hook_uuid():
        return getattr(threading.current_thread(), bstack1l1ll11_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧἨ"), None)
    @staticmethod
    def bstack11l11l11l1_opy_():
        if getattr(threading.current_thread(), bstack1l1ll11_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨἩ"), None):
            return {
                bstack1l1ll11_opy_ (u"ࠬࡺࡹࡱࡧࠪἪ"): bstack1l1ll11_opy_ (u"࠭ࡴࡦࡵࡷࠫἫ"),
                bstack1l1ll11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧἬ"): getattr(threading.current_thread(), bstack1l1ll11_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬἭ"), None)
            }
        if getattr(threading.current_thread(), bstack1l1ll11_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭Ἦ"), None):
            return {
                bstack1l1ll11_opy_ (u"ࠪࡸࡾࡶࡥࠨἯ"): bstack1l1ll11_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩἰ"),
                bstack1l1ll11_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬἱ"): getattr(threading.current_thread(), bstack1l1ll11_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪἲ"), None)
            }
        return None
    @staticmethod
    def bstack1111l1l11l1_opy_(func):
        def wrap(*args, **kwargs):
            if bstack1l1llll11_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def bstack111lll11ll_opy_(test, hook_name=None):
        bstack1111l1l1111_opy_ = test.parent
        if hook_name in [bstack1l1ll11_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥࡣ࡭ࡣࡶࡷࠬἳ"), bstack1l1ll11_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡧࡱࡧࡳࡴࠩἴ"), bstack1l1ll11_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠ࡯ࡲࡨࡺࡲࡥࠨἵ"), bstack1l1ll11_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳ࡯ࡥࡷ࡯ࡩࠬἶ")]:
            bstack1111l1l1111_opy_ = test
        scope = []
        while bstack1111l1l1111_opy_ is not None:
            scope.append(bstack1111l1l1111_opy_.name)
            bstack1111l1l1111_opy_ = bstack1111l1l1111_opy_.parent
        scope.reverse()
        return scope[2:]
    @staticmethod
    def bstack1111l1l111l_opy_(hook_type):
        if hook_type == bstack1l1ll11_opy_ (u"ࠦࡇࡋࡆࡐࡔࡈࡣࡊࡇࡃࡉࠤἷ"):
            return bstack1l1ll11_opy_ (u"࡙ࠧࡥࡵࡷࡳࠤ࡭ࡵ࡯࡬ࠤἸ")
        elif hook_type == bstack1l1ll11_opy_ (u"ࠨࡁࡇࡖࡈࡖࡤࡋࡁࡄࡊࠥἹ"):
            return bstack1l1ll11_opy_ (u"ࠢࡕࡧࡤࡶࡩࡵࡷ࡯ࠢ࡫ࡳࡴࡱࠢἺ")
    @staticmethod
    def bstack1111l11llll_opy_(bstack1l1l1l1l_opy_):
        try:
            if not bstack1l1llll11_opy_.on():
                return bstack1l1l1l1l_opy_
            if os.environ.get(bstack1l1ll11_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡓࡇࡕ࡙ࡓࠨἻ"), None) == bstack1l1ll11_opy_ (u"ࠤࡷࡶࡺ࡫ࠢἼ"):
                tests = os.environ.get(bstack1l1ll11_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡕࡉࡗ࡛ࡎࡠࡖࡈࡗ࡙࡙ࠢἽ"), None)
                if tests is None or tests == bstack1l1ll11_opy_ (u"ࠦࡳࡻ࡬࡭ࠤἾ"):
                    return bstack1l1l1l1l_opy_
                bstack1l1l1l1l_opy_ = tests.split(bstack1l1ll11_opy_ (u"ࠬ࠲ࠧἿ"))
                return bstack1l1l1l1l_opy_
        except Exception as exc:
            logger.debug(bstack1l1ll11_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡸࡥࡳࡷࡱࠤ࡭ࡧ࡮ࡥ࡮ࡨࡶ࠿ࠦࠢὀ") + str(str(exc)) + bstack1l1ll11_opy_ (u"ࠢࠣὁ"))
        return bstack1l1l1l1l_opy_