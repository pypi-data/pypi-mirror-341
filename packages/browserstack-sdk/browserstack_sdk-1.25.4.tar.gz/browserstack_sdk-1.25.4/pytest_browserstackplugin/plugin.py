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
import atexit
import datetime
import inspect
import logging
import signal
import threading
from uuid import uuid4
from bstack_utils.measure import bstack1lll111l_opy_
from bstack_utils.percy_sdk import PercySDK
import pytest
from packaging import version
from browserstack_sdk.__init__ import (bstack1llll1l11_opy_, bstack11l1l1llll_opy_, update, bstack1llll1llll_opy_,
                                       bstack1l11ll1lll_opy_, bstack111ll1ll1_opy_, bstack1llll1l11l_opy_, bstack1l11lll1l_opy_,
                                       bstack11lllll111_opy_, bstack1l1lll1ll1_opy_, bstack11lllllll1_opy_, bstack1l1lll1111_opy_,
                                       bstack1llll111l1_opy_, getAccessibilityResults, getAccessibilityResultsSummary, perform_scan, bstack1l111llll_opy_)
from browserstack_sdk.bstack1l111lll11_opy_ import bstack1l1l1l1ll1_opy_
from browserstack_sdk._version import __version__
from bstack_utils import bstack111l1l111_opy_
from bstack_utils.capture import bstack11l1111l11_opy_
from bstack_utils.config import Config
from bstack_utils.percy import *
from bstack_utils.constants import bstack1111lll1l_opy_, bstack111lll1l1_opy_, bstack11lll111l1_opy_, \
    bstack1111l1111_opy_
from bstack_utils.helper import bstack1lllll11_opy_, bstack11ll11111ll_opy_, bstack111l11l11l_opy_, bstack1l1l1lll11_opy_, bstack1ll11111111_opy_, bstack1l11111ll_opy_, \
    bstack11l1l1111l1_opy_, \
    bstack11l1l11ll1l_opy_, bstack1l1llll1l_opy_, bstack11l1lll11_opy_, bstack11l1l11ll11_opy_, bstack1lll111ll_opy_, Notset, \
    bstack1ll1l11ll_opy_, bstack11l1l111ll1_opy_, bstack11l11llll11_opy_, Result, bstack11ll11llll1_opy_, bstack11ll1111l11_opy_, bstack111l11ll1l_opy_, \
    bstack1l11111lll_opy_, bstack1llll1111_opy_, bstack11111ll1l_opy_, bstack11l1l1l1l1l_opy_
from bstack_utils.bstack11l11lll1l1_opy_ import bstack11l11ll1l1l_opy_
from bstack_utils.messages import bstack1l11l1l1l_opy_, bstack1ll11ll1l_opy_, bstack11lll11l1l_opy_, bstack11111lll_opy_, bstack1l1l11l11_opy_, \
    bstack1ll1l11lll_opy_, bstack1l11l111ll_opy_, bstack1llll1ll1l_opy_, bstack11111l11_opy_, bstack11lll1111_opy_, \
    bstack1llll1ll_opy_, bstack1l1lll1lll_opy_
from bstack_utils.proxy import bstack1lll1l1l_opy_, bstack1l1lll111l_opy_
from bstack_utils.bstack111111ll_opy_ import bstack111l1l11l11_opy_, bstack111l1ll111l_opy_, bstack111l1ll1111_opy_, bstack111l1l11ll1_opy_, \
    bstack111l1l11lll_opy_, bstack111l1l11l1l_opy_, bstack111l1l1lll1_opy_, bstack1lllll11ll_opy_, bstack111l1l1ll1l_opy_
from bstack_utils.bstack11l1llll1l_opy_ import bstack11l1l111l1_opy_
from bstack_utils.bstack11ll11l1ll_opy_ import bstack1lll11l111_opy_, bstack1l1l1l1111_opy_, bstack1l1l111l_opy_, \
    bstack11lll1lll_opy_, bstack11l1ll1l1l_opy_
from bstack_utils.bstack11l111lll1_opy_ import bstack11l111ll11_opy_
from bstack_utils.bstack11l111ll1l_opy_ import bstack1l1llll11_opy_
import bstack_utils.accessibility as bstack1ll11llll1_opy_
from bstack_utils.bstack11l111l1ll_opy_ import bstack111l111ll_opy_
from bstack_utils.bstack11ll1l11ll_opy_ import bstack11ll1l11ll_opy_
from browserstack_sdk.__init__ import bstack1ll1ll1lll_opy_
from browserstack_sdk.sdk_cli.bstack1llll1l1l1l_opy_ import bstack1ll1lllll11_opy_
from browserstack_sdk.sdk_cli.bstack1l1l11ll1_opy_ import bstack1l1l11ll1_opy_, bstack1llll1111l_opy_, bstack1l11l1l11l_opy_
from browserstack_sdk.sdk_cli.test_framework import bstack1l11ll11l1l_opy_, bstack1lll11l11l1_opy_, bstack1lll1ll111l_opy_
from browserstack_sdk.sdk_cli.cli import cli
from browserstack_sdk.sdk_cli.bstack1l1l11ll1_opy_ import bstack1l1l11ll1_opy_, bstack1llll1111l_opy_, bstack1l11l1l11l_opy_
bstack1ll1111lll_opy_ = None
bstack1lll1lll1l_opy_ = None
bstack1l1111l11l_opy_ = None
bstack1l1ll1111l_opy_ = None
bstack1l1ll1l1ll_opy_ = None
bstack111l1llll_opy_ = None
bstack11l1l1lll1_opy_ = None
bstack1l1ll1lll_opy_ = None
bstack11l1lll1l1_opy_ = None
bstack1ll1l111l_opy_ = None
bstack1lll11111l_opy_ = None
bstack1l111l1ll1_opy_ = None
bstack1111l1l11_opy_ = None
bstack1l1l1111l_opy_ = bstack1l1ll11_opy_ (u"ࠨࠩὂ")
CONFIG = {}
bstack11l1l1l1ll_opy_ = False
bstack1l1ll1l1_opy_ = bstack1l1ll11_opy_ (u"ࠩࠪὃ")
bstack11l11lll11_opy_ = bstack1l1ll11_opy_ (u"ࠪࠫὄ")
bstack1l11lll1l1_opy_ = False
bstack1l1lll11_opy_ = []
bstack11l11l111_opy_ = bstack1111lll1l_opy_
bstack11111lll1l1_opy_ = bstack1l1ll11_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫὅ")
bstack11llll1lll_opy_ = {}
bstack11ll1lll11_opy_ = None
bstack1ll1l1111_opy_ = False
logger = bstack111l1l111_opy_.get_logger(__name__, bstack11l11l111_opy_)
store = {
    bstack1l1ll11_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩ὆"): []
}
bstack11111llllll_opy_ = False
try:
    from playwright.sync_api import (
        BrowserContext,
        Page
    )
except:
    pass
import json
_111l11llll_opy_ = {}
current_test_uuid = None
cli_context = bstack1l11ll11l1l_opy_(
    test_framework_name=bstack1ll11111l1_opy_[bstack1l1ll11_opy_ (u"࠭ࡐ࡚ࡖࡈࡗ࡙࠳ࡂࡅࡆࠪ὇")] if bstack1lll111ll_opy_() else bstack1ll11111l1_opy_[bstack1l1ll11_opy_ (u"ࠧࡑ࡛ࡗࡉࡘ࡚ࠧὈ")],
    test_framework_version=pytest.__version__,
    platform_index=-1,
)
def bstack1l1l11l111_opy_(page, bstack1lll11llll_opy_):
    try:
        page.evaluate(bstack1l1ll11_opy_ (u"ࠣࡡࠣࡁࡃࠦࡻࡾࠤὉ"),
                      bstack1l1ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨ࡮ࡢ࡯ࡨࠦ࠿࠭Ὂ") + json.dumps(
                          bstack1lll11llll_opy_) + bstack1l1ll11_opy_ (u"ࠥࢁࢂࠨὋ"))
    except Exception as e:
        print(bstack1l1ll11_opy_ (u"ࠦࡪࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡰࡤࡱࡪࠦࡻࡾࠤὌ"), e)
def bstack11l1ll111l_opy_(page, message, level):
    try:
        page.evaluate(bstack1l1ll11_opy_ (u"ࠧࡥࠠ࠾ࡀࠣࡿࢂࠨὍ"), bstack1l1ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡩࡧࡴࡢࠤ࠽ࠫ὎") + json.dumps(
            message) + bstack1l1ll11_opy_ (u"ࠧ࠭ࠤ࡯ࡩࡻ࡫࡬ࠣ࠼ࠪ὏") + json.dumps(level) + bstack1l1ll11_opy_ (u"ࠨࡿࢀࠫὐ"))
    except Exception as e:
        print(bstack1l1ll11_opy_ (u"ࠤࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡧ࡮࡯ࡱࡷࡥࡹ࡯࡯࡯ࠢࡾࢁࠧὑ"), e)
def pytest_configure(config):
    global bstack1l1ll1l1_opy_
    global CONFIG
    bstack11llllllll_opy_ = Config.bstack1l1111llll_opy_()
    config.args = bstack1l1llll11_opy_.bstack1111l11llll_opy_(config.args)
    bstack11llllllll_opy_.bstack11l11l1l_opy_(bstack11111ll1l_opy_(config.getoption(bstack1l1ll11_opy_ (u"ࠪࡷࡰ࡯ࡰࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠧὒ"))))
    try:
        bstack111l1l111_opy_.bstack11l11l111l1_opy_(config.inipath, config.rootpath)
    except:
        pass
    if cli.is_running():
        bstack1l1l11ll1_opy_.invoke(bstack1llll1111l_opy_.CONNECT, bstack1l11l1l11l_opy_())
        cli_context.platform_index = int(os.environ.get(bstack1l1ll11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫὓ"), bstack1l1ll11_opy_ (u"ࠬ࠶ࠧὔ")))
        config = json.loads(os.environ.get(bstack1l1ll11_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡉࡏࡏࡈࡌࡋࠧὕ"), bstack1l1ll11_opy_ (u"ࠢࡼࡿࠥὖ")))
        cli.bstack1lllllll111_opy_(bstack11l1lll11_opy_(bstack1l1ll1l1_opy_, CONFIG), cli_context.platform_index, bstack1llll1llll_opy_)
    if cli.bstack1llll1l1ll1_opy_(bstack1ll1lllll11_opy_):
        cli.bstack1lll111111l_opy_()
        logger.debug(bstack1l1ll11_opy_ (u"ࠣࡅࡏࡍࠥ࡯ࡳࠡࡣࡦࡸ࡮ࡼࡥࠡࡨࡲࡶࠥࡶ࡬ࡢࡶࡩࡳࡷࡳ࡟ࡪࡰࡧࡩࡽࡃࠢὗ") + str(cli_context.platform_index) + bstack1l1ll11_opy_ (u"ࠤࠥ὘"))
        cli.test_framework.track_event(cli_context, bstack1lll11l11l1_opy_.BEFORE_ALL, bstack1lll1ll111l_opy_.PRE, config)
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    when = getattr(call, bstack1l1ll11_opy_ (u"ࠥࡻ࡭࡫࡮ࠣὙ"), None)
    if cli.is_running() and when == bstack1l1ll11_opy_ (u"ࠦࡨࡧ࡬࡭ࠤ὚"):
        cli.test_framework.track_event(cli_context, bstack1lll11l11l1_opy_.LOG_REPORT, bstack1lll1ll111l_opy_.PRE, item, call)
    outcome = yield
    if cli.is_running():
        if when == bstack1l1ll11_opy_ (u"ࠧࡹࡥࡵࡷࡳࠦὛ"):
            cli.test_framework.track_event(cli_context, bstack1lll11l11l1_opy_.BEFORE_EACH, bstack1lll1ll111l_opy_.POST, item, call, outcome)
        elif when == bstack1l1ll11_opy_ (u"ࠨࡣࡢ࡮࡯ࠦ὜"):
            cli.test_framework.track_event(cli_context, bstack1lll11l11l1_opy_.LOG_REPORT, bstack1lll1ll111l_opy_.POST, item, call, outcome)
        elif when == bstack1l1ll11_opy_ (u"ࠢࡵࡧࡤࡶࡩࡵࡷ࡯ࠤὝ"):
            cli.test_framework.track_event(cli_context, bstack1lll11l11l1_opy_.AFTER_EACH, bstack1lll1ll111l_opy_.POST, item, call, outcome)
        return # skip all existing bstack1111l111l11_opy_
    bstack11111lllll1_opy_ = item.config.getoption(bstack1l1ll11_opy_ (u"ࠨࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ὞"))
    plugins = item.config.getoption(bstack1l1ll11_opy_ (u"ࠤࡳࡰࡺ࡭ࡩ࡯ࡵࠥὟ"))
    report = outcome.get_result()
    bstack1111l111lll_opy_(item, call, report)
    if bstack1l1ll11_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶࡢࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡲ࡯ࡹ࡬࡯࡮ࠣὠ") not in plugins or bstack1lll111ll_opy_():
        return
    summary = []
    driver = getattr(item, bstack1l1ll11_opy_ (u"ࠦࡤࡪࡲࡪࡸࡨࡶࠧὡ"), None)
    page = getattr(item, bstack1l1ll11_opy_ (u"ࠧࡥࡰࡢࡩࡨࠦὢ"), None)
    try:
        if (driver == None or driver.session_id == None):
            driver = threading.current_thread().bstackSessionDriver
    except:
        pass
    item._driver = driver
    if (driver is not None or cli.is_running()):
        bstack11111llll11_opy_(item, report, summary, bstack11111lllll1_opy_)
    if (page is not None):
        bstack1111l1111ll_opy_(item, report, summary, bstack11111lllll1_opy_)
def bstack11111llll11_opy_(item, report, summary, bstack11111lllll1_opy_):
    if report.when == bstack1l1ll11_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬὣ") and report.skipped:
        bstack111l1l1ll1l_opy_(report)
    if report.when in [bstack1l1ll11_opy_ (u"ࠢࡴࡧࡷࡹࡵࠨὤ"), bstack1l1ll11_opy_ (u"ࠣࡶࡨࡥࡷࡪ࡯ࡸࡰࠥὥ")]:
        return
    if not bstack1ll11111111_opy_():
        return
    try:
        if (str(bstack11111lllll1_opy_).lower() != bstack1l1ll11_opy_ (u"ࠩࡷࡶࡺ࡫ࠧὦ") and not cli.is_running()):
            item._driver.execute_script(
                bstack1l1ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢ࡯ࡣࡰࡩࠧࡀࠠࠨὧ") + json.dumps(
                    report.nodeid) + bstack1l1ll11_opy_ (u"ࠫࢂࢃࠧὨ"))
        os.environ[bstack1l1ll11_opy_ (u"ࠬࡖ࡙ࡕࡇࡖࡘࡤ࡚ࡅࡔࡖࡢࡒࡆࡓࡅࠨὩ")] = report.nodeid
    except Exception as e:
        summary.append(
            bstack1l1ll11_opy_ (u"ࠨࡗࡂࡔࡑࡍࡓࡍ࠺ࠡࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡲࡧࡲ࡬ࠢࡶࡩࡸࡹࡩࡰࡰࠣࡲࡦࡳࡥ࠻ࠢࡾ࠴ࢂࠨὪ").format(e)
        )
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack1l1ll11_opy_ (u"ࠢࡸࡣࡶࡼ࡫ࡧࡩ࡭ࠤὫ")))
    bstack11l111ll_opy_ = bstack1l1ll11_opy_ (u"ࠣࠤὬ")
    bstack111l1l1ll1l_opy_(report)
    if not passed:
        try:
            bstack11l111ll_opy_ = report.longrepr.reprcrash
        except Exception as e:
            summary.append(
                bstack1l1ll11_opy_ (u"ࠤ࡚ࡅࡗࡔࡉࡏࡉ࠽ࠤࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡥࡧࡷࡩࡷࡳࡩ࡯ࡧࠣࡪࡦ࡯࡬ࡶࡴࡨࠤࡷ࡫ࡡࡴࡱࡱ࠾ࠥࢁ࠰ࡾࠤὭ").format(e)
            )
        try:
            if (threading.current_thread().bstackTestErrorMessages == None):
                threading.current_thread().bstackTestErrorMessages = []
        except Exception as e:
            threading.current_thread().bstackTestErrorMessages = []
        threading.current_thread().bstackTestErrorMessages.append(str(bstack11l111ll_opy_))
    if not report.skipped:
        passed = report.passed or (report.failed and hasattr(report, bstack1l1ll11_opy_ (u"ࠥࡻࡦࡹࡸࡧࡣ࡬ࡰࠧὮ")))
        bstack11l111ll_opy_ = bstack1l1ll11_opy_ (u"ࠦࠧὯ")
        if not passed:
            try:
                bstack11l111ll_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack1l1ll11_opy_ (u"ࠧ࡝ࡁࡓࡐࡌࡒࡌࡀࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡨࡪࡺࡥࡳ࡯࡬ࡲࡪࠦࡦࡢ࡫࡯ࡹࡷ࡫ࠠࡳࡧࡤࡷࡴࡴ࠺ࠡࡽ࠳ࢁࠧὰ").format(e)
                )
            try:
                if (threading.current_thread().bstackTestErrorMessages == None):
                    threading.current_thread().bstackTestErrorMessages = []
            except Exception as e:
                threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(str(bstack11l111ll_opy_))
        try:
            if passed:
                item._driver.execute_script(
                    bstack1l1ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥ࠰ࠥࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠢ࡭ࡧࡹࡩࡱࠨ࠺ࠡࠤ࡬ࡲ࡫ࡵࠢ࠭ࠢ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠤࡧࡥࡹࡧࠢ࠻ࠢࠪά")
                    + json.dumps(bstack1l1ll11_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠡࠣὲ"))
                    + bstack1l1ll11_opy_ (u"ࠣ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࢁࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࢀࠦέ")
                )
            else:
                item._driver.execute_script(
                    bstack1l1ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠥࡰࡪࡼࡥ࡭ࠤ࠽ࠤࠧ࡫ࡲࡳࡱࡵࠦ࠱ࠦ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠨࡤࡢࡶࡤࠦ࠿ࠦࠧὴ")
                    + json.dumps(str(bstack11l111ll_opy_))
                    + bstack1l1ll11_opy_ (u"ࠥࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࢃ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࢂࠨή")
                )
        except Exception as e:
            summary.append(bstack1l1ll11_opy_ (u"ࠦ࡜ࡇࡒࡏࡋࡑࡋ࠿ࠦࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡤࡲࡳࡵࡴࡢࡶࡨ࠾ࠥࢁ࠰ࡾࠤὶ").format(e))
def bstack11111ll1111_opy_(test_name, error_message):
    try:
        bstack1111l11l1ll_opy_ = []
        bstack11111l11l_opy_ = os.environ.get(bstack1l1ll11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬί"), bstack1l1ll11_opy_ (u"࠭࠰ࠨὸ"))
        bstack11llll1l1l_opy_ = {bstack1l1ll11_opy_ (u"ࠧ࡯ࡣࡰࡩࠬό"): test_name, bstack1l1ll11_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧὺ"): error_message, bstack1l1ll11_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨύ"): bstack11111l11l_opy_}
        bstack1111l11ll11_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1ll11_opy_ (u"ࠪࡴࡼࡥࡰࡺࡶࡨࡷࡹࡥࡥࡳࡴࡲࡶࡤࡲࡩࡴࡶ࠱࡮ࡸࡵ࡮ࠨὼ"))
        if os.path.exists(bstack1111l11ll11_opy_):
            with open(bstack1111l11ll11_opy_) as f:
                bstack1111l11l1ll_opy_ = json.load(f)
        bstack1111l11l1ll_opy_.append(bstack11llll1l1l_opy_)
        with open(bstack1111l11ll11_opy_, bstack1l1ll11_opy_ (u"ࠫࡼ࠭ώ")) as f:
            json.dump(bstack1111l11l1ll_opy_, f)
    except Exception as e:
        logger.debug(bstack1l1ll11_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡱࡧࡵࡷ࡮ࡹࡴࡪࡰࡪࠤࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡲࡼࡸࡪࡹࡴࠡࡧࡵࡶࡴࡸࡳ࠻ࠢࠪ὾") + str(e))
def bstack1111l1111ll_opy_(item, report, summary, bstack11111lllll1_opy_):
    if report.when in [bstack1l1ll11_opy_ (u"ࠨࡳࡦࡶࡸࡴࠧ὿"), bstack1l1ll11_opy_ (u"ࠢࡵࡧࡤࡶࡩࡵࡷ࡯ࠤᾀ")]:
        return
    if (str(bstack11111lllll1_opy_).lower() != bstack1l1ll11_opy_ (u"ࠨࡶࡵࡹࡪ࠭ᾁ")):
        bstack1l1l11l111_opy_(item._page, report.nodeid)
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack1l1ll11_opy_ (u"ࠤࡺࡥࡸࡾࡦࡢ࡫࡯ࠦᾂ")))
    bstack11l111ll_opy_ = bstack1l1ll11_opy_ (u"ࠥࠦᾃ")
    bstack111l1l1ll1l_opy_(report)
    if not report.skipped:
        if not passed:
            try:
                bstack11l111ll_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack1l1ll11_opy_ (u"ࠦ࡜ࡇࡒࡏࡋࡑࡋ࠿ࠦࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡧࡩࡹ࡫ࡲ࡮࡫ࡱࡩࠥ࡬ࡡࡪ࡮ࡸࡶࡪࠦࡲࡦࡣࡶࡳࡳࡀࠠࡼ࠲ࢀࠦᾄ").format(e)
                )
        try:
            if passed:
                bstack11l1ll1l1l_opy_(getattr(item, bstack1l1ll11_opy_ (u"ࠬࡥࡰࡢࡩࡨࠫᾅ"), None), bstack1l1ll11_opy_ (u"ࠨࡰࡢࡵࡶࡩࡩࠨᾆ"))
            else:
                error_message = bstack1l1ll11_opy_ (u"ࠧࠨᾇ")
                if bstack11l111ll_opy_:
                    bstack11l1ll111l_opy_(item._page, str(bstack11l111ll_opy_), bstack1l1ll11_opy_ (u"ࠣࡧࡵࡶࡴࡸࠢᾈ"))
                    bstack11l1ll1l1l_opy_(getattr(item, bstack1l1ll11_opy_ (u"ࠩࡢࡴࡦ࡭ࡥࠨᾉ"), None), bstack1l1ll11_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥᾊ"), str(bstack11l111ll_opy_))
                    error_message = str(bstack11l111ll_opy_)
                else:
                    bstack11l1ll1l1l_opy_(getattr(item, bstack1l1ll11_opy_ (u"ࠫࡤࡶࡡࡨࡧࠪᾋ"), None), bstack1l1ll11_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧᾌ"))
                bstack11111ll1111_opy_(report.nodeid, error_message)
        except Exception as e:
            summary.append(bstack1l1ll11_opy_ (u"ࠨࡗࡂࡔࡑࡍࡓࡍ࠺ࠡࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡺࡶࡤࡢࡶࡨࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡹࡴࡢࡶࡸࡷ࠿ࠦࡻ࠱ࡿࠥᾍ").format(e))
def pytest_addoption(parser):
    parser.addoption(bstack1l1ll11_opy_ (u"ࠢ࠮࠯ࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠦᾎ"), default=bstack1l1ll11_opy_ (u"ࠣࡈࡤࡰࡸ࡫ࠢᾏ"), help=bstack1l1ll11_opy_ (u"ࠤࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡧࠥࡹࡥࡵࠢࡶࡩࡸࡹࡩࡰࡰࠣࡲࡦࡳࡥࠣᾐ"))
    parser.addoption(bstack1l1ll11_opy_ (u"ࠥ࠱࠲ࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠤᾑ"), default=bstack1l1ll11_opy_ (u"ࠦࡋࡧ࡬ࡴࡧࠥᾒ"), help=bstack1l1ll11_opy_ (u"ࠧࡇࡵࡵࡱࡰࡥࡹ࡯ࡣࠡࡵࡨࡸࠥࡹࡥࡴࡵ࡬ࡳࡳࠦ࡮ࡢ࡯ࡨࠦᾓ"))
    try:
        import pytest_selenium.pytest_selenium
    except:
        parser.addoption(bstack1l1ll11_opy_ (u"ࠨ࠭࠮ࡦࡵ࡭ࡻ࡫ࡲࠣᾔ"), action=bstack1l1ll11_opy_ (u"ࠢࡴࡶࡲࡶࡪࠨᾕ"), default=bstack1l1ll11_opy_ (u"ࠣࡥ࡫ࡶࡴࡳࡥࠣᾖ"),
                         help=bstack1l1ll11_opy_ (u"ࠤࡇࡶ࡮ࡼࡥࡳࠢࡷࡳࠥࡸࡵ࡯ࠢࡷࡩࡸࡺࡳࠣᾗ"))
def bstack111llll11l_opy_(log):
    if not (log[bstack1l1ll11_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᾘ")] and log[bstack1l1ll11_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᾙ")].strip()):
        return
    active = bstack11l11l11l1_opy_()
    log = {
        bstack1l1ll11_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫᾚ"): log[bstack1l1ll11_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬᾛ")],
        bstack1l1ll11_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪᾜ"): bstack111l11l11l_opy_().isoformat() + bstack1l1ll11_opy_ (u"ࠨ࡜ࠪᾝ"),
        bstack1l1ll11_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᾞ"): log[bstack1l1ll11_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᾟ")],
    }
    if active:
        if active[bstack1l1ll11_opy_ (u"ࠫࡹࡿࡰࡦࠩᾠ")] == bstack1l1ll11_opy_ (u"ࠬ࡮࡯ࡰ࡭ࠪᾡ"):
            log[bstack1l1ll11_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᾢ")] = active[bstack1l1ll11_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᾣ")]
        elif active[bstack1l1ll11_opy_ (u"ࠨࡶࡼࡴࡪ࠭ᾤ")] == bstack1l1ll11_opy_ (u"ࠩࡷࡩࡸࡺࠧᾥ"):
            log[bstack1l1ll11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᾦ")] = active[bstack1l1ll11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᾧ")]
    bstack111l111ll_opy_.bstack1l11lll1_opy_([log])
def bstack11l11l11l1_opy_():
    if len(store[bstack1l1ll11_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩᾨ")]) > 0 and store[bstack1l1ll11_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪᾩ")][-1]:
        return {
            bstack1l1ll11_opy_ (u"ࠧࡵࡻࡳࡩࠬᾪ"): bstack1l1ll11_opy_ (u"ࠨࡪࡲࡳࡰ࠭ᾫ"),
            bstack1l1ll11_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᾬ"): store[bstack1l1ll11_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧᾭ")][-1]
        }
    if store.get(bstack1l1ll11_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨᾮ"), None):
        return {
            bstack1l1ll11_opy_ (u"ࠬࡺࡹࡱࡧࠪᾯ"): bstack1l1ll11_opy_ (u"࠭ࡴࡦࡵࡷࠫᾰ"),
            bstack1l1ll11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᾱ"): store[bstack1l1ll11_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬᾲ")]
        }
    return None
def pytest_runtest_logstart(nodeid, location):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lll11l11l1_opy_.INIT_TEST, bstack1lll1ll111l_opy_.PRE, nodeid, location)
def pytest_runtest_logfinish(nodeid, location):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lll11l11l1_opy_.INIT_TEST, bstack1lll1ll111l_opy_.POST, nodeid, location)
def pytest_runtest_call(item):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lll11l11l1_opy_.TEST, bstack1lll1ll111l_opy_.PRE, item)
        return
    try:
        global CONFIG
        item._11111ll1lll_opy_ = True
        bstack1llll1l111_opy_ = bstack1ll11llll1_opy_.bstack1ll11l11_opy_(bstack11l1l11ll1l_opy_(item.own_markers))
        if not cli.bstack1llll1l1ll1_opy_(bstack1ll1lllll11_opy_):
            item._a11y_test_case = bstack1llll1l111_opy_
            if bstack1lllll11_opy_(threading.current_thread(), bstack1l1ll11_opy_ (u"ࠩࡤ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨᾳ"), None):
                driver = getattr(item, bstack1l1ll11_opy_ (u"ࠪࡣࡩࡸࡩࡷࡧࡵࠫᾴ"), None)
                item._a11y_started = bstack1ll11llll1_opy_.bstack11ll111l1l_opy_(driver, bstack1llll1l111_opy_)
        if not bstack111l111ll_opy_.on() or bstack11111lll1l1_opy_ != bstack1l1ll11_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ᾵"):
            return
        global current_test_uuid #, bstack111lllll1l_opy_
        bstack111lll111l_opy_ = {
            bstack1l1ll11_opy_ (u"ࠬࡻࡵࡪࡦࠪᾶ"): uuid4().__str__(),
            bstack1l1ll11_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪᾷ"): bstack111l11l11l_opy_().isoformat() + bstack1l1ll11_opy_ (u"࡛ࠧࠩᾸ")
        }
        current_test_uuid = bstack111lll111l_opy_[bstack1l1ll11_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭Ᾱ")]
        store[bstack1l1ll11_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭Ὰ")] = bstack111lll111l_opy_[bstack1l1ll11_opy_ (u"ࠪࡹࡺ࡯ࡤࠨΆ")]
        threading.current_thread().current_test_uuid = current_test_uuid
        _111l11llll_opy_[item.nodeid] = {**_111l11llll_opy_[item.nodeid], **bstack111lll111l_opy_}
        bstack11111ll11ll_opy_(item, _111l11llll_opy_[item.nodeid], bstack1l1ll11_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬᾼ"))
    except Exception as err:
        print(bstack1l1ll11_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷࡣࡷࡻ࡮ࡵࡧࡶࡸࡤࡩࡡ࡭࡮࠽ࠤࢀࢃࠧ᾽"), str(err))
def pytest_runtest_setup(item):
    store[bstack1l1ll11_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡴࡦ࡯ࠪι")] = item
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lll11l11l1_opy_.BEFORE_EACH, bstack1lll1ll111l_opy_.PRE, item, bstack1l1ll11_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭᾿"))
        return # skip all existing bstack1111l111l11_opy_
    global bstack11111llllll_opy_
    threading.current_thread().percySessionName = item.nodeid
    if bstack11l1l11ll11_opy_():
        atexit.register(bstack11ll11l111_opy_)
        if not bstack11111llllll_opy_:
            try:
                bstack11111ll11l1_opy_ = [signal.SIGINT, signal.SIGTERM]
                if not bstack11l1l1l1l1l_opy_():
                    bstack11111ll11l1_opy_.extend([signal.SIGHUP, signal.SIGQUIT])
                for s in bstack11111ll11l1_opy_:
                    signal.signal(s, bstack11111ll1l11_opy_)
                bstack11111llllll_opy_ = True
            except Exception as e:
                logger.debug(
                    bstack1l1ll11_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡪࡰࠣࡶࡪ࡭ࡩࡴࡶࡨࡶࠥࡹࡩࡨࡰࡤࡰࠥ࡮ࡡ࡯ࡦ࡯ࡩࡷࡹ࠺ࠡࠤ῀") + str(e))
        try:
            item.config.hook.pytest_selenium_runtest_makereport = bstack111l1l11l11_opy_
        except Exception as err:
            threading.current_thread().testStatus = bstack1l1ll11_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩ῁")
    try:
        if not bstack111l111ll_opy_.on():
            return
        uuid = uuid4().__str__()
        bstack111lll111l_opy_ = {
            bstack1l1ll11_opy_ (u"ࠪࡹࡺ࡯ࡤࠨῂ"): uuid,
            bstack1l1ll11_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨῃ"): bstack111l11l11l_opy_().isoformat() + bstack1l1ll11_opy_ (u"ࠬࡠࠧῄ"),
            bstack1l1ll11_opy_ (u"࠭ࡴࡺࡲࡨࠫ῅"): bstack1l1ll11_opy_ (u"ࠧࡩࡱࡲ࡯ࠬῆ"),
            bstack1l1ll11_opy_ (u"ࠨࡪࡲࡳࡰࡥࡴࡺࡲࡨࠫῇ"): bstack1l1ll11_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡈࡅࡈࡎࠧῈ"),
            bstack1l1ll11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡰࡤࡱࡪ࠭Έ"): bstack1l1ll11_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪῊ")
        }
        threading.current_thread().current_hook_uuid = uuid
        threading.current_thread().current_test_item = item
        store[bstack1l1ll11_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡺࡥ࡮ࠩΉ")] = item
        store[bstack1l1ll11_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪῌ")] = [uuid]
        if not _111l11llll_opy_.get(item.nodeid, None):
            _111l11llll_opy_[item.nodeid] = {bstack1l1ll11_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭῍"): [], bstack1l1ll11_opy_ (u"ࠨࡨ࡬ࡼࡹࡻࡲࡦࡵࠪ῎"): []}
        _111l11llll_opy_[item.nodeid][bstack1l1ll11_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨ῏")].append(bstack111lll111l_opy_[bstack1l1ll11_opy_ (u"ࠪࡹࡺ࡯ࡤࠨῐ")])
        _111l11llll_opy_[item.nodeid + bstack1l1ll11_opy_ (u"ࠫ࠲ࡹࡥࡵࡷࡳࠫῑ")] = bstack111lll111l_opy_
        bstack1111l11111l_opy_(item, bstack111lll111l_opy_, bstack1l1ll11_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭ῒ"))
    except Exception as err:
        print(bstack1l1ll11_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶࡹࡵࡧࡶࡸࡤࡸࡵ࡯ࡶࡨࡷࡹࡥࡳࡦࡶࡸࡴ࠿ࠦࡻࡾࠩΐ"), str(err))
def pytest_runtest_teardown(item):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lll11l11l1_opy_.TEST, bstack1lll1ll111l_opy_.POST, item)
        cli.test_framework.track_event(cli_context, bstack1lll11l11l1_opy_.AFTER_EACH, bstack1lll1ll111l_opy_.PRE, item, bstack1l1ll11_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࠩ῔"))
        return # skip all existing bstack1111l111l11_opy_
    try:
        global bstack11llll1lll_opy_
        bstack11111l11l_opy_ = 0
        if bstack1l11lll1l1_opy_ is True:
            bstack11111l11l_opy_ = int(os.environ.get(bstack1l1ll11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨ῕")))
        if bstack11ll111ll1_opy_.bstack1lll111111_opy_() == bstack1l1ll11_opy_ (u"ࠤࡷࡶࡺ࡫ࠢῖ"):
            if bstack11ll111ll1_opy_.bstack1ll1111l1l_opy_() == bstack1l1ll11_opy_ (u"ࠥࡸࡪࡹࡴࡤࡣࡶࡩࠧῗ"):
                bstack1111l11lll1_opy_ = bstack1lllll11_opy_(threading.current_thread(), bstack1l1ll11_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧῘ"), None)
                bstack11111ll11_opy_ = bstack1111l11lll1_opy_ + bstack1l1ll11_opy_ (u"ࠧ࠳ࡴࡦࡵࡷࡧࡦࡹࡥࠣῙ")
                driver = getattr(item, bstack1l1ll11_opy_ (u"࠭࡟ࡥࡴ࡬ࡺࡪࡸࠧῚ"), None)
                bstack1llll1l1ll_opy_ = getattr(item, bstack1l1ll11_opy_ (u"ࠧ࡯ࡣࡰࡩࠬΊ"), None)
                bstack1l1l1l1l11_opy_ = getattr(item, bstack1l1ll11_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭῜"), None)
                PercySDK.screenshot(driver, bstack11111ll11_opy_, bstack1llll1l1ll_opy_=bstack1llll1l1ll_opy_, bstack1l1l1l1l11_opy_=bstack1l1l1l1l11_opy_, bstack111lll1ll_opy_=bstack11111l11l_opy_)
        if not cli.bstack1llll1l1ll1_opy_(bstack1ll1lllll11_opy_):
            if getattr(item, bstack1l1ll11_opy_ (u"ࠩࡢࡥ࠶࠷ࡹࡠࡵࡷࡥࡷࡺࡥࡥࠩ῝"), False):
                bstack1l1l1l1ll1_opy_.bstack1ll111ll_opy_(getattr(item, bstack1l1ll11_opy_ (u"ࠪࡣࡩࡸࡩࡷࡧࡵࠫ῞"), None), bstack11llll1lll_opy_, logger, item)
        if not bstack111l111ll_opy_.on():
            return
        bstack111lll111l_opy_ = {
            bstack1l1ll11_opy_ (u"ࠫࡺࡻࡩࡥࠩ῟"): uuid4().__str__(),
            bstack1l1ll11_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩῠ"): bstack111l11l11l_opy_().isoformat() + bstack1l1ll11_opy_ (u"࡚࠭ࠨῡ"),
            bstack1l1ll11_opy_ (u"ࠧࡵࡻࡳࡩࠬῢ"): bstack1l1ll11_opy_ (u"ࠨࡪࡲࡳࡰ࠭ΰ"),
            bstack1l1ll11_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡵࡻࡳࡩࠬῤ"): bstack1l1ll11_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡈࡅࡈࡎࠧῥ"),
            bstack1l1ll11_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡱࡥࡲ࡫ࠧῦ"): bstack1l1ll11_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴࠧῧ")
        }
        _111l11llll_opy_[item.nodeid + bstack1l1ll11_opy_ (u"࠭࠭ࡵࡧࡤࡶࡩࡵࡷ࡯ࠩῨ")] = bstack111lll111l_opy_
        bstack1111l11111l_opy_(item, bstack111lll111l_opy_, bstack1l1ll11_opy_ (u"ࠧࡉࡱࡲ࡯ࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨῩ"))
    except Exception as err:
        print(bstack1l1ll11_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࡟ࡳࡷࡱࡸࡪࡹࡴࡠࡶࡨࡥࡷࡪ࡯ࡸࡰ࠽ࠤࢀࢃࠧῪ"), str(err))
@pytest.hookimpl(hookwrapper=True)
def pytest_fixture_setup(fixturedef, request):
    if bstack111l1l11ll1_opy_(fixturedef.argname):
        store[bstack1l1ll11_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡱࡴࡪࡵ࡭ࡧࡢ࡭ࡹ࡫࡭ࠨΎ")] = request.node
    elif bstack111l1l11lll_opy_(fixturedef.argname):
        store[bstack1l1ll11_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡨࡲࡡࡴࡵࡢ࡭ࡹ࡫࡭ࠨῬ")] = request.node
    if not bstack111l111ll_opy_.on():
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1lll11l11l1_opy_.SETUP_FIXTURE, bstack1lll1ll111l_opy_.PRE, fixturedef, request)
        outcome = yield
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1lll11l11l1_opy_.SETUP_FIXTURE, bstack1lll1ll111l_opy_.POST, fixturedef, request, outcome)
        return # skip all existing bstack1111l111l11_opy_
    start_time = datetime.datetime.now()
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lll11l11l1_opy_.SETUP_FIXTURE, bstack1lll1ll111l_opy_.PRE, fixturedef, request)
    outcome = yield
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lll11l11l1_opy_.SETUP_FIXTURE, bstack1lll1ll111l_opy_.POST, fixturedef, request, outcome)
        return # skip all existing bstack1111l111l11_opy_
    try:
        fixture = {
            bstack1l1ll11_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ῭"): fixturedef.argname,
            bstack1l1ll11_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬ΅"): bstack11l1l1111l1_opy_(outcome),
            bstack1l1ll11_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࠨ`"): (datetime.datetime.now() - start_time).total_seconds() * 1000
        }
        current_test_item = store[bstack1l1ll11_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡩࡵࡧࡰࠫ῰")]
        if not _111l11llll_opy_.get(current_test_item.nodeid, None):
            _111l11llll_opy_[current_test_item.nodeid] = {bstack1l1ll11_opy_ (u"ࠨࡨ࡬ࡼࡹࡻࡲࡦࡵࠪ῱"): []}
        _111l11llll_opy_[current_test_item.nodeid][bstack1l1ll11_opy_ (u"ࠩࡩ࡭ࡽࡺࡵࡳࡧࡶࠫῲ")].append(fixture)
    except Exception as err:
        logger.debug(bstack1l1ll11_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵࡡࡩ࡭ࡽࡺࡵࡳࡧࡢࡷࡪࡺࡵࡱ࠼ࠣࡿࢂ࠭ῳ"), str(err))
if bstack1lll111ll_opy_() and bstack111l111ll_opy_.on():
    def pytest_bdd_before_step(request, step):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1lll11l11l1_opy_.STEP, bstack1lll1ll111l_opy_.PRE, request, step)
            return
        try:
            _111l11llll_opy_[request.node.nodeid][bstack1l1ll11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧῴ")].bstack1lll1l1l1_opy_(id(step))
        except Exception as err:
            print(bstack1l1ll11_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷࡣࡧࡪࡤࡠࡤࡨࡪࡴࡸࡥࡠࡵࡷࡩࡵࡀࠠࡼࡿࠪ῵"), str(err))
    def pytest_bdd_step_error(request, step, exception):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1lll11l11l1_opy_.STEP, bstack1lll1ll111l_opy_.POST, request, step, exception)
            return
        try:
            _111l11llll_opy_[request.node.nodeid][bstack1l1ll11_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩῶ")].bstack111lllllll_opy_(id(step), Result.failed(exception=exception))
        except Exception as err:
            print(bstack1l1ll11_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡺࡶࡨࡷࡹࡥࡢࡥࡦࡢࡷࡹ࡫ࡰࡠࡧࡵࡶࡴࡸ࠺ࠡࡽࢀࠫῷ"), str(err))
    def pytest_bdd_after_step(request, step):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1lll11l11l1_opy_.STEP, bstack1lll1ll111l_opy_.POST, request, step)
            return
        try:
            bstack11l111lll1_opy_: bstack11l111ll11_opy_ = _111l11llll_opy_[request.node.nodeid][bstack1l1ll11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫῸ")]
            bstack11l111lll1_opy_.bstack111lllllll_opy_(id(step), Result.passed())
        except Exception as err:
            print(bstack1l1ll11_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲࡼࡸࡪࡹࡴࡠࡤࡧࡨࡤࡹࡴࡦࡲࡢࡩࡷࡸ࡯ࡳ࠼ࠣࡿࢂ࠭Ό"), str(err))
    def pytest_bdd_before_scenario(request, feature, scenario):
        global bstack11111lll1l1_opy_
        try:
            if not bstack111l111ll_opy_.on() or bstack11111lll1l1_opy_ != bstack1l1ll11_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠧῺ"):
                return
            if cli.is_running():
                cli.test_framework.track_event(cli_context, bstack1lll11l11l1_opy_.TEST, bstack1lll1ll111l_opy_.PRE, request, feature, scenario)
                return
            driver = bstack1lllll11_opy_(threading.current_thread(), bstack1l1ll11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡗࡪࡹࡳࡪࡱࡱࡈࡷ࡯ࡶࡦࡴࠪΏ"), None)
            if not _111l11llll_opy_.get(request.node.nodeid, None):
                _111l11llll_opy_[request.node.nodeid] = {}
            bstack11l111lll1_opy_ = bstack11l111ll11_opy_.bstack111l111l1ll_opy_(
                scenario, feature, request.node,
                name=bstack111l1l11l1l_opy_(request.node, scenario),
                started_at=bstack1l11111ll_opy_(),
                file_path=feature.filename,
                scope=[feature.name],
                framework=bstack1l1ll11_opy_ (u"ࠬࡖࡹࡵࡧࡶࡸ࠲ࡩࡵࡤࡷࡰࡦࡪࡸࠧῼ"),
                tags=bstack111l1l1lll1_opy_(feature, scenario),
                bstack11l1111ll1_opy_=bstack111l111ll_opy_.bstack11l111l11l_opy_(driver) if driver and driver.session_id else {}
            )
            _111l11llll_opy_[request.node.nodeid][bstack1l1ll11_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ´")] = bstack11l111lll1_opy_
            bstack1111l11ll1l_opy_(bstack11l111lll1_opy_.uuid)
            bstack111l111ll_opy_.bstack111lllll11_opy_(bstack1l1ll11_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨ῾"), bstack11l111lll1_opy_)
        except Exception as err:
            print(bstack1l1ll11_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࡟ࡣࡦࡧࡣࡧ࡫ࡦࡰࡴࡨࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴࡀࠠࡼࡿࠪ῿"), str(err))
def bstack1111l111ll1_opy_(bstack111llllll1_opy_):
    if bstack111llllll1_opy_ in store[bstack1l1ll11_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭ ")]:
        store[bstack1l1ll11_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧ ")].remove(bstack111llllll1_opy_)
def bstack1111l11ll1l_opy_(test_uuid):
    store[bstack1l1ll11_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨ ")] = test_uuid
    threading.current_thread().current_test_uuid = test_uuid
@bstack111l111ll_opy_.bstack1111ll1l1l1_opy_
def bstack1111l111lll_opy_(item, call, report):
    logger.debug(bstack1l1ll11_opy_ (u"ࠬ࡮ࡡ࡯ࡦ࡯ࡩࡤࡵ࠱࠲ࡻࡢࡸࡪࡹࡴࡠࡧࡹࡩࡳࡺ࠺ࠡࡵࡷࡥࡷࡺࠧ "))
    global bstack11111lll1l1_opy_
    bstack1l1l111ll_opy_ = bstack1l11111ll_opy_()
    if hasattr(report, bstack1l1ll11_opy_ (u"࠭ࡳࡵࡱࡳࠫ ")):
        bstack1l1l111ll_opy_ = bstack11ll11llll1_opy_(report.stop)
    elif hasattr(report, bstack1l1ll11_opy_ (u"ࠧࡴࡶࡤࡶࡹ࠭ ")):
        bstack1l1l111ll_opy_ = bstack11ll11llll1_opy_(report.start)
    try:
        if getattr(report, bstack1l1ll11_opy_ (u"ࠨࡹ࡫ࡩࡳ࠭ "), bstack1l1ll11_opy_ (u"ࠩࠪ ")) == bstack1l1ll11_opy_ (u"ࠪࡧࡦࡲ࡬ࠨ "):
            logger.debug(bstack1l1ll11_opy_ (u"ࠫ࡭ࡧ࡮ࡥ࡮ࡨࡣࡴ࠷࠱ࡺࡡࡷࡩࡸࡺ࡟ࡦࡸࡨࡲࡹࡀࠠࡴࡶࡤࡸࡪࠦ࠭ࠡࡽࢀ࠰ࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠡ࠯ࠣࡿࢂ࠭ ").format(getattr(report, bstack1l1ll11_opy_ (u"ࠬࡽࡨࡦࡰࠪ "), bstack1l1ll11_opy_ (u"࠭ࠧ​")).__str__(), bstack11111lll1l1_opy_))
            if bstack11111lll1l1_opy_ == bstack1l1ll11_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ‌"):
                _111l11llll_opy_[item.nodeid][bstack1l1ll11_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭‍")] = bstack1l1l111ll_opy_
                bstack11111ll11ll_opy_(item, _111l11llll_opy_[item.nodeid], bstack1l1ll11_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫ‎"), report, call)
                store[bstack1l1ll11_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧ‏")] = None
            elif bstack11111lll1l1_opy_ == bstack1l1ll11_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠣ‐"):
                bstack11l111lll1_opy_ = _111l11llll_opy_[item.nodeid][bstack1l1ll11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨ‑")]
                bstack11l111lll1_opy_.set(hooks=_111l11llll_opy_[item.nodeid].get(bstack1l1ll11_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬ‒"), []))
                exception, bstack11l11111l1_opy_ = None, None
                if call.excinfo:
                    exception = call.excinfo.value
                    bstack11l11111l1_opy_ = [call.excinfo.exconly(), getattr(report, bstack1l1ll11_opy_ (u"ࠧ࡭ࡱࡱ࡫ࡷ࡫ࡰࡳࡶࡨࡼࡹ࠭–"), bstack1l1ll11_opy_ (u"ࠨࠩ—"))]
                bstack11l111lll1_opy_.stop(time=bstack1l1l111ll_opy_, result=Result(result=getattr(report, bstack1l1ll11_opy_ (u"ࠩࡲࡹࡹࡩ࡯࡮ࡧࠪ―"), bstack1l1ll11_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪ‖")), exception=exception, bstack11l11111l1_opy_=bstack11l11111l1_opy_))
                bstack111l111ll_opy_.bstack111lllll11_opy_(bstack1l1ll11_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭‗"), _111l11llll_opy_[item.nodeid][bstack1l1ll11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨ‘")])
        elif getattr(report, bstack1l1ll11_opy_ (u"࠭ࡷࡩࡧࡱࠫ’"), bstack1l1ll11_opy_ (u"ࠧࠨ‚")) in [bstack1l1ll11_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧ‛"), bstack1l1ll11_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࠫ“")]:
            logger.debug(bstack1l1ll11_opy_ (u"ࠪ࡬ࡦࡴࡤ࡭ࡧࡢࡳ࠶࠷ࡹࡠࡶࡨࡷࡹࡥࡥࡷࡧࡱࡸ࠿ࠦࡳࡵࡣࡷࡩࠥ࠳ࠠࡼࡿ࠯ࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠠ࠮ࠢࡾࢁࠬ”").format(getattr(report, bstack1l1ll11_opy_ (u"ࠫࡼ࡮ࡥ࡯ࠩ„"), bstack1l1ll11_opy_ (u"ࠬ࠭‟")).__str__(), bstack11111lll1l1_opy_))
            bstack11l111l111_opy_ = item.nodeid + bstack1l1ll11_opy_ (u"࠭࠭ࠨ†") + getattr(report, bstack1l1ll11_opy_ (u"ࠧࡸࡪࡨࡲࠬ‡"), bstack1l1ll11_opy_ (u"ࠨࠩ•"))
            if getattr(report, bstack1l1ll11_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪ‣"), False):
                hook_type = bstack1l1ll11_opy_ (u"ࠪࡆࡊࡌࡏࡓࡇࡢࡉࡆࡉࡈࠨ․") if getattr(report, bstack1l1ll11_opy_ (u"ࠫࡼ࡮ࡥ࡯ࠩ‥"), bstack1l1ll11_opy_ (u"ࠬ࠭…")) == bstack1l1ll11_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬ‧") else bstack1l1ll11_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡅࡂࡅࡋࠫ ")
                _111l11llll_opy_[bstack11l111l111_opy_] = {
                    bstack1l1ll11_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ "): uuid4().__str__(),
                    bstack1l1ll11_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭‪"): bstack1l1l111ll_opy_,
                    bstack1l1ll11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡶࡼࡴࡪ࠭‫"): hook_type
                }
            _111l11llll_opy_[bstack11l111l111_opy_][bstack1l1ll11_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ‬")] = bstack1l1l111ll_opy_
            bstack1111l111ll1_opy_(_111l11llll_opy_[bstack11l111l111_opy_][bstack1l1ll11_opy_ (u"ࠬࡻࡵࡪࡦࠪ‭")])
            bstack1111l11111l_opy_(item, _111l11llll_opy_[bstack11l111l111_opy_], bstack1l1ll11_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨ‮"), report, call)
            if getattr(report, bstack1l1ll11_opy_ (u"ࠧࡸࡪࡨࡲࠬ "), bstack1l1ll11_opy_ (u"ࠨࠩ‰")) == bstack1l1ll11_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨ‱"):
                if getattr(report, bstack1l1ll11_opy_ (u"ࠪࡳࡺࡺࡣࡰ࡯ࡨࠫ′"), bstack1l1ll11_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫ″")) == bstack1l1ll11_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ‴"):
                    bstack111lll111l_opy_ = {
                        bstack1l1ll11_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ‵"): uuid4().__str__(),
                        bstack1l1ll11_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫ‶"): bstack1l11111ll_opy_(),
                        bstack1l1ll11_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭‷"): bstack1l11111ll_opy_()
                    }
                    _111l11llll_opy_[item.nodeid] = {**_111l11llll_opy_[item.nodeid], **bstack111lll111l_opy_}
                    bstack11111ll11ll_opy_(item, _111l11llll_opy_[item.nodeid], bstack1l1ll11_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪ‸"))
                    bstack11111ll11ll_opy_(item, _111l11llll_opy_[item.nodeid], bstack1l1ll11_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬ‹"), report, call)
    except Exception as err:
        print(bstack1l1ll11_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣ࡬ࡦࡴࡤ࡭ࡧࡢࡳ࠶࠷ࡹࡠࡶࡨࡷࡹࡥࡥࡷࡧࡱࡸ࠿ࠦࡻࡾࠩ›"), str(err))
def bstack1111l11l11l_opy_(test, bstack111lll111l_opy_, result=None, call=None, bstack1l11l11l1_opy_=None, outcome=None):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    bstack11l111lll1_opy_ = {
        bstack1l1ll11_opy_ (u"ࠬࡻࡵࡪࡦࠪ※"): bstack111lll111l_opy_[bstack1l1ll11_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ‼")],
        bstack1l1ll11_opy_ (u"ࠧࡵࡻࡳࡩࠬ‽"): bstack1l1ll11_opy_ (u"ࠨࡶࡨࡷࡹ࠭‾"),
        bstack1l1ll11_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ‿"): test.name,
        bstack1l1ll11_opy_ (u"ࠪࡦࡴࡪࡹࠨ⁀"): {
            bstack1l1ll11_opy_ (u"ࠫࡱࡧ࡮ࡨࠩ⁁"): bstack1l1ll11_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬ⁂"),
            bstack1l1ll11_opy_ (u"࠭ࡣࡰࡦࡨࠫ⁃"): inspect.getsource(test.obj)
        },
        bstack1l1ll11_opy_ (u"ࠧࡪࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ⁄"): test.name,
        bstack1l1ll11_opy_ (u"ࠨࡵࡦࡳࡵ࡫ࠧ⁅"): test.name,
        bstack1l1ll11_opy_ (u"ࠩࡶࡧࡴࡶࡥࡴࠩ⁆"): bstack1l1llll11_opy_.bstack111lll11ll_opy_(test),
        bstack1l1ll11_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭⁇"): file_path,
        bstack1l1ll11_opy_ (u"ࠫࡱࡵࡣࡢࡶ࡬ࡳࡳ࠭⁈"): file_path,
        bstack1l1ll11_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬ⁉"): bstack1l1ll11_opy_ (u"࠭ࡰࡦࡰࡧ࡭ࡳ࡭ࠧ⁊"),
        bstack1l1ll11_opy_ (u"ࠧࡷࡥࡢࡪ࡮ࡲࡥࡱࡣࡷ࡬ࠬ⁋"): file_path,
        bstack1l1ll11_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬ⁌"): bstack111lll111l_opy_[bstack1l1ll11_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭⁍")],
        bstack1l1ll11_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭⁎"): bstack1l1ll11_opy_ (u"ࠫࡕࡿࡴࡦࡵࡷࠫ⁏"),
        bstack1l1ll11_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡗ࡫ࡲࡶࡰࡓࡥࡷࡧ࡭ࠨ⁐"): {
            bstack1l1ll11_opy_ (u"࠭ࡲࡦࡴࡸࡲࡤࡴࡡ࡮ࡧࠪ⁑"): test.nodeid
        },
        bstack1l1ll11_opy_ (u"ࠧࡵࡣࡪࡷࠬ⁒"): bstack11l1l11ll1l_opy_(test.own_markers)
    }
    if bstack1l11l11l1_opy_ in [bstack1l1ll11_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕ࡮࡭ࡵࡶࡥࡥࠩ⁓"), bstack1l1ll11_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫ⁔")]:
        bstack11l111lll1_opy_[bstack1l1ll11_opy_ (u"ࠪࡱࡪࡺࡡࠨ⁕")] = {
            bstack1l1ll11_opy_ (u"ࠫ࡫࡯ࡸࡵࡷࡵࡩࡸ࠭⁖"): bstack111lll111l_opy_.get(bstack1l1ll11_opy_ (u"ࠬ࡬ࡩࡹࡶࡸࡶࡪࡹࠧ⁗"), [])
        }
    if bstack1l11l11l1_opy_ == bstack1l1ll11_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓ࡬࡫ࡳࡴࡪࡪࠧ⁘"):
        bstack11l111lll1_opy_[bstack1l1ll11_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ⁙")] = bstack1l1ll11_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩ⁚")
        bstack11l111lll1_opy_[bstack1l1ll11_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨ⁛")] = bstack111lll111l_opy_[bstack1l1ll11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩ⁜")]
        bstack11l111lll1_opy_[bstack1l1ll11_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ⁝")] = bstack111lll111l_opy_[bstack1l1ll11_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ⁞")]
    if result:
        bstack11l111lll1_opy_[bstack1l1ll11_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ ")] = result.outcome
        bstack11l111lll1_opy_[bstack1l1ll11_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࡡ࡬ࡲࡤࡳࡳࠨ⁠")] = result.duration * 1000
        bstack11l111lll1_opy_[bstack1l1ll11_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭⁡")] = bstack111lll111l_opy_[bstack1l1ll11_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧ⁢")]
        if result.failed:
            bstack11l111lll1_opy_[bstack1l1ll11_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࡣࡹࡿࡰࡦࠩ⁣")] = bstack111l111ll_opy_.bstack1111ll111l_opy_(call.excinfo.typename)
            bstack11l111lll1_opy_[bstack1l1ll11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࠬ⁤")] = bstack111l111ll_opy_.bstack1111ll1l11l_opy_(call.excinfo, result)
        bstack11l111lll1_opy_[bstack1l1ll11_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫ⁥")] = bstack111lll111l_opy_[bstack1l1ll11_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬ⁦")]
    if outcome:
        bstack11l111lll1_opy_[bstack1l1ll11_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ⁧")] = bstack11l1l1111l1_opy_(outcome)
        bstack11l111lll1_opy_[bstack1l1ll11_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࡢ࡭ࡳࡥ࡭ࡴࠩ⁨")] = 0
        bstack11l111lll1_opy_[bstack1l1ll11_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧ⁩")] = bstack111lll111l_opy_[bstack1l1ll11_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨ⁪")]
        if bstack11l111lll1_opy_[bstack1l1ll11_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫ⁫")] == bstack1l1ll11_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ⁬"):
            bstack11l111lll1_opy_[bstack1l1ll11_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫࡟ࡵࡻࡳࡩࠬ⁭")] = bstack1l1ll11_opy_ (u"ࠧࡖࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡈࡶࡷࡵࡲࠨ⁮")  # bstack1111l111111_opy_
            bstack11l111lll1_opy_[bstack1l1ll11_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࠩ⁯")] = [{bstack1l1ll11_opy_ (u"ࠩࡥࡥࡨࡱࡴࡳࡣࡦࡩࠬ⁰"): [bstack1l1ll11_opy_ (u"ࠪࡷࡴࡳࡥࠡࡧࡵࡶࡴࡸࠧⁱ")]}]
        bstack11l111lll1_opy_[bstack1l1ll11_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪ⁲")] = bstack111lll111l_opy_[bstack1l1ll11_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫ⁳")]
    return bstack11l111lll1_opy_
def bstack1111l1111l1_opy_(test, bstack111l1l1l11_opy_, bstack1l11l11l1_opy_, result, call, outcome, bstack11111ll1ll1_opy_):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    hook_type = bstack111l1l1l11_opy_[bstack1l1ll11_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡹࡿࡰࡦࠩ⁴")]
    hook_name = bstack111l1l1l11_opy_[bstack1l1ll11_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡴࡡ࡮ࡧࠪ⁵")]
    hook_data = {
        bstack1l1ll11_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭⁶"): bstack111l1l1l11_opy_[bstack1l1ll11_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ⁷")],
        bstack1l1ll11_opy_ (u"ࠪࡸࡾࡶࡥࠨ⁸"): bstack1l1ll11_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩ⁹"),
        bstack1l1ll11_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ⁺"): bstack1l1ll11_opy_ (u"࠭ࡻࡾࠩ⁻").format(bstack111l1ll111l_opy_(hook_name)),
        bstack1l1ll11_opy_ (u"ࠧࡣࡱࡧࡽࠬ⁼"): {
            bstack1l1ll11_opy_ (u"ࠨ࡮ࡤࡲ࡬࠭⁽"): bstack1l1ll11_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩ⁾"),
            bstack1l1ll11_opy_ (u"ࠪࡧࡴࡪࡥࠨⁿ"): None
        },
        bstack1l1ll11_opy_ (u"ࠫࡸࡩ࡯ࡱࡧࠪ₀"): test.name,
        bstack1l1ll11_opy_ (u"ࠬࡹࡣࡰࡲࡨࡷࠬ₁"): bstack1l1llll11_opy_.bstack111lll11ll_opy_(test, hook_name),
        bstack1l1ll11_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩ₂"): file_path,
        bstack1l1ll11_opy_ (u"ࠧ࡭ࡱࡦࡥࡹ࡯࡯࡯ࠩ₃"): file_path,
        bstack1l1ll11_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨ₄"): bstack1l1ll11_opy_ (u"ࠩࡳࡩࡳࡪࡩ࡯ࡩࠪ₅"),
        bstack1l1ll11_opy_ (u"ࠪࡺࡨࡥࡦࡪ࡮ࡨࡴࡦࡺࡨࠨ₆"): file_path,
        bstack1l1ll11_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨ₇"): bstack111l1l1l11_opy_[bstack1l1ll11_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩ₈")],
        bstack1l1ll11_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩ₉"): bstack1l1ll11_opy_ (u"ࠧࡑࡻࡷࡩࡸࡺ࠭ࡤࡷࡦࡹࡲࡨࡥࡳࠩ₊") if bstack11111lll1l1_opy_ == bstack1l1ll11_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠬ₋") else bstack1l1ll11_opy_ (u"ࠩࡓࡽࡹ࡫ࡳࡵࠩ₌"),
        bstack1l1ll11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡶࡼࡴࡪ࠭₍"): hook_type
    }
    bstack1111llllll1_opy_ = bstack111l1lll11_opy_(_111l11llll_opy_.get(test.nodeid, None))
    if bstack1111llllll1_opy_:
        hook_data[bstack1l1ll11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡩࡥࠩ₎")] = bstack1111llllll1_opy_
    if result:
        hook_data[bstack1l1ll11_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬ₏")] = result.outcome
        hook_data[bstack1l1ll11_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࡠ࡫ࡱࡣࡲࡹࠧₐ")] = result.duration * 1000
        hook_data[bstack1l1ll11_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬₑ")] = bstack111l1l1l11_opy_[bstack1l1ll11_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ₒ")]
        if result.failed:
            hook_data[bstack1l1ll11_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࡢࡸࡾࡶࡥࠨₓ")] = bstack111l111ll_opy_.bstack1111ll111l_opy_(call.excinfo.typename)
            hook_data[bstack1l1ll11_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࠫₔ")] = bstack111l111ll_opy_.bstack1111ll1l11l_opy_(call.excinfo, result)
    if outcome:
        hook_data[bstack1l1ll11_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫₕ")] = bstack11l1l1111l1_opy_(outcome)
        hook_data[bstack1l1ll11_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴ࡟ࡪࡰࡢࡱࡸ࠭ₖ")] = 100
        hook_data[bstack1l1ll11_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫₗ")] = bstack111l1l1l11_opy_[bstack1l1ll11_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬₘ")]
        if hook_data[bstack1l1ll11_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨₙ")] == bstack1l1ll11_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩₚ"):
            hook_data[bstack1l1ll11_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࡣࡹࡿࡰࡦࠩₛ")] = bstack1l1ll11_opy_ (u"࡚ࠫࡴࡨࡢࡰࡧࡰࡪࡪࡅࡳࡴࡲࡶࠬₜ")  # bstack1111l111111_opy_
            hook_data[bstack1l1ll11_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪ࠭₝")] = [{bstack1l1ll11_opy_ (u"࠭ࡢࡢࡥ࡮ࡸࡷࡧࡣࡦࠩ₞"): [bstack1l1ll11_opy_ (u"ࠧࡴࡱࡰࡩࠥ࡫ࡲࡳࡱࡵࠫ₟")]}]
    if bstack11111ll1ll1_opy_:
        hook_data[bstack1l1ll11_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨ₠")] = bstack11111ll1ll1_opy_.result
        hook_data[bstack1l1ll11_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࡣ࡮ࡴ࡟࡮ࡵࠪ₡")] = bstack11l1l111ll1_opy_(bstack111l1l1l11_opy_[bstack1l1ll11_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧ₢")], bstack111l1l1l11_opy_[bstack1l1ll11_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ₣")])
        hook_data[bstack1l1ll11_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ₤")] = bstack111l1l1l11_opy_[bstack1l1ll11_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ₥")]
        if hook_data[bstack1l1ll11_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ₦")] == bstack1l1ll11_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ₧"):
            hook_data[bstack1l1ll11_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࡢࡸࡾࡶࡥࠨ₨")] = bstack111l111ll_opy_.bstack1111ll111l_opy_(bstack11111ll1ll1_opy_.exception_type)
            hook_data[bstack1l1ll11_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࠫ₩")] = [{bstack1l1ll11_opy_ (u"ࠫࡧࡧࡣ࡬ࡶࡵࡥࡨ࡫ࠧ₪"): bstack11l11llll11_opy_(bstack11111ll1ll1_opy_.exception)}]
    return hook_data
def bstack11111ll11ll_opy_(test, bstack111lll111l_opy_, bstack1l11l11l1_opy_, result=None, call=None, outcome=None):
    logger.debug(bstack1l1ll11_opy_ (u"ࠬࡹࡥ࡯ࡦࡢࡸࡪࡹࡴࡠࡴࡸࡲࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡇࡴࡵࡧࡰࡴࡹ࡯࡮ࡨࠢࡷࡳࠥ࡭ࡥ࡯ࡧࡵࡥࡹ࡫ࠠࡵࡧࡶࡸࠥࡪࡡࡵࡣࠣࡪࡴࡸࠠࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠤ࠲ࠦࡻࡾࠩ₫").format(bstack1l11l11l1_opy_))
    bstack11l111lll1_opy_ = bstack1111l11l11l_opy_(test, bstack111lll111l_opy_, result, call, bstack1l11l11l1_opy_, outcome)
    driver = getattr(test, bstack1l1ll11_opy_ (u"࠭࡟ࡥࡴ࡬ࡺࡪࡸࠧ€"), None)
    if bstack1l11l11l1_opy_ == bstack1l1ll11_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨ₭") and driver:
        bstack11l111lll1_opy_[bstack1l1ll11_opy_ (u"ࠨ࡫ࡱࡸࡪ࡭ࡲࡢࡶ࡬ࡳࡳࡹࠧ₮")] = bstack111l111ll_opy_.bstack11l111l11l_opy_(driver)
    if bstack1l11l11l1_opy_ == bstack1l1ll11_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖ࡯࡮ࡶࡰࡦࡦࠪ₯"):
        bstack1l11l11l1_opy_ = bstack1l1ll11_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬ₰")
    bstack111l1ll1l1_opy_ = {
        bstack1l1ll11_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨ₱"): bstack1l11l11l1_opy_,
        bstack1l1ll11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴࠧ₲"): bstack11l111lll1_opy_
    }
    bstack111l111ll_opy_.bstack1ll11l11l1_opy_(bstack111l1ll1l1_opy_)
    if bstack1l11l11l1_opy_ == bstack1l1ll11_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧ₳"):
        threading.current_thread().bstackTestMeta = {bstack1l1ll11_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧ₴"): bstack1l1ll11_opy_ (u"ࠨࡲࡨࡲࡩ࡯࡮ࡨࠩ₵")}
    elif bstack1l11l11l1_opy_ == bstack1l1ll11_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫ₶"):
        threading.current_thread().bstackTestMeta = {bstack1l1ll11_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪ₷"): getattr(result, bstack1l1ll11_opy_ (u"ࠫࡴࡻࡴࡤࡱࡰࡩࠬ₸"), bstack1l1ll11_opy_ (u"ࠬ࠭₹"))}
def bstack1111l11111l_opy_(test, bstack111lll111l_opy_, bstack1l11l11l1_opy_, result=None, call=None, outcome=None, bstack11111ll1ll1_opy_=None):
    logger.debug(bstack1l1ll11_opy_ (u"࠭ࡳࡦࡰࡧࡣ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡥࡷࡧࡱࡸ࠿ࠦࡁࡵࡶࡨࡱࡵࡺࡩ࡯ࡩࠣࡸࡴࠦࡧࡦࡰࡨࡶࡦࡺࡥࠡࡪࡲࡳࡰࠦࡤࡢࡶࡤ࠰ࠥ࡫ࡶࡦࡰࡷࡘࡾࡶࡥࠡ࠯ࠣࡿࢂ࠭₺").format(bstack1l11l11l1_opy_))
    hook_data = bstack1111l1111l1_opy_(test, bstack111lll111l_opy_, bstack1l11l11l1_opy_, result, call, outcome, bstack11111ll1ll1_opy_)
    bstack111l1ll1l1_opy_ = {
        bstack1l1ll11_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫ₻"): bstack1l11l11l1_opy_,
        bstack1l1ll11_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࠪ₼"): hook_data
    }
    bstack111l111ll_opy_.bstack1ll11l11l1_opy_(bstack111l1ll1l1_opy_)
def bstack111l1lll11_opy_(bstack111lll111l_opy_):
    if not bstack111lll111l_opy_:
        return None
    if bstack111lll111l_opy_.get(bstack1l1ll11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬ₽"), None):
        return getattr(bstack111lll111l_opy_[bstack1l1ll11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭₾")], bstack1l1ll11_opy_ (u"ࠫࡺࡻࡩࡥࠩ₿"), None)
    return bstack111lll111l_opy_.get(bstack1l1ll11_opy_ (u"ࠬࡻࡵࡪࡦࠪ⃀"), None)
@pytest.fixture(autouse=True)
def second_fixture(caplog, request):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lll11l11l1_opy_.LOG, bstack1lll1ll111l_opy_.PRE, request, caplog)
    yield
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lll11l11l1_opy_.LOG, bstack1lll1ll111l_opy_.POST, request, caplog)
        return # skip all existing bstack1111l111l11_opy_
    try:
        if not bstack111l111ll_opy_.on():
            return
        places = [bstack1l1ll11_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬ⃁"), bstack1l1ll11_opy_ (u"ࠧࡤࡣ࡯ࡰࠬ⃂"), bstack1l1ll11_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࠪ⃃")]
        logs = []
        for bstack11111lll11l_opy_ in places:
            records = caplog.get_records(bstack11111lll11l_opy_)
            bstack11111ll111l_opy_ = bstack1l1ll11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ⃄") if bstack11111lll11l_opy_ == bstack1l1ll11_opy_ (u"ࠪࡧࡦࡲ࡬ࠨ⃅") else bstack1l1ll11_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ⃆")
            bstack11111llll1l_opy_ = request.node.nodeid + (bstack1l1ll11_opy_ (u"ࠬ࠭⃇") if bstack11111lll11l_opy_ == bstack1l1ll11_opy_ (u"࠭ࡣࡢ࡮࡯ࠫ⃈") else bstack1l1ll11_opy_ (u"ࠧ࠮ࠩ⃉") + bstack11111lll11l_opy_)
            test_uuid = bstack111l1lll11_opy_(_111l11llll_opy_.get(bstack11111llll1l_opy_, None))
            if not test_uuid:
                continue
            for record in records:
                if bstack11ll1111l11_opy_(record.message):
                    continue
                logs.append({
                    bstack1l1ll11_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫ⃊"): bstack11ll11111ll_opy_(record.created).isoformat() + bstack1l1ll11_opy_ (u"ࠩ࡝ࠫ⃋"),
                    bstack1l1ll11_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩ⃌"): record.levelname,
                    bstack1l1ll11_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ⃍"): record.message,
                    bstack11111ll111l_opy_: test_uuid
                })
        if len(logs) > 0:
            bstack111l111ll_opy_.bstack1l11lll1_opy_(logs)
    except Exception as err:
        print(bstack1l1ll11_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡸ࡫ࡣࡰࡰࡧࡣ࡫࡯ࡸࡵࡷࡵࡩ࠿ࠦࡻࡾࠩ⃎"), str(err))
def bstack1111l1lll_opy_(sequence, driver_command, response=None, driver = None, args = None):
    global bstack1ll1l1111_opy_
    bstack11l1l11l11_opy_ = bstack1lllll11_opy_(threading.current_thread(), bstack1l1ll11_opy_ (u"࠭ࡩࡴࡃ࠴࠵ࡾ࡚ࡥࡴࡶࠪ⃏"), None) and bstack1lllll11_opy_(
            threading.current_thread(), bstack1l1ll11_opy_ (u"ࠧࡢ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭⃐"), None)
    bstack11l1l1lll_opy_ = getattr(driver, bstack1l1ll11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡂ࠳࠴ࡽࡘ࡮࡯ࡶ࡮ࡧࡗࡨࡧ࡮ࠨ⃑"), None) != None and getattr(driver, bstack1l1ll11_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡃ࠴࠵ࡾ࡙ࡨࡰࡷ࡯ࡨࡘࡩࡡ࡯⃒ࠩ"), None) == True
    if sequence == bstack1l1ll11_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧ⃓ࠪ") and driver != None:
      if not bstack1ll1l1111_opy_ and bstack1ll11111111_opy_() and bstack1l1ll11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ⃔") in CONFIG and CONFIG[bstack1l1ll11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ⃕")] == True and bstack11ll1l11ll_opy_.bstack1llll1ll11_opy_(driver_command) and (bstack11l1l1lll_opy_ or bstack11l1l11l11_opy_) and not bstack1l111llll_opy_(args):
        try:
          bstack1ll1l1111_opy_ = True
          logger.debug(bstack1l1ll11_opy_ (u"࠭ࡐࡦࡴࡩࡳࡷࡳࡩ࡯ࡩࠣࡷࡨࡧ࡮ࠡࡨࡲࡶࠥࢁࡽࠨ⃖").format(driver_command))
          logger.debug(perform_scan(driver, driver_command=driver_command))
        except Exception as err:
          logger.debug(bstack1l1ll11_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡴࡪࡸࡦࡰࡴࡰࠤࡸࡩࡡ࡯ࠢࡾࢁࠬ⃗").format(str(err)))
        bstack1ll1l1111_opy_ = False
    if sequence == bstack1l1ll11_opy_ (u"ࠨࡣࡩࡸࡪࡸ⃘ࠧ"):
        if driver_command == bstack1l1ll11_opy_ (u"ࠩࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹ⃙࠭"):
            bstack111l111ll_opy_.bstack1lllll111_opy_({
                bstack1l1ll11_opy_ (u"ࠪ࡭ࡲࡧࡧࡦ⃚ࠩ"): response[bstack1l1ll11_opy_ (u"ࠫࡻࡧ࡬ࡶࡧࠪ⃛")],
                bstack1l1ll11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ⃜"): store[bstack1l1ll11_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪ⃝")]
            })
def bstack11ll11l111_opy_():
    global bstack1l1lll11_opy_
    bstack111l1l111_opy_.bstack1lllllll11_opy_()
    logging.shutdown()
    bstack111l111ll_opy_.bstack111ll1111l_opy_()
    for driver in bstack1l1lll11_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack11111ll1l11_opy_(*args):
    global bstack1l1lll11_opy_
    bstack111l111ll_opy_.bstack111ll1111l_opy_()
    for driver in bstack1l1lll11_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack1lllll1l1_opy_, stage=STAGE.bstack1ll1111ll1_opy_, bstack1l11lll11_opy_=bstack11ll1lll11_opy_)
def bstack1l11ll1l11_opy_(self, *args, **kwargs):
    bstack11l1ll1111_opy_ = bstack1ll1111lll_opy_(self, *args, **kwargs)
    bstack1ll11lll11_opy_ = getattr(threading.current_thread(), bstack1l1ll11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡔࡦࡵࡷࡑࡪࡺࡡࠨ⃞"), None)
    if bstack1ll11lll11_opy_ and bstack1ll11lll11_opy_.get(bstack1l1ll11_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ⃟"), bstack1l1ll11_opy_ (u"ࠩࠪ⃠")) == bstack1l1ll11_opy_ (u"ࠪࡴࡪࡴࡤࡪࡰࡪࠫ⃡"):
        bstack111l111ll_opy_.bstack1ll1lllll_opy_(self)
    return bstack11l1ll1111_opy_
@measure(event_name=EVENTS.bstack1l1ll11l11_opy_, stage=STAGE.bstack1l1l1l111_opy_, bstack1l11lll11_opy_=bstack11ll1lll11_opy_)
def bstack1ll1lll1_opy_(framework_name):
    from bstack_utils.config import Config
    bstack11llllllll_opy_ = Config.bstack1l1111llll_opy_()
    if bstack11llllllll_opy_.get_property(bstack1l1ll11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡲࡵࡤࡠࡥࡤࡰࡱ࡫ࡤࠨ⃢")):
        return
    bstack11llllllll_opy_.bstack1l1ll11l_opy_(bstack1l1ll11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡳ࡯ࡥࡡࡦࡥࡱࡲࡥࡥࠩ⃣"), True)
    global bstack1l1l1111l_opy_
    global bstack11lll11lll_opy_
    bstack1l1l1111l_opy_ = framework_name
    logger.info(bstack1l1lll1lll_opy_.format(bstack1l1l1111l_opy_.split(bstack1l1ll11_opy_ (u"࠭࠭ࠨ⃤"))[0]))
    try:
        from selenium import webdriver
        from selenium.webdriver.common.service import Service
        from selenium.webdriver.remote.webdriver import WebDriver
        if bstack1ll11111111_opy_():
            Service.start = bstack1llll1l11l_opy_
            Service.stop = bstack1l11lll1l_opy_
            webdriver.Remote.get = bstack1l1lll1ll_opy_
            webdriver.Remote.__init__ = bstack11ll111l11_opy_
            if not isinstance(os.getenv(bstack1l1ll11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐ࡚ࡖࡈࡗ࡙ࡥࡐࡂࡔࡄࡐࡑࡋࡌࠨ⃥")), str):
                return
            WebDriver.close = bstack11lllll111_opy_
            WebDriver.quit = bstack1ll1lll1ll_opy_
            WebDriver.getAccessibilityResults = getAccessibilityResults
            WebDriver.get_accessibility_results = getAccessibilityResults
            WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
            WebDriver.get_accessibility_results_summary = getAccessibilityResultsSummary
            WebDriver.performScan = perform_scan
            WebDriver.perform_scan = perform_scan
        elif bstack111l111ll_opy_.on():
            webdriver.Remote.__init__ = bstack1l11ll1l11_opy_
        bstack11lll11lll_opy_ = True
    except Exception as e:
        pass
    if os.environ.get(bstack1l1ll11_opy_ (u"ࠨࡕࡈࡐࡊࡔࡉࡖࡏࡢࡓࡗࡥࡐࡍࡃ࡜࡛ࡗࡏࡇࡉࡖࡢࡍࡓ࡙ࡔࡂࡎࡏࡉࡉ⃦࠭")):
        bstack11lll11lll_opy_ = eval(os.environ.get(bstack1l1ll11_opy_ (u"ࠩࡖࡉࡑࡋࡎࡊࡗࡐࡣࡔࡘ࡟ࡑࡎࡄ࡝࡜ࡘࡉࡈࡊࡗࡣࡎࡔࡓࡕࡃࡏࡐࡊࡊࠧ⃧")))
    if not bstack11lll11lll_opy_:
        bstack11lllllll1_opy_(bstack1l1ll11_opy_ (u"ࠥࡔࡦࡩ࡫ࡢࡩࡨࡷࠥࡴ࡯ࡵࠢ࡬ࡲࡸࡺࡡ࡭࡮ࡨࡨ⃨ࠧ"), bstack1llll1ll_opy_)
    if bstack1l1lll1l1l_opy_():
        try:
            from selenium.webdriver.remote.remote_connection import RemoteConnection
            RemoteConnection._111ll1l1_opy_ = bstack1l1l11ll1l_opy_
        except Exception as e:
            logger.error(bstack1ll1l11lll_opy_.format(str(e)))
    if bstack1l1ll11_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ⃩") in str(framework_name).lower():
        if not bstack1ll11111111_opy_():
            return
        try:
            from pytest_selenium import pytest_selenium
            from _pytest.config import Config
            pytest_selenium.pytest_report_header = bstack1l11ll1lll_opy_
            from pytest_selenium.drivers import browserstack
            browserstack.pytest_selenium_runtest_makereport = bstack111ll1ll1_opy_
            Config.getoption = bstack11l1ll1ll_opy_
        except Exception as e:
            pass
        try:
            from pytest_bdd import reporting
            reporting.runtest_makereport = bstack11l11l1l1l_opy_
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack11l1l1ll1l_opy_, stage=STAGE.bstack1ll1111ll1_opy_, bstack1l11lll11_opy_=bstack11ll1lll11_opy_)
def bstack1ll1lll1ll_opy_(self):
    global bstack1l1l1111l_opy_
    global bstack1ll1lll11_opy_
    global bstack1lll1lll1l_opy_
    try:
        if bstack1l1ll11_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸ⃪ࠬ") in bstack1l1l1111l_opy_ and self.session_id != None and bstack1lllll11_opy_(threading.current_thread(), bstack1l1ll11_opy_ (u"࠭ࡴࡦࡵࡷࡗࡹࡧࡴࡶࡵ⃫ࠪ"), bstack1l1ll11_opy_ (u"ࠧࠨ⃬")) != bstack1l1ll11_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥ⃭ࠩ"):
            bstack11l1l1l11_opy_ = bstack1l1ll11_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥ⃮ࠩ") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack1l1ll11_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦ⃯ࠪ")
            bstack1llll1111_opy_(logger, True)
            if self != None:
                bstack11lll1lll_opy_(self, bstack11l1l1l11_opy_, bstack1l1ll11_opy_ (u"ࠫ࠱ࠦࠧ⃰").join(threading.current_thread().bstackTestErrorMessages))
        if not cli.bstack1llll1l1ll1_opy_(bstack1ll1lllll11_opy_):
            item = store.get(bstack1l1ll11_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡺࡥ࡮ࠩ⃱"), None)
            if item is not None and bstack1lllll11_opy_(threading.current_thread(), bstack1l1ll11_opy_ (u"࠭ࡡ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬ⃲"), None):
                bstack1l1l1l1ll1_opy_.bstack1ll111ll_opy_(self, bstack11llll1lll_opy_, logger, item)
        threading.current_thread().testStatus = bstack1l1ll11_opy_ (u"ࠧࠨ⃳")
    except Exception as e:
        logger.debug(bstack1l1ll11_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦ࡭ࡢࡴ࡮࡭ࡳ࡭ࠠࡴࡶࡤࡸࡺࡹ࠺ࠡࠤ⃴") + str(e))
    bstack1lll1lll1l_opy_(self)
    self.session_id = None
@measure(event_name=EVENTS.bstack11l1llll_opy_, stage=STAGE.bstack1ll1111ll1_opy_, bstack1l11lll11_opy_=bstack11ll1lll11_opy_)
def bstack11ll111l11_opy_(self, command_executor,
             desired_capabilities=None, bstack1l1lll11ll_opy_=None, proxy=None,
             keep_alive=True, file_detector=None, options=None):
    global CONFIG
    global bstack1ll1lll11_opy_
    global bstack11ll1lll11_opy_
    global bstack1l11lll1l1_opy_
    global bstack1l1l1111l_opy_
    global bstack1ll1111lll_opy_
    global bstack1l1lll11_opy_
    global bstack1l1ll1l1_opy_
    global bstack11l11lll11_opy_
    global bstack11llll1lll_opy_
    CONFIG[bstack1l1ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡔࡆࡎࠫ⃵")] = str(bstack1l1l1111l_opy_) + str(__version__)
    command_executor = bstack11l1lll11_opy_(bstack1l1ll1l1_opy_, CONFIG)
    logger.debug(bstack11111lll_opy_.format(command_executor))
    proxy = bstack1llll111l1_opy_(CONFIG, proxy)
    bstack11111l11l_opy_ = 0
    try:
        if bstack1l11lll1l1_opy_ is True:
            bstack11111l11l_opy_ = int(os.environ.get(bstack1l1ll11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪ⃶")))
    except:
        bstack11111l11l_opy_ = 0
    bstack11l1l1ll11_opy_ = bstack1llll1l11_opy_(CONFIG, bstack11111l11l_opy_)
    logger.debug(bstack1llll1ll1l_opy_.format(str(bstack11l1l1ll11_opy_)))
    bstack11llll1lll_opy_ = CONFIG.get(bstack1l1ll11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ⃷"))[bstack11111l11l_opy_]
    if bstack1l1ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩ⃸") in CONFIG and CONFIG[bstack1l1ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪ⃹")]:
        bstack1l1l111l_opy_(bstack11l1l1ll11_opy_, bstack11l11lll11_opy_)
    if bstack1ll11llll1_opy_.bstack1l1llll1_opy_(CONFIG, bstack11111l11l_opy_) and bstack1ll11llll1_opy_.bstack11lll1lll1_opy_(bstack11l1l1ll11_opy_, options, desired_capabilities):
        threading.current_thread().a11yPlatform = True
        if not cli.bstack1llll1l1ll1_opy_(bstack1ll1lllll11_opy_):
            bstack1ll11llll1_opy_.set_capabilities(bstack11l1l1ll11_opy_, CONFIG)
    if desired_capabilities:
        bstack1l111l111l_opy_ = bstack11l1l1llll_opy_(desired_capabilities)
        bstack1l111l111l_opy_[bstack1l1ll11_opy_ (u"ࠧࡶࡵࡨ࡛࠸ࡉࠧ⃺")] = bstack1ll1l11ll_opy_(CONFIG)
        bstack1l11llll11_opy_ = bstack1llll1l11_opy_(bstack1l111l111l_opy_)
        if bstack1l11llll11_opy_:
            bstack11l1l1ll11_opy_ = update(bstack1l11llll11_opy_, bstack11l1l1ll11_opy_)
        desired_capabilities = None
    if options:
        bstack1l1lll1ll1_opy_(options, bstack11l1l1ll11_opy_)
    if not options:
        options = bstack1llll1llll_opy_(bstack11l1l1ll11_opy_)
    if proxy and bstack1l1llll1l_opy_() >= version.parse(bstack1l1ll11_opy_ (u"ࠨ࠶࠱࠵࠵࠴࠰ࠨ⃻")):
        options.proxy(proxy)
    if options and bstack1l1llll1l_opy_() >= version.parse(bstack1l1ll11_opy_ (u"ࠩ࠶࠲࠽࠴࠰ࠨ⃼")):
        desired_capabilities = None
    if (
            not options and not desired_capabilities
    ) or (
            bstack1l1llll1l_opy_() < version.parse(bstack1l1ll11_opy_ (u"ࠪ࠷࠳࠾࠮࠱ࠩ⃽")) and not desired_capabilities
    ):
        desired_capabilities = {}
        desired_capabilities.update(bstack11l1l1ll11_opy_)
    logger.info(bstack11lll11l1l_opy_)
    bstack1lll111l_opy_.end(EVENTS.bstack1l1ll11l11_opy_.value, EVENTS.bstack1l1ll11l11_opy_.value + bstack1l1ll11_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦ⃾"),
                               EVENTS.bstack1l1ll11l11_opy_.value + bstack1l1ll11_opy_ (u"ࠧࡀࡥ࡯ࡦࠥ⃿"), True, None)
    if bstack1l1llll1l_opy_() >= version.parse(bstack1l1ll11_opy_ (u"࠭࠴࠯࠳࠳࠲࠵࠭℀")):
        bstack1ll1111lll_opy_(self, command_executor=command_executor,
                  options=options, keep_alive=keep_alive, file_detector=file_detector)
    elif bstack1l1llll1l_opy_() >= version.parse(bstack1l1ll11_opy_ (u"ࠧ࠴࠰࠻࠲࠵࠭℁")):
        bstack1ll1111lll_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities, options=options,
                  bstack1l1lll11ll_opy_=bstack1l1lll11ll_opy_, proxy=proxy,
                  keep_alive=keep_alive, file_detector=file_detector)
    elif bstack1l1llll1l_opy_() >= version.parse(bstack1l1ll11_opy_ (u"ࠨ࠴࠱࠹࠸࠴࠰ࠨℂ")):
        bstack1ll1111lll_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities,
                  bstack1l1lll11ll_opy_=bstack1l1lll11ll_opy_, proxy=proxy,
                  keep_alive=keep_alive, file_detector=file_detector)
    else:
        bstack1ll1111lll_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities,
                  bstack1l1lll11ll_opy_=bstack1l1lll11ll_opy_, proxy=proxy,
                  keep_alive=keep_alive)
    try:
        bstack11ll1111ll_opy_ = bstack1l1ll11_opy_ (u"ࠩࠪ℃")
        if bstack1l1llll1l_opy_() >= version.parse(bstack1l1ll11_opy_ (u"ࠪ࠸࠳࠶࠮࠱ࡤ࠴ࠫ℄")):
            bstack11ll1111ll_opy_ = self.caps.get(bstack1l1ll11_opy_ (u"ࠦࡴࡶࡴࡪ࡯ࡤࡰࡍࡻࡢࡖࡴ࡯ࠦ℅"))
        else:
            bstack11ll1111ll_opy_ = self.capabilities.get(bstack1l1ll11_opy_ (u"ࠧࡵࡰࡵ࡫ࡰࡥࡱࡎࡵࡣࡗࡵࡰࠧ℆"))
        if bstack11ll1111ll_opy_:
            bstack1l11111lll_opy_(bstack11ll1111ll_opy_)
            if bstack1l1llll1l_opy_() <= version.parse(bstack1l1ll11_opy_ (u"࠭࠳࠯࠳࠶࠲࠵࠭ℇ")):
                self.command_executor._url = bstack1l1ll11_opy_ (u"ࠢࡩࡶࡷࡴ࠿࠵࠯ࠣ℈") + bstack1l1ll1l1_opy_ + bstack1l1ll11_opy_ (u"ࠣ࠼࠻࠴࠴ࡽࡤ࠰ࡪࡸࡦࠧ℉")
            else:
                self.command_executor._url = bstack1l1ll11_opy_ (u"ࠤ࡫ࡸࡹࡶࡳ࠻࠱࠲ࠦℊ") + bstack11ll1111ll_opy_ + bstack1l1ll11_opy_ (u"ࠥ࠳ࡼࡪ࠯ࡩࡷࡥࠦℋ")
            logger.debug(bstack1ll11ll1l_opy_.format(bstack11ll1111ll_opy_))
        else:
            logger.debug(bstack1l11l1l1l_opy_.format(bstack1l1ll11_opy_ (u"ࠦࡔࡶࡴࡪ࡯ࡤࡰࠥࡎࡵࡣࠢࡱࡳࡹࠦࡦࡰࡷࡱࡨࠧℌ")))
    except Exception as e:
        logger.debug(bstack1l11l1l1l_opy_.format(e))
    bstack1ll1lll11_opy_ = self.session_id
    if bstack1l1ll11_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬℍ") in bstack1l1l1111l_opy_:
        threading.current_thread().bstackSessionId = self.session_id
        threading.current_thread().bstackSessionDriver = self
        threading.current_thread().bstackTestErrorMessages = []
        item = store.get(bstack1l1ll11_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡴࡦ࡯ࠪℎ"), None)
        if item:
            bstack1111l11l1l1_opy_ = getattr(item, bstack1l1ll11_opy_ (u"ࠧࡠࡶࡨࡷࡹࡥࡣࡢࡵࡨࡣࡸࡺࡡࡳࡶࡨࡨࠬℏ"), False)
            if not getattr(item, bstack1l1ll11_opy_ (u"ࠨࡡࡧࡶ࡮ࡼࡥࡳࠩℐ"), None) and bstack1111l11l1l1_opy_:
                setattr(store[bstack1l1ll11_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡷࡩࡲ࠭ℑ")], bstack1l1ll11_opy_ (u"ࠪࡣࡩࡸࡩࡷࡧࡵࠫℒ"), self)
        bstack1ll11lll11_opy_ = getattr(threading.current_thread(), bstack1l1ll11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡘࡪࡹࡴࡎࡧࡷࡥࠬℓ"), None)
        if bstack1ll11lll11_opy_ and bstack1ll11lll11_opy_.get(bstack1l1ll11_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬ℔"), bstack1l1ll11_opy_ (u"࠭ࠧℕ")) == bstack1l1ll11_opy_ (u"ࠧࡱࡧࡱࡨ࡮ࡴࡧࠨ№"):
            bstack111l111ll_opy_.bstack1ll1lllll_opy_(self)
    bstack1l1lll11_opy_.append(self)
    if bstack1l1ll11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ℗") in CONFIG and bstack1l1ll11_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ℘") in CONFIG[bstack1l1ll11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ℙ")][bstack11111l11l_opy_]:
        bstack11ll1lll11_opy_ = CONFIG[bstack1l1ll11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧℚ")][bstack11111l11l_opy_][bstack1l1ll11_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪℛ")]
    logger.debug(bstack11lll1111_opy_.format(bstack1ll1lll11_opy_))
@measure(event_name=EVENTS.bstack11111111_opy_, stage=STAGE.bstack1ll1111ll1_opy_, bstack1l11lll11_opy_=bstack11ll1lll11_opy_)
def bstack1l1lll1ll_opy_(self, url):
    global bstack11l1lll1l1_opy_
    global CONFIG
    try:
        bstack1l1l1l1111_opy_(url, CONFIG, logger)
    except Exception as err:
        logger.debug(bstack11111l11_opy_.format(str(err)))
    try:
        bstack11l1lll1l1_opy_(self, url)
    except Exception as e:
        try:
            bstack1l11lllll1_opy_ = str(e)
            if any(err_msg in bstack1l11lllll1_opy_ for err_msg in bstack11lll111l1_opy_):
                bstack1l1l1l1111_opy_(url, CONFIG, logger, True)
        except Exception as err:
            logger.debug(bstack11111l11_opy_.format(str(err)))
        raise e
def bstack1ll1ll1ll1_opy_(item, when):
    global bstack1l111l1ll1_opy_
    try:
        bstack1l111l1ll1_opy_(item, when)
    except Exception as e:
        pass
def bstack11l11l1l1l_opy_(item, call, rep):
    global bstack1111l1l11_opy_
    global bstack1l1lll11_opy_
    name = bstack1l1ll11_opy_ (u"࠭ࠧℜ")
    try:
        if rep.when == bstack1l1ll11_opy_ (u"ࠧࡤࡣ࡯ࡰࠬℝ"):
            bstack1ll1lll11_opy_ = threading.current_thread().bstackSessionId
            bstack11111lllll1_opy_ = item.config.getoption(bstack1l1ll11_opy_ (u"ࠨࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ℞"))
            try:
                if (str(bstack11111lllll1_opy_).lower() != bstack1l1ll11_opy_ (u"ࠩࡷࡶࡺ࡫ࠧ℟")):
                    name = str(rep.nodeid)
                    bstack111l1ll1_opy_ = bstack1lll11l111_opy_(bstack1l1ll11_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫ℠"), name, bstack1l1ll11_opy_ (u"ࠫࠬ℡"), bstack1l1ll11_opy_ (u"ࠬ࠭™"), bstack1l1ll11_opy_ (u"࠭ࠧ℣"), bstack1l1ll11_opy_ (u"ࠧࠨℤ"))
                    os.environ[bstack1l1ll11_opy_ (u"ࠨࡒ࡜ࡘࡊ࡙ࡔࡠࡖࡈࡗ࡙ࡥࡎࡂࡏࡈࠫ℥")] = name
                    for driver in bstack1l1lll11_opy_:
                        if bstack1ll1lll11_opy_ == driver.session_id:
                            driver.execute_script(bstack111l1ll1_opy_)
            except Exception as e:
                logger.debug(bstack1l1ll11_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠣࡪࡴࡸࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠿ࠦࡻࡾࠩΩ").format(str(e)))
            try:
                bstack1lllll11ll_opy_(rep.outcome.lower())
                if rep.outcome.lower() != bstack1l1ll11_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫ℧"):
                    status = bstack1l1ll11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫℨ") if rep.outcome.lower() == bstack1l1ll11_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ℩") else bstack1l1ll11_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭K")
                    reason = bstack1l1ll11_opy_ (u"ࠧࠨÅ")
                    if status == bstack1l1ll11_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨℬ"):
                        reason = rep.longrepr.reprcrash.message
                        if (not threading.current_thread().bstackTestErrorMessages):
                            threading.current_thread().bstackTestErrorMessages = []
                        threading.current_thread().bstackTestErrorMessages.append(reason)
                    level = bstack1l1ll11_opy_ (u"ࠩ࡬ࡲ࡫ࡵࠧℭ") if status == bstack1l1ll11_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪ℮") else bstack1l1ll11_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪℯ")
                    data = name + bstack1l1ll11_opy_ (u"ࠬࠦࡰࡢࡵࡶࡩࡩࠧࠧℰ") if status == bstack1l1ll11_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ℱ") else name + bstack1l1ll11_opy_ (u"ࠧࠡࡨࡤ࡭ࡱ࡫ࡤࠢࠢࠪℲ") + reason
                    bstack11ll1l111_opy_ = bstack1lll11l111_opy_(bstack1l1ll11_opy_ (u"ࠨࡣࡱࡲࡴࡺࡡࡵࡧࠪℳ"), bstack1l1ll11_opy_ (u"ࠩࠪℴ"), bstack1l1ll11_opy_ (u"ࠪࠫℵ"), bstack1l1ll11_opy_ (u"ࠫࠬℶ"), level, data)
                    for driver in bstack1l1lll11_opy_:
                        if bstack1ll1lll11_opy_ == driver.session_id:
                            driver.execute_script(bstack11ll1l111_opy_)
            except Exception as e:
                logger.debug(bstack1l1ll11_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡴࡧࡷࡸ࡮ࡴࡧࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡦࡳࡳࡺࡥࡹࡶࠣࡪࡴࡸࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠿ࠦࡻࡾࠩℷ").format(str(e)))
    except Exception as e:
        logger.debug(bstack1l1ll11_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡩࡨࡸࡹ࡯࡮ࡨࠢࡶࡸࡦࡺࡥࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡶࡨࡷࡹࠦࡳࡵࡣࡷࡹࡸࡀࠠࡼࡿࠪℸ").format(str(e)))
    bstack1111l1l11_opy_(item, call, rep)
notset = Notset()
def bstack11l1ll1ll_opy_(self, name: str, default=notset, skip: bool = False):
    global bstack1lll11111l_opy_
    if str(name).lower() == bstack1l1ll11_opy_ (u"ࠧࡥࡴ࡬ࡺࡪࡸࠧℹ"):
        return bstack1l1ll11_opy_ (u"ࠣࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠢ℺")
    else:
        return bstack1lll11111l_opy_(self, name, default, skip)
def bstack1l1l11ll1l_opy_(self):
    global CONFIG
    global bstack11l1l1lll1_opy_
    try:
        proxy = bstack1lll1l1l_opy_(CONFIG)
        if proxy:
            if proxy.endswith(bstack1l1ll11_opy_ (u"ࠩ࠱ࡴࡦࡩࠧ℻")):
                proxies = bstack1l1lll111l_opy_(proxy, bstack11l1lll11_opy_())
                if len(proxies) > 0:
                    protocol, bstack1lll1ll1_opy_ = proxies.popitem()
                    if bstack1l1ll11_opy_ (u"ࠥ࠾࠴࠵ࠢℼ") in bstack1lll1ll1_opy_:
                        return bstack1lll1ll1_opy_
                    else:
                        return bstack1l1ll11_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳ࠧℽ") + bstack1lll1ll1_opy_
            else:
                return proxy
    except Exception as e:
        logger.error(bstack1l1ll11_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡴࡧࡷࡸ࡮ࡴࡧࠡࡲࡵࡳࡽࡿࠠࡶࡴ࡯ࠤ࠿ࠦࡻࡾࠤℾ").format(str(e)))
    return bstack11l1l1lll1_opy_(self)
def bstack1l1lll1l1l_opy_():
    return (bstack1l1ll11_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩℿ") in CONFIG or bstack1l1ll11_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫ⅀") in CONFIG) and bstack1l1l1lll11_opy_() and bstack1l1llll1l_opy_() >= version.parse(
        bstack111lll1l1_opy_)
def bstack111l11ll1_opy_(self,
               executablePath=None,
               channel=None,
               args=None,
               ignoreDefaultArgs=None,
               handleSIGINT=None,
               handleSIGTERM=None,
               handleSIGHUP=None,
               timeout=None,
               env=None,
               headless=None,
               devtools=None,
               proxy=None,
               downloadsPath=None,
               slowMo=None,
               tracesDir=None,
               chromiumSandbox=None,
               firefoxUserPrefs=None
               ):
    global CONFIG
    global bstack11ll1lll11_opy_
    global bstack1l11lll1l1_opy_
    global bstack1l1l1111l_opy_
    CONFIG[bstack1l1ll11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪ⅁")] = str(bstack1l1l1111l_opy_) + str(__version__)
    bstack11111l11l_opy_ = 0
    try:
        if bstack1l11lll1l1_opy_ is True:
            bstack11111l11l_opy_ = int(os.environ.get(bstack1l1ll11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩ⅂")))
    except:
        bstack11111l11l_opy_ = 0
    CONFIG[bstack1l1ll11_opy_ (u"ࠥ࡭ࡸࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤ⅃")] = True
    bstack11l1l1ll11_opy_ = bstack1llll1l11_opy_(CONFIG, bstack11111l11l_opy_)
    logger.debug(bstack1llll1ll1l_opy_.format(str(bstack11l1l1ll11_opy_)))
    if CONFIG.get(bstack1l1ll11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨ⅄")):
        bstack1l1l111l_opy_(bstack11l1l1ll11_opy_, bstack11l11lll11_opy_)
    if bstack1l1ll11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨⅅ") in CONFIG and bstack1l1ll11_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫⅆ") in CONFIG[bstack1l1ll11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪⅇ")][bstack11111l11l_opy_]:
        bstack11ll1lll11_opy_ = CONFIG[bstack1l1ll11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫⅈ")][bstack11111l11l_opy_][bstack1l1ll11_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧⅉ")]
    import urllib
    import json
    if bstack1l1ll11_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧ⅊") in CONFIG and str(CONFIG[bstack1l1ll11_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨ⅋")]).lower() != bstack1l1ll11_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫ⅌"):
        bstack1l1111l111_opy_ = bstack1ll1ll1lll_opy_()
        bstack1l1111111_opy_ = bstack1l1111l111_opy_ + urllib.parse.quote(json.dumps(bstack11l1l1ll11_opy_))
    else:
        bstack1l1111111_opy_ = bstack1l1ll11_opy_ (u"࠭ࡷࡴࡵ࠽࠳࠴ࡩࡤࡱ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࡁࡦࡥࡵࡹ࠽ࠨ⅍") + urllib.parse.quote(json.dumps(bstack11l1l1ll11_opy_))
    browser = self.connect(bstack1l1111111_opy_)
    return browser
def bstack11l1l1l11l_opy_():
    global bstack11lll11lll_opy_
    global bstack1l1l1111l_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        from bstack_utils.helper import bstack11l1l1ll_opy_
        if not bstack1ll11111111_opy_():
            global bstack1ll1ll111l_opy_
            if not bstack1ll1ll111l_opy_:
                from bstack_utils.helper import bstack11ll1lll1l_opy_, bstack11ll111l1_opy_
                bstack1ll1ll111l_opy_ = bstack11ll1lll1l_opy_()
                bstack11ll111l1_opy_(bstack1l1l1111l_opy_)
            BrowserType.connect = bstack11l1l1ll_opy_
            return
        BrowserType.launch = bstack111l11ll1_opy_
        bstack11lll11lll_opy_ = True
    except Exception as e:
        pass
def bstack1111l11l111_opy_():
    global CONFIG
    global bstack11l1l1l1ll_opy_
    global bstack1l1ll1l1_opy_
    global bstack11l11lll11_opy_
    global bstack1l11lll1l1_opy_
    global bstack11l11l111_opy_
    CONFIG = json.loads(os.environ.get(bstack1l1ll11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡐࡐࡉࡍࡌ࠭ⅎ")))
    bstack11l1l1l1ll_opy_ = eval(os.environ.get(bstack1l1ll11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩ⅏")))
    bstack1l1ll1l1_opy_ = os.environ.get(bstack1l1ll11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡊࡘࡆࡤ࡛ࡒࡍࠩ⅐"))
    bstack1l1lll1111_opy_(CONFIG, bstack11l1l1l1ll_opy_)
    bstack11l11l111_opy_ = bstack111l1l111_opy_.bstack11l11l11_opy_(CONFIG, bstack11l11l111_opy_)
    if cli.bstack11l11llll1_opy_():
        bstack1l1l11ll1_opy_.invoke(bstack1llll1111l_opy_.CONNECT, bstack1l11l1l11l_opy_())
        cli_context.platform_index = int(os.environ.get(bstack1l1ll11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪ⅑"), bstack1l1ll11_opy_ (u"ࠫ࠵࠭⅒")))
        cli.bstack1lll1llll1l_opy_(cli_context.platform_index)
        cli.bstack1lllllll111_opy_(bstack11l1lll11_opy_(bstack1l1ll1l1_opy_, CONFIG), cli_context.platform_index, bstack1llll1llll_opy_)
        cli.bstack1lll111111l_opy_()
        logger.debug(bstack1l1ll11_opy_ (u"ࠧࡉࡌࡊࠢ࡬ࡷࠥࡧࡣࡵ࡫ࡹࡩࠥ࡬࡯ࡳࠢࡳࡰࡦࡺࡦࡰࡴࡰࡣ࡮ࡴࡤࡦࡺࡀࠦ⅓") + str(cli_context.platform_index) + bstack1l1ll11_opy_ (u"ࠨࠢ⅔"))
        return # skip all existing bstack1111l111l11_opy_
    global bstack1ll1111lll_opy_
    global bstack1lll1lll1l_opy_
    global bstack1l1111l11l_opy_
    global bstack1l1ll1111l_opy_
    global bstack1l1ll1l1ll_opy_
    global bstack111l1llll_opy_
    global bstack1l1ll1lll_opy_
    global bstack11l1lll1l1_opy_
    global bstack11l1l1lll1_opy_
    global bstack1lll11111l_opy_
    global bstack1l111l1ll1_opy_
    global bstack1111l1l11_opy_
    try:
        from selenium import webdriver
        from selenium.webdriver.remote.webdriver import WebDriver
        bstack1ll1111lll_opy_ = webdriver.Remote.__init__
        bstack1lll1lll1l_opy_ = WebDriver.quit
        bstack1l1ll1lll_opy_ = WebDriver.close
        bstack11l1lll1l1_opy_ = WebDriver.get
    except Exception as e:
        pass
    if (bstack1l1ll11_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪ⅕") in CONFIG or bstack1l1ll11_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬ⅖") in CONFIG) and bstack1l1l1lll11_opy_():
        if bstack1l1llll1l_opy_() < version.parse(bstack111lll1l1_opy_):
            logger.error(bstack1l11l111ll_opy_.format(bstack1l1llll1l_opy_()))
        else:
            try:
                from selenium.webdriver.remote.remote_connection import RemoteConnection
                bstack11l1l1lll1_opy_ = RemoteConnection._111ll1l1_opy_
            except Exception as e:
                logger.error(bstack1ll1l11lll_opy_.format(str(e)))
    try:
        from _pytest.config import Config
        bstack1lll11111l_opy_ = Config.getoption
        from _pytest import runner
        bstack1l111l1ll1_opy_ = runner._update_current_test_var
    except Exception as e:
        logger.warn(e, bstack1l1l11l11_opy_)
    try:
        from pytest_bdd import reporting
        bstack1111l1l11_opy_ = reporting.runtest_makereport
    except Exception as e:
        logger.debug(bstack1l1ll11_opy_ (u"ࠩࡓࡰࡪࡧࡳࡦࠢ࡬ࡲࡸࡺࡡ࡭࡮ࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡵࡱࠣࡶࡺࡴࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡹ࡫ࡳࡵࡵࠪ⅗"))
    bstack11l11lll11_opy_ = CONFIG.get(bstack1l1ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧ⅘"), {}).get(bstack1l1ll11_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭⅙"))
    bstack1l11lll1l1_opy_ = True
    bstack1ll1lll1_opy_(bstack1111l1111_opy_)
if (bstack11l1l11ll11_opy_()):
    bstack1111l11l111_opy_()
@bstack111l11ll1l_opy_(class_method=False)
def bstack1111l111l1l_opy_(hook_name, event, bstack1l11l1l1111_opy_=None):
    if hook_name not in [bstack1l1ll11_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳ࠭⅚"), bstack1l1ll11_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡨࡸࡲࡨࡺࡩࡰࡰࠪ⅛"), bstack1l1ll11_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥ࡭ࡰࡦࡸࡰࡪ࠭⅜"), bstack1l1ll11_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡴࡪࡵ࡭ࡧࠪ⅝"), bstack1l1ll11_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠࡥ࡯ࡥࡸࡹࠧ⅞"), bstack1l1ll11_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡩ࡬ࡢࡵࡶࠫ⅟"), bstack1l1ll11_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡱࡪࡺࡨࡰࡦࠪⅠ"), bstack1l1ll11_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡧࡷ࡬ࡴࡪࠧⅡ")]:
        return
    node = store[bstack1l1ll11_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡴࡦ࡯ࠪⅢ")]
    if hook_name in [bstack1l1ll11_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥ࡭ࡰࡦࡸࡰࡪ࠭Ⅳ"), bstack1l1ll11_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡴࡪࡵ࡭ࡧࠪⅤ")]:
        node = store[bstack1l1ll11_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡱࡴࡪࡵ࡭ࡧࡢ࡭ࡹ࡫࡭ࠨⅥ")]
    elif hook_name in [bstack1l1ll11_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡦࡰࡦࡹࡳࠨⅦ"), bstack1l1ll11_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡣ࡭ࡣࡶࡷࠬⅧ")]:
        node = store[bstack1l1ll11_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡣ࡭ࡣࡶࡷࡤ࡯ࡴࡦ࡯ࠪⅨ")]
    hook_type = bstack111l1ll1111_opy_(hook_name)
    if event == bstack1l1ll11_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪ࠭Ⅹ"):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1lll11l11l1_opy_[hook_type], bstack1lll1ll111l_opy_.PRE, node, hook_name)
            return
        uuid = uuid4().__str__()
        bstack111l1l1l11_opy_ = {
            bstack1l1ll11_opy_ (u"ࠧࡶࡷ࡬ࡨࠬⅪ"): uuid,
            bstack1l1ll11_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬⅫ"): bstack1l11111ll_opy_(),
            bstack1l1ll11_opy_ (u"ࠩࡷࡽࡵ࡫ࠧⅬ"): bstack1l1ll11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࠨⅭ"),
            bstack1l1ll11_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡷࡽࡵ࡫ࠧⅮ"): hook_type,
            bstack1l1ll11_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡲࡦࡳࡥࠨⅯ"): hook_name
        }
        store[bstack1l1ll11_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪⅰ")].append(uuid)
        bstack11111lll1ll_opy_ = node.nodeid
        if hook_type == bstack1l1ll11_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡆࡃࡆࡌࠬⅱ"):
            if not _111l11llll_opy_.get(bstack11111lll1ll_opy_, None):
                _111l11llll_opy_[bstack11111lll1ll_opy_] = {bstack1l1ll11_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧⅲ"): []}
            _111l11llll_opy_[bstack11111lll1ll_opy_][bstack1l1ll11_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨⅳ")].append(bstack111l1l1l11_opy_[bstack1l1ll11_opy_ (u"ࠪࡹࡺ࡯ࡤࠨⅴ")])
        _111l11llll_opy_[bstack11111lll1ll_opy_ + bstack1l1ll11_opy_ (u"ࠫ࠲࠭ⅵ") + hook_name] = bstack111l1l1l11_opy_
        bstack1111l11111l_opy_(node, bstack111l1l1l11_opy_, bstack1l1ll11_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭ⅶ"))
    elif event == bstack1l1ll11_opy_ (u"࠭ࡡࡧࡶࡨࡶࠬⅷ"):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1lll11l11l1_opy_[hook_type], bstack1lll1ll111l_opy_.POST, node, None, bstack1l11l1l1111_opy_)
            return
        bstack11l111l111_opy_ = node.nodeid + bstack1l1ll11_opy_ (u"ࠧ࠮ࠩⅸ") + hook_name
        _111l11llll_opy_[bstack11l111l111_opy_][bstack1l1ll11_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ⅹ")] = bstack1l11111ll_opy_()
        bstack1111l111ll1_opy_(_111l11llll_opy_[bstack11l111l111_opy_][bstack1l1ll11_opy_ (u"ࠩࡸࡹ࡮ࡪࠧⅺ")])
        bstack1111l11111l_opy_(node, _111l11llll_opy_[bstack11l111l111_opy_], bstack1l1ll11_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬⅻ"), bstack11111ll1ll1_opy_=bstack1l11l1l1111_opy_)
def bstack11111lll111_opy_():
    global bstack11111lll1l1_opy_
    if bstack1lll111ll_opy_():
        bstack11111lll1l1_opy_ = bstack1l1ll11_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠨⅼ")
    else:
        bstack11111lll1l1_opy_ = bstack1l1ll11_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬⅽ")
@bstack111l111ll_opy_.bstack1111ll1l1l1_opy_
def bstack11111ll1l1l_opy_():
    bstack11111lll111_opy_()
    if cli.is_running():
        try:
            bstack11l11ll1l1l_opy_(bstack1111l111l1l_opy_)
        except Exception as e:
            logger.debug(bstack1l1ll11_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥ࡮࡯ࡰ࡭ࡶࠤࡵࡧࡴࡤࡪ࠽ࠤࢀࢃࠢⅾ").format(e))
        return
    if bstack1l1l1lll11_opy_():
        bstack11llllllll_opy_ = Config.bstack1l1111llll_opy_()
        bstack1l1ll11_opy_ (u"ࠧࠨࠩࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡈࡲࡶࠥࡶࡰࡱࠢࡀࠤ࠶࠲ࠠ࡮ࡱࡧࡣࡪࡾࡥࡤࡷࡷࡩࠥ࡭ࡥࡵࡵࠣࡹࡸ࡫ࡤࠡࡨࡲࡶࠥࡧ࠱࠲ࡻࠣࡧࡴࡳ࡭ࡢࡰࡧࡷ࠲ࡽࡲࡢࡲࡳ࡭ࡳ࡭ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡌ࡯ࡳࠢࡳࡴࡵࠦ࠾ࠡ࠳࠯ࠤࡲࡵࡤࡠࡧࡻࡩࡨࡻࡴࡦࠢࡧࡳࡪࡹࠠ࡯ࡱࡷࠤࡷࡻ࡮ࠡࡤࡨࡧࡦࡻࡳࡦࠢ࡬ࡸࠥ࡯ࡳࠡࡲࡤࡸࡨ࡮ࡥࡥࠢ࡬ࡲࠥࡧࠠࡥ࡫ࡩࡪࡪࡸࡥ࡯ࡶࠣࡴࡷࡵࡣࡦࡵࡶࠤ࡮ࡪࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࡚ࠥࡨࡶࡵࠣࡻࡪࠦ࡮ࡦࡧࡧࠤࡹࡵࠠࡶࡵࡨࠤࡘ࡫࡬ࡦࡰ࡬ࡹࡲࡖࡡࡵࡥ࡫ࠬࡸ࡫࡬ࡦࡰ࡬ࡹࡲࡥࡨࡢࡰࡧࡰࡪࡸࠩࠡࡨࡲࡶࠥࡶࡰࡱࠢࡁࠤ࠶ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠨࠩࠪⅿ")
        if bstack11llllllll_opy_.get_property(bstack1l1ll11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠ࡯ࡲࡨࡤࡩࡡ࡭࡮ࡨࡨࠬↀ")):
            if CONFIG.get(bstack1l1ll11_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩↁ")) is not None and int(CONFIG[bstack1l1ll11_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪↂ")]) > 1:
                bstack11l1l111l1_opy_(bstack1111l1lll_opy_)
            return
        bstack11l1l111l1_opy_(bstack1111l1lll_opy_)
    try:
        bstack11l11ll1l1l_opy_(bstack1111l111l1l_opy_)
    except Exception as e:
        logger.debug(bstack1l1ll11_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣ࡬ࡴࡵ࡫ࡴࠢࡳࡥࡹࡩࡨ࠻ࠢࡾࢁࠧↃ").format(e))
bstack11111ll1l1l_opy_()