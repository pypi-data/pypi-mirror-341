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
import logging
from enum import Enum
from typing import Dict, Tuple, Callable, Type, List, Any
import abc
from datetime import datetime, timezone, timedelta
from browserstack_sdk.sdk_cli.bstack11111l11ll_opy_ import bstack111111l1l1_opy_, bstack1111l111ll_opy_
import os
import threading
class bstack1llllllll1l_opy_(Enum):
    PRE = 0
    POST = 1
    def __repr__(self) -> str:
        return bstack1l1_opy_ (u"ࠧࡎ࡯ࡰ࡭ࡖࡸࡦࡺࡥ࠯ࡽࢀࠦဒ").format(self.name)
class bstack11111ll1ll_opy_(Enum):
    NONE = 0
    bstack11111l111l_opy_ = 1
    bstack11111l1111_opy_ = 3
    bstack1llllllll11_opy_ = 4
    bstack11111ll11l_opy_ = 5
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
        return bstack1l1_opy_ (u"ࠨࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࡉࡶࡦࡳࡥࡸࡱࡵ࡯ࡘࡺࡡࡵࡧ࠱ࡿࢂࠨဓ").format(self.name)
class bstack1111111l1l_opy_(bstack111111l1l1_opy_):
    framework_name: str
    framework_version: str
    state: bstack11111ll1ll_opy_
    previous_state: bstack11111ll1ll_opy_
    bstack111111ll11_opy_: datetime
    bstack11111lllll_opy_: datetime
    def __init__(
        self,
        context: bstack1111l111ll_opy_,
        framework_name: str,
        framework_version: str,
        state=bstack11111ll1ll_opy_.NONE,
    ):
        super().__init__(context)
        self.framework_name = framework_name
        self.framework_version = framework_version
        self.state = state
        self.previous_state = bstack11111ll1ll_opy_.NONE
        self.bstack111111ll11_opy_ = datetime.now(tz=timezone.utc)
        self.bstack11111lllll_opy_ = datetime.now(tz=timezone.utc)
    def bstack11111111ll_opy_(self, bstack11111l1ll1_opy_: bstack11111ll1ll_opy_):
        bstack11111ll1l1_opy_ = bstack11111ll1ll_opy_(bstack11111l1ll1_opy_).name
        if not bstack11111ll1l1_opy_:
            return False
        if bstack11111l1ll1_opy_ == self.state:
            return False
        if self.state == bstack11111ll1ll_opy_.bstack11111l1111_opy_: # bstack1111l11ll1_opy_ bstack11111ll111_opy_ for bstack111111l1ll_opy_ in bstack111111111l_opy_, it bstack1111l11111_opy_ bstack1111l1l1l1_opy_ bstack1111111111_opy_ times bstack1111111ll1_opy_ a new state
            return True
        if (
            bstack11111l1ll1_opy_ == bstack11111ll1ll_opy_.NONE
            or (self.state != bstack11111ll1ll_opy_.NONE and bstack11111l1ll1_opy_ == bstack11111ll1ll_opy_.bstack11111l111l_opy_)
            or (self.state < bstack11111ll1ll_opy_.bstack11111l111l_opy_ and bstack11111l1ll1_opy_ == bstack11111ll1ll_opy_.bstack1llllllll11_opy_)
            or (self.state < bstack11111ll1ll_opy_.bstack11111l111l_opy_ and bstack11111l1ll1_opy_ == bstack11111ll1ll_opy_.QUIT)
        ):
            raise ValueError(bstack1l1_opy_ (u"ࠢࡪࡰࡹࡥࡱ࡯ࡤࠡࡵࡷࡥࡹ࡫ࠠࡵࡴࡤࡲࡸ࡯ࡴࡪࡱࡱ࠾ࠥࠨန") + str(self.state) + bstack1l1_opy_ (u"ࠣࠢࡀࡂࠥࠨပ") + str(bstack11111l1ll1_opy_))
        self.previous_state = self.state
        self.state = bstack11111l1ll1_opy_
        self.bstack11111lllll_opy_ = datetime.now(tz=timezone.utc)
        return True
class bstack11111lll1l_opy_(abc.ABC):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    bstack11111l1l1l_opy_: Dict[str, bstack1111111l1l_opy_] = dict()
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
    def bstack11111lll11_opy_(self, instance: bstack1111111l1l_opy_, method_name: str, bstack111111ll1l_opy_: timedelta, *args, **kwargs):
        return
    @abc.abstractmethod
    def bstack1111l111l1_opy_(
        self, method_name, previous_state: bstack11111ll1ll_opy_, *args, **kwargs
    ) -> bstack11111ll1ll_opy_:
        return
    @abc.abstractmethod
    def bstack11111l1l11_opy_(
        self,
        target: object,
        exec: Tuple[bstack1111111l1l_opy_, str],
        bstack111111l11l_opy_: Tuple[bstack11111ll1ll_opy_, bstack1llllllll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable:
        return
    def bstack1111l11l1l_opy_(self, bstack1111l1l11l_opy_: List[str]):
        for clazz in self.classes:
            for method_name in bstack1111l1l11l_opy_:
                bstack1111111lll_opy_ = getattr(clazz, method_name, None)
                if not callable(bstack1111111lll_opy_):
                    self.logger.warning(bstack1l1_opy_ (u"ࠤࡸࡲࡵࡧࡴࡤࡪࡨࡨࠥࡳࡥࡵࡪࡲࡨ࠿ࠦࠢဖ") + str(method_name) + bstack1l1_opy_ (u"ࠥࠦဗ"))
                    continue
                bstack11111l11l1_opy_ = self.bstack1111l111l1_opy_(
                    method_name, previous_state=bstack11111ll1ll_opy_.NONE
                )
                bstack1llllllllll_opy_ = self.bstack111111llll_opy_(
                    method_name,
                    (bstack11111l11l1_opy_ if bstack11111l11l1_opy_ else bstack11111ll1ll_opy_.NONE),
                    bstack1111111lll_opy_,
                )
                if not callable(bstack1llllllllll_opy_):
                    self.logger.warning(bstack1l1_opy_ (u"ࠦࡲ࡫ࡴࡩࡱࡧࠤࡳࡵࡴࠡࡲࡤࡸࡨ࡮ࡥࡥ࠼ࠣࡿࡲ࡫ࡴࡩࡱࡧࡣࡳࡧ࡭ࡦࡿࠣࠬࢀࡹࡥ࡭ࡨ࠱ࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࢁ࠿ࠦࠢဘ") + str(self.framework_version) + bstack1l1_opy_ (u"ࠧ࠯ࠢမ"))
                    continue
                setattr(clazz, method_name, bstack1llllllllll_opy_)
    def bstack111111llll_opy_(
        self,
        method_name: str,
        bstack11111l11l1_opy_: bstack11111ll1ll_opy_,
        bstack1111111lll_opy_: Callable,
    ):
        def wrapped(target, *args, **kwargs):
            bstack1l1l1llll1_opy_ = datetime.now()
            (bstack11111l11l1_opy_,) = wrapped.__vars__
            bstack11111l11l1_opy_ = (
                bstack11111l11l1_opy_
                if bstack11111l11l1_opy_ and bstack11111l11l1_opy_ != bstack11111ll1ll_opy_.NONE
                else self.bstack1111l111l1_opy_(method_name, previous_state=bstack11111l11l1_opy_, *args, **kwargs)
            )
            if bstack11111l11l1_opy_ == bstack11111ll1ll_opy_.bstack11111l111l_opy_:
                ctx = bstack111111l1l1_opy_.create_context(self.bstack111111l111_opy_(target))
                if not self.bstack1111l1111l_opy_() or ctx.id not in bstack11111lll1l_opy_.bstack11111l1l1l_opy_:
                    bstack11111lll1l_opy_.bstack11111l1l1l_opy_[ctx.id] = bstack1111111l1l_opy_(
                        ctx, self.framework_name, self.framework_version, bstack11111l11l1_opy_
                    )
                self.logger.debug(bstack1l1_opy_ (u"ࠨࡷࡳࡣࡳࡴࡪࡪࠠ࡮ࡧࡷ࡬ࡴࡪࠠࡤࡴࡨࡥࡹ࡫ࡤ࠻ࠢࡾࡸࡦࡸࡧࡦࡶ࠱ࡣࡤࡩ࡬ࡢࡵࡶࡣࡤࢃࠠ࡮ࡧࡷ࡬ࡴࡪ࡟࡯ࡣࡰࡩࡂࢁ࡭ࡦࡶ࡫ࡳࡩࡥ࡮ࡢ࡯ࡨࢁࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫࠽ࡼࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀࠤࡨࡺࡸ࠾ࡽࡦࡸࡽ࠴ࡩࡥࡿࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡸࡃࠢယ") + str(bstack11111lll1l_opy_.bstack11111l1l1l_opy_.keys()) + bstack1l1_opy_ (u"ࠢࠣရ"))
            else:
                self.logger.debug(bstack1l1_opy_ (u"ࠣࡹࡵࡥࡵࡶࡥࡥࠢࡰࡩࡹ࡮࡯ࡥࠢ࡬ࡲࡻࡵ࡫ࡦࡦ࠽ࠤࢀࡺࡡࡳࡩࡨࡸ࠳ࡥ࡟ࡤ࡮ࡤࡷࡸࡥ࡟ࡾࠢࡰࡩࡹ࡮࡯ࡥࡡࡱࡥࡲ࡫࠽ࡼ࡯ࡨࡸ࡭ࡵࡤࡠࡰࡤࡱࡪࢃࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦ࠿ࡾࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂࠦࡩ࡯ࡵࡷࡥࡳࡩࡥࡴ࠿ࠥလ") + str(bstack11111lll1l_opy_.bstack11111l1l1l_opy_.keys()) + bstack1l1_opy_ (u"ࠤࠥဝ"))
            instance = bstack11111lll1l_opy_.bstack111111lll1_opy_(self.bstack111111l111_opy_(target))
            if bstack11111l11l1_opy_ == bstack11111ll1ll_opy_.NONE or not instance:
                ctx = bstack111111l1l1_opy_.create_context(self.bstack111111l111_opy_(target))
                self.logger.warning(bstack1l1_opy_ (u"ࠥࡻࡷࡧࡰࡱࡧࡧࠤࡲ࡫ࡴࡩࡱࡧࠤࡺࡴࡴࡳࡣࡦ࡯ࡪࡪ࠺ࠡࡽࡰࡩࡹ࡮࡯ࡥࡡࡱࡥࡲ࡫ࡽࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࡀࡿ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃࠠࡤࡶࡻࡁࢀࡩࡴࡹࡿࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡸࡃࠢသ") + str(bstack11111lll1l_opy_.bstack11111l1l1l_opy_.keys()) + bstack1l1_opy_ (u"ࠦࠧဟ"))
                return bstack1111111lll_opy_(target, *args, **kwargs)
            bstack1111l1l111_opy_ = self.bstack11111l1l11_opy_(
                target,
                (instance, method_name),
                (bstack11111l11l1_opy_, bstack1llllllll1l_opy_.PRE),
                None,
                *args,
                **kwargs,
            )
            if instance.bstack11111111ll_opy_(bstack11111l11l1_opy_):
                self.logger.debug(bstack1l1_opy_ (u"ࠧࡧࡰࡱ࡮࡬ࡩࡩࠦࡳࡵࡣࡷࡩ࠲ࡺࡲࡢࡰࡶ࡭ࡹ࡯࡯࡯࠼ࠣࡿ࡮ࡴࡳࡵࡣࡱࡧࡪ࠴ࡰࡳࡧࡹ࡭ࡴࡻࡳࡠࡵࡷࡥࡹ࡫ࡽࠡ࠿ࡁࠤࢀ࡯࡮ࡴࡶࡤࡲࡨ࡫࠮ࡴࡶࡤࡸࡪࢃࠠࠩࡽࡷࡽࡵ࡫ࠨࡵࡣࡵ࡫ࡪࡺࠩࡾ࠰ࡾࡱࡪࡺࡨࡰࡦࡢࡲࡦࡳࡥࡾࠢࡾࡥࡷ࡭ࡳࡾࠫࠣ࡟ࠧဠ") + str(instance.ref()) + bstack1l1_opy_ (u"ࠨ࡝ࠣအ"))
            result = (
                bstack1111l1l111_opy_(target, bstack1111111lll_opy_, *args, **kwargs)
                if callable(bstack1111l1l111_opy_)
                else bstack1111111lll_opy_(target, *args, **kwargs)
            )
            bstack1lllllllll1_opy_ = self.bstack11111l1l11_opy_(
                target,
                (instance, method_name),
                (bstack11111l11l1_opy_, bstack1llllllll1l_opy_.POST),
                result,
                *args,
                **kwargs,
            )
            self.bstack11111lll11_opy_(instance, method_name, datetime.now() - bstack1l1l1llll1_opy_, *args, **kwargs)
            return bstack1lllllllll1_opy_ if bstack1lllllllll1_opy_ else result
        wrapped.__name__ = method_name
        wrapped.__vars__ = (bstack11111l11l1_opy_,)
        return wrapped
    @staticmethod
    def bstack111111lll1_opy_(target: object, strict=True):
        ctx = bstack111111l1l1_opy_.create_context(target)
        instance = bstack11111lll1l_opy_.bstack11111l1l1l_opy_.get(ctx.id, None)
        if instance and instance.bstack11111l1lll_opy_(target):
            return instance
        return instance if instance and not strict else None
    @staticmethod
    def bstack1111111l11_opy_(
        ctx: bstack1111l111ll_opy_, state: bstack11111ll1ll_opy_, reverse=True
    ) -> List[bstack1111111l1l_opy_]:
        return sorted(
            filter(
                lambda t: t.state == state
                and t.context.thread_id == ctx.thread_id
                and t.context.process_id == ctx.process_id,
                bstack11111lll1l_opy_.bstack11111l1l1l_opy_.values(),
            ),
            key=lambda t: t.bstack111111ll11_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack11111llll1_opy_(instance: bstack1111111l1l_opy_, key: str):
        return instance and key in instance.data
    @staticmethod
    def bstack1111l11lll_opy_(instance: bstack1111111l1l_opy_, key: str, default_value=None):
        return instance.data.get(key, default_value) if instance else default_value
    @staticmethod
    def bstack11111111ll_opy_(instance: bstack1111111l1l_opy_, key: str, value: Any) -> bool:
        instance.data[key] = value
        bstack11111lll1l_opy_.logger.debug(bstack1l1_opy_ (u"ࠢࡴࡧࡷࡣࡸࡺࡡࡵࡧ࠽ࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࡻࡪࡰࡶࡸࡦࡴࡣࡦ࠰ࡵࡩ࡫࠮ࠩࡾࠢ࡮ࡩࡾࡃࡻ࡬ࡧࡼࢁࠥࡼࡡ࡭ࡷࡨࡁࠧဢ") + str(value) + bstack1l1_opy_ (u"ࠣࠤဣ"))
        return True
    @staticmethod
    def get_data(key: str, target: object, strict=True, default_value=None):
        instance = bstack11111lll1l_opy_.bstack111111lll1_opy_(target, strict)
        return bstack11111lll1l_opy_.bstack1111l11lll_opy_(instance, key, default_value)
    @staticmethod
    def set_data(key: str, value: Any, target: object, strict=True):
        instance = bstack11111lll1l_opy_.bstack111111lll1_opy_(target, strict)
        if not instance:
            return False
        instance.data[key] = value
        return True
    def bstack1111l1111l_opy_(self):
        return self.framework_name == bstack1l1_opy_ (u"ࠩࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠭ဤ")
    def bstack111111l111_opy_(self, target):
        return target if not self.bstack1111l1111l_opy_() else self.bstack1111l11l11_opy_()
    @staticmethod
    def bstack1111l11l11_opy_():
        return str(os.getpid()) + str(threading.get_ident())