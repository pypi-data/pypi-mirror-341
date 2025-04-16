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
import traceback
from typing import Dict, Tuple, Callable, Type, List, Any
from urllib.parse import urlparse
from browserstack_sdk.sdk_cli.bstack11111111l1_opy_ import (
    bstack11111lll1l_opy_,
    bstack1111111l1l_opy_,
    bstack11111ll1ll_opy_,
    bstack1llllllll1l_opy_,
)
import copy
from datetime import datetime, timezone, timedelta
class bstack1llll1l11ll_opy_(bstack11111lll1l_opy_):
    bstack1l1l1111111_opy_ = bstack1l1_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠢፇ")
    bstack1l1ll11lll1_opy_ = bstack1l1_opy_ (u"ࠣࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡯ࡤࠣፈ")
    bstack1l1ll111ll1_opy_ = bstack1l1_opy_ (u"ࠤ࡫ࡹࡧࡥࡵࡳ࡮ࠥፉ")
    bstack1l1ll11llll_opy_ = bstack1l1_opy_ (u"ࠥࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠤፊ")
    bstack1l1l11111l1_opy_ = bstack1l1_opy_ (u"ࠦࡼ࠹ࡣࡦࡺࡨࡧࡺࡺࡥࡴࡥࡵ࡭ࡵࡺࠢፋ")
    bstack1l1l111111l_opy_ = bstack1l1_opy_ (u"ࠧࡽ࠳ࡤࡧࡻࡩࡨࡻࡴࡦࡵࡦࡶ࡮ࡶࡴࡢࡵࡼࡲࡨࠨፌ")
    NAME = bstack1l1_opy_ (u"ࠨࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠥፍ")
    bstack1l1l11111ll_opy_: Dict[str, List[Callable]] = dict()
    platform_index: int
    options: Any
    desired_capabilities: Any
    bstack1lll1l1l1ll_opy_: Any
    bstack1l11lllll1l_opy_: Dict
    def __init__(
        self,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        classes: List[Type],
        methods=[bstack1l1_opy_ (u"ࠢ࡭ࡣࡸࡲࡨ࡮ࠢፎ"), bstack1l1_opy_ (u"ࠣࡥࡲࡲࡳ࡫ࡣࡵࠤፏ"), bstack1l1_opy_ (u"ࠤࡱࡩࡼࡥࡰࡢࡩࡨࠦፐ"), bstack1l1_opy_ (u"ࠥࡧࡱࡵࡳࡦࠤፑ"), bstack1l1_opy_ (u"ࠦࡩ࡯ࡳࡱࡣࡷࡧ࡭ࠨፒ")],
    ):
        super().__init__(
            framework_name,
            framework_version,
            classes,
        )
        self.platform_index = platform_index
        self.bstack1111l11l1l_opy_(methods)
    def bstack11111lll11_opy_(self, instance: bstack1111111l1l_opy_, method_name: str, bstack111111ll1l_opy_: timedelta, *args, **kwargs):
        pass
    def bstack11111l1l11_opy_(
        self,
        target: object,
        exec: Tuple[bstack1111111l1l_opy_, str],
        bstack111111l11l_opy_: Tuple[bstack11111ll1ll_opy_, bstack1llllllll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable[..., Any]:
        instance, method_name = exec
        bstack11111l11l1_opy_, bstack1l11lllll11_opy_ = bstack111111l11l_opy_
        bstack1l1l1111l11_opy_ = bstack1llll1l11ll_opy_.bstack1l11llllll1_opy_(bstack111111l11l_opy_)
        if bstack1l1l1111l11_opy_ in bstack1llll1l11ll_opy_.bstack1l1l11111ll_opy_:
            bstack1l1l1111l1l_opy_ = None
            for callback in bstack1llll1l11ll_opy_.bstack1l1l11111ll_opy_[bstack1l1l1111l11_opy_]:
                try:
                    bstack1l11lllllll_opy_ = callback(self, target, exec, bstack111111l11l_opy_, result, *args, **kwargs)
                    if bstack1l1l1111l1l_opy_ == None:
                        bstack1l1l1111l1l_opy_ = bstack1l11lllllll_opy_
                except Exception as e:
                    self.logger.error(bstack1l1_opy_ (u"ࠧ࡫ࡲࡳࡱࡵࠤ࡮ࡴࡶࡰ࡭࡬ࡲ࡬ࠦࡣࡢ࡮࡯ࡦࡦࡩ࡫࠻ࠢࠥፓ") + str(e) + bstack1l1_opy_ (u"ࠨࠢፔ"))
                    traceback.print_exc()
            if bstack1l11lllll11_opy_ == bstack1llllllll1l_opy_.PRE and callable(bstack1l1l1111l1l_opy_):
                return bstack1l1l1111l1l_opy_
            elif bstack1l11lllll11_opy_ == bstack1llllllll1l_opy_.POST and bstack1l1l1111l1l_opy_:
                return bstack1l1l1111l1l_opy_
    def bstack1111l111l1_opy_(
        self, method_name, previous_state: bstack11111ll1ll_opy_, *args, **kwargs
    ) -> bstack11111ll1ll_opy_:
        if method_name == bstack1l1_opy_ (u"ࠧ࡭ࡣࡸࡲࡨ࡮ࠧፕ") or method_name == bstack1l1_opy_ (u"ࠨࡥࡲࡲࡳ࡫ࡣࡵࠩፖ") or method_name == bstack1l1_opy_ (u"ࠩࡱࡩࡼࡥࡰࡢࡩࡨࠫፗ"):
            return bstack11111ll1ll_opy_.bstack11111l111l_opy_
        if method_name == bstack1l1_opy_ (u"ࠪࡨ࡮ࡹࡰࡢࡶࡦ࡬ࠬፘ"):
            return bstack11111ll1ll_opy_.bstack11111l1111_opy_
        if method_name == bstack1l1_opy_ (u"ࠫࡨࡲ࡯ࡴࡧࠪፙ"):
            return bstack11111ll1ll_opy_.QUIT
        return bstack11111ll1ll_opy_.NONE
    @staticmethod
    def bstack1l11llllll1_opy_(bstack111111l11l_opy_: Tuple[bstack11111ll1ll_opy_, bstack1llllllll1l_opy_]):
        return bstack1l1_opy_ (u"ࠧࡀࠢፚ").join((bstack11111ll1ll_opy_(bstack111111l11l_opy_[0]).name, bstack1llllllll1l_opy_(bstack111111l11l_opy_[1]).name))
    @staticmethod
    def bstack1ll1l1ll11l_opy_(bstack111111l11l_opy_: Tuple[bstack11111ll1ll_opy_, bstack1llllllll1l_opy_], callback: Callable):
        bstack1l1l1111l11_opy_ = bstack1llll1l11ll_opy_.bstack1l11llllll1_opy_(bstack111111l11l_opy_)
        if not bstack1l1l1111l11_opy_ in bstack1llll1l11ll_opy_.bstack1l1l11111ll_opy_:
            bstack1llll1l11ll_opy_.bstack1l1l11111ll_opy_[bstack1l1l1111l11_opy_] = []
        bstack1llll1l11ll_opy_.bstack1l1l11111ll_opy_[bstack1l1l1111l11_opy_].append(callback)
    @staticmethod
    def bstack1ll1ll1lll1_opy_(method_name: str):
        return True
    @staticmethod
    def bstack1ll1l11111l_opy_(method_name: str, *args) -> bool:
        return True
    @staticmethod
    def bstack1ll1ll1l1l1_opy_(instance: bstack1111111l1l_opy_, default_value=None):
        return bstack11111lll1l_opy_.bstack1111l11lll_opy_(instance, bstack1llll1l11ll_opy_.bstack1l1ll11llll_opy_, default_value)
    @staticmethod
    def bstack1ll1l1l1l1l_opy_(instance: bstack1111111l1l_opy_) -> bool:
        return True
    @staticmethod
    def bstack1ll1l1lll1l_opy_(instance: bstack1111111l1l_opy_, default_value=None):
        return bstack11111lll1l_opy_.bstack1111l11lll_opy_(instance, bstack1llll1l11ll_opy_.bstack1l1ll111ll1_opy_, default_value)
    @staticmethod
    def bstack1ll1ll111l1_opy_(*args):
        return args[0] if args and type(args) in [list, tuple] and isinstance(args[0], str) else None
    @staticmethod
    def bstack1ll1l111111_opy_(method_name: str, *args):
        if not bstack1llll1l11ll_opy_.bstack1ll1ll1lll1_opy_(method_name):
            return False
        if not bstack1llll1l11ll_opy_.bstack1l1l11111l1_opy_ in bstack1llll1l11ll_opy_.bstack1l1l1l1l111_opy_(*args):
            return False
        bstack1ll11ll1ll1_opy_ = bstack1llll1l11ll_opy_.bstack1ll11ll1l11_opy_(*args)
        return bstack1ll11ll1ll1_opy_ and bstack1l1_opy_ (u"ࠨࡳࡤࡴ࡬ࡴࡹࠨ፛") in bstack1ll11ll1ll1_opy_ and bstack1l1_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲࠣ፜") in bstack1ll11ll1ll1_opy_[bstack1l1_opy_ (u"ࠣࡵࡦࡶ࡮ࡶࡴࠣ፝")]
    @staticmethod
    def bstack1ll11llllll_opy_(method_name: str, *args):
        if not bstack1llll1l11ll_opy_.bstack1ll1ll1lll1_opy_(method_name):
            return False
        if not bstack1llll1l11ll_opy_.bstack1l1l11111l1_opy_ in bstack1llll1l11ll_opy_.bstack1l1l1l1l111_opy_(*args):
            return False
        bstack1ll11ll1ll1_opy_ = bstack1llll1l11ll_opy_.bstack1ll11ll1l11_opy_(*args)
        return (
            bstack1ll11ll1ll1_opy_
            and bstack1l1_opy_ (u"ࠤࡶࡧࡷ࡯ࡰࡵࠤ፞") in bstack1ll11ll1ll1_opy_
            and bstack1l1_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡡࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡥࡳࡤࡴ࡬ࡴࡹࠨ፟") in bstack1ll11ll1ll1_opy_[bstack1l1_opy_ (u"ࠦࡸࡩࡲࡪࡲࡷࠦ፠")]
        )
    @staticmethod
    def bstack1l1l1l1l111_opy_(*args):
        return str(bstack1llll1l11ll_opy_.bstack1ll1ll111l1_opy_(*args)).lower()