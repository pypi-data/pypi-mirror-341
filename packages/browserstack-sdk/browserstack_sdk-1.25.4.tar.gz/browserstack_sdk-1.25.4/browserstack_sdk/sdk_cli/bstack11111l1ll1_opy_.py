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
import logging
from enum import Enum
from typing import Dict, Tuple, Callable, Type, List, Any
import abc
from datetime import datetime, timezone, timedelta
from browserstack_sdk.sdk_cli.bstack11111ll11l_opy_ import bstack1111111l11_opy_, bstack1111l1l1l1_opy_
import os
import threading
class bstack111111l11l_opy_(Enum):
    PRE = 0
    POST = 1
    def __repr__(self) -> str:
        return bstack1l1ll11_opy_ (u"ࠧࡎ࡯ࡰ࡭ࡖࡸࡦࡺࡥ࠯ࡽࢀࠦဒ").format(self.name)
class bstack111111ll1l_opy_(Enum):
    NONE = 0
    bstack11111111ll_opy_ = 1
    bstack1111l11lll_opy_ = 3
    bstack1111l1l111_opy_ = 4
    bstack111111l111_opy_ = 5
    QUIT = 6
    def __eq__(self, other):
        if self.__class__ is other.__class__:
            return self.value == other.value
        return NotImplemented
    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented
    def __repr__(self) -> str:
        return bstack1l1ll11_opy_ (u"ࠨࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࡉࡶࡦࡳࡥࡸࡱࡵ࡯ࡘࡺࡡࡵࡧ࠱ࡿࢂࠨဓ").format(self.name)
class bstack11111l1l1l_opy_(bstack1111111l11_opy_):
    framework_name: str
    framework_version: str
    state: bstack111111ll1l_opy_
    previous_state: bstack111111ll1l_opy_
    bstack11111ll111_opy_: datetime
    bstack111111111l_opy_: datetime
    def __init__(
        self,
        context: bstack1111l1l1l1_opy_,
        framework_name: str,
        framework_version: str,
        state=bstack111111ll1l_opy_.NONE,
    ):
        super().__init__(context)
        self.framework_name = framework_name
        self.framework_version = framework_version
        self.state = state
        self.previous_state = bstack111111ll1l_opy_.NONE
        self.bstack11111ll111_opy_ = datetime.now(tz=timezone.utc)
        self.bstack111111111l_opy_ = datetime.now(tz=timezone.utc)
    def bstack111111l1l1_opy_(self, bstack111111l1ll_opy_: bstack111111ll1l_opy_):
        bstack1111l11ll1_opy_ = bstack111111ll1l_opy_(bstack111111l1ll_opy_).name
        if not bstack1111l11ll1_opy_:
            return False
        if bstack111111l1ll_opy_ == self.state:
            return False
        if self.state == bstack111111ll1l_opy_.bstack1111l11lll_opy_: # bstack11111llll1_opy_ bstack11111lll11_opy_ for bstack1111111ll1_opy_ in bstack1111l11l1l_opy_, it bstack111111llll_opy_ bstack11111l1lll_opy_ bstack11111l111l_opy_ times bstack11111ll1ll_opy_ a new state
            return True
        if (
            bstack111111l1ll_opy_ == bstack111111ll1l_opy_.NONE
            or (self.state != bstack111111ll1l_opy_.NONE and bstack111111l1ll_opy_ == bstack111111ll1l_opy_.bstack11111111ll_opy_)
            or (self.state < bstack111111ll1l_opy_.bstack11111111ll_opy_ and bstack111111l1ll_opy_ == bstack111111ll1l_opy_.bstack1111l1l111_opy_)
            or (self.state < bstack111111ll1l_opy_.bstack11111111ll_opy_ and bstack111111l1ll_opy_ == bstack111111ll1l_opy_.QUIT)
        ):
            raise ValueError(bstack1l1ll11_opy_ (u"ࠢࡪࡰࡹࡥࡱ࡯ࡤࠡࡵࡷࡥࡹ࡫ࠠࡵࡴࡤࡲࡸ࡯ࡴࡪࡱࡱ࠾ࠥࠨန") + str(self.state) + bstack1l1ll11_opy_ (u"ࠣࠢࡀࡂࠥࠨပ") + str(bstack111111l1ll_opy_))
        self.previous_state = self.state
        self.state = bstack111111l1ll_opy_
        self.bstack111111111l_opy_ = datetime.now(tz=timezone.utc)
        return True
class bstack1111l11111_opy_(abc.ABC):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    bstack1111l1111l_opy_: Dict[str, bstack11111l1l1l_opy_] = dict()
    framework_name: str
    framework_version: str
    classes: List[Type]
    def __init__(
        self,
        framework_name: str,
        framework_version: str,
        classes: List[Type],
    ):
        self.framework_name = framework_name
        self.framework_version = framework_version
        self.classes = classes
    @abc.abstractmethod
    def bstack11111lll1l_opy_(self, instance: bstack11111l1l1l_opy_, method_name: str, bstack1111l11l11_opy_: timedelta, *args, **kwargs):
        return
    @abc.abstractmethod
    def bstack1lllllllll1_opy_(
        self, method_name, previous_state: bstack111111ll1l_opy_, *args, **kwargs
    ) -> bstack111111ll1l_opy_:
        return
    @abc.abstractmethod
    def bstack11111l11l1_opy_(
        self,
        target: object,
        exec: Tuple[bstack11111l1l1l_opy_, str],
        bstack11111l11ll_opy_: Tuple[bstack111111ll1l_opy_, bstack111111l11l_opy_],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable:
        return
    def bstack1111l111l1_opy_(self, bstack11111l1l11_opy_: List[str]):
        for clazz in self.classes:
            for method_name in bstack11111l1l11_opy_:
                bstack1llllllllll_opy_ = getattr(clazz, method_name, None)
                if not callable(bstack1llllllllll_opy_):
                    self.logger.warning(bstack1l1ll11_opy_ (u"ࠤࡸࡲࡵࡧࡴࡤࡪࡨࡨࠥࡳࡥࡵࡪࡲࡨ࠿ࠦࠢဖ") + str(method_name) + bstack1l1ll11_opy_ (u"ࠥࠦဗ"))
                    continue
                bstack11111ll1l1_opy_ = self.bstack1lllllllll1_opy_(
                    method_name, previous_state=bstack111111ll1l_opy_.NONE
                )
                bstack1111111lll_opy_ = self.bstack1111111l1l_opy_(
                    method_name,
                    (bstack11111ll1l1_opy_ if bstack11111ll1l1_opy_ else bstack111111ll1l_opy_.NONE),
                    bstack1llllllllll_opy_,
                )
                if not callable(bstack1111111lll_opy_):
                    self.logger.warning(bstack1l1ll11_opy_ (u"ࠦࡲ࡫ࡴࡩࡱࡧࠤࡳࡵࡴࠡࡲࡤࡸࡨ࡮ࡥࡥ࠼ࠣࡿࡲ࡫ࡴࡩࡱࡧࡣࡳࡧ࡭ࡦࡿࠣࠬࢀࡹࡥ࡭ࡨ࠱ࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࢁ࠿ࠦࠢဘ") + str(self.framework_version) + bstack1l1ll11_opy_ (u"ࠧ࠯ࠢမ"))
                    continue
                setattr(clazz, method_name, bstack1111111lll_opy_)
    def bstack1111111l1l_opy_(
        self,
        method_name: str,
        bstack11111ll1l1_opy_: bstack111111ll1l_opy_,
        bstack1llllllllll_opy_: Callable,
    ):
        def wrapped(target, *args, **kwargs):
            bstack1l1l1llll_opy_ = datetime.now()
            (bstack11111ll1l1_opy_,) = wrapped.__vars__
            bstack11111ll1l1_opy_ = (
                bstack11111ll1l1_opy_
                if bstack11111ll1l1_opy_ and bstack11111ll1l1_opy_ != bstack111111ll1l_opy_.NONE
                else self.bstack1lllllllll1_opy_(method_name, previous_state=bstack11111ll1l1_opy_, *args, **kwargs)
            )
            if bstack11111ll1l1_opy_ == bstack111111ll1l_opy_.bstack11111111ll_opy_:
                ctx = bstack1111111l11_opy_.create_context(self.bstack1111l1l11l_opy_(target))
                if not self.bstack1llllllll1l_opy_() or ctx.id not in bstack1111l11111_opy_.bstack1111l1111l_opy_:
                    bstack1111l11111_opy_.bstack1111l1111l_opy_[ctx.id] = bstack11111l1l1l_opy_(
                        ctx, self.framework_name, self.framework_version, bstack11111ll1l1_opy_
                    )
                self.logger.debug(bstack1l1ll11_opy_ (u"ࠨࡷࡳࡣࡳࡴࡪࡪࠠ࡮ࡧࡷ࡬ࡴࡪࠠࡤࡴࡨࡥࡹ࡫ࡤ࠻ࠢࡾࡸࡦࡸࡧࡦࡶ࠱ࡣࡤࡩ࡬ࡢࡵࡶࡣࡤࢃࠠ࡮ࡧࡷ࡬ࡴࡪ࡟࡯ࡣࡰࡩࡂࢁ࡭ࡦࡶ࡫ࡳࡩࡥ࡮ࡢ࡯ࡨࢁࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫࠽ࡼࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀࠤࡨࡺࡸ࠾ࡽࡦࡸࡽ࠴ࡩࡥࡿࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡸࡃࠢယ") + str(bstack1111l11111_opy_.bstack1111l1111l_opy_.keys()) + bstack1l1ll11_opy_ (u"ࠢࠣရ"))
            else:
                self.logger.debug(bstack1l1ll11_opy_ (u"ࠣࡹࡵࡥࡵࡶࡥࡥࠢࡰࡩࡹ࡮࡯ࡥࠢ࡬ࡲࡻࡵ࡫ࡦࡦ࠽ࠤࢀࡺࡡࡳࡩࡨࡸ࠳ࡥ࡟ࡤ࡮ࡤࡷࡸࡥ࡟ࡾࠢࡰࡩࡹ࡮࡯ࡥࡡࡱࡥࡲ࡫࠽ࡼ࡯ࡨࡸ࡭ࡵࡤࡠࡰࡤࡱࡪࢃࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦ࠿ࡾࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂࠦࡩ࡯ࡵࡷࡥࡳࡩࡥࡴ࠿ࠥလ") + str(bstack1111l11111_opy_.bstack1111l1111l_opy_.keys()) + bstack1l1ll11_opy_ (u"ࠤࠥဝ"))
            instance = bstack1111l11111_opy_.bstack11111111l1_opy_(self.bstack1111l1l11l_opy_(target))
            if bstack11111ll1l1_opy_ == bstack111111ll1l_opy_.NONE or not instance:
                ctx = bstack1111111l11_opy_.create_context(self.bstack1111l1l11l_opy_(target))
                self.logger.warning(bstack1l1ll11_opy_ (u"ࠥࡻࡷࡧࡰࡱࡧࡧࠤࡲ࡫ࡴࡩࡱࡧࠤࡺࡴࡴࡳࡣࡦ࡯ࡪࡪ࠺ࠡࡽࡰࡩࡹ࡮࡯ࡥࡡࡱࡥࡲ࡫ࡽࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࡀࡿ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃࠠࡤࡶࡻࡁࢀࡩࡴࡹࡿࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡸࡃࠢသ") + str(bstack1111l11111_opy_.bstack1111l1111l_opy_.keys()) + bstack1l1ll11_opy_ (u"ࠦࠧဟ"))
                return bstack1llllllllll_opy_(target, *args, **kwargs)
            bstack1llllllll11_opy_ = self.bstack11111l11l1_opy_(
                target,
                (instance, method_name),
                (bstack11111ll1l1_opy_, bstack111111l11l_opy_.PRE),
                None,
                *args,
                **kwargs,
            )
            if instance.bstack111111l1l1_opy_(bstack11111ll1l1_opy_):
                self.logger.debug(bstack1l1ll11_opy_ (u"ࠧࡧࡰࡱ࡮࡬ࡩࡩࠦࡳࡵࡣࡷࡩ࠲ࡺࡲࡢࡰࡶ࡭ࡹ࡯࡯࡯࠼ࠣࡿ࡮ࡴࡳࡵࡣࡱࡧࡪ࠴ࡰࡳࡧࡹ࡭ࡴࡻࡳࡠࡵࡷࡥࡹ࡫ࡽࠡ࠿ࡁࠤࢀ࡯࡮ࡴࡶࡤࡲࡨ࡫࠮ࡴࡶࡤࡸࡪࢃࠠࠩࡽࡷࡽࡵ࡫ࠨࡵࡣࡵ࡫ࡪࡺࠩࡾ࠰ࡾࡱࡪࡺࡨࡰࡦࡢࡲࡦࡳࡥࡾࠢࡾࡥࡷ࡭ࡳࡾࠫࠣ࡟ࠧဠ") + str(instance.ref()) + bstack1l1ll11_opy_ (u"ࠨ࡝ࠣအ"))
            result = (
                bstack1llllllll11_opy_(target, bstack1llllllllll_opy_, *args, **kwargs)
                if callable(bstack1llllllll11_opy_)
                else bstack1llllllllll_opy_(target, *args, **kwargs)
            )
            bstack11111lllll_opy_ = self.bstack11111l11l1_opy_(
                target,
                (instance, method_name),
                (bstack11111ll1l1_opy_, bstack111111l11l_opy_.POST),
                result,
                *args,
                **kwargs,
            )
            self.bstack11111lll1l_opy_(instance, method_name, datetime.now() - bstack1l1l1llll_opy_, *args, **kwargs)
            return bstack11111lllll_opy_ if bstack11111lllll_opy_ else result
        wrapped.__name__ = method_name
        wrapped.__vars__ = (bstack11111ll1l1_opy_,)
        return wrapped
    @staticmethod
    def bstack11111111l1_opy_(target: object, strict=True):
        ctx = bstack1111111l11_opy_.create_context(target)
        instance = bstack1111l11111_opy_.bstack1111l1111l_opy_.get(ctx.id, None)
        if instance and instance.bstack111111lll1_opy_(target):
            return instance
        return instance if instance and not strict else None
    @staticmethod
    def bstack1111111111_opy_(
        ctx: bstack1111l1l1l1_opy_, state: bstack111111ll1l_opy_, reverse=True
    ) -> List[bstack11111l1l1l_opy_]:
        return sorted(
            filter(
                lambda t: t.state == state
                and t.context.thread_id == ctx.thread_id
                and t.context.process_id == ctx.process_id,
                bstack1111l11111_opy_.bstack1111l1111l_opy_.values(),
            ),
            key=lambda t: t.bstack11111ll111_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack11111l1111_opy_(instance: bstack11111l1l1l_opy_, key: str):
        return instance and key in instance.data
    @staticmethod
    def bstack111111ll11_opy_(instance: bstack11111l1l1l_opy_, key: str, default_value=None):
        return instance.data.get(key, default_value) if instance else default_value
    @staticmethod
    def bstack111111l1l1_opy_(instance: bstack11111l1l1l_opy_, key: str, value: Any) -> bool:
        instance.data[key] = value
        bstack1111l11111_opy_.logger.debug(bstack1l1ll11_opy_ (u"ࠢࡴࡧࡷࡣࡸࡺࡡࡵࡧ࠽ࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࡻࡪࡰࡶࡸࡦࡴࡣࡦ࠰ࡵࡩ࡫࠮ࠩࡾࠢ࡮ࡩࡾࡃࡻ࡬ࡧࡼࢁࠥࡼࡡ࡭ࡷࡨࡁࠧဢ") + str(value) + bstack1l1ll11_opy_ (u"ࠣࠤဣ"))
        return True
    @staticmethod
    def get_data(key: str, target: object, strict=True, default_value=None):
        instance = bstack1111l11111_opy_.bstack11111111l1_opy_(target, strict)
        return bstack1111l11111_opy_.bstack111111ll11_opy_(instance, key, default_value)
    @staticmethod
    def set_data(key: str, value: Any, target: object, strict=True):
        instance = bstack1111l11111_opy_.bstack11111111l1_opy_(target, strict)
        if not instance:
            return False
        instance.data[key] = value
        return True
    def bstack1llllllll1l_opy_(self):
        return self.framework_name == bstack1l1ll11_opy_ (u"ࠩࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠭ဤ")
    def bstack1111l1l11l_opy_(self, target):
        return target if not self.bstack1llllllll1l_opy_() else self.bstack1111l111ll_opy_()
    @staticmethod
    def bstack1111l111ll_opy_():
        return str(os.getpid()) + str(threading.get_ident())