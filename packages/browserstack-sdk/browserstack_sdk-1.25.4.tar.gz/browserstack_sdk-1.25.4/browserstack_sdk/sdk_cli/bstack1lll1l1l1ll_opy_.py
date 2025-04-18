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
import copy
import asyncio
import threading
from browserstack_sdk import sdk_pb2 as structs
from packaging import version
import traceback
from browserstack_sdk.sdk_cli.bstack1llll11ll11_opy_ import bstack1llllll1l1l_opy_
from browserstack_sdk.sdk_cli.bstack11111l1ll1_opy_ import (
    bstack111111ll1l_opy_,
    bstack111111l11l_opy_,
    bstack11111l1l1l_opy_,
)
from bstack_utils.constants import *
from typing import Any, List, Union, Dict
from pathlib import Path
from browserstack_sdk.sdk_cli.bstack1llll1lll1l_opy_ import bstack1llllll1ll1_opy_
from datetime import datetime
from typing import Tuple, Any
from bstack_utils.messages import bstack11lll11l1l_opy_
from bstack_utils.helper import bstack1ll11111111_opy_
import threading
import os
import urllib.parse
class bstack1llll111lll_opy_(bstack1llllll1l1l_opy_):
    def __init__(self, bstack1lllll11lll_opy_):
        super().__init__()
        bstack1llllll1ll1_opy_.bstack1ll1l1ll1l1_opy_((bstack111111ll1l_opy_.bstack11111111ll_opy_, bstack111111l11l_opy_.PRE), self.bstack1l1ll11llll_opy_)
        bstack1llllll1ll1_opy_.bstack1ll1l1ll1l1_opy_((bstack111111ll1l_opy_.bstack11111111ll_opy_, bstack111111l11l_opy_.PRE), self.bstack1l1ll11l1l1_opy_)
        bstack1llllll1ll1_opy_.bstack1ll1l1ll1l1_opy_((bstack111111ll1l_opy_.bstack1111l11lll_opy_, bstack111111l11l_opy_.PRE), self.bstack1l1ll11l111_opy_)
        bstack1llllll1ll1_opy_.bstack1ll1l1ll1l1_opy_((bstack111111ll1l_opy_.bstack1111l1l111_opy_, bstack111111l11l_opy_.PRE), self.bstack1l1ll111lll_opy_)
        bstack1llllll1ll1_opy_.bstack1ll1l1ll1l1_opy_((bstack111111ll1l_opy_.bstack11111111ll_opy_, bstack111111l11l_opy_.PRE), self.bstack1l1ll11ll11_opy_)
        bstack1llllll1ll1_opy_.bstack1ll1l1ll1l1_opy_((bstack111111ll1l_opy_.QUIT, bstack111111l11l_opy_.PRE), self.on_close)
        self.bstack1lllll11lll_opy_ = bstack1lllll11lll_opy_
    def is_enabled(self) -> bool:
        return True
    def bstack1l1ll11llll_opy_(
        self,
        f: bstack1llllll1ll1_opy_,
        bstack1l1ll1111ll_opy_: object,
        exec: Tuple[bstack11111l1l1l_opy_, str],
        bstack11111l11ll_opy_: Tuple[bstack111111ll1l_opy_, bstack111111l11l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1l1ll11_opy_ (u"ࠥࡰࡦࡻ࡮ࡤࡪࠥቀ"):
            return
        if not bstack1ll11111111_opy_():
            self.logger.debug(bstack1l1ll11_opy_ (u"ࠦࡗ࡫ࡴࡶࡴࡱ࡭ࡳ࡭ࠠࡪࡰࠣࡰࡦࡻ࡮ࡤࡪࠣࡱࡪࡺࡨࡰࡦ࠯ࠤࡳࡵࡴࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠣቁ"))
            return
        def wrapped(bstack1l1ll1111ll_opy_, launch, *args, **kwargs):
            response = self.bstack1l1ll1l111l_opy_(f.platform_index, instance.ref(), json.dumps({bstack1l1ll11_opy_ (u"ࠬ࡯ࡳࡑ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠫቂ"): True}).encode(bstack1l1ll11_opy_ (u"ࠨࡵࡵࡨ࠰࠼ࠧቃ")))
            if response is not None and response.capabilities:
                if not bstack1ll11111111_opy_():
                    browser = launch(bstack1l1ll1111ll_opy_)
                    return browser
                bstack1l1ll11111l_opy_ = json.loads(response.capabilities.decode(bstack1l1ll11_opy_ (u"ࠢࡶࡶࡩ࠱࠽ࠨቄ")))
                if not bstack1l1ll11111l_opy_: # empty caps bstack1l1ll111ll1_opy_ bstack1l1ll11l11l_opy_ bstack1l1ll11ll1l_opy_ bstack1lll111l1l1_opy_ or error in processing
                    return
                bstack1l1ll111111_opy_ = PLAYWRIGHT_HUB_URL + urllib.parse.quote(json.dumps(bstack1l1ll11111l_opy_))
                f.bstack111111l1l1_opy_(instance, bstack1llllll1ll1_opy_.bstack1l1ll1111l1_opy_, bstack1l1ll111111_opy_)
                f.bstack111111l1l1_opy_(instance, bstack1llllll1ll1_opy_.bstack1l1ll1l1111_opy_, bstack1l1ll11111l_opy_)
                browser = bstack1l1ll1111ll_opy_.connect(bstack1l1ll111111_opy_)
                return browser
        return wrapped
    def bstack1l1ll11l111_opy_(
        self,
        f: bstack1llllll1ll1_opy_,
        Connection: object,
        exec: Tuple[bstack11111l1l1l_opy_, str],
        bstack11111l11ll_opy_: Tuple[bstack111111ll1l_opy_, bstack111111l11l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1l1ll11_opy_ (u"ࠣࡦ࡬ࡷࡵࡧࡴࡤࡪࠥቅ"):
            self.logger.debug(bstack1l1ll11_opy_ (u"ࠤࡕࡩࡹࡻࡲ࡯࡫ࡱ࡫ࠥ࡯࡮ࠡࡦ࡬ࡷࡵࡧࡴࡤࡪࠣࡱࡪࡺࡨࡰࡦ࠯ࠤࡳࡵࡴࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠣቆ"))
            return
        if not bstack1ll11111111_opy_():
            return
        def wrapped(Connection, dispatch, *args, **kwargs):
            data = args[0]
            try:
                if args and args[0].get(bstack1l1ll11_opy_ (u"ࠪࡴࡦࡸࡡ࡮ࡵࠪቇ"), {}).get(bstack1l1ll11_opy_ (u"ࠫࡧࡹࡐࡢࡴࡤࡱࡸ࠭ቈ")):
                    bstack1l1ll11l1ll_opy_ = args[0][bstack1l1ll11_opy_ (u"ࠧࡶࡡࡳࡣࡰࡷࠧ቉")][bstack1l1ll11_opy_ (u"ࠨࡢࡴࡒࡤࡶࡦࡳࡳࠣቊ")]
                    session_id = bstack1l1ll11l1ll_opy_.get(bstack1l1ll11_opy_ (u"ࠢࡴࡧࡶࡷ࡮ࡵ࡮ࡊࡦࠥቋ"))
                    f.bstack111111l1l1_opy_(instance, bstack1llllll1ll1_opy_.bstack1l1ll11lll1_opy_, session_id)
            except Exception as e:
                self.logger.debug(bstack1l1ll11_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡥ࡫ࡶࡴࡦࡺࡣࡩࠢࡰࡩࡹ࡮࡯ࡥ࠼ࠣࠦቌ"), e)
            dispatch(Connection, *args)
        return wrapped
    def bstack1l1ll11ll11_opy_(
        self,
        f: bstack1llllll1ll1_opy_,
        bstack1l1ll1111ll_opy_: object,
        exec: Tuple[bstack11111l1l1l_opy_, str],
        bstack11111l11ll_opy_: Tuple[bstack111111ll1l_opy_, bstack111111l11l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1l1ll11_opy_ (u"ࠤࡦࡳࡳࡴࡥࡤࡶࠥቍ"):
            return
        if not bstack1ll11111111_opy_():
            self.logger.debug(bstack1l1ll11_opy_ (u"ࠥࡖࡪࡺࡵࡳࡰ࡬ࡲ࡬ࠦࡩ࡯ࠢࡦࡳࡳࡴࡥࡤࡶࠣࡱࡪࡺࡨࡰࡦ࠯ࠤࡳࡵࡴࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠣ቎"))
            return
        def wrapped(bstack1l1ll1111ll_opy_, connect, *args, **kwargs):
            response = self.bstack1l1ll1l111l_opy_(f.platform_index, instance.ref(), json.dumps({bstack1l1ll11_opy_ (u"ࠫ࡮ࡹࡐ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠪ቏"): True}).encode(bstack1l1ll11_opy_ (u"ࠧࡻࡴࡧ࠯࠻ࠦቐ")))
            if response is not None and response.capabilities:
                bstack1l1ll11111l_opy_ = json.loads(response.capabilities.decode(bstack1l1ll11_opy_ (u"ࠨࡵࡵࡨ࠰࠼ࠧቑ")))
                if not bstack1l1ll11111l_opy_:
                    return
                bstack1l1ll111111_opy_ = PLAYWRIGHT_HUB_URL + urllib.parse.quote(json.dumps(bstack1l1ll11111l_opy_))
                if bstack1l1ll11111l_opy_.get(bstack1l1ll11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ቒ")):
                    browser = bstack1l1ll1111ll_opy_.bstack1l1l1llllll_opy_(bstack1l1ll111111_opy_)
                    return browser
                else:
                    args = list(args)
                    args[0] = bstack1l1ll111111_opy_
                    return connect(bstack1l1ll1111ll_opy_, *args, **kwargs)
        return wrapped
    def bstack1l1ll11l1l1_opy_(
        self,
        f: bstack1llllll1ll1_opy_,
        bstack1ll11l1l1ll_opy_: object,
        exec: Tuple[bstack11111l1l1l_opy_, str],
        bstack11111l11ll_opy_: Tuple[bstack111111ll1l_opy_, bstack111111l11l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1l1ll11_opy_ (u"ࠣࡰࡨࡻࡤࡶࡡࡨࡧࠥቓ"):
            return
        if not bstack1ll11111111_opy_():
            self.logger.debug(bstack1l1ll11_opy_ (u"ࠤࡕࡩࡹࡻࡲ࡯࡫ࡱ࡫ࠥ࡯࡮ࠡࡰࡨࡻࡤࡶࡡࡨࡧࠣࡱࡪࡺࡨࡰࡦ࠯ࠤࡳࡵࡴࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠣቔ"))
            return
        def wrapped(bstack1ll11l1l1ll_opy_, bstack1l1ll111l1l_opy_, *args, **kwargs):
            contexts = bstack1ll11l1l1ll_opy_.browser.contexts
            if contexts:
                for context in contexts:
                    if context.pages:
                        for page in context.pages:
                                if bstack1l1ll11_opy_ (u"ࠥࡥࡧࡵࡵࡵ࠼ࡥࡰࡦࡴ࡫ࠣቕ") in page.url:
                                    return page
                    else:
                        return bstack1l1ll111l1l_opy_(bstack1ll11l1l1ll_opy_)
        return wrapped
    def bstack1l1ll1l111l_opy_(self, platform_index: int, ref, user_input_params: bytes):
        req = structs.DriverInitRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.user_input_params = user_input_params
        req.ref = ref
        self.logger.debug(bstack1l1ll11_opy_ (u"ࠦࡷ࡫ࡧࡪࡵࡷࡩࡷࡥࡷࡦࡤࡧࡶ࡮ࡼࡥࡳࡡ࡬ࡲ࡮ࡺ࠺ࠡࠤቖ") + str(req) + bstack1l1ll11_opy_ (u"ࠧࠨ቗"))
        try:
            r = self.bstack1llll111ll1_opy_.DriverInit(req)
            if not r.success:
                self.logger.debug(bstack1l1ll11_opy_ (u"ࠨࡲࡦࡥࡨ࡭ࡻ࡫ࡤࠡࡨࡵࡳࡲࠦࡳࡦࡴࡹࡩࡷࡀࠠࡴࡷࡦࡧࡪࡹࡳ࠾ࠤቘ") + str(r.success) + bstack1l1ll11_opy_ (u"ࠢࠣ቙"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1l1ll11_opy_ (u"ࠣࡴࡳࡧ࠲࡫ࡲࡳࡱࡵ࠾ࠥࠨቚ") + str(e) + bstack1l1ll11_opy_ (u"ࠤࠥቛ"))
            traceback.print_exc()
            raise e
    def bstack1l1ll111lll_opy_(
        self,
        f: bstack1llllll1ll1_opy_,
        Connection: object,
        exec: Tuple[bstack11111l1l1l_opy_, str],
        bstack11111l11ll_opy_: Tuple[bstack111111ll1l_opy_, bstack111111l11l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1l1ll11_opy_ (u"ࠥࡣࡸ࡫࡮ࡥࡡࡰࡩࡸࡹࡡࡨࡧࡢࡸࡴࡥࡳࡦࡴࡹࡩࡷࠨቜ"):
            return
        if not bstack1ll11111111_opy_():
            return
        def wrapped(Connection, bstack1l1ll111l11_opy_, *args, **kwargs):
            return bstack1l1ll111l11_opy_(Connection, *args, **kwargs)
        return wrapped
    def on_close(
        self,
        f: bstack1llllll1ll1_opy_,
        bstack1l1ll1111ll_opy_: object,
        exec: Tuple[bstack11111l1l1l_opy_, str],
        bstack11111l11ll_opy_: Tuple[bstack111111ll1l_opy_, bstack111111l11l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1l1ll11_opy_ (u"ࠦࡨࡲ࡯ࡴࡧࠥቝ"):
            return
        if not bstack1ll11111111_opy_():
            self.logger.debug(bstack1l1ll11_opy_ (u"ࠧࡘࡥࡵࡷࡵࡲ࡮ࡴࡧࠡ࡫ࡱࠤࡨࡲ࡯ࡴࡧࠣࡱࡪࡺࡨࡰࡦ࠯ࠤࡳࡵࡴࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠣ቞"))
            return
        def wrapped(Connection, close, *args, **kwargs):
            return close(Connection)
        return wrapped