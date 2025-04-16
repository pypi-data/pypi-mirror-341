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
from browserstack_sdk.sdk_cli.bstack1lll1llll1l_opy_ import bstack1llll1l1111_opy_
from browserstack_sdk.sdk_cli.bstack11111111l1_opy_ import (
    bstack11111ll1ll_opy_,
    bstack1llllllll1l_opy_,
    bstack11111lll1l_opy_,
    bstack1111111l1l_opy_,
)
from browserstack_sdk.sdk_cli.bstack1ll1lllll11_opy_ import bstack1lll1111l11_opy_
from browserstack_sdk.sdk_cli.bstack1lll1l11111_opy_ import bstack1llll1l11ll_opy_
from browserstack_sdk.sdk_cli.bstack11111l11ll_opy_ import bstack1111l111ll_opy_
from typing import Tuple, Dict, Any, List, Callable
from browserstack_sdk.sdk_cli.bstack1lll1llll1l_opy_ import bstack1llll1l1111_opy_
import weakref
class bstack1ll11l11lll_opy_(bstack1llll1l1111_opy_):
    bstack1ll11l11l11_opy_: str
    frameworks: List[str]
    drivers: Dict[str, Tuple[Callable, bstack1111111l1l_opy_]]
    pages: Dict[str, Tuple[Callable, bstack1111111l1l_opy_]]
    def __init__(self, bstack1ll11l11l11_opy_: str, frameworks: List[str]):
        super().__init__()
        self.drivers = dict()
        self.pages = dict()
        self.bstack1ll11l1ll11_opy_ = dict()
        self.bstack1ll11l11l11_opy_ = bstack1ll11l11l11_opy_
        self.frameworks = frameworks
        bstack1llll1l11ll_opy_.bstack1ll1l1ll11l_opy_((bstack11111ll1ll_opy_.bstack11111l111l_opy_, bstack1llllllll1l_opy_.POST), self.__1ll11l1l1ll_opy_)
        if any(bstack1lll1111l11_opy_.NAME in f.lower().strip() for f in frameworks):
            bstack1lll1111l11_opy_.bstack1ll1l1ll11l_opy_(
                (bstack11111ll1ll_opy_.bstack1llllllll11_opy_, bstack1llllllll1l_opy_.PRE), self.__1ll11l11ll1_opy_
            )
            bstack1lll1111l11_opy_.bstack1ll1l1ll11l_opy_(
                (bstack11111ll1ll_opy_.QUIT, bstack1llllllll1l_opy_.POST), self.__1ll11l1lll1_opy_
            )
    def __1ll11l1l1ll_opy_(
        self,
        f: bstack1llll1l11ll_opy_,
        bstack1ll11l111ll_opy_: object,
        exec: Tuple[bstack1111111l1l_opy_, str],
        bstack111111l11l_opy_: Tuple[bstack11111ll1ll_opy_, bstack1llllllll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            instance, method_name = exec
            if method_name != bstack1l1_opy_ (u"ࠥࡲࡪࡽ࡟ࡱࡣࡪࡩࠧᆟ"):
                return
            contexts = bstack1ll11l111ll_opy_.browser.contexts
            if contexts:
                for context in contexts:
                    if context.pages:
                        for page in context.pages:
                            if bstack1l1_opy_ (u"ࠦࡦࡨ࡯ࡶࡶ࠽ࡦࡱࡧ࡮࡬ࠤᆠ") in page.url:
                                self.logger.debug(bstack1l1_opy_ (u"࡙ࠧࡴࡰࡴ࡬ࡲ࡬ࠦࡴࡩࡧࠣࡲࡪࡽࠠࡱࡣࡪࡩࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫ࠢᆡ"))
                                self.pages[instance.ref()] = weakref.ref(page), instance
                                bstack11111lll1l_opy_.bstack11111111ll_opy_(instance, self.bstack1ll11l11l11_opy_, True)
                                self.logger.debug(bstack1l1_opy_ (u"ࠨ࡟ࡠࡱࡱࡣࡵࡧࡧࡦࡡ࡬ࡲ࡮ࡺ࠺ࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࠦᆢ") + str(instance.ref()) + bstack1l1_opy_ (u"ࠢࠣᆣ"))
        except Exception as e:
            self.logger.debug(bstack1l1_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡴࡶࡲࡶ࡮ࡴࡧࠡࡰࡨࡻࠥࡶࡡࡨࡧࠣ࠾ࠧᆤ"),e)
    def __1ll11l11ll1_opy_(
        self,
        f: bstack1lll1111l11_opy_,
        driver: object,
        exec: Tuple[bstack1111111l1l_opy_, str],
        bstack111111l11l_opy_: Tuple[bstack11111ll1ll_opy_, bstack1llllllll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, _ = exec
        if instance.ref() in self.drivers or bstack11111lll1l_opy_.bstack1111l11lll_opy_(instance, self.bstack1ll11l11l11_opy_, False):
            return
        if not f.bstack1ll11ll111l_opy_(f.hub_url(driver)):
            self.bstack1ll11l1ll11_opy_[instance.ref()] = weakref.ref(driver), instance
            bstack11111lll1l_opy_.bstack11111111ll_opy_(instance, self.bstack1ll11l11l11_opy_, True)
            self.logger.debug(bstack1l1_opy_ (u"ࠤࡢࡣࡴࡴ࡟ࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡡ࡬ࡲ࡮ࡺ࠺ࠡࡰࡲࡲࡤࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡩࡸࡩࡷࡧࡵࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࠢᆥ") + str(instance.ref()) + bstack1l1_opy_ (u"ࠥࠦᆦ"))
            return
        self.drivers[instance.ref()] = weakref.ref(driver), instance
        bstack11111lll1l_opy_.bstack11111111ll_opy_(instance, self.bstack1ll11l11l11_opy_, True)
        self.logger.debug(bstack1l1_opy_ (u"ࠦࡤࡥ࡯࡯ࡡࡶࡩࡱ࡫࡮ࡪࡷࡰࡣ࡮ࡴࡩࡵ࠼ࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࠨᆧ") + str(instance.ref()) + bstack1l1_opy_ (u"ࠧࠨᆨ"))
    def __1ll11l1lll1_opy_(
        self,
        f: bstack1lll1111l11_opy_,
        driver: object,
        exec: Tuple[bstack1111111l1l_opy_, str],
        bstack111111l11l_opy_: Tuple[bstack11111ll1ll_opy_, bstack1llllllll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, _ = exec
        if not instance.ref() in self.drivers:
            return
        self.bstack1ll11l1l1l1_opy_(instance)
        self.logger.debug(bstack1l1_opy_ (u"ࠨ࡟ࡠࡱࡱࡣࡸ࡫࡬ࡦࡰ࡬ࡹࡲࡥࡱࡶ࡫ࡷ࠾ࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࠣᆩ") + str(instance.ref()) + bstack1l1_opy_ (u"ࠢࠣᆪ"))
    def bstack1ll11l1l111_opy_(self, context: bstack1111l111ll_opy_, reverse=True) -> List[Tuple[Callable, bstack1111111l1l_opy_]]:
        matches = []
        if self.pages:
            for data in self.pages.values():
                if data[1].bstack1ll11l11l1l_opy_(context):
                    matches.append(data)
        if self.drivers:
            for data in self.drivers.values():
                if (
                    bstack1lll1111l11_opy_.bstack1ll1l1l1l1l_opy_(data[1])
                    and data[1].bstack1ll11l11l1l_opy_(context)
                    and getattr(data[0](), bstack1l1_opy_ (u"ࠣࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨࠧᆫ"), False)
                ):
                    matches.append(data)
        return sorted(matches, key=lambda d: d[1].bstack111111ll11_opy_, reverse=reverse)
    def bstack1ll11l1llll_opy_(self, context: bstack1111l111ll_opy_, reverse=True) -> List[Tuple[Callable, bstack1111111l1l_opy_]]:
        matches = []
        for data in self.bstack1ll11l1ll11_opy_.values():
            if (
                data[1].bstack1ll11l11l1l_opy_(context)
                and getattr(data[0](), bstack1l1_opy_ (u"ࠤࡶࡩࡸࡹࡩࡰࡰࡢ࡭ࡩࠨᆬ"), False)
            ):
                matches.append(data)
        return sorted(matches, key=lambda d: d[1].bstack111111ll11_opy_, reverse=reverse)
    def bstack1ll11l1l11l_opy_(self, instance: bstack1111111l1l_opy_) -> bool:
        return instance and instance.ref() in self.drivers
    def bstack1ll11l1l1l1_opy_(self, instance: bstack1111111l1l_opy_) -> bool:
        if self.bstack1ll11l1l11l_opy_(instance):
            self.drivers.pop(instance.ref())
            bstack11111lll1l_opy_.bstack11111111ll_opy_(instance, self.bstack1ll11l11l11_opy_, False)
            return True
        return False