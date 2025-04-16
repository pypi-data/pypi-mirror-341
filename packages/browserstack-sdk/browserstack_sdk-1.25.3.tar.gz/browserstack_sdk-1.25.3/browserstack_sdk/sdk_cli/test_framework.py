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
import os
import threading
import traceback
from typing import Dict, List, Any, Callable, Tuple, Union
import abc
from datetime import datetime, timezone
from dataclasses import dataclass
from browserstack_sdk.sdk_cli.bstack1111l1llll_opy_ import bstack1111l1ll1l_opy_
from browserstack_sdk.sdk_cli.bstack11111l11ll_opy_ import bstack111111l1l1_opy_, bstack1111l111ll_opy_
class bstack1llll111ll1_opy_(Enum):
    PRE = 0
    POST = 1
    def __repr__(self) -> str:
        return bstack1l1_opy_ (u"࡙ࠦ࡫ࡳࡵࡊࡲࡳࡰ࡙ࡴࡢࡶࡨ࠲ࢀࢃࠢᓨ").format(self.name)
class bstack1lll1l1lll1_opy_(Enum):
    NONE = 0
    BEFORE_ALL = 1
    LOG = 2
    SETUP_FIXTURE = 3
    INIT_TEST = 4
    BEFORE_EACH = 5
    AFTER_EACH = 6
    TEST = 7
    STEP = 8
    LOG_REPORT = 9
    AFTER_ALL = 10
    def __eq__(self, other):
        if self.__class__ is other.__class__:
            return self.value == other.value
        return NotImplemented
    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented
    def __repr__(self) -> str:
        return bstack1l1_opy_ (u"࡚ࠧࡥࡴࡶࡉࡶࡦࡳࡥࡸࡱࡵ࡯ࡘࡺࡡࡵࡧ࠱ࡿࢂࠨᓩ").format(self.name)
class bstack1lll11l1ll1_opy_(bstack111111l1l1_opy_):
    bstack1ll1l1ll1ll_opy_: List[str]
    bstack1l111lll1l1_opy_: Dict[str, str]
    state: bstack1lll1l1lll1_opy_
    bstack111111ll11_opy_: datetime
    bstack11111lllll_opy_: datetime
    def __init__(
        self,
        context: bstack1111l111ll_opy_,
        bstack1ll1l1ll1ll_opy_: List[str],
        bstack1l111lll1l1_opy_: Dict[str, str],
        state=bstack1lll1l1lll1_opy_.NONE,
    ):
        super().__init__(context)
        self.bstack1ll1l1ll1ll_opy_ = bstack1ll1l1ll1ll_opy_
        self.bstack1l111lll1l1_opy_ = bstack1l111lll1l1_opy_
        self.state = state
        self.bstack111111ll11_opy_ = datetime.now(tz=timezone.utc)
        self.bstack11111lllll_opy_ = datetime.now(tz=timezone.utc)
    def bstack11111111ll_opy_(self, bstack11111l1ll1_opy_: bstack1lll1l1lll1_opy_):
        bstack11111ll1l1_opy_ = bstack1lll1l1lll1_opy_(bstack11111l1ll1_opy_).name
        if not bstack11111ll1l1_opy_:
            return False
        if bstack11111l1ll1_opy_ == self.state:
            return False
        self.state = bstack11111l1ll1_opy_
        self.bstack11111lllll_opy_ = datetime.now(tz=timezone.utc)
        return True
@dataclass
class bstack1l11l1l11l1_opy_:
    test_framework_name: str
    test_framework_version: str
    platform_index: int
@dataclass
class bstack1llll1111l1_opy_:
    kind: str
    message: str
    level: Union[None, str] = None
    timestamp: Union[None, datetime] = datetime.now(tz=timezone.utc)
    fileName: str = None
    bstack1l1llll1111_opy_: int = None
    bstack1l1llllllll_opy_: str = None
    bstack1l11ll1_opy_: str = None
    bstack111llll1l_opy_: str = None
    bstack1l1lll11ll1_opy_: str = None
    bstack1l11llll1l1_opy_: str = None
class TestFramework(abc.ABC):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    bstack1ll1l111lll_opy_ = bstack1l1_opy_ (u"ࠨࡴࡦࡵࡷࡣࡺࡻࡩࡥࠤᓪ")
    bstack1l111lllll1_opy_ = bstack1l1_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡯ࡤࠣᓫ")
    bstack1ll1l1l1ll1_opy_ = bstack1l1_opy_ (u"ࠣࡶࡨࡷࡹࡥ࡮ࡢ࡯ࡨࠦᓬ")
    bstack1l11l1l1111_opy_ = bstack1l1_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡧ࡫࡯ࡩࡤࡶࡡࡵࡪࠥᓭ")
    bstack1l11l1lll1l_opy_ = bstack1l1_opy_ (u"ࠥࡸࡪࡹࡴࡠࡶࡤ࡫ࡸࠨᓮ")
    bstack1l1l1lll1l1_opy_ = bstack1l1_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡵࡩࡸࡻ࡬ࡵࠤᓯ")
    bstack1ll1111ll11_opy_ = bstack1l1_opy_ (u"ࠧࡺࡥࡴࡶࡢࡶࡪࡹࡵ࡭ࡶࡢࡥࡹࠨᓰ")
    bstack1ll1111111l_opy_ = bstack1l1_opy_ (u"ࠨࡴࡦࡵࡷࡣࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠣᓱ")
    bstack1ll1111l1l1_opy_ = bstack1l1_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡫࡮ࡥࡧࡧࡣࡦࡺࠢᓲ")
    bstack1l11l111ll1_opy_ = bstack1l1_opy_ (u"ࠣࡶࡨࡷࡹࡥ࡬ࡰࡥࡤࡸ࡮ࡵ࡮ࠣᓳ")
    bstack1ll1l1111ll_opy_ = bstack1l1_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥࠣᓴ")
    bstack1ll111l111l_opy_ = bstack1l1_opy_ (u"ࠥࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠧᓵ")
    bstack1l11l111l11_opy_ = bstack1l1_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡦࡳࡩ࡫ࠢᓶ")
    bstack1l1ll1llll1_opy_ = bstack1l1_opy_ (u"ࠧࡺࡥࡴࡶࡢࡶࡪࡸࡵ࡯ࡡࡱࡥࡲ࡫ࠢᓷ")
    bstack1ll1l11llll_opy_ = bstack1l1_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡠ࡫ࡱࡨࡪࡾࠢᓸ")
    bstack1l1l1ll1l11_opy_ = bstack1l1_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡬ࡡࡪ࡮ࡸࡶࡪࠨᓹ")
    bstack1l111lll11l_opy_ = bstack1l1_opy_ (u"ࠣࡶࡨࡷࡹࡥࡦࡢ࡫࡯ࡹࡷ࡫࡟ࡵࡻࡳࡩࠧᓺ")
    bstack1l11ll11ll1_opy_ = bstack1l1_opy_ (u"ࠤࡷࡩࡸࡺ࡟࡭ࡱࡪࡷࠧᓻ")
    bstack1l11lll111l_opy_ = bstack1l1_opy_ (u"ࠥࡸࡪࡹࡴࡠ࡯ࡨࡸࡦࠨᓼ")
    bstack1l111l11ll1_opy_ = bstack1l1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡶࡧࡴࡶࡥࡴࠩᓽ")
    bstack1l1l111l1ll_opy_ = bstack1l1_opy_ (u"ࠧࡧࡵࡵࡱࡰࡥࡹ࡫࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠࡰࡤࡱࡪࠨᓾ")
    bstack1l111ll1111_opy_ = bstack1l1_opy_ (u"ࠨࡥࡷࡧࡱࡸࡤࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠤᓿ")
    bstack1l11ll11l1l_opy_ = bstack1l1_opy_ (u"ࠢࡦࡸࡨࡲࡹࡥࡥ࡯ࡦࡨࡨࡤࡧࡴࠣᔀ")
    bstack1l11ll1lll1_opy_ = bstack1l1_opy_ (u"ࠣࡪࡲࡳࡰࡥࡩࡥࠤᔁ")
    bstack1l11l1ll1l1_opy_ = bstack1l1_opy_ (u"ࠤ࡫ࡳࡴࡱ࡟ࡳࡧࡶࡹࡱࡺࠢᔂ")
    bstack1l11llll111_opy_ = bstack1l1_opy_ (u"ࠥ࡬ࡴࡵ࡫ࡠ࡮ࡲ࡫ࡸࠨᔃ")
    bstack1l11l1l1lll_opy_ = bstack1l1_opy_ (u"ࠦ࡭ࡵ࡯࡬ࡡࡱࡥࡲ࡫ࠢᔄ")
    bstack1l111llllll_opy_ = bstack1l1_opy_ (u"ࠧࡲ࡯ࡨࡵࠥᔅ")
    bstack1l11ll111l1_opy_ = bstack1l1_opy_ (u"ࠨࡣࡶࡵࡷࡳࡲࡥ࡭ࡦࡶࡤࡨࡦࡺࡡࠣᔆ")
    bstack1l111ll1ll1_opy_ = bstack1l1_opy_ (u"ࠢࡱࡧࡱࡨ࡮ࡴࡧࠣᔇ")
    bstack1l111l1lll1_opy_ = bstack1l1_opy_ (u"ࠣࡲࡨࡲࡩ࡯࡮ࡨࠤᔈ")
    bstack1l1lllll11l_opy_ = bstack1l1_opy_ (u"ࠤࡗࡉࡘ࡚࡟ࡔࡅࡕࡉࡊࡔࡓࡉࡑࡗࠦᔉ")
    bstack1ll1111l11l_opy_ = bstack1l1_opy_ (u"ࠥࡘࡊ࡙ࡔࡠࡎࡒࡋࠧᔊ")
    bstack1l1ll1lllll_opy_ = bstack1l1_opy_ (u"࡙ࠦࡋࡓࡕࡡࡄࡘ࡙ࡇࡃࡉࡏࡈࡒ࡙ࠨᔋ")
    bstack11111l1l1l_opy_: Dict[str, bstack1lll11l1ll1_opy_] = dict()
    bstack1l1111llll1_opy_: Dict[str, List[Callable]] = dict()
    bstack1ll1l1ll1ll_opy_: List[str]
    bstack1l111lll1l1_opy_: Dict[str, str]
    def __init__(
        self,
        bstack1ll1l1ll1ll_opy_: List[str],
        bstack1l111lll1l1_opy_: Dict[str, str],
        bstack1111l1llll_opy_: bstack1111l1ll1l_opy_
    ):
        self.bstack1ll1l1ll1ll_opy_ = bstack1ll1l1ll1ll_opy_
        self.bstack1l111lll1l1_opy_ = bstack1l111lll1l1_opy_
        self.bstack1111l1llll_opy_ = bstack1111l1llll_opy_
    def track_event(
        self,
        context: bstack1l11l1l11l1_opy_,
        test_framework_state: bstack1lll1l1lll1_opy_,
        test_hook_state: bstack1llll111ll1_opy_,
        *args,
        **kwargs,
    ):
        self.logger.debug(bstack1l1_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࡁࢀࢃࠠࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦ࠿ࡾࢁࠥࡧࡲࡨࡵࡀࡿࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࡻࡾࠤᔌ").format(test_framework_state,test_hook_state,args,kwargs))
    def bstack1l11l11111l_opy_(
        self,
        instance: bstack1lll11l1ll1_opy_,
        bstack111111l11l_opy_: Tuple[bstack1lll1l1lll1_opy_, bstack1llll111ll1_opy_],
        *args,
        **kwargs,
    ):
        bstack1l1l1111l11_opy_ = TestFramework.bstack1l11llllll1_opy_(bstack111111l11l_opy_)
        if not bstack1l1l1111l11_opy_ in TestFramework.bstack1l1111llll1_opy_:
            return
        self.logger.debug(bstack1l1_opy_ (u"ࠨࡩ࡯ࡸࡲ࡯࡮ࡴࡧࠡࡽࢀࠤࡨࡧ࡬࡭ࡤࡤࡧࡰࡹࠢᔍ").format(len(TestFramework.bstack1l1111llll1_opy_[bstack1l1l1111l11_opy_])))
        for callback in TestFramework.bstack1l1111llll1_opy_[bstack1l1l1111l11_opy_]:
            try:
                callback(self, instance, bstack111111l11l_opy_, *args, **kwargs)
            except Exception as e:
                self.logger.error(bstack1l1_opy_ (u"ࠢࡦࡴࡵࡳࡷࠦࡩ࡯ࡸࡲ࡯࡮ࡴࡧࠡࡥࡤࡰࡱࡨࡡࡤ࡭࠽ࠤࢀࢃࠢᔎ").format(e))
                traceback.print_exc()
    @abc.abstractmethod
    def bstack1ll11111ll1_opy_(self):
        return
    @abc.abstractmethod
    def bstack1ll11111l1l_opy_(self, instance, bstack111111l11l_opy_):
        return
    @abc.abstractmethod
    def bstack1ll111l1l1l_opy_(self, instance, bstack111111l11l_opy_):
        return
    @staticmethod
    def bstack111111lll1_opy_(target: object, strict=True):
        if target is None:
            return None
        ctx = bstack111111l1l1_opy_.create_context(target)
        instance = TestFramework.bstack11111l1l1l_opy_.get(ctx.id, None)
        if instance and instance.bstack11111l1lll_opy_(target):
            return instance
        return instance if instance and not strict else None
    @staticmethod
    def bstack1l1lllll1l1_opy_(reverse=True) -> List[bstack1lll11l1ll1_opy_]:
        thread_id = threading.get_ident()
        process_id = os.getpid()
        return sorted(
            filter(
                lambda t: t.context.thread_id == thread_id
                and t.context.process_id == process_id,
                TestFramework.bstack11111l1l1l_opy_.values(),
            ),
            key=lambda t: t.bstack111111ll11_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack1111111l11_opy_(ctx: bstack1111l111ll_opy_, reverse=True) -> List[bstack1lll11l1ll1_opy_]:
        return sorted(
            filter(
                lambda t: t.context.thread_id == ctx.thread_id
                and t.context.process_id == ctx.process_id,
                TestFramework.bstack11111l1l1l_opy_.values(),
            ),
            key=lambda t: t.bstack111111ll11_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack11111llll1_opy_(instance: bstack1lll11l1ll1_opy_, key: str):
        return instance and key in instance.data
    @staticmethod
    def bstack1111l11lll_opy_(instance: bstack1lll11l1ll1_opy_, key: str, default_value=None):
        return instance.data.get(key, default_value) if instance else default_value
    @staticmethod
    def bstack11111111ll_opy_(instance: bstack1lll11l1ll1_opy_, key: str, value: Any):
        TestFramework.logger.debug(bstack1l1_opy_ (u"ࠣࡵࡨࡸࡤࡹࡴࡢࡶࡨ࠾ࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࡼࡿࠣ࡯ࡪࡿ࠽ࡼࡿࠣࡺࡦࡲࡵࡦ࠿ࡾࢁࠧᔏ").format(instance.ref(),key,value))
        instance.data[key] = value
        return True
    @staticmethod
    def bstack1l11l111lll_opy_(instance: bstack1lll11l1ll1_opy_, entries: Dict[str, Any]):
        TestFramework.logger.debug(bstack1l1_opy_ (u"ࠤࡶࡩࡹࡥࡳࡵࡣࡷࡩࡤ࡫࡮ࡵࡴ࡬ࡩࡸࡀࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࡾࢁࠥ࡫࡮ࡵࡴ࡬ࡩࡸࡃࡻࡾࠤᔐ").format(instance.ref(),entries,))
        instance.data.update(entries)
        return True
    @staticmethod
    def bstack1l1111ll11l_opy_(instance: bstack1lll1l1lll1_opy_, key: str, value: Any):
        TestFramework.logger.debug(bstack1l1_opy_ (u"ࠥࡹࡵࡪࡡࡵࡧࡢࡷࡹࡧࡴࡦ࠼ࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࢁࡽࠡ࡭ࡨࡽࡂࢁࡽࠡࡸࡤࡰࡺ࡫࠽ࡼࡿࠥᔑ").format(instance.ref(),key,value))
        instance.data.update(key, value)
        return True
    @staticmethod
    def get_data(key: str, target: object, strict=True, default_value=None):
        instance = TestFramework.bstack111111lll1_opy_(target, strict)
        return TestFramework.bstack1111l11lll_opy_(instance, key, default_value)
    @staticmethod
    def set_data(key: str, value: Any, target: object, strict=True):
        instance = TestFramework.bstack111111lll1_opy_(target, strict)
        if not instance:
            return False
        instance.data[key] = value
        return True
    @staticmethod
    def bstack1l11l1ll11l_opy_(instance: bstack1lll11l1ll1_opy_, key: str, value: object):
        if instance == None:
            return
        instance.data[key] = value
    @staticmethod
    def bstack1l111l1ll1l_opy_(instance: bstack1lll11l1ll1_opy_, key: str):
        return instance.data[key]
    @staticmethod
    def bstack1l11llllll1_opy_(bstack111111l11l_opy_: Tuple[bstack1lll1l1lll1_opy_, bstack1llll111ll1_opy_]):
        return bstack1l1_opy_ (u"ࠦ࠿ࠨᔒ").join((bstack1lll1l1lll1_opy_(bstack111111l11l_opy_[0]).name, bstack1llll111ll1_opy_(bstack111111l11l_opy_[1]).name))
    @staticmethod
    def bstack1ll1l1ll11l_opy_(bstack111111l11l_opy_: Tuple[bstack1lll1l1lll1_opy_, bstack1llll111ll1_opy_], callback: Callable):
        bstack1l1l1111l11_opy_ = TestFramework.bstack1l11llllll1_opy_(bstack111111l11l_opy_)
        TestFramework.logger.debug(bstack1l1_opy_ (u"ࠧࡹࡥࡵࡡ࡫ࡳࡴࡱ࡟ࡤࡣ࡯ࡰࡧࡧࡣ࡬࠼ࠣ࡬ࡴࡵ࡫ࡠࡴࡨ࡫࡮ࡹࡴࡳࡻࡢ࡯ࡪࡿ࠽ࡼࡿࠥᔓ").format(bstack1l1l1111l11_opy_))
        if not bstack1l1l1111l11_opy_ in TestFramework.bstack1l1111llll1_opy_:
            TestFramework.bstack1l1111llll1_opy_[bstack1l1l1111l11_opy_] = []
        TestFramework.bstack1l1111llll1_opy_[bstack1l1l1111l11_opy_].append(callback)
    @staticmethod
    def bstack1ll111111l1_opy_(o):
        klass = o.__class__
        module = klass.__module__
        if module == bstack1l1_opy_ (u"ࠨࡢࡶ࡫࡯ࡸ࡮ࡴࡳࠣᔔ"):
            return klass.__qualname__
        return module + bstack1l1_opy_ (u"ࠢ࠯ࠤᔕ") + klass.__qualname__
    @staticmethod
    def bstack1ll111lllll_opy_(obj, keys, default_value=None):
        return {k: getattr(obj, k, default_value) for k in keys}