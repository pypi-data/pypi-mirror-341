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
import traceback
from typing import Dict, Tuple, Callable, Type, List, Any
from urllib.parse import urlparse
from browserstack_sdk.sdk_cli.bstack11111l1ll1_opy_ import (
    bstack1111l11111_opy_,
    bstack11111l1l1l_opy_,
    bstack111111ll1l_opy_,
    bstack111111l11l_opy_,
)
import copy
from datetime import datetime, timezone, timedelta
from bstack_utils.bstack1lll111l_opy_ import bstack1ll1llllll1_opy_
from bstack_utils.constants import EVENTS
class bstack1llllll1l11_opy_(bstack1111l11111_opy_):
    bstack1l1l1111111_opy_ = bstack1l1ll11_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠦᒰ")
    NAME = bstack1l1ll11_opy_ (u"ࠧࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠢᒱ")
    bstack1l1ll1111l1_opy_ = bstack1l1ll11_opy_ (u"ࠨࡨࡶࡤࡢࡹࡷࡲࠢᒲ")
    bstack1l1ll11lll1_opy_ = bstack1l1ll11_opy_ (u"ࠢࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡪࡹࡳࡪࡱࡱࡣ࡮ࡪࠢᒳ")
    bstack1l1111lll1l_opy_ = bstack1l1ll11_opy_ (u"ࠣ࡫ࡱࡴࡺࡺ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠨᒴ")
    bstack1l1ll1l1111_opy_ = bstack1l1ll11_opy_ (u"ࠤࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠣᒵ")
    bstack1l1l1111lll_opy_ = bstack1l1ll11_opy_ (u"ࠥ࡭ࡸࡥࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡮ࡵࡣࠤᒶ")
    bstack1l111l111ll_opy_ = bstack1l1ll11_opy_ (u"ࠦࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠣᒷ")
    bstack1l111l1111l_opy_ = bstack1l1ll11_opy_ (u"ࠧ࡫࡮ࡥࡧࡧࡣࡦࡺࠢᒸ")
    bstack1ll11lllll1_opy_ = bstack1l1ll11_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡠ࡫ࡱࡨࡪࡾࠢᒹ")
    bstack1l1l11lll1l_opy_ = bstack1l1ll11_opy_ (u"ࠢ࡯ࡧࡺࡷࡪࡹࡳࡪࡱࡱࠦᒺ")
    bstack1l1111llll1_opy_ = bstack1l1ll11_opy_ (u"ࠣࡩࡨࡸࠧᒻ")
    bstack1ll111l11ll_opy_ = bstack1l1ll11_opy_ (u"ࠤࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࠨᒼ")
    bstack1l11lllllll_opy_ = bstack1l1ll11_opy_ (u"ࠥࡻ࠸ࡩࡥࡹࡧࡦࡹࡹ࡫ࡳࡤࡴ࡬ࡴࡹࠨᒽ")
    bstack1l1l11111ll_opy_ = bstack1l1ll11_opy_ (u"ࠦࡼ࠹ࡣࡦࡺࡨࡧࡺࡺࡥࡴࡥࡵ࡭ࡵࡺࡡࡴࡻࡱࡧࠧᒾ")
    bstack1l1111ll1ll_opy_ = bstack1l1ll11_opy_ (u"ࠧࡷࡵࡪࡶࠥᒿ")
    bstack1l1111ll1l1_opy_: Dict[str, List[Callable]] = dict()
    bstack1l1l11l11l1_opy_: str
    platform_index: int
    options: Any
    desired_capabilities: Any
    bstack1llll1ll1l1_opy_: Any
    bstack1l11lllll11_opy_: Dict
    def __init__(
        self,
        bstack1l1l11l11l1_opy_: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        classes: List[Type],
        bstack1llll1ll1l1_opy_: Dict[str, Any],
        methods=[bstack1l1ll11_opy_ (u"ࠨ࡟ࡠ࡫ࡱ࡭ࡹࡥ࡟ࠣᓀ"), bstack1l1ll11_opy_ (u"ࠢࡴࡶࡤࡶࡹࡥࡳࡦࡵࡶ࡭ࡴࡴࠢᓁ"), bstack1l1ll11_opy_ (u"ࠣࡧࡻࡩࡨࡻࡴࡦࠤᓂ"), bstack1l1ll11_opy_ (u"ࠤࡴࡹ࡮ࡺࠢᓃ")],
    ):
        super().__init__(
            framework_name,
            framework_version,
            classes,
        )
        self.bstack1l1l11l11l1_opy_ = bstack1l1l11l11l1_opy_
        self.platform_index = platform_index
        self.bstack1111l111l1_opy_(methods)
        self.bstack1llll1ll1l1_opy_ = bstack1llll1ll1l1_opy_
    @staticmethod
    def session_id(target: object, strict=True):
        return bstack1111l11111_opy_.get_data(bstack1llllll1l11_opy_.bstack1l1ll11lll1_opy_, target, strict)
    @staticmethod
    def hub_url(target: object, strict=True):
        return bstack1111l11111_opy_.get_data(bstack1llllll1l11_opy_.bstack1l1ll1111l1_opy_, target, strict)
    @staticmethod
    def bstack1l1111lll11_opy_(target: object, strict=True):
        return bstack1111l11111_opy_.get_data(bstack1llllll1l11_opy_.bstack1l1111lll1l_opy_, target, strict)
    @staticmethod
    def capabilities(target: object, strict=True):
        return bstack1111l11111_opy_.get_data(bstack1llllll1l11_opy_.bstack1l1ll1l1111_opy_, target, strict)
    @staticmethod
    def bstack1ll1l11l1ll_opy_(instance: bstack11111l1l1l_opy_) -> bool:
        return bstack1111l11111_opy_.bstack111111ll11_opy_(instance, bstack1llllll1l11_opy_.bstack1l1l1111lll_opy_, False)
    @staticmethod
    def bstack1ll1l11l11l_opy_(instance: bstack11111l1l1l_opy_, default_value=None):
        return bstack1111l11111_opy_.bstack111111ll11_opy_(instance, bstack1llllll1l11_opy_.bstack1l1ll1111l1_opy_, default_value)
    @staticmethod
    def bstack1ll1ll11ll1_opy_(instance: bstack11111l1l1l_opy_, default_value=None):
        return bstack1111l11111_opy_.bstack111111ll11_opy_(instance, bstack1llllll1l11_opy_.bstack1l1ll1l1111_opy_, default_value)
    @staticmethod
    def bstack1ll11ll1ll1_opy_(hub_url: str, bstack1l111l111l1_opy_=bstack1l1ll11_opy_ (u"ࠥ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳࠢᓄ")):
        try:
            bstack1l111l11111_opy_ = str(urlparse(hub_url).netloc) if hub_url else None
            return bstack1l111l11111_opy_.endswith(bstack1l111l111l1_opy_)
        except:
            pass
        return False
    @staticmethod
    def bstack1ll1l11ll1l_opy_(method_name: str):
        return method_name == bstack1l1ll11_opy_ (u"ࠦࡪࡾࡥࡤࡷࡷࡩࠧᓅ")
    @staticmethod
    def bstack1ll1ll111l1_opy_(method_name: str, *args):
        return (
            bstack1llllll1l11_opy_.bstack1ll1l11ll1l_opy_(method_name)
            and bstack1llllll1l11_opy_.bstack1l1l11ll11l_opy_(*args) == bstack1llllll1l11_opy_.bstack1l1l11lll1l_opy_
        )
    @staticmethod
    def bstack1ll1l11ll11_opy_(method_name: str, *args):
        if not bstack1llllll1l11_opy_.bstack1ll1l11ll1l_opy_(method_name):
            return False
        if not bstack1llllll1l11_opy_.bstack1l11lllllll_opy_ in bstack1llllll1l11_opy_.bstack1l1l11ll11l_opy_(*args):
            return False
        bstack1ll11ll1111_opy_ = bstack1llllll1l11_opy_.bstack1ll11lll111_opy_(*args)
        return bstack1ll11ll1111_opy_ and bstack1l1ll11_opy_ (u"ࠧࡹࡣࡳ࡫ࡳࡸࠧᓆ") in bstack1ll11ll1111_opy_ and bstack1l1ll11_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸࠢᓇ") in bstack1ll11ll1111_opy_[bstack1l1ll11_opy_ (u"ࠢࡴࡥࡵ࡭ࡵࡺࠢᓈ")]
    @staticmethod
    def bstack1ll1ll1llll_opy_(method_name: str, *args):
        if not bstack1llllll1l11_opy_.bstack1ll1l11ll1l_opy_(method_name):
            return False
        if not bstack1llllll1l11_opy_.bstack1l11lllllll_opy_ in bstack1llllll1l11_opy_.bstack1l1l11ll11l_opy_(*args):
            return False
        bstack1ll11ll1111_opy_ = bstack1llllll1l11_opy_.bstack1ll11lll111_opy_(*args)
        return (
            bstack1ll11ll1111_opy_
            and bstack1l1ll11_opy_ (u"ࠣࡵࡦࡶ࡮ࡶࡴࠣᓉ") in bstack1ll11ll1111_opy_
            and bstack1l1ll11_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡠࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡤࡹࡣࡳ࡫ࡳࡸࠧᓊ") in bstack1ll11ll1111_opy_[bstack1l1ll11_opy_ (u"ࠥࡷࡨࡸࡩࡱࡶࠥᓋ")]
        )
    @staticmethod
    def bstack1l1l11ll11l_opy_(*args):
        return str(bstack1llllll1l11_opy_.bstack1ll1l1l1111_opy_(*args)).lower()
    @staticmethod
    def bstack1ll1l1l1111_opy_(*args):
        return args[0] if args and type(args) in [list, tuple] and isinstance(args[0], str) else None
    @staticmethod
    def bstack1ll11lll111_opy_(*args):
        return args[1] if len(args) > 1 and isinstance(args[1], dict) else None
    @staticmethod
    def bstack11l1lll11_opy_(driver):
        command_executor = getattr(driver, bstack1l1ll11_opy_ (u"ࠦࡨࡵ࡭࡮ࡣࡱࡨࡤ࡫ࡸࡦࡥࡸࡸࡴࡸࠢᓌ"), None)
        if not command_executor:
            return None
        hub_url = str(command_executor) if isinstance(command_executor, (str, bytes)) else None
        hub_url = str(command_executor._url) if not hub_url and getattr(command_executor, bstack1l1ll11_opy_ (u"ࠧࡥࡵࡳ࡮ࠥᓍ"), None) else None
        if not hub_url:
            client_config = getattr(command_executor, bstack1l1ll11_opy_ (u"ࠨ࡟ࡤ࡮࡬ࡩࡳࡺ࡟ࡤࡱࡱࡪ࡮࡭ࠢᓎ"), None)
            if not client_config:
                return None
            hub_url = getattr(client_config, bstack1l1ll11_opy_ (u"ࠢࡳࡧࡰࡳࡹ࡫࡟ࡴࡧࡵࡺࡪࡸ࡟ࡢࡦࡧࡶࠧᓏ"), None)
        return hub_url
    def bstack1l1l11llll1_opy_(self, instance, driver, hub_url: str):
        result = False
        if not hub_url:
            return result
        command_executor = getattr(driver, bstack1l1ll11_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࡡࡨࡼࡪࡩࡵࡵࡱࡵࠦᓐ"), None)
        if command_executor:
            if isinstance(command_executor, (str, bytes)):
                setattr(driver, bstack1l1ll11_opy_ (u"ࠤࡦࡳࡲࡳࡡ࡯ࡦࡢࡩࡽ࡫ࡣࡶࡶࡲࡶࠧᓑ"), hub_url)
                result = True
            elif hasattr(command_executor, bstack1l1ll11_opy_ (u"ࠥࡣࡺࡸ࡬ࠣᓒ")):
                setattr(command_executor, bstack1l1ll11_opy_ (u"ࠦࡤࡻࡲ࡭ࠤᓓ"), hub_url)
                result = True
        if result:
            self.bstack1l1l11l11l1_opy_ = hub_url
            bstack1llllll1l11_opy_.bstack111111l1l1_opy_(instance, bstack1llllll1l11_opy_.bstack1l1ll1111l1_opy_, hub_url)
            bstack1llllll1l11_opy_.bstack111111l1l1_opy_(
                instance, bstack1llllll1l11_opy_.bstack1l1l1111lll_opy_, bstack1llllll1l11_opy_.bstack1ll11ll1ll1_opy_(hub_url)
            )
        return result
    @staticmethod
    def bstack1l1l1111l11_opy_(bstack11111l11ll_opy_: Tuple[bstack111111ll1l_opy_, bstack111111l11l_opy_]):
        return bstack1l1ll11_opy_ (u"ࠧࡀࠢᓔ").join((bstack111111ll1l_opy_(bstack11111l11ll_opy_[0]).name, bstack111111l11l_opy_(bstack11111l11ll_opy_[1]).name))
    @staticmethod
    def bstack1ll1l1ll1l1_opy_(bstack11111l11ll_opy_: Tuple[bstack111111ll1l_opy_, bstack111111l11l_opy_], callback: Callable):
        bstack1l11llllll1_opy_ = bstack1llllll1l11_opy_.bstack1l1l1111l11_opy_(bstack11111l11ll_opy_)
        if not bstack1l11llllll1_opy_ in bstack1llllll1l11_opy_.bstack1l1111ll1l1_opy_:
            bstack1llllll1l11_opy_.bstack1l1111ll1l1_opy_[bstack1l11llllll1_opy_] = []
        bstack1llllll1l11_opy_.bstack1l1111ll1l1_opy_[bstack1l11llllll1_opy_].append(callback)
    def bstack11111lll1l_opy_(self, instance: bstack11111l1l1l_opy_, method_name: str, bstack1111l11l11_opy_: timedelta, *args, **kwargs):
        if not instance or method_name in (bstack1l1ll11_opy_ (u"ࠨࡳࡵࡣࡵࡸࡤࡹࡥࡴࡵ࡬ࡳࡳࠨᓕ")):
            return
        cmd = args[0] if method_name == bstack1l1ll11_opy_ (u"ࠢࡦࡺࡨࡧࡺࡺࡥࠣᓖ") and args and type(args) in [list, tuple] and isinstance(args[0], str) else None
        bstack1l1111lllll_opy_ = bstack1l1ll11_opy_ (u"ࠣ࠼ࠥᓗ").join(map(str, filter(None, [method_name, cmd])))
        instance.bstack11lll111l_opy_(bstack1l1ll11_opy_ (u"ࠤࡧࡶ࡮ࡼࡥࡳ࠼ࠥᓘ") + bstack1l1111lllll_opy_, bstack1111l11l11_opy_)
    def bstack11111l11l1_opy_(
        self,
        target: object,
        exec: Tuple[bstack11111l1l1l_opy_, str],
        bstack11111l11ll_opy_: Tuple[bstack111111ll1l_opy_, bstack111111l11l_opy_],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable[..., Any]:
        instance, method_name = exec
        bstack11111ll1l1_opy_, bstack1l1l11111l1_opy_ = bstack11111l11ll_opy_
        bstack1l11llllll1_opy_ = bstack1llllll1l11_opy_.bstack1l1l1111l11_opy_(bstack11111l11ll_opy_)
        self.logger.debug(bstack1l1ll11_opy_ (u"ࠥࡳࡳࡥࡨࡰࡱ࡮࠾ࠥࡳࡥࡵࡪࡲࡨࡤࡴࡡ࡮ࡧࡀࡿࡲ࡫ࡴࡩࡱࡧࡣࡳࡧ࡭ࡦࡿࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥᓙ") + str(kwargs) + bstack1l1ll11_opy_ (u"ࠦࠧᓚ"))
        if bstack11111ll1l1_opy_ == bstack111111ll1l_opy_.QUIT:
            if bstack1l1l11111l1_opy_ == bstack111111l11l_opy_.PRE:
                bstack1ll1ll11l1l_opy_ = bstack1ll1llllll1_opy_.bstack1ll1ll1l11l_opy_(EVENTS.bstack11l1l1ll1l_opy_.value)
                bstack1111l11111_opy_.bstack111111l1l1_opy_(instance, EVENTS.bstack11l1l1ll1l_opy_.value, bstack1ll1ll11l1l_opy_)
                self.logger.debug(bstack1l1ll11_opy_ (u"ࠧ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࡼࡿࠣࡱࡪࡺࡨࡰࡦࡢࡲࡦࡳࡥ࠾ࡽࢀࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࡃࡻࡾࠢ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࡃࡻࡾࠤᓛ").format(instance, method_name, bstack11111ll1l1_opy_, bstack1l1l11111l1_opy_))
        if bstack11111ll1l1_opy_ == bstack111111ll1l_opy_.bstack11111111ll_opy_:
            if bstack1l1l11111l1_opy_ == bstack111111l11l_opy_.POST and not bstack1llllll1l11_opy_.bstack1l1ll11lll1_opy_ in instance.data:
                session_id = getattr(target, bstack1l1ll11_opy_ (u"ࠨࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡪࡦࠥᓜ"), None)
                if session_id:
                    instance.data[bstack1llllll1l11_opy_.bstack1l1ll11lll1_opy_] = session_id
        elif (
            bstack11111ll1l1_opy_ == bstack111111ll1l_opy_.bstack1111l1l111_opy_
            and bstack1llllll1l11_opy_.bstack1l1l11ll11l_opy_(*args) == bstack1llllll1l11_opy_.bstack1l1l11lll1l_opy_
        ):
            if bstack1l1l11111l1_opy_ == bstack111111l11l_opy_.PRE:
                hub_url = bstack1llllll1l11_opy_.bstack11l1lll11_opy_(target)
                if hub_url:
                    instance.data.update(
                        {
                            bstack1llllll1l11_opy_.bstack1l1ll1111l1_opy_: hub_url,
                            bstack1llllll1l11_opy_.bstack1l1l1111lll_opy_: bstack1llllll1l11_opy_.bstack1ll11ll1ll1_opy_(hub_url),
                            bstack1llllll1l11_opy_.bstack1ll11lllll1_opy_: int(
                                os.environ.get(bstack1l1ll11_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠢᓝ"), str(self.platform_index))
                            ),
                        }
                    )
                bstack1ll11ll1111_opy_ = bstack1llllll1l11_opy_.bstack1ll11lll111_opy_(*args)
                bstack1l1111lll11_opy_ = bstack1ll11ll1111_opy_.get(bstack1l1ll11_opy_ (u"ࠣࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠢᓞ"), None) if bstack1ll11ll1111_opy_ else None
                if isinstance(bstack1l1111lll11_opy_, dict):
                    instance.data[bstack1llllll1l11_opy_.bstack1l1111lll1l_opy_] = copy.deepcopy(bstack1l1111lll11_opy_)
                    instance.data[bstack1llllll1l11_opy_.bstack1l1ll1l1111_opy_] = bstack1l1111lll11_opy_
            elif bstack1l1l11111l1_opy_ == bstack111111l11l_opy_.POST:
                if isinstance(result, dict):
                    framework_session_id = result.get(bstack1l1ll11_opy_ (u"ࠤࡹࡥࡱࡻࡥࠣᓟ"), dict()).get(bstack1l1ll11_opy_ (u"ࠥࡷࡪࡹࡳࡪࡱࡱࡍࡩࠨᓠ"), None)
                    if framework_session_id:
                        instance.data.update(
                            {
                                bstack1llllll1l11_opy_.bstack1l1ll11lll1_opy_: framework_session_id,
                                bstack1llllll1l11_opy_.bstack1l111l111ll_opy_: datetime.now(tz=timezone.utc),
                            }
                        )
        elif (
            bstack11111ll1l1_opy_ == bstack111111ll1l_opy_.bstack1111l1l111_opy_
            and bstack1llllll1l11_opy_.bstack1l1l11ll11l_opy_(*args) == bstack1llllll1l11_opy_.bstack1l1111ll1ll_opy_
            and bstack1l1l11111l1_opy_ == bstack111111l11l_opy_.POST
        ):
            instance.data[bstack1llllll1l11_opy_.bstack1l111l1111l_opy_] = datetime.now(tz=timezone.utc)
        if bstack1l11llllll1_opy_ in bstack1llllll1l11_opy_.bstack1l1111ll1l1_opy_:
            bstack1l11lllll1l_opy_ = None
            for callback in bstack1llllll1l11_opy_.bstack1l1111ll1l1_opy_[bstack1l11llllll1_opy_]:
                try:
                    bstack1l1l1111l1l_opy_ = callback(self, target, exec, bstack11111l11ll_opy_, result, *args, **kwargs)
                    if bstack1l11lllll1l_opy_ == None:
                        bstack1l11lllll1l_opy_ = bstack1l1l1111l1l_opy_
                except Exception as e:
                    self.logger.error(bstack1l1ll11_opy_ (u"ࠦࡪࡸࡲࡰࡴࠣ࡭ࡳࡼ࡯࡬࡫ࡱ࡫ࠥࡩࡡ࡭࡮ࡥࡥࡨࡱ࠺ࠡࠤᓡ") + str(e) + bstack1l1ll11_opy_ (u"ࠧࠨᓢ"))
                    traceback.print_exc()
            if bstack11111ll1l1_opy_ == bstack111111ll1l_opy_.QUIT:
                if bstack1l1l11111l1_opy_ == bstack111111l11l_opy_.POST:
                    bstack1ll1ll11l1l_opy_ = bstack1111l11111_opy_.bstack111111ll11_opy_(instance, EVENTS.bstack11l1l1ll1l_opy_.value)
                    if bstack1ll1ll11l1l_opy_!=None:
                        bstack1ll1llllll1_opy_.end(EVENTS.bstack11l1l1ll1l_opy_.value, bstack1ll1ll11l1l_opy_+bstack1l1ll11_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨᓣ"), bstack1ll1ll11l1l_opy_+bstack1l1ll11_opy_ (u"ࠢ࠻ࡧࡱࡨࠧᓤ"), True, None)
            if bstack1l1l11111l1_opy_ == bstack111111l11l_opy_.PRE and callable(bstack1l11lllll1l_opy_):
                return bstack1l11lllll1l_opy_
            elif bstack1l1l11111l1_opy_ == bstack111111l11l_opy_.POST and bstack1l11lllll1l_opy_:
                return bstack1l11lllll1l_opy_
    def bstack1lllllllll1_opy_(
        self, method_name, previous_state: bstack111111ll1l_opy_, *args, **kwargs
    ) -> bstack111111ll1l_opy_:
        if method_name == bstack1l1ll11_opy_ (u"ࠣࡡࡢ࡭ࡳ࡯ࡴࡠࡡࠥᓥ") or method_name == bstack1l1ll11_opy_ (u"ࠤࡶࡸࡦࡸࡴࡠࡵࡨࡷࡸ࡯࡯࡯ࠤᓦ"):
            return bstack111111ll1l_opy_.bstack11111111ll_opy_
        if method_name == bstack1l1ll11_opy_ (u"ࠥࡵࡺ࡯ࡴࠣᓧ"):
            return bstack111111ll1l_opy_.QUIT
        if method_name == bstack1l1ll11_opy_ (u"ࠦࡪࡾࡥࡤࡷࡷࡩࠧᓨ"):
            if previous_state != bstack111111ll1l_opy_.NONE:
                bstack1ll1l11llll_opy_ = bstack1llllll1l11_opy_.bstack1l1l11ll11l_opy_(*args)
                if bstack1ll1l11llll_opy_ == bstack1llllll1l11_opy_.bstack1l1l11lll1l_opy_:
                    return bstack111111ll1l_opy_.bstack11111111ll_opy_
            return bstack111111ll1l_opy_.bstack1111l1l111_opy_
        return bstack111111ll1l_opy_.NONE