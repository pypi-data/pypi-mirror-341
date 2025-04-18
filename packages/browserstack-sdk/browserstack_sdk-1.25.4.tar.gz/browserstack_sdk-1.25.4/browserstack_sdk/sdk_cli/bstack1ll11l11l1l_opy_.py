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
from browserstack_sdk.sdk_cli.bstack1llll11ll11_opy_ import bstack1llllll1l1l_opy_
from browserstack_sdk.sdk_cli.bstack11111l1ll1_opy_ import (
    bstack111111ll1l_opy_,
    bstack111111l11l_opy_,
    bstack1111l11111_opy_,
    bstack11111l1l1l_opy_,
)
from browserstack_sdk.sdk_cli.bstack1lll111llll_opy_ import bstack1llllll1l11_opy_
from browserstack_sdk.sdk_cli.bstack1llll1lll1l_opy_ import bstack1llllll1ll1_opy_
from browserstack_sdk.sdk_cli.bstack11111ll11l_opy_ import bstack1111l1l1l1_opy_
from typing import Tuple, Dict, Any, List, Callable
from browserstack_sdk.sdk_cli.bstack1llll11ll11_opy_ import bstack1llllll1l1l_opy_
import weakref
class bstack1ll11l11lll_opy_(bstack1llllll1l1l_opy_):
    bstack1ll11l1l1l1_opy_: str
    frameworks: List[str]
    drivers: Dict[str, Tuple[Callable, bstack11111l1l1l_opy_]]
    pages: Dict[str, Tuple[Callable, bstack11111l1l1l_opy_]]
    def __init__(self, bstack1ll11l1l1l1_opy_: str, frameworks: List[str]):
        super().__init__()
        self.drivers = dict()
        self.pages = dict()
        self.bstack1ll11l111ll_opy_ = dict()
        self.bstack1ll11l1l1l1_opy_ = bstack1ll11l1l1l1_opy_
        self.frameworks = frameworks
        bstack1llllll1ll1_opy_.bstack1ll1l1ll1l1_opy_((bstack111111ll1l_opy_.bstack11111111ll_opy_, bstack111111l11l_opy_.POST), self.__1ll11l1ll1l_opy_)
        if any(bstack1llllll1l11_opy_.NAME in f.lower().strip() for f in frameworks):
            bstack1llllll1l11_opy_.bstack1ll1l1ll1l1_opy_(
                (bstack111111ll1l_opy_.bstack1111l1l111_opy_, bstack111111l11l_opy_.PRE), self.__1ll11l1l111_opy_
            )
            bstack1llllll1l11_opy_.bstack1ll1l1ll1l1_opy_(
                (bstack111111ll1l_opy_.QUIT, bstack111111l11l_opy_.POST), self.__1ll11l1ll11_opy_
            )
    def __1ll11l1ll1l_opy_(
        self,
        f: bstack1llllll1ll1_opy_,
        bstack1ll11l1l1ll_opy_: object,
        exec: Tuple[bstack11111l1l1l_opy_, str],
        bstack11111l11ll_opy_: Tuple[bstack111111ll1l_opy_, bstack111111l11l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            instance, method_name = exec
            if method_name != bstack1l1ll11_opy_ (u"ࠥࡲࡪࡽ࡟ࡱࡣࡪࡩࠧᆟ"):
                return
            contexts = bstack1ll11l1l1ll_opy_.browser.contexts
            if contexts:
                for context in contexts:
                    if context.pages:
                        for page in context.pages:
                            if bstack1l1ll11_opy_ (u"ࠦࡦࡨ࡯ࡶࡶ࠽ࡦࡱࡧ࡮࡬ࠤᆠ") in page.url:
                                self.logger.debug(bstack1l1ll11_opy_ (u"࡙ࠧࡴࡰࡴ࡬ࡲ࡬ࠦࡴࡩࡧࠣࡲࡪࡽࠠࡱࡣࡪࡩࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫ࠢᆡ"))
                                self.pages[instance.ref()] = weakref.ref(page), instance
                                bstack1111l11111_opy_.bstack111111l1l1_opy_(instance, self.bstack1ll11l1l1l1_opy_, True)
                                self.logger.debug(bstack1l1ll11_opy_ (u"ࠨ࡟ࡠࡱࡱࡣࡵࡧࡧࡦࡡ࡬ࡲ࡮ࡺ࠺ࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࠦᆢ") + str(instance.ref()) + bstack1l1ll11_opy_ (u"ࠢࠣᆣ"))
        except Exception as e:
            self.logger.debug(bstack1l1ll11_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡴࡶࡲࡶ࡮ࡴࡧࠡࡰࡨࡻࠥࡶࡡࡨࡧࠣ࠾ࠧᆤ"),e)
    def __1ll11l1l111_opy_(
        self,
        f: bstack1llllll1l11_opy_,
        driver: object,
        exec: Tuple[bstack11111l1l1l_opy_, str],
        bstack11111l11ll_opy_: Tuple[bstack111111ll1l_opy_, bstack111111l11l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, _ = exec
        if instance.ref() in self.drivers or bstack1111l11111_opy_.bstack111111ll11_opy_(instance, self.bstack1ll11l1l1l1_opy_, False):
            return
        if not f.bstack1ll11ll1ll1_opy_(f.hub_url(driver)):
            self.bstack1ll11l111ll_opy_[instance.ref()] = weakref.ref(driver), instance
            bstack1111l11111_opy_.bstack111111l1l1_opy_(instance, self.bstack1ll11l1l1l1_opy_, True)
            self.logger.debug(bstack1l1ll11_opy_ (u"ࠤࡢࡣࡴࡴ࡟ࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡡ࡬ࡲ࡮ࡺ࠺ࠡࡰࡲࡲࡤࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡩࡸࡩࡷࡧࡵࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࠢᆥ") + str(instance.ref()) + bstack1l1ll11_opy_ (u"ࠥࠦᆦ"))
            return
        self.drivers[instance.ref()] = weakref.ref(driver), instance
        bstack1111l11111_opy_.bstack111111l1l1_opy_(instance, self.bstack1ll11l1l1l1_opy_, True)
        self.logger.debug(bstack1l1ll11_opy_ (u"ࠦࡤࡥ࡯࡯ࡡࡶࡩࡱ࡫࡮ࡪࡷࡰࡣ࡮ࡴࡩࡵ࠼ࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࠨᆧ") + str(instance.ref()) + bstack1l1ll11_opy_ (u"ࠧࠨᆨ"))
    def __1ll11l1ll11_opy_(
        self,
        f: bstack1llllll1l11_opy_,
        driver: object,
        exec: Tuple[bstack11111l1l1l_opy_, str],
        bstack11111l11ll_opy_: Tuple[bstack111111ll1l_opy_, bstack111111l11l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, _ = exec
        if not instance.ref() in self.drivers:
            return
        self.bstack1ll11l1llll_opy_(instance)
        self.logger.debug(bstack1l1ll11_opy_ (u"ࠨ࡟ࡠࡱࡱࡣࡸ࡫࡬ࡦࡰ࡬ࡹࡲࡥࡱࡶ࡫ࡷ࠾ࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࠣᆩ") + str(instance.ref()) + bstack1l1ll11_opy_ (u"ࠢࠣᆪ"))
    def bstack1ll11l1lll1_opy_(self, context: bstack1111l1l1l1_opy_, reverse=True) -> List[Tuple[Callable, bstack11111l1l1l_opy_]]:
        matches = []
        if self.pages:
            for data in self.pages.values():
                if data[1].bstack1ll11l11ll1_opy_(context):
                    matches.append(data)
        if self.drivers:
            for data in self.drivers.values():
                if (
                    bstack1llllll1l11_opy_.bstack1ll1l11l1ll_opy_(data[1])
                    and data[1].bstack1ll11l11ll1_opy_(context)
                    and getattr(data[0](), bstack1l1ll11_opy_ (u"ࠣࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨࠧᆫ"), False)
                ):
                    matches.append(data)
        return sorted(matches, key=lambda d: d[1].bstack11111ll111_opy_, reverse=reverse)
    def bstack1ll11l1l11l_opy_(self, context: bstack1111l1l1l1_opy_, reverse=True) -> List[Tuple[Callable, bstack11111l1l1l_opy_]]:
        matches = []
        for data in self.bstack1ll11l111ll_opy_.values():
            if (
                data[1].bstack1ll11l11ll1_opy_(context)
                and getattr(data[0](), bstack1l1ll11_opy_ (u"ࠤࡶࡩࡸࡹࡩࡰࡰࡢ࡭ࡩࠨᆬ"), False)
            ):
                matches.append(data)
        return sorted(matches, key=lambda d: d[1].bstack11111ll111_opy_, reverse=reverse)
    def bstack1ll11l11l11_opy_(self, instance: bstack11111l1l1l_opy_) -> bool:
        return instance and instance.ref() in self.drivers
    def bstack1ll11l1llll_opy_(self, instance: bstack11111l1l1l_opy_) -> bool:
        if self.bstack1ll11l11l11_opy_(instance):
            self.drivers.pop(instance.ref())
            bstack1111l11111_opy_.bstack111111l1l1_opy_(instance, self.bstack1ll11l1l1l1_opy_, False)
            return True
        return False