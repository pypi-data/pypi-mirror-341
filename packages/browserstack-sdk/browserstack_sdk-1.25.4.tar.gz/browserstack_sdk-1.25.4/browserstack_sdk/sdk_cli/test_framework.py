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
import os
import threading
import traceback
from typing import Dict, List, Any, Callable, Tuple, Union
import abc
from datetime import datetime, timezone
from dataclasses import dataclass
from browserstack_sdk.sdk_cli.bstack1111l1l1ll_opy_ import bstack1111l1lll1_opy_
from browserstack_sdk.sdk_cli.bstack11111ll11l_opy_ import bstack1111111l11_opy_, bstack1111l1l1l1_opy_
class bstack1lll1ll111l_opy_(Enum):
    PRE = 0
    POST = 1
    def __repr__(self) -> str:
        return bstack1l1ll11_opy_ (u"࡚ࠧࡥࡴࡶࡋࡳࡴࡱࡓࡵࡣࡷࡩ࠳ࢁࡽࠣᓩ").format(self.name)
class bstack1lll11l11l1_opy_(Enum):
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
        return bstack1l1ll11_opy_ (u"ࠨࡔࡦࡵࡷࡊࡷࡧ࡭ࡦࡹࡲࡶࡰ࡙ࡴࡢࡶࡨ࠲ࢀࢃࠢᓪ").format(self.name)
class bstack1lll1ll11l1_opy_(bstack1111111l11_opy_):
    bstack1ll1ll1l111_opy_: List[str]
    bstack1l11l11lll1_opy_: Dict[str, str]
    state: bstack1lll11l11l1_opy_
    bstack11111ll111_opy_: datetime
    bstack111111111l_opy_: datetime
    def __init__(
        self,
        context: bstack1111l1l1l1_opy_,
        bstack1ll1ll1l111_opy_: List[str],
        bstack1l11l11lll1_opy_: Dict[str, str],
        state=bstack1lll11l11l1_opy_.NONE,
    ):
        super().__init__(context)
        self.bstack1ll1ll1l111_opy_ = bstack1ll1ll1l111_opy_
        self.bstack1l11l11lll1_opy_ = bstack1l11l11lll1_opy_
        self.state = state
        self.bstack11111ll111_opy_ = datetime.now(tz=timezone.utc)
        self.bstack111111111l_opy_ = datetime.now(tz=timezone.utc)
    def bstack111111l1l1_opy_(self, bstack111111l1ll_opy_: bstack1lll11l11l1_opy_):
        bstack1111l11ll1_opy_ = bstack1lll11l11l1_opy_(bstack111111l1ll_opy_).name
        if not bstack1111l11ll1_opy_:
            return False
        if bstack111111l1ll_opy_ == self.state:
            return False
        self.state = bstack111111l1ll_opy_
        self.bstack111111111l_opy_ = datetime.now(tz=timezone.utc)
        return True
@dataclass
class bstack1l11ll11l1l_opy_:
    test_framework_name: str
    test_framework_version: str
    platform_index: int
@dataclass
class bstack1lll11llll1_opy_:
    kind: str
    message: str
    level: Union[None, str] = None
    timestamp: Union[None, datetime] = datetime.now(tz=timezone.utc)
    fileName: str = None
    bstack1ll1111llll_opy_: int = None
    bstack1l1lll1l11l_opy_: str = None
    bstack11lll11_opy_: str = None
    bstack1ll1ll111_opy_: str = None
    bstack1l1llll1lll_opy_: str = None
    bstack1l11l1lll1l_opy_: str = None
class TestFramework(abc.ABC):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    bstack1ll1ll1111l_opy_ = bstack1l1ll11_opy_ (u"ࠢࡵࡧࡶࡸࡤࡻࡵࡪࡦࠥᓫ")
    bstack1l11l1l1lll_opy_ = bstack1l1ll11_opy_ (u"ࠣࡶࡨࡷࡹࡥࡩࡥࠤᓬ")
    bstack1ll1l111111_opy_ = bstack1l1ll11_opy_ (u"ࠤࡷࡩࡸࡺ࡟࡯ࡣࡰࡩࠧᓭ")
    bstack1l11l11ll1l_opy_ = bstack1l1ll11_opy_ (u"ࠥࡸࡪࡹࡴࡠࡨ࡬ࡰࡪࡥࡰࡢࡶ࡫ࠦᓮ")
    bstack1l11llll1ll_opy_ = bstack1l1ll11_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡷࡥ࡬ࡹࠢᓯ")
    bstack1l1l1ll111l_opy_ = bstack1l1ll11_opy_ (u"ࠧࡺࡥࡴࡶࡢࡶࡪࡹࡵ࡭ࡶࠥᓰ")
    bstack1ll111ll1ll_opy_ = bstack1l1ll11_opy_ (u"ࠨࡴࡦࡵࡷࡣࡷ࡫ࡳࡶ࡮ࡷࡣࡦࡺࠢᓱ")
    bstack1l1lll11l11_opy_ = bstack1l1ll11_opy_ (u"ࠢࡵࡧࡶࡸࡤࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠤᓲ")
    bstack1l1lll11111_opy_ = bstack1l1ll11_opy_ (u"ࠣࡶࡨࡷࡹࡥࡥ࡯ࡦࡨࡨࡤࡧࡴࠣᓳ")
    bstack1l111l1l1ll_opy_ = bstack1l1ll11_opy_ (u"ࠤࡷࡩࡸࡺ࡟࡭ࡱࡦࡥࡹ࡯࡯࡯ࠤᓴ")
    bstack1ll1l1l11ll_opy_ = bstack1l1ll11_opy_ (u"ࠥࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦࠤᓵ")
    bstack1ll11111ll1_opy_ = bstack1l1ll11_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡼࡥࡳࡵ࡬ࡳࡳࠨᓶ")
    bstack1l111llll11_opy_ = bstack1l1ll11_opy_ (u"ࠧࡺࡥࡴࡶࡢࡧࡴࡪࡥࠣᓷ")
    bstack1l1ll1ll11l_opy_ = bstack1l1ll11_opy_ (u"ࠨࡴࡦࡵࡷࡣࡷ࡫ࡲࡶࡰࡢࡲࡦࡳࡥࠣᓸ")
    bstack1ll11lllll1_opy_ = bstack1l1ll11_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡡ࡬ࡲࡩ࡫ࡸࠣᓹ")
    bstack1l1l1ll1ll1_opy_ = bstack1l1ll11_opy_ (u"ࠣࡶࡨࡷࡹࡥࡦࡢ࡫࡯ࡹࡷ࡫ࠢᓺ")
    bstack1l111l1ll1l_opy_ = bstack1l1ll11_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡧࡣ࡬ࡰࡺࡸࡥࡠࡶࡼࡴࡪࠨᓻ")
    bstack1l11llll1l1_opy_ = bstack1l1ll11_opy_ (u"ࠥࡸࡪࡹࡴࡠ࡮ࡲ࡫ࡸࠨᓼ")
    bstack1l11ll1l1ll_opy_ = bstack1l1ll11_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡰࡩࡹࡧࠢᓽ")
    bstack1l111l11lll_opy_ = bstack1l1ll11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡷࡨࡵࡰࡦࡵࠪᓾ")
    bstack1l1l111l11l_opy_ = bstack1l1ll11_opy_ (u"ࠨࡡࡶࡶࡲࡱࡦࡺࡥࡠࡵࡨࡷࡸ࡯࡯࡯ࡡࡱࡥࡲ࡫ࠢᓿ")
    bstack1l11l11111l_opy_ = bstack1l1ll11_opy_ (u"ࠢࡦࡸࡨࡲࡹࡥࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠥᔀ")
    bstack1l111lll1ll_opy_ = bstack1l1ll11_opy_ (u"ࠣࡧࡹࡩࡳࡺ࡟ࡦࡰࡧࡩࡩࡥࡡࡵࠤᔁ")
    bstack1l111ll1lll_opy_ = bstack1l1ll11_opy_ (u"ࠤ࡫ࡳࡴࡱ࡟ࡪࡦࠥᔂ")
    bstack1l11ll11l11_opy_ = bstack1l1ll11_opy_ (u"ࠥ࡬ࡴࡵ࡫ࡠࡴࡨࡷࡺࡲࡴࠣᔃ")
    bstack1l11ll111ll_opy_ = bstack1l1ll11_opy_ (u"ࠦ࡭ࡵ࡯࡬ࡡ࡯ࡳ࡬ࡹࠢᔄ")
    bstack1l111lll11l_opy_ = bstack1l1ll11_opy_ (u"ࠧ࡮࡯ࡰ࡭ࡢࡲࡦࡳࡥࠣᔅ")
    bstack1l11l1ll111_opy_ = bstack1l1ll11_opy_ (u"ࠨ࡬ࡰࡩࡶࠦᔆ")
    bstack1l11lll11ll_opy_ = bstack1l1ll11_opy_ (u"ࠢࡤࡷࡶࡸࡴࡳ࡟࡮ࡧࡷࡥࡩࡧࡴࡢࠤᔇ")
    bstack1l111ll1ll1_opy_ = bstack1l1ll11_opy_ (u"ࠣࡲࡨࡲࡩ࡯࡮ࡨࠤᔈ")
    bstack1l111l1llll_opy_ = bstack1l1ll11_opy_ (u"ࠤࡳࡩࡳࡪࡩ࡯ࡩࠥᔉ")
    bstack1ll111l1l11_opy_ = bstack1l1ll11_opy_ (u"ࠥࡘࡊ࡙ࡔࡠࡕࡆࡖࡊࡋࡎࡔࡊࡒࡘࠧᔊ")
    bstack1l1lll1l111_opy_ = bstack1l1ll11_opy_ (u"࡙ࠦࡋࡓࡕࡡࡏࡓࡌࠨᔋ")
    bstack1l1lll11ll1_opy_ = bstack1l1ll11_opy_ (u"࡚ࠧࡅࡔࡖࡢࡅ࡙࡚ࡁࡄࡊࡐࡉࡓ࡚ࠢᔌ")
    bstack1111l1111l_opy_: Dict[str, bstack1lll1ll11l1_opy_] = dict()
    bstack1l1111ll1l1_opy_: Dict[str, List[Callable]] = dict()
    bstack1ll1ll1l111_opy_: List[str]
    bstack1l11l11lll1_opy_: Dict[str, str]
    def __init__(
        self,
        bstack1ll1ll1l111_opy_: List[str],
        bstack1l11l11lll1_opy_: Dict[str, str],
        bstack1111l1l1ll_opy_: bstack1111l1lll1_opy_
    ):
        self.bstack1ll1ll1l111_opy_ = bstack1ll1ll1l111_opy_
        self.bstack1l11l11lll1_opy_ = bstack1l11l11lll1_opy_
        self.bstack1111l1l1ll_opy_ = bstack1111l1l1ll_opy_
    def track_event(
        self,
        context: bstack1l11ll11l1l_opy_,
        test_framework_state: bstack1lll11l11l1_opy_,
        test_hook_state: bstack1lll1ll111l_opy_,
        *args,
        **kwargs,
    ):
        self.logger.debug(bstack1l1ll11_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࡂࢁࡽࠡࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࡀࡿࢂࠦࡡࡳࡩࡶࡁࢀࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࡼࡿࠥᔍ").format(test_framework_state,test_hook_state,args,kwargs))
    def bstack1l11ll1l1l1_opy_(
        self,
        instance: bstack1lll1ll11l1_opy_,
        bstack11111l11ll_opy_: Tuple[bstack1lll11l11l1_opy_, bstack1lll1ll111l_opy_],
        *args,
        **kwargs,
    ):
        bstack1l11llllll1_opy_ = TestFramework.bstack1l1l1111l11_opy_(bstack11111l11ll_opy_)
        if not bstack1l11llllll1_opy_ in TestFramework.bstack1l1111ll1l1_opy_:
            return
        self.logger.debug(bstack1l1ll11_opy_ (u"ࠢࡪࡰࡹࡳࡰ࡯࡮ࡨࠢࡾࢁࠥࡩࡡ࡭࡮ࡥࡥࡨࡱࡳࠣᔎ").format(len(TestFramework.bstack1l1111ll1l1_opy_[bstack1l11llllll1_opy_])))
        for callback in TestFramework.bstack1l1111ll1l1_opy_[bstack1l11llllll1_opy_]:
            try:
                callback(self, instance, bstack11111l11ll_opy_, *args, **kwargs)
            except Exception as e:
                self.logger.error(bstack1l1ll11_opy_ (u"ࠣࡧࡵࡶࡴࡸࠠࡪࡰࡹࡳࡰ࡯࡮ࡨࠢࡦࡥࡱࡲࡢࡢࡥ࡮࠾ࠥࢁࡽࠣᔏ").format(e))
                traceback.print_exc()
    @abc.abstractmethod
    def bstack1ll1111111l_opy_(self):
        return
    @abc.abstractmethod
    def bstack1l1lll1l1ll_opy_(self, instance, bstack11111l11ll_opy_):
        return
    @abc.abstractmethod
    def bstack1ll111l111l_opy_(self, instance, bstack11111l11ll_opy_):
        return
    @staticmethod
    def bstack11111111l1_opy_(target: object, strict=True):
        if target is None:
            return None
        ctx = bstack1111111l11_opy_.create_context(target)
        instance = TestFramework.bstack1111l1111l_opy_.get(ctx.id, None)
        if instance and instance.bstack111111lll1_opy_(target):
            return instance
        return instance if instance and not strict else None
    @staticmethod
    def bstack1ll111l1lll_opy_(reverse=True) -> List[bstack1lll1ll11l1_opy_]:
        thread_id = threading.get_ident()
        process_id = os.getpid()
        return sorted(
            filter(
                lambda t: t.context.thread_id == thread_id
                and t.context.process_id == process_id,
                TestFramework.bstack1111l1111l_opy_.values(),
            ),
            key=lambda t: t.bstack11111ll111_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack1111111111_opy_(ctx: bstack1111l1l1l1_opy_, reverse=True) -> List[bstack1lll1ll11l1_opy_]:
        return sorted(
            filter(
                lambda t: t.context.thread_id == ctx.thread_id
                and t.context.process_id == ctx.process_id,
                TestFramework.bstack1111l1111l_opy_.values(),
            ),
            key=lambda t: t.bstack11111ll111_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack11111l1111_opy_(instance: bstack1lll1ll11l1_opy_, key: str):
        return instance and key in instance.data
    @staticmethod
    def bstack111111ll11_opy_(instance: bstack1lll1ll11l1_opy_, key: str, default_value=None):
        return instance.data.get(key, default_value) if instance else default_value
    @staticmethod
    def bstack111111l1l1_opy_(instance: bstack1lll1ll11l1_opy_, key: str, value: Any):
        TestFramework.logger.debug(bstack1l1ll11_opy_ (u"ࠤࡶࡩࡹࡥࡳࡵࡣࡷࡩ࠿ࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࡽࢀࠤࡰ࡫ࡹ࠾ࡽࢀࠤࡻࡧ࡬ࡶࡧࡀࡿࢂࠨᔐ").format(instance.ref(),key,value))
        instance.data[key] = value
        return True
    @staticmethod
    def bstack1l11ll1111l_opy_(instance: bstack1lll1ll11l1_opy_, entries: Dict[str, Any]):
        TestFramework.logger.debug(bstack1l1ll11_opy_ (u"ࠥࡷࡪࡺ࡟ࡴࡶࡤࡸࡪࡥࡥ࡯ࡶࡵ࡭ࡪࡹ࠺ࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࡿࢂࠦࡥ࡯ࡶࡵ࡭ࡪࡹ࠽ࡼࡿࠥᔑ").format(instance.ref(),entries,))
        instance.data.update(entries)
        return True
    @staticmethod
    def bstack1l1111ll11l_opy_(instance: bstack1lll11l11l1_opy_, key: str, value: Any):
        TestFramework.logger.debug(bstack1l1ll11_opy_ (u"ࠦࡺࡶࡤࡢࡶࡨࡣࡸࡺࡡࡵࡧ࠽ࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࡻࡾࠢ࡮ࡩࡾࡃࡻࡾࠢࡹࡥࡱࡻࡥ࠾ࡽࢀࠦᔒ").format(instance.ref(),key,value))
        instance.data.update(key, value)
        return True
    @staticmethod
    def get_data(key: str, target: object, strict=True, default_value=None):
        instance = TestFramework.bstack11111111l1_opy_(target, strict)
        return TestFramework.bstack111111ll11_opy_(instance, key, default_value)
    @staticmethod
    def set_data(key: str, value: Any, target: object, strict=True):
        instance = TestFramework.bstack11111111l1_opy_(target, strict)
        if not instance:
            return False
        instance.data[key] = value
        return True
    @staticmethod
    def bstack1l11l1lllll_opy_(instance: bstack1lll1ll11l1_opy_, key: str, value: object):
        if instance == None:
            return
        instance.data[key] = value
    @staticmethod
    def bstack1l11lll1l11_opy_(instance: bstack1lll1ll11l1_opy_, key: str):
        return instance.data[key]
    @staticmethod
    def bstack1l1l1111l11_opy_(bstack11111l11ll_opy_: Tuple[bstack1lll11l11l1_opy_, bstack1lll1ll111l_opy_]):
        return bstack1l1ll11_opy_ (u"ࠧࡀࠢᔓ").join((bstack1lll11l11l1_opy_(bstack11111l11ll_opy_[0]).name, bstack1lll1ll111l_opy_(bstack11111l11ll_opy_[1]).name))
    @staticmethod
    def bstack1ll1l1ll1l1_opy_(bstack11111l11ll_opy_: Tuple[bstack1lll11l11l1_opy_, bstack1lll1ll111l_opy_], callback: Callable):
        bstack1l11llllll1_opy_ = TestFramework.bstack1l1l1111l11_opy_(bstack11111l11ll_opy_)
        TestFramework.logger.debug(bstack1l1ll11_opy_ (u"ࠨࡳࡦࡶࡢ࡬ࡴࡵ࡫ࡠࡥࡤࡰࡱࡨࡡࡤ࡭࠽ࠤ࡭ࡵ࡯࡬ࡡࡵࡩ࡬࡯ࡳࡵࡴࡼࡣࡰ࡫ࡹ࠾ࡽࢀࠦᔔ").format(bstack1l11llllll1_opy_))
        if not bstack1l11llllll1_opy_ in TestFramework.bstack1l1111ll1l1_opy_:
            TestFramework.bstack1l1111ll1l1_opy_[bstack1l11llllll1_opy_] = []
        TestFramework.bstack1l1111ll1l1_opy_[bstack1l11llllll1_opy_].append(callback)
    @staticmethod
    def bstack1ll1111l1ll_opy_(o):
        klass = o.__class__
        module = klass.__module__
        if module == bstack1l1ll11_opy_ (u"ࠢࡣࡷ࡬ࡰࡹ࡯࡮ࡴࠤᔕ"):
            return klass.__qualname__
        return module + bstack1l1ll11_opy_ (u"ࠣ࠰ࠥᔖ") + klass.__qualname__
    @staticmethod
    def bstack1l1llllll1l_opy_(obj, keys, default_value=None):
        return {k: getattr(obj, k, default_value) for k in keys}