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
import json
import os
import grpc
from browserstack_sdk import sdk_pb2 as structs
from packaging import version
import traceback
from browserstack_sdk.sdk_cli.bstack1llll11ll11_opy_ import bstack1llllll1l1l_opy_
from browserstack_sdk.sdk_cli.bstack11111l1ll1_opy_ import (
    bstack111111ll1l_opy_,
    bstack111111l11l_opy_,
    bstack11111l1l1l_opy_,
)
from browserstack_sdk.sdk_cli.bstack1lll111llll_opy_ import bstack1llllll1l11_opy_
from datetime import datetime
from typing import Tuple, Any
from bstack_utils.messages import bstack11lll11l1l_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
import threading
import os
from bstack_utils.bstack1lll111l_opy_ import bstack1ll1llllll1_opy_
class bstack1lllll11l11_opy_(bstack1llllll1l1l_opy_):
    bstack1l1l1l11l1l_opy_ = bstack1l1ll11_opy_ (u"ࠢࡳࡧࡪ࡭ࡸࡺࡥࡳࡡ࡬ࡲ࡮ࡺࠢኴ")
    bstack1l1l1l1111l_opy_ = bstack1l1ll11_opy_ (u"ࠣࡴࡨ࡫࡮ࡹࡴࡦࡴࡢࡷࡹࡧࡲࡵࠤኵ")
    bstack1l1l11l1lll_opy_ = bstack1l1ll11_opy_ (u"ࠤࡵࡩ࡬࡯ࡳࡵࡧࡵࡣࡸࡺ࡯ࡱࠤ኶")
    def __init__(self, bstack1llllll111l_opy_):
        super().__init__()
        bstack1llllll1l11_opy_.bstack1ll1l1ll1l1_opy_((bstack111111ll1l_opy_.bstack11111111ll_opy_, bstack111111l11l_opy_.PRE), self.bstack1l1l1l11l11_opy_)
        bstack1llllll1l11_opy_.bstack1ll1l1ll1l1_opy_((bstack111111ll1l_opy_.bstack1111l1l111_opy_, bstack111111l11l_opy_.PRE), self.bstack1ll11lll11l_opy_)
        bstack1llllll1l11_opy_.bstack1ll1l1ll1l1_opy_((bstack111111ll1l_opy_.bstack1111l1l111_opy_, bstack111111l11l_opy_.POST), self.bstack1l1l11ll1l1_opy_)
        bstack1llllll1l11_opy_.bstack1ll1l1ll1l1_opy_((bstack111111ll1l_opy_.bstack1111l1l111_opy_, bstack111111l11l_opy_.POST), self.bstack1l1l11l11ll_opy_)
        bstack1llllll1l11_opy_.bstack1ll1l1ll1l1_opy_((bstack111111ll1l_opy_.QUIT, bstack111111l11l_opy_.POST), self.bstack1l1l11l1l1l_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l1l1l11l11_opy_(
        self,
        f: bstack1llllll1l11_opy_,
        driver: object,
        exec: Tuple[bstack11111l1l1l_opy_, str],
        bstack11111l11ll_opy_: Tuple[bstack111111ll1l_opy_, bstack111111l11l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1l1ll11_opy_ (u"ࠥࡣࡤ࡯࡮ࡪࡶࡢࡣࠧ኷"):
            return
        def wrapped(driver, init, *args, **kwargs):
            self.bstack1l1l11l1l11_opy_(instance, f, kwargs)
            self.logger.debug(bstack1l1ll11_opy_ (u"ࠦࡩࡸࡩࡷࡧࡵ࠲ࢀࡳࡥࡵࡪࡲࡨࡤࡴࡡ࡮ࡧࢀࠤࡵࡲࡡࡵࡨࡲࡶࡲࡥࡩ࡯ࡦࡨࡼࡂࢁࡦ࠯ࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢ࡭ࡳࡪࡥࡹࡿ࠽ࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥኸ") + str(kwargs) + bstack1l1ll11_opy_ (u"ࠧࠨኹ"))
            threading.current_thread().bstackSessionDriver = driver
            return init(driver, *args, **kwargs)
        return wrapped
    def bstack1ll11lll11l_opy_(
        self,
        f: bstack1llllll1l11_opy_,
        driver: object,
        exec: Tuple[bstack11111l1l1l_opy_, str],
        bstack11111l11ll_opy_: Tuple[bstack111111ll1l_opy_, bstack111111l11l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if f.bstack111111ll11_opy_(instance, bstack1lllll11l11_opy_.bstack1l1l1l11l1l_opy_, False):
            return
        if not f.bstack11111l1111_opy_(instance, bstack1llllll1l11_opy_.bstack1ll11lllll1_opy_):
            return
        platform_index = f.bstack111111ll11_opy_(instance, bstack1llllll1l11_opy_.bstack1ll11lllll1_opy_)
        if f.bstack1ll1ll111l1_opy_(method_name, *args) and len(args) > 1:
            bstack1l1l1llll_opy_ = datetime.now()
            hub_url = bstack1llllll1l11_opy_.hub_url(driver)
            self.logger.warning(bstack1l1ll11_opy_ (u"ࠨࡨࡶࡤࡢࡹࡷࡲ࠽ࠣኺ") + str(hub_url) + bstack1l1ll11_opy_ (u"ࠢࠣኻ"))
            bstack1l1l11lll11_opy_ = args[1][bstack1l1ll11_opy_ (u"ࠣࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠢኼ")] if isinstance(args[1], dict) and bstack1l1ll11_opy_ (u"ࠤࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠣኽ") in args[1] else None
            bstack1l1l11l111l_opy_ = bstack1l1ll11_opy_ (u"ࠥࡥࡱࡽࡡࡺࡵࡐࡥࡹࡩࡨࠣኾ")
            if isinstance(bstack1l1l11lll11_opy_, dict):
                bstack1l1l1llll_opy_ = datetime.now()
                r = self.bstack1l1l1l1ll11_opy_(
                    instance.ref(),
                    platform_index,
                    f.framework_name,
                    f.framework_version,
                    hub_url
                )
                instance.bstack11lll111l_opy_(bstack1l1ll11_opy_ (u"ࠦ࡬ࡸࡰࡤ࠼ࡵࡩ࡬࡯ࡳࡵࡧࡵࡣ࡮ࡴࡩࡵࠤ኿"), datetime.now() - bstack1l1l1llll_opy_)
                try:
                    if not r.success:
                        self.logger.info(bstack1l1ll11_opy_ (u"ࠧࡹ࡯࡮ࡧࡷ࡬࡮ࡴࡧࠡࡹࡨࡲࡹࠦࡷࡳࡱࡱ࡫࠿ࠦࠢዀ") + str(r) + bstack1l1ll11_opy_ (u"ࠨࠢ዁"))
                        return
                    if r.hub_url:
                        f.bstack1l1l11llll1_opy_(instance, driver, r.hub_url)
                        f.bstack111111l1l1_opy_(instance, bstack1lllll11l11_opy_.bstack1l1l1l11l1l_opy_, True)
                except Exception as e:
                    self.logger.error(bstack1l1ll11_opy_ (u"ࠢࡦࡴࡵࡳࡷࠨዂ"), e)
    def bstack1l1l11ll1l1_opy_(
        self,
        f: bstack1llllll1l11_opy_,
        driver: object,
        exec: Tuple[bstack11111l1l1l_opy_, str],
        bstack11111l11ll_opy_: Tuple[bstack111111ll1l_opy_, bstack111111l11l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
            session_id = bstack1llllll1l11_opy_.session_id(driver)
            if session_id:
                bstack1l1l11lllll_opy_ = bstack1l1ll11_opy_ (u"ࠣࡽࢀ࠾ࡸࡺࡡࡳࡶࠥዃ").format(session_id)
                bstack1ll1llllll1_opy_.mark(bstack1l1l11lllll_opy_)
    def bstack1l1l11l11ll_opy_(
        self,
        f: bstack1llllll1l11_opy_,
        driver: object,
        exec: Tuple[bstack11111l1l1l_opy_, str],
        bstack11111l11ll_opy_: Tuple[bstack111111ll1l_opy_, bstack111111l11l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if f.bstack111111ll11_opy_(instance, bstack1lllll11l11_opy_.bstack1l1l1l1111l_opy_, False):
            return
        ref = instance.ref()
        hub_url = bstack1llllll1l11_opy_.hub_url(driver)
        if not hub_url:
            self.logger.warning(bstack1l1ll11_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡶࡡࡳࡵࡨࠤ࡭ࡻࡢࡠࡷࡵࡰࡂࠨዄ") + str(hub_url) + bstack1l1ll11_opy_ (u"ࠥࠦዅ"))
            return
        framework_session_id = bstack1llllll1l11_opy_.session_id(driver)
        if not framework_session_id:
            self.logger.warning(bstack1l1ll11_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡱࡣࡵࡷࡪࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡩࡸࡹࡩࡰࡰࡢ࡭ࡩࡃࠢ዆") + str(framework_session_id) + bstack1l1ll11_opy_ (u"ࠧࠨ዇"))
            return
        if bstack1llllll1l11_opy_.bstack1l1l11ll11l_opy_(*args) == bstack1llllll1l11_opy_.bstack1l1l11lll1l_opy_:
            bstack1l1l1l111l1_opy_ = bstack1l1ll11_opy_ (u"ࠨࡻࡾ࠼ࡨࡲࡩࠨወ").format(framework_session_id)
            bstack1l1l11lllll_opy_ = bstack1l1ll11_opy_ (u"ࠢࡼࡿ࠽ࡷࡹࡧࡲࡵࠤዉ").format(framework_session_id)
            bstack1ll1llllll1_opy_.end(
                label=bstack1l1ll11_opy_ (u"ࠣࡵࡧ࡯࠿ࡪࡲࡪࡸࡨࡶ࠿ࡶ࡯ࡴࡶ࠰࡭ࡳ࡯ࡴࡪࡣ࡯࡭ࡿࡧࡴࡪࡱࡱࠦዊ"),
                start=bstack1l1l11lllll_opy_,
                end=bstack1l1l1l111l1_opy_,
                status=True,
                failure=None
            )
            bstack1l1l1llll_opy_ = datetime.now()
            r = self.bstack1l1l11ll1ll_opy_(
                ref,
                f.bstack111111ll11_opy_(instance, bstack1llllll1l11_opy_.bstack1ll11lllll1_opy_, 0),
                f.framework_name,
                f.framework_version,
                framework_session_id,
                hub_url,
            )
            instance.bstack11lll111l_opy_(bstack1l1ll11_opy_ (u"ࠤࡪࡶࡵࡩ࠺ࡳࡧࡪ࡭ࡸࡺࡥࡳࡡࡶࡸࡦࡸࡴࠣዋ"), datetime.now() - bstack1l1l1llll_opy_)
            f.bstack111111l1l1_opy_(instance, bstack1lllll11l11_opy_.bstack1l1l1l1111l_opy_, r.success)
    def bstack1l1l11l1l1l_opy_(
        self,
        f: bstack1llllll1l11_opy_,
        driver: object,
        exec: Tuple[bstack11111l1l1l_opy_, str],
        bstack11111l11ll_opy_: Tuple[bstack111111ll1l_opy_, bstack111111l11l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if f.bstack111111ll11_opy_(instance, bstack1lllll11l11_opy_.bstack1l1l11l1lll_opy_, False):
            return
        ref = instance.ref()
        framework_session_id = bstack1llllll1l11_opy_.session_id(driver)
        hub_url = bstack1llllll1l11_opy_.hub_url(driver)
        bstack1l1l1llll_opy_ = datetime.now()
        r = self.bstack1l1l1l1l11l_opy_(
            ref,
            f.bstack111111ll11_opy_(instance, bstack1llllll1l11_opy_.bstack1ll11lllll1_opy_, 0),
            f.framework_name,
            f.framework_version,
            framework_session_id,
            hub_url,
        )
        instance.bstack11lll111l_opy_(bstack1l1ll11_opy_ (u"ࠥ࡫ࡷࡶࡣ࠻ࡴࡨ࡫࡮ࡹࡴࡦࡴࡢࡷࡹࡵࡰࠣዌ"), datetime.now() - bstack1l1l1llll_opy_)
        f.bstack111111l1l1_opy_(instance, bstack1lllll11l11_opy_.bstack1l1l11l1lll_opy_, r.success)
    @measure(event_name=EVENTS.bstack11111111_opy_, stage=STAGE.bstack1ll1111ll1_opy_)
    def bstack1l1ll1l111l_opy_(self, platform_index: int, ref, user_input_params: bytes):
        req = structs.DriverInitRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.user_input_params = user_input_params
        req.ref = ref
        self.logger.debug(bstack1l1ll11_opy_ (u"ࠦࡷ࡫ࡧࡪࡵࡷࡩࡷࡥࡷࡦࡤࡧࡶ࡮ࡼࡥࡳࡡ࡬ࡲ࡮ࡺ࠺ࠡࠤው") + str(req) + bstack1l1ll11_opy_ (u"ࠧࠨዎ"))
        try:
            r = self.bstack1llll111ll1_opy_.DriverInit(req)
            if not r.success:
                self.logger.debug(bstack1l1ll11_opy_ (u"ࠨࡲࡦࡥࡨ࡭ࡻ࡫ࡤࠡࡨࡵࡳࡲࠦࡳࡦࡴࡹࡩࡷࡀࠠࡴࡷࡦࡧࡪࡹࡳ࠾ࠤዏ") + str(r.success) + bstack1l1ll11_opy_ (u"ࠢࠣዐ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1l1ll11_opy_ (u"ࠣࡴࡳࡧ࠲࡫ࡲࡳࡱࡵ࠾ࠥࠨዑ") + str(e) + bstack1l1ll11_opy_ (u"ࠤࠥዒ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l1l1l1l111_opy_, stage=STAGE.bstack1ll1111ll1_opy_)
    def bstack1l1l1l1ll11_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        hub_url: str
    ):
        self.bstack1ll1lll111l_opy_()
        req = structs.AutomationFrameworkInitRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.hub_url = hub_url
        self.logger.debug(bstack1l1ll11_opy_ (u"ࠥࡶࡪ࡭ࡩࡴࡶࡨࡶࡤ࡯࡮ࡪࡶ࠽ࠤࠧዓ") + str(req) + bstack1l1ll11_opy_ (u"ࠦࠧዔ"))
        try:
            r = self.bstack1llll111ll1_opy_.AutomationFrameworkInit(req)
            if not r.success:
                self.logger.debug(bstack1l1ll11_opy_ (u"ࠧࡸࡥࡤࡧ࡬ࡺࡪࡪࠠࡧࡴࡲࡱࠥࡹࡥࡳࡸࡨࡶ࠿ࠦࡳࡶࡥࡦࡩࡸࡹ࠽ࠣዕ") + str(r.success) + bstack1l1ll11_opy_ (u"ࠨࠢዖ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1l1ll11_opy_ (u"ࠢࡳࡲࡦ࠱ࡪࡸࡲࡰࡴ࠽ࠤࠧ዗") + str(e) + bstack1l1ll11_opy_ (u"ࠣࠤዘ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l1l11ll111_opy_, stage=STAGE.bstack1ll1111ll1_opy_)
    def bstack1l1l11ll1ll_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        framework_session_id: str,
        hub_url: str,
    ):
        self.bstack1ll1lll111l_opy_()
        req = structs.AutomationFrameworkStartRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.framework_session_id = framework_session_id
        req.hub_url = hub_url
        self.logger.debug(bstack1l1ll11_opy_ (u"ࠤࡵࡩ࡬࡯ࡳࡵࡧࡵࡣࡸࡺࡡࡳࡶ࠽ࠤࠧዙ") + str(req) + bstack1l1ll11_opy_ (u"ࠥࠦዚ"))
        try:
            r = self.bstack1llll111ll1_opy_.AutomationFrameworkStart(req)
            if not r.success:
                self.logger.debug(bstack1l1ll11_opy_ (u"ࠦࡷ࡫ࡣࡦ࡫ࡹࡩࡩࠦࡦࡳࡱࡰࠤࡸ࡫ࡲࡷࡧࡵ࠾ࠥࠨዛ") + str(r) + bstack1l1ll11_opy_ (u"ࠧࠨዜ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1l1ll11_opy_ (u"ࠨࡲࡱࡥ࠰ࡩࡷࡸ࡯ࡳ࠼ࠣࠦዝ") + str(e) + bstack1l1ll11_opy_ (u"ࠢࠣዞ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l1l1l11ll1_opy_, stage=STAGE.bstack1ll1111ll1_opy_)
    def bstack1l1l1l1l11l_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        framework_session_id: str,
        hub_url: str,
    ):
        self.bstack1ll1lll111l_opy_()
        req = structs.AutomationFrameworkStopRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.framework_session_id = framework_session_id
        req.hub_url = hub_url
        self.logger.debug(bstack1l1ll11_opy_ (u"ࠣࡴࡨ࡫࡮ࡹࡴࡦࡴࡢࡷࡹࡵࡰ࠻ࠢࠥዟ") + str(req) + bstack1l1ll11_opy_ (u"ࠤࠥዠ"))
        try:
            r = self.bstack1llll111ll1_opy_.AutomationFrameworkStop(req)
            if not r.success:
                self.logger.debug(bstack1l1ll11_opy_ (u"ࠥࡶࡪࡩࡥࡪࡸࡨࡨࠥ࡬ࡲࡰ࡯ࠣࡷࡪࡸࡶࡦࡴ࠽ࠤࠧዡ") + str(r) + bstack1l1ll11_opy_ (u"ࠦࠧዢ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1l1ll11_opy_ (u"ࠧࡸࡰࡤ࠯ࡨࡶࡷࡵࡲ࠻ࠢࠥዣ") + str(e) + bstack1l1ll11_opy_ (u"ࠨࠢዤ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack11l1llll_opy_, stage=STAGE.bstack1ll1111ll1_opy_)
    def bstack1l1l11l1l11_opy_(self, instance: bstack11111l1l1l_opy_, f: bstack1llllll1l11_opy_, kwargs):
        bstack1l1l1l111ll_opy_ = version.parse(f.framework_version)
        bstack1l1l1l11lll_opy_ = kwargs.get(bstack1l1ll11_opy_ (u"ࠢࡰࡲࡷ࡭ࡴࡴࡳࠣዥ"))
        bstack1l1l1l1l1l1_opy_ = kwargs.get(bstack1l1ll11_opy_ (u"ࠣࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠣዦ"))
        bstack1l1ll11111l_opy_ = {}
        bstack1l1l1l11111_opy_ = {}
        bstack1l1l11l1ll1_opy_ = None
        bstack1l1l1l1l1ll_opy_ = {}
        if bstack1l1l1l1l1l1_opy_ is not None or bstack1l1l1l11lll_opy_ is not None: # check top level caps
            if bstack1l1l1l1l1l1_opy_ is not None:
                bstack1l1l1l1l1ll_opy_[bstack1l1ll11_opy_ (u"ࠩࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩዧ")] = bstack1l1l1l1l1l1_opy_
            if bstack1l1l1l11lll_opy_ is not None and callable(getattr(bstack1l1l1l11lll_opy_, bstack1l1ll11_opy_ (u"ࠥࡸࡴࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠧየ"))):
                bstack1l1l1l1l1ll_opy_[bstack1l1ll11_opy_ (u"ࠫࡴࡶࡴࡪࡱࡱࡷࡤࡧࡳࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧዩ")] = bstack1l1l1l11lll_opy_.to_capabilities()
        response = self.bstack1l1ll1l111l_opy_(f.platform_index, instance.ref(), json.dumps(bstack1l1l1l1l1ll_opy_).encode(bstack1l1ll11_opy_ (u"ࠧࡻࡴࡧ࠯࠻ࠦዪ")))
        if response is not None and response.capabilities:
            bstack1l1ll11111l_opy_ = json.loads(response.capabilities.decode(bstack1l1ll11_opy_ (u"ࠨࡵࡵࡨ࠰࠼ࠧያ")))
            if not bstack1l1ll11111l_opy_: # empty caps bstack1l1ll111ll1_opy_ bstack1l1ll11l11l_opy_ bstack1l1ll11ll1l_opy_ bstack1lll111l1l1_opy_ or error in processing
                return
            bstack1l1l11l1ll1_opy_ = f.bstack1llll1ll1l1_opy_[bstack1l1ll11_opy_ (u"ࠢࡤࡴࡨࡥࡹ࡫࡟ࡰࡲࡷ࡭ࡴࡴࡳࡠࡨࡵࡳࡲࡥࡣࡢࡲࡶࠦዬ")](bstack1l1ll11111l_opy_)
        if bstack1l1l1l11lll_opy_ is not None and bstack1l1l1l111ll_opy_ >= version.parse(bstack1l1ll11_opy_ (u"ࠨ࠵࠱࠼࠳࠶ࠧይ")):
            bstack1l1l1l11111_opy_ = None
        if (
                not bstack1l1l1l11lll_opy_ and not bstack1l1l1l1l1l1_opy_
        ) or (
                bstack1l1l1l111ll_opy_ < version.parse(bstack1l1ll11_opy_ (u"ࠩ࠶࠲࠽࠴࠰ࠨዮ"))
        ):
            bstack1l1l1l11111_opy_ = {}
            bstack1l1l1l11111_opy_.update(bstack1l1ll11111l_opy_)
        self.logger.info(bstack11lll11l1l_opy_)
        if os.environ.get(bstack1l1ll11_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄ࡙࡙ࡕࡍࡂࡖࡌࡓࡓࠨዯ")).lower().__eq__(bstack1l1ll11_opy_ (u"ࠦࡹࡸࡵࡦࠤደ")):
            kwargs.update(
                {
                    bstack1l1ll11_opy_ (u"ࠧࡩ࡯࡮࡯ࡤࡲࡩࡥࡥࡹࡧࡦࡹࡹࡵࡲࠣዱ"): f.bstack1l1l11l11l1_opy_,
                }
            )
        if bstack1l1l1l111ll_opy_ >= version.parse(bstack1l1ll11_opy_ (u"࠭࠴࠯࠳࠳࠲࠵࠭ዲ")):
            if bstack1l1l1l1l1l1_opy_ is not None:
                del kwargs[bstack1l1ll11_opy_ (u"ࠢࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠢዳ")]
            kwargs.update(
                {
                    bstack1l1ll11_opy_ (u"ࠣࡱࡳࡸ࡮ࡵ࡮ࡴࠤዴ"): bstack1l1l11l1ll1_opy_,
                    bstack1l1ll11_opy_ (u"ࠤ࡮ࡩࡪࡶ࡟ࡢ࡮࡬ࡺࡪࠨድ"): True,
                    bstack1l1ll11_opy_ (u"ࠥࡪ࡮ࡲࡥࡠࡦࡨࡸࡪࡩࡴࡰࡴࠥዶ"): None,
                }
            )
        elif bstack1l1l1l111ll_opy_ >= version.parse(bstack1l1ll11_opy_ (u"ࠫ࠸࠴࠸࠯࠲ࠪዷ")):
            kwargs.update(
                {
                    bstack1l1ll11_opy_ (u"ࠧࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠧዸ"): bstack1l1l1l11111_opy_,
                    bstack1l1ll11_opy_ (u"ࠨ࡯ࡱࡶ࡬ࡳࡳࡹࠢዹ"): bstack1l1l11l1ll1_opy_,
                    bstack1l1ll11_opy_ (u"ࠢ࡬ࡧࡨࡴࡤࡧ࡬ࡪࡸࡨࠦዺ"): True,
                    bstack1l1ll11_opy_ (u"ࠣࡨ࡬ࡰࡪࡥࡤࡦࡶࡨࡧࡹࡵࡲࠣዻ"): None,
                }
            )
        elif bstack1l1l1l111ll_opy_ >= version.parse(bstack1l1ll11_opy_ (u"ࠩ࠵࠲࠺࠹࠮࠱ࠩዼ")):
            kwargs.update(
                {
                    bstack1l1ll11_opy_ (u"ࠥࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠥዽ"): bstack1l1l1l11111_opy_,
                    bstack1l1ll11_opy_ (u"ࠦࡰ࡫ࡥࡱࡡࡤࡰ࡮ࡼࡥࠣዾ"): True,
                    bstack1l1ll11_opy_ (u"ࠧ࡬ࡩ࡭ࡧࡢࡨࡪࡺࡥࡤࡶࡲࡶࠧዿ"): None,
                }
            )
        else:
            kwargs.update(
                {
                    bstack1l1ll11_opy_ (u"ࠨࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠨጀ"): bstack1l1l1l11111_opy_,
                    bstack1l1ll11_opy_ (u"ࠢ࡬ࡧࡨࡴࡤࡧ࡬ࡪࡸࡨࠦጁ"): True,
                    bstack1l1ll11_opy_ (u"ࠣࡨ࡬ࡰࡪࡥࡤࡦࡶࡨࡧࡹࡵࡲࠣጂ"): None,
                }
            )