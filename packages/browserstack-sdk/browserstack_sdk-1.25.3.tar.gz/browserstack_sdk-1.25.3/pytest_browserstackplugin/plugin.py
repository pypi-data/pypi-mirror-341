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
import atexit
import datetime
import inspect
import logging
import signal
import threading
from uuid import uuid4
from bstack_utils.measure import bstack1l11l111l1_opy_
from bstack_utils.percy_sdk import PercySDK
import pytest
from packaging import version
from browserstack_sdk.__init__ import (bstack1111l1l11_opy_, bstack1lll1l1lll_opy_, update, bstack1l1l1l1ll1_opy_,
                                       bstack11l1l1l1_opy_, bstack111l1l11_opy_, bstack111lll1ll_opy_, bstack111l11ll1_opy_,
                                       bstack1l1lll11l1_opy_, bstack1ll1l1l11l_opy_, bstack11llllll1l_opy_, bstack11l1l1l1l1_opy_,
                                       bstack1l1ll11ll1_opy_, getAccessibilityResults, getAccessibilityResultsSummary, perform_scan, bstack1l111l111l_opy_)
from browserstack_sdk.bstack1l1ll1l111_opy_ import bstack111111l11_opy_
from browserstack_sdk._version import __version__
from bstack_utils import bstack1l11l11lll_opy_
from bstack_utils.capture import bstack11l11l111l_opy_
from bstack_utils.config import Config
from bstack_utils.percy import *
from bstack_utils.constants import bstack1ll1llll_opy_, bstack11llll11ll_opy_, bstack1l11ll1lll_opy_, \
    bstack11l1ll111l_opy_
from bstack_utils.helper import bstack1l1l11l1l_opy_, bstack11l1l111lll_opy_, bstack111ll11ll1_opy_, bstack1l11l1l1_opy_, bstack1ll111l1ll1_opy_, bstack11l1l11ll1_opy_, \
    bstack11l1ll1l111_opy_, \
    bstack11ll1111l11_opy_, bstack11ll1ll11l_opy_, bstack1l1ll1l1ll_opy_, bstack11l1l1l1l11_opy_, bstack11111l1l1_opy_, Notset, \
    bstack1lll1l1l11_opy_, bstack11l1l111ll1_opy_, bstack11l1ll1ll11_opy_, Result, bstack11l1l11l1ll_opy_, bstack11l1l1lll1l_opy_, bstack111l1ll1l1_opy_, \
    bstack1ll1lll1_opy_, bstack11llll1111_opy_, bstack111llll11_opy_, bstack11l1lllll11_opy_
from bstack_utils.bstack11l11ll11l1_opy_ import bstack11l11lll1l1_opy_
from bstack_utils.messages import bstack1ll11111l_opy_, bstack1l1l11ll1l_opy_, bstack1l1l1lllll_opy_, bstack11ll1l1ll1_opy_, bstack1lllll111_opy_, \
    bstack1111ll1ll_opy_, bstack1111lll1l_opy_, bstack1l11llll11_opy_, bstack11l1l111ll_opy_, bstack1111ll111_opy_, \
    bstack11l1l11l_opy_, bstack1ll1ll1lll_opy_
from bstack_utils.proxy import bstack1lll11l111_opy_, bstack1l111ll1_opy_
from bstack_utils.bstack1ll1l11l1l_opy_ import bstack111l1l1ll11_opy_, bstack111l1l1lll1_opy_, bstack111l1l1ll1l_opy_, bstack111l1l11ll1_opy_, \
    bstack111l1l1l1ll_opy_, bstack111l1l1l11l_opy_, bstack111l1l1l1l1_opy_, bstack11lll1l1ll_opy_, bstack111l1l11l11_opy_
from bstack_utils.bstack11ll111lll_opy_ import bstack1ll1l1l111_opy_
from bstack_utils.bstack111lll1l_opy_ import bstack11ll1lll1_opy_, bstack11l11l11_opy_, bstack1ll111llll_opy_, \
    bstack1ll1llll1_opy_, bstack11111ll1l_opy_
from bstack_utils.bstack111lllll11_opy_ import bstack11l11111l1_opy_
from bstack_utils.bstack11l11l1111_opy_ import bstack11llll111l_opy_
import bstack_utils.accessibility as bstack1l1l11l11_opy_
from bstack_utils.bstack11l11l11l1_opy_ import bstack111111l1_opy_
from bstack_utils.bstack11ll111l1_opy_ import bstack11ll111l1_opy_
from browserstack_sdk.__init__ import bstack1ll1ll11l_opy_
from browserstack_sdk.sdk_cli.bstack1llll111lll_opy_ import bstack1lll11l1l1l_opy_
from browserstack_sdk.sdk_cli.bstack1llll1l111_opy_ import bstack1llll1l111_opy_, bstack1lll111l11_opy_, bstack1l1ll1lll_opy_
from browserstack_sdk.sdk_cli.test_framework import bstack1l11l1l11l1_opy_, bstack1lll1l1lll1_opy_, bstack1llll111ll1_opy_
from browserstack_sdk.sdk_cli.cli import cli
from browserstack_sdk.sdk_cli.bstack1llll1l111_opy_ import bstack1llll1l111_opy_, bstack1lll111l11_opy_, bstack1l1ll1lll_opy_
bstack11l11llll_opy_ = None
bstack11l1lllll_opy_ = None
bstack11ll1l11ll_opy_ = None
bstack111ll111l_opy_ = None
bstack1l1ll11lll_opy_ = None
bstack11l1l1l11_opy_ = None
bstack1l111lll1_opy_ = None
bstack1ll11llll1_opy_ = None
bstack1ll1l11ll1_opy_ = None
bstack1l11l1llll_opy_ = None
bstack1l1ll1111_opy_ = None
bstack11ll1l111_opy_ = None
bstack1l11llll1l_opy_ = None
bstack111l1l1l_opy_ = bstack1l1_opy_ (u"ࠧࠨὁ")
CONFIG = {}
bstack11lll1ll1_opy_ = False
bstack1lll11l1l_opy_ = bstack1l1_opy_ (u"ࠨࠩὂ")
bstack1lll11l1_opy_ = bstack1l1_opy_ (u"ࠩࠪὃ")
bstack1l11l1ll1_opy_ = False
bstack1l11lll111_opy_ = []
bstack1l11l1lll_opy_ = bstack1ll1llll_opy_
bstack1111l111ll1_opy_ = bstack1l1_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪὄ")
bstack1l111ll11l_opy_ = {}
bstack11l1l11l11_opy_ = None
bstack1l111111l_opy_ = False
logger = bstack1l11l11lll_opy_.get_logger(__name__, bstack1l11l1lll_opy_)
store = {
    bstack1l1_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨὅ"): []
}
bstack11111lll1ll_opy_ = False
try:
    from playwright.sync_api import (
        BrowserContext,
        Page
    )
except:
    pass
import json
_111llll111_opy_ = {}
current_test_uuid = None
cli_context = bstack1l11l1l11l1_opy_(
    test_framework_name=bstack1l1lll1111_opy_[bstack1l1_opy_ (u"ࠬࡖ࡙ࡕࡇࡖࡘ࠲ࡈࡄࡅࠩ὆")] if bstack11111l1l1_opy_() else bstack1l1lll1111_opy_[bstack1l1_opy_ (u"࠭ࡐ࡚ࡖࡈࡗ࡙࠭὇")],
    test_framework_version=pytest.__version__,
    platform_index=-1,
)
def bstack1lll111ll1_opy_(page, bstack11l1l11111_opy_):
    try:
        page.evaluate(bstack1l1_opy_ (u"ࠢࡠࠢࡀࡂࠥࢁࡽࠣὈ"),
                      bstack1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡴࡡ࡮ࡧࠥ࠾ࠬὉ") + json.dumps(
                          bstack11l1l11111_opy_) + bstack1l1_opy_ (u"ࠤࢀࢁࠧὊ"))
    except Exception as e:
        print(bstack1l1_opy_ (u"ࠥࡩࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩࠥࢁࡽࠣὋ"), e)
def bstack1ll1lllll_opy_(page, message, level):
    try:
        page.evaluate(bstack1l1_opy_ (u"ࠦࡤࠦ࠽࠿ࠢࡾࢁࠧὌ"), bstack1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡨࡦࡺࡡࠣ࠼ࠪὍ") + json.dumps(
            message) + bstack1l1_opy_ (u"࠭ࠬࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠩ὎") + json.dumps(level) + bstack1l1_opy_ (u"ࠧࡾࡿࠪ὏"))
    except Exception as e:
        print(bstack1l1_opy_ (u"ࠣࡧࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࡦࡴ࡮ࡰࡶࡤࡸ࡮ࡵ࡮ࠡࡽࢀࠦὐ"), e)
def pytest_configure(config):
    global bstack1lll11l1l_opy_
    global CONFIG
    bstack11llllll1_opy_ = Config.bstack111111ll_opy_()
    config.args = bstack11llll111l_opy_.bstack1111l1l111l_opy_(config.args)
    bstack11llllll1_opy_.bstack1ll1lll111_opy_(bstack111llll11_opy_(config.getoption(bstack1l1_opy_ (u"ࠩࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸ࠭ὑ"))))
    try:
        bstack1l11l11lll_opy_.bstack11l111lll1l_opy_(config.inipath, config.rootpath)
    except:
        pass
    if cli.is_running():
        bstack1llll1l111_opy_.invoke(bstack1lll111l11_opy_.CONNECT, bstack1l1ll1lll_opy_())
        cli_context.platform_index = int(os.environ.get(bstack1l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪὒ"), bstack1l1_opy_ (u"ࠫ࠵࠭ὓ")))
        config = json.loads(os.environ.get(bstack1l1_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡈࡕࡎࡇࡋࡊࠦὔ"), bstack1l1_opy_ (u"ࠨࡻࡾࠤὕ")))
        cli.bstack1lll111l111_opy_(bstack1l1ll1l1ll_opy_(bstack1lll11l1l_opy_, CONFIG), cli_context.platform_index, bstack1l1l1l1ll1_opy_)
    if cli.bstack1lll1lll11l_opy_(bstack1lll11l1l1l_opy_):
        cli.bstack1lllllll11l_opy_()
        logger.debug(bstack1l1_opy_ (u"ࠢࡄࡎࡌࠤ࡮ࡹࠠࡢࡥࡷ࡭ࡻ࡫ࠠࡧࡱࡵࠤࡵࡲࡡࡵࡨࡲࡶࡲࡥࡩ࡯ࡦࡨࡼࡂࠨὖ") + str(cli_context.platform_index) + bstack1l1_opy_ (u"ࠣࠤὗ"))
        cli.test_framework.track_event(cli_context, bstack1lll1l1lll1_opy_.BEFORE_ALL, bstack1llll111ll1_opy_.PRE, config)
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    when = getattr(call, bstack1l1_opy_ (u"ࠤࡺ࡬ࡪࡴࠢ὘"), None)
    if cli.is_running() and when == bstack1l1_opy_ (u"ࠥࡧࡦࡲ࡬ࠣὙ"):
        cli.test_framework.track_event(cli_context, bstack1lll1l1lll1_opy_.LOG_REPORT, bstack1llll111ll1_opy_.PRE, item, call)
    outcome = yield
    if cli.is_running():
        if when == bstack1l1_opy_ (u"ࠦࡸ࡫ࡴࡶࡲࠥ὚"):
            cli.test_framework.track_event(cli_context, bstack1lll1l1lll1_opy_.BEFORE_EACH, bstack1llll111ll1_opy_.POST, item, call, outcome)
        elif when == bstack1l1_opy_ (u"ࠧࡩࡡ࡭࡮ࠥὛ"):
            cli.test_framework.track_event(cli_context, bstack1lll1l1lll1_opy_.LOG_REPORT, bstack1llll111ll1_opy_.POST, item, call, outcome)
        elif when == bstack1l1_opy_ (u"ࠨࡴࡦࡣࡵࡨࡴࡽ࡮ࠣ὜"):
            cli.test_framework.track_event(cli_context, bstack1lll1l1lll1_opy_.AFTER_EACH, bstack1llll111ll1_opy_.POST, item, call, outcome)
        return # skip all existing bstack1111l11l1ll_opy_
    bstack11111ll11ll_opy_ = item.config.getoption(bstack1l1_opy_ (u"ࠧࡴ࡭࡬ࡴࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩὝ"))
    plugins = item.config.getoption(bstack1l1_opy_ (u"ࠣࡲ࡯ࡹ࡬࡯࡮ࡴࠤ὞"))
    report = outcome.get_result()
    bstack11111ll1ll1_opy_(item, call, report)
    if bstack1l1_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵࡡࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡱ࡮ࡸ࡫࡮ࡴࠢὟ") not in plugins or bstack11111l1l1_opy_():
        return
    summary = []
    driver = getattr(item, bstack1l1_opy_ (u"ࠥࡣࡩࡸࡩࡷࡧࡵࠦὠ"), None)
    page = getattr(item, bstack1l1_opy_ (u"ࠦࡤࡶࡡࡨࡧࠥὡ"), None)
    try:
        if (driver == None or driver.session_id == None):
            driver = threading.current_thread().bstackSessionDriver
    except:
        pass
    item._driver = driver
    if (driver is not None or cli.is_running()):
        bstack1111l1111ll_opy_(item, report, summary, bstack11111ll11ll_opy_)
    if (page is not None):
        bstack11111ll1l1l_opy_(item, report, summary, bstack11111ll11ll_opy_)
def bstack1111l1111ll_opy_(item, report, summary, bstack11111ll11ll_opy_):
    if report.when == bstack1l1_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫὢ") and report.skipped:
        bstack111l1l11l11_opy_(report)
    if report.when in [bstack1l1_opy_ (u"ࠨࡳࡦࡶࡸࡴࠧὣ"), bstack1l1_opy_ (u"ࠢࡵࡧࡤࡶࡩࡵࡷ࡯ࠤὤ")]:
        return
    if not bstack1ll111l1ll1_opy_():
        return
    try:
        if (str(bstack11111ll11ll_opy_).lower() != bstack1l1_opy_ (u"ࠨࡶࡵࡹࡪ࠭ὥ") and not cli.is_running()):
            item._driver.execute_script(
                bstack1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨ࡮ࡢ࡯ࡨࠦ࠿ࠦࠧὦ") + json.dumps(
                    report.nodeid) + bstack1l1_opy_ (u"ࠪࢁࢂ࠭ὧ"))
        os.environ[bstack1l1_opy_ (u"ࠫࡕ࡟ࡔࡆࡕࡗࡣ࡙ࡋࡓࡕࡡࡑࡅࡒࡋࠧὨ")] = report.nodeid
    except Exception as e:
        summary.append(
            bstack1l1_opy_ (u"ࠧ࡝ࡁࡓࡐࡌࡒࡌࡀࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡱࡦࡸ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡱࡥࡲ࡫࠺ࠡࡽ࠳ࢁࠧὩ").format(e)
        )
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack1l1_opy_ (u"ࠨࡷࡢࡵࡻࡪࡦ࡯࡬ࠣὪ")))
    bstack11l1l1l11l_opy_ = bstack1l1_opy_ (u"ࠢࠣὫ")
    bstack111l1l11l11_opy_(report)
    if not passed:
        try:
            bstack11l1l1l11l_opy_ = report.longrepr.reprcrash
        except Exception as e:
            summary.append(
                bstack1l1_opy_ (u"࡙ࠣࡄࡖࡓࡏࡎࡈ࠼ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡤࡦࡶࡨࡶࡲ࡯࡮ࡦࠢࡩࡥ࡮ࡲࡵࡳࡧࠣࡶࡪࡧࡳࡰࡰ࠽ࠤࢀ࠶ࡽࠣὬ").format(e)
            )
        try:
            if (threading.current_thread().bstackTestErrorMessages == None):
                threading.current_thread().bstackTestErrorMessages = []
        except Exception as e:
            threading.current_thread().bstackTestErrorMessages = []
        threading.current_thread().bstackTestErrorMessages.append(str(bstack11l1l1l11l_opy_))
    if not report.skipped:
        passed = report.passed or (report.failed and hasattr(report, bstack1l1_opy_ (u"ࠤࡺࡥࡸࡾࡦࡢ࡫࡯ࠦὭ")))
        bstack11l1l1l11l_opy_ = bstack1l1_opy_ (u"ࠥࠦὮ")
        if not passed:
            try:
                bstack11l1l1l11l_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack1l1_opy_ (u"ࠦ࡜ࡇࡒࡏࡋࡑࡋ࠿ࠦࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡧࡩࡹ࡫ࡲ࡮࡫ࡱࡩࠥ࡬ࡡࡪ࡮ࡸࡶࡪࠦࡲࡦࡣࡶࡳࡳࡀࠠࡼ࠲ࢀࠦὯ").format(e)
                )
            try:
                if (threading.current_thread().bstackTestErrorMessages == None):
                    threading.current_thread().bstackTestErrorMessages = []
            except Exception as e:
                threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(str(bstack11l1l1l11l_opy_))
        try:
            if passed:
                item._driver.execute_script(
                    bstack1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤ࠯ࠤࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠨ࡬ࡦࡸࡨࡰࠧࡀࠠࠣ࡫ࡱࡪࡴࠨࠬࠡ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠣࡦࡤࡸࡦࠨ࠺ࠡࠩὰ")
                    + json.dumps(bstack1l1_opy_ (u"ࠨࡰࡢࡵࡶࡩࡩࠧࠢά"))
                    + bstack1l1_opy_ (u"ࠢ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࢀࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡿࠥὲ")
                )
            else:
                item._driver.execute_script(
                    bstack1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧ࠲ࠠ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠤ࡯ࡩࡻ࡫࡬ࠣ࠼ࠣࠦࡪࡸࡲࡰࡴࠥ࠰ࠥࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠧࡪࡡࡵࡣࠥ࠾ࠥ࠭έ")
                    + json.dumps(str(bstack11l1l1l11l_opy_))
                    + bstack1l1_opy_ (u"ࠤ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࢂࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࢁࠧὴ")
                )
        except Exception as e:
            summary.append(bstack1l1_opy_ (u"࡛ࠥࡆࡘࡎࡊࡐࡊ࠾ࠥࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡣࡱࡲࡴࡺࡡࡵࡧ࠽ࠤࢀ࠶ࡽࠣή").format(e))
def bstack11111lll111_opy_(test_name, error_message):
    try:
        bstack11111ll11l1_opy_ = []
        bstack11ll11ll11_opy_ = os.environ.get(bstack1l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫὶ"), bstack1l1_opy_ (u"ࠬ࠶ࠧί"))
        bstack11lll111_opy_ = {bstack1l1_opy_ (u"࠭࡮ࡢ࡯ࡨࠫὸ"): test_name, bstack1l1_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ό"): error_message, bstack1l1_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧὺ"): bstack11ll11ll11_opy_}
        bstack1111l11l1l1_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1_opy_ (u"ࠩࡳࡻࡤࡶࡹࡵࡧࡶࡸࡤ࡫ࡲࡳࡱࡵࡣࡱ࡯ࡳࡵ࠰࡭ࡷࡴࡴࠧύ"))
        if os.path.exists(bstack1111l11l1l1_opy_):
            with open(bstack1111l11l1l1_opy_) as f:
                bstack11111ll11l1_opy_ = json.load(f)
        bstack11111ll11l1_opy_.append(bstack11lll111_opy_)
        with open(bstack1111l11l1l1_opy_, bstack1l1_opy_ (u"ࠪࡻࠬὼ")) as f:
            json.dump(bstack11111ll11l1_opy_, f)
    except Exception as e:
        logger.debug(bstack1l1_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡰࡦࡴࡶ࡭ࡸࡺࡩ࡯ࡩࠣࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡱࡻࡷࡩࡸࡺࠠࡦࡴࡵࡳࡷࡹ࠺ࠡࠩώ") + str(e))
def bstack11111ll1l1l_opy_(item, report, summary, bstack11111ll11ll_opy_):
    if report.when in [bstack1l1_opy_ (u"ࠧࡹࡥࡵࡷࡳࠦ὾"), bstack1l1_opy_ (u"ࠨࡴࡦࡣࡵࡨࡴࡽ࡮ࠣ὿")]:
        return
    if (str(bstack11111ll11ll_opy_).lower() != bstack1l1_opy_ (u"ࠧࡵࡴࡸࡩࠬᾀ")):
        bstack1lll111ll1_opy_(item._page, report.nodeid)
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack1l1_opy_ (u"ࠣࡹࡤࡷࡽ࡬ࡡࡪ࡮ࠥᾁ")))
    bstack11l1l1l11l_opy_ = bstack1l1_opy_ (u"ࠤࠥᾂ")
    bstack111l1l11l11_opy_(report)
    if not report.skipped:
        if not passed:
            try:
                bstack11l1l1l11l_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack1l1_opy_ (u"࡛ࠥࡆࡘࡎࡊࡐࡊ࠾ࠥࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡦࡨࡸࡪࡸ࡭ࡪࡰࡨࠤ࡫ࡧࡩ࡭ࡷࡵࡩࠥࡸࡥࡢࡵࡲࡲ࠿ࠦࡻ࠱ࡿࠥᾃ").format(e)
                )
        try:
            if passed:
                bstack11111ll1l_opy_(getattr(item, bstack1l1_opy_ (u"ࠫࡤࡶࡡࡨࡧࠪᾄ"), None), bstack1l1_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧᾅ"))
            else:
                error_message = bstack1l1_opy_ (u"࠭ࠧᾆ")
                if bstack11l1l1l11l_opy_:
                    bstack1ll1lllll_opy_(item._page, str(bstack11l1l1l11l_opy_), bstack1l1_opy_ (u"ࠢࡦࡴࡵࡳࡷࠨᾇ"))
                    bstack11111ll1l_opy_(getattr(item, bstack1l1_opy_ (u"ࠨࡡࡳࡥ࡬࡫ࠧᾈ"), None), bstack1l1_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤᾉ"), str(bstack11l1l1l11l_opy_))
                    error_message = str(bstack11l1l1l11l_opy_)
                else:
                    bstack11111ll1l_opy_(getattr(item, bstack1l1_opy_ (u"ࠪࡣࡵࡧࡧࡦࠩᾊ"), None), bstack1l1_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦᾋ"))
                bstack11111lll111_opy_(report.nodeid, error_message)
        except Exception as e:
            summary.append(bstack1l1_opy_ (u"ࠧ࡝ࡁࡓࡐࡌࡒࡌࡀࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡹࡵࡪࡡࡵࡧࠣࡷࡪࡹࡳࡪࡱࡱࠤࡸࡺࡡࡵࡷࡶ࠾ࠥࢁ࠰ࡾࠤᾌ").format(e))
def pytest_addoption(parser):
    parser.addoption(bstack1l1_opy_ (u"ࠨ࠭࠮ࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠥᾍ"), default=bstack1l1_opy_ (u"ࠢࡇࡣ࡯ࡷࡪࠨᾎ"), help=bstack1l1_opy_ (u"ࠣࡃࡸࡸࡴࡳࡡࡵ࡫ࡦࠤࡸ࡫ࡴࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡱࡥࡲ࡫ࠢᾏ"))
    parser.addoption(bstack1l1_opy_ (u"ࠤ࠰࠱ࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠣᾐ"), default=bstack1l1_opy_ (u"ࠥࡊࡦࡲࡳࡦࠤᾑ"), help=bstack1l1_opy_ (u"ࠦࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡩࠠࡴࡧࡷࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡴࡡ࡮ࡧࠥᾒ"))
    try:
        import pytest_selenium.pytest_selenium
    except:
        parser.addoption(bstack1l1_opy_ (u"ࠧ࠳࠭ࡥࡴ࡬ࡺࡪࡸࠢᾓ"), action=bstack1l1_opy_ (u"ࠨࡳࡵࡱࡵࡩࠧᾔ"), default=bstack1l1_opy_ (u"ࠢࡤࡪࡵࡳࡲ࡫ࠢᾕ"),
                         help=bstack1l1_opy_ (u"ࠣࡆࡵ࡭ࡻ࡫ࡲࠡࡶࡲࠤࡷࡻ࡮ࠡࡶࡨࡷࡹࡹࠢᾖ"))
def bstack11l111l1l1_opy_(log):
    if not (log[bstack1l1_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᾗ")] and log[bstack1l1_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᾘ")].strip()):
        return
    active = bstack11l1111l11_opy_()
    log = {
        bstack1l1_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪᾙ"): log[bstack1l1_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫᾚ")],
        bstack1l1_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩᾛ"): bstack111ll11ll1_opy_().isoformat() + bstack1l1_opy_ (u"࡛ࠧࠩᾜ"),
        bstack1l1_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᾝ"): log[bstack1l1_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᾞ")],
    }
    if active:
        if active[bstack1l1_opy_ (u"ࠪࡸࡾࡶࡥࠨᾟ")] == bstack1l1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩᾠ"):
            log[bstack1l1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᾡ")] = active[bstack1l1_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᾢ")]
        elif active[bstack1l1_opy_ (u"ࠧࡵࡻࡳࡩࠬᾣ")] == bstack1l1_opy_ (u"ࠨࡶࡨࡷࡹ࠭ᾤ"):
            log[bstack1l1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᾥ")] = active[bstack1l1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᾦ")]
    bstack111111l1_opy_.bstack1ll1l1l1l1_opy_([log])
def bstack11l1111l11_opy_():
    if len(store[bstack1l1_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨᾧ")]) > 0 and store[bstack1l1_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩᾨ")][-1]:
        return {
            bstack1l1_opy_ (u"࠭ࡴࡺࡲࡨࠫᾩ"): bstack1l1_opy_ (u"ࠧࡩࡱࡲ࡯ࠬᾪ"),
            bstack1l1_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᾫ"): store[bstack1l1_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭ᾬ")][-1]
        }
    if store.get(bstack1l1_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧᾭ"), None):
        return {
            bstack1l1_opy_ (u"ࠫࡹࡿࡰࡦࠩᾮ"): bstack1l1_opy_ (u"ࠬࡺࡥࡴࡶࠪᾯ"),
            bstack1l1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᾰ"): store[bstack1l1_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫᾱ")]
        }
    return None
def pytest_runtest_logstart(nodeid, location):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lll1l1lll1_opy_.INIT_TEST, bstack1llll111ll1_opy_.PRE, nodeid, location)
def pytest_runtest_logfinish(nodeid, location):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lll1l1lll1_opy_.INIT_TEST, bstack1llll111ll1_opy_.POST, nodeid, location)
def pytest_runtest_call(item):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lll1l1lll1_opy_.TEST, bstack1llll111ll1_opy_.PRE, item)
        return
    try:
        global CONFIG
        item._11111ll111l_opy_ = True
        bstack1lll11111l_opy_ = bstack1l1l11l11_opy_.bstack1l1ll1l1_opy_(bstack11ll1111l11_opy_(item.own_markers))
        if not cli.bstack1lll1lll11l_opy_(bstack1lll11l1l1l_opy_):
            item._a11y_test_case = bstack1lll11111l_opy_
            if bstack1l1l11l1l_opy_(threading.current_thread(), bstack1l1_opy_ (u"ࠨࡣ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧᾲ"), None):
                driver = getattr(item, bstack1l1_opy_ (u"ࠩࡢࡨࡷ࡯ࡶࡦࡴࠪᾳ"), None)
                item._a11y_started = bstack1l1l11l11_opy_.bstack1llll111_opy_(driver, bstack1lll11111l_opy_)
        if not bstack111111l1_opy_.on() or bstack1111l111ll1_opy_ != bstack1l1_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪᾴ"):
            return
        global current_test_uuid #, bstack11l111ll1l_opy_
        bstack111lll1111_opy_ = {
            bstack1l1_opy_ (u"ࠫࡺࡻࡩࡥࠩ᾵"): uuid4().__str__(),
            bstack1l1_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩᾶ"): bstack111ll11ll1_opy_().isoformat() + bstack1l1_opy_ (u"࡚࠭ࠨᾷ")
        }
        current_test_uuid = bstack111lll1111_opy_[bstack1l1_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᾸ")]
        store[bstack1l1_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬᾹ")] = bstack111lll1111_opy_[bstack1l1_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᾺ")]
        threading.current_thread().current_test_uuid = current_test_uuid
        _111llll111_opy_[item.nodeid] = {**_111llll111_opy_[item.nodeid], **bstack111lll1111_opy_}
        bstack1111l111lll_opy_(item, _111llll111_opy_[item.nodeid], bstack1l1_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫΆ"))
    except Exception as err:
        print(bstack1l1_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶࡢࡶࡺࡴࡴࡦࡵࡷࡣࡨࡧ࡬࡭࠼ࠣࡿࢂ࠭ᾼ"), str(err))
def pytest_runtest_setup(item):
    store[bstack1l1_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡺࡥ࡮ࠩ᾽")] = item
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lll1l1lll1_opy_.BEFORE_EACH, bstack1llll111ll1_opy_.PRE, item, bstack1l1_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬι"))
        return # skip all existing bstack1111l11l1ll_opy_
    global bstack11111lll1ll_opy_
    threading.current_thread().percySessionName = item.nodeid
    if bstack11l1l1l1l11_opy_():
        atexit.register(bstack11111l1l_opy_)
        if not bstack11111lll1ll_opy_:
            try:
                bstack11111lll1l1_opy_ = [signal.SIGINT, signal.SIGTERM]
                if not bstack11l1lllll11_opy_():
                    bstack11111lll1l1_opy_.extend([signal.SIGHUP, signal.SIGQUIT])
                for s in bstack11111lll1l1_opy_:
                    signal.signal(s, bstack11111ll1lll_opy_)
                bstack11111lll1ll_opy_ = True
            except Exception as e:
                logger.debug(
                    bstack1l1_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡵࡩ࡬࡯ࡳࡵࡧࡵࠤࡸ࡯ࡧ࡯ࡣ࡯ࠤ࡭ࡧ࡮ࡥ࡮ࡨࡶࡸࡀࠠࠣ᾿") + str(e))
        try:
            item.config.hook.pytest_selenium_runtest_makereport = bstack111l1l1ll11_opy_
        except Exception as err:
            threading.current_thread().testStatus = bstack1l1_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨ῀")
    try:
        if not bstack111111l1_opy_.on():
            return
        uuid = uuid4().__str__()
        bstack111lll1111_opy_ = {
            bstack1l1_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ῁"): uuid,
            bstack1l1_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧῂ"): bstack111ll11ll1_opy_().isoformat() + bstack1l1_opy_ (u"ࠫ࡟࠭ῃ"),
            bstack1l1_opy_ (u"ࠬࡺࡹࡱࡧࠪῄ"): bstack1l1_opy_ (u"࠭ࡨࡰࡱ࡮ࠫ῅"),
            bstack1l1_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡺࡹࡱࡧࠪῆ"): bstack1l1_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡇࡄࡇࡍ࠭ῇ"),
            bstack1l1_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟࡯ࡣࡰࡩࠬῈ"): bstack1l1_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩΈ")
        }
        threading.current_thread().current_hook_uuid = uuid
        threading.current_thread().current_test_item = item
        store[bstack1l1_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡹ࡫࡭ࠨῊ")] = item
        store[bstack1l1_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩΉ")] = [uuid]
        if not _111llll111_opy_.get(item.nodeid, None):
            _111llll111_opy_[item.nodeid] = {bstack1l1_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬῌ"): [], bstack1l1_opy_ (u"ࠧࡧ࡫ࡻࡸࡺࡸࡥࡴࠩ῍"): []}
        _111llll111_opy_[item.nodeid][bstack1l1_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧ῎")].append(bstack111lll1111_opy_[bstack1l1_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ῏")])
        _111llll111_opy_[item.nodeid + bstack1l1_opy_ (u"ࠪ࠱ࡸ࡫ࡴࡶࡲࠪῐ")] = bstack111lll1111_opy_
        bstack11111lllll1_opy_(item, bstack111lll1111_opy_, bstack1l1_opy_ (u"ࠫࡍࡵ࡯࡬ࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬῑ"))
    except Exception as err:
        print(bstack1l1_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷࡣࡷࡻ࡮ࡵࡧࡶࡸࡤࡹࡥࡵࡷࡳ࠾ࠥࢁࡽࠨῒ"), str(err))
def pytest_runtest_teardown(item):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lll1l1lll1_opy_.TEST, bstack1llll111ll1_opy_.POST, item)
        cli.test_framework.track_event(cli_context, bstack1lll1l1lll1_opy_.AFTER_EACH, bstack1llll111ll1_opy_.PRE, item, bstack1l1_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࠨΐ"))
        return # skip all existing bstack1111l11l1ll_opy_
    try:
        global bstack1l111ll11l_opy_
        bstack11ll11ll11_opy_ = 0
        if bstack1l11l1ll1_opy_ is True:
            bstack11ll11ll11_opy_ = int(os.environ.get(bstack1l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧ῔")))
        if bstack1111ll11_opy_.bstack1l111l11_opy_() == bstack1l1_opy_ (u"ࠣࡶࡵࡹࡪࠨ῕"):
            if bstack1111ll11_opy_.bstack1l111ll111_opy_() == bstack1l1_opy_ (u"ࠤࡷࡩࡸࡺࡣࡢࡵࡨࠦῖ"):
                bstack1111l11lll1_opy_ = bstack1l1l11l1l_opy_(threading.current_thread(), bstack1l1_opy_ (u"ࠪࡴࡪࡸࡣࡺࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ῗ"), None)
                bstack1ll1l111l_opy_ = bstack1111l11lll1_opy_ + bstack1l1_opy_ (u"ࠦ࠲ࡺࡥࡴࡶࡦࡥࡸ࡫ࠢῘ")
                driver = getattr(item, bstack1l1_opy_ (u"ࠬࡥࡤࡳ࡫ࡹࡩࡷ࠭Ῑ"), None)
                bstack1l11l11l1l_opy_ = getattr(item, bstack1l1_opy_ (u"࠭࡮ࡢ࡯ࡨࠫῚ"), None)
                bstack1lll1ll11l_opy_ = getattr(item, bstack1l1_opy_ (u"ࠧࡶࡷ࡬ࡨࠬΊ"), None)
                PercySDK.screenshot(driver, bstack1ll1l111l_opy_, bstack1l11l11l1l_opy_=bstack1l11l11l1l_opy_, bstack1lll1ll11l_opy_=bstack1lll1ll11l_opy_, bstack11l1ll111_opy_=bstack11ll11ll11_opy_)
        if not cli.bstack1lll1lll11l_opy_(bstack1lll11l1l1l_opy_):
            if getattr(item, bstack1l1_opy_ (u"ࠨࡡࡤ࠵࠶ࡿ࡟ࡴࡶࡤࡶࡹ࡫ࡤࠨ῜"), False):
                bstack111111l11_opy_.bstack1lll11ll11_opy_(getattr(item, bstack1l1_opy_ (u"ࠩࡢࡨࡷ࡯ࡶࡦࡴࠪ῝"), None), bstack1l111ll11l_opy_, logger, item)
        if not bstack111111l1_opy_.on():
            return
        bstack111lll1111_opy_ = {
            bstack1l1_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ῞"): uuid4().__str__(),
            bstack1l1_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨ῟"): bstack111ll11ll1_opy_().isoformat() + bstack1l1_opy_ (u"ࠬࡠࠧῠ"),
            bstack1l1_opy_ (u"࠭ࡴࡺࡲࡨࠫῡ"): bstack1l1_opy_ (u"ࠧࡩࡱࡲ࡯ࠬῢ"),
            bstack1l1_opy_ (u"ࠨࡪࡲࡳࡰࡥࡴࡺࡲࡨࠫΰ"): bstack1l1_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡇࡄࡇࡍ࠭ῤ"),
            bstack1l1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡰࡤࡱࡪ࠭ῥ"): bstack1l1_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭ῦ")
        }
        _111llll111_opy_[item.nodeid + bstack1l1_opy_ (u"ࠬ࠳ࡴࡦࡣࡵࡨࡴࡽ࡮ࠨῧ")] = bstack111lll1111_opy_
        bstack11111lllll1_opy_(item, bstack111lll1111_opy_, bstack1l1_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧῨ"))
    except Exception as err:
        print(bstack1l1_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡺࡶࡨࡷࡹࡥࡲࡶࡰࡷࡩࡸࡺ࡟ࡵࡧࡤࡶࡩࡵࡷ࡯࠼ࠣࡿࢂ࠭Ῡ"), str(err))
@pytest.hookimpl(hookwrapper=True)
def pytest_fixture_setup(fixturedef, request):
    if bstack111l1l11ll1_opy_(fixturedef.argname):
        store[bstack1l1_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡰࡳࡩࡻ࡬ࡦࡡ࡬ࡸࡪࡳࠧῪ")] = request.node
    elif bstack111l1l1l1ll_opy_(fixturedef.argname):
        store[bstack1l1_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡧࡱࡧࡳࡴࡡ࡬ࡸࡪࡳࠧΎ")] = request.node
    if not bstack111111l1_opy_.on():
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1lll1l1lll1_opy_.SETUP_FIXTURE, bstack1llll111ll1_opy_.PRE, fixturedef, request)
        outcome = yield
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1lll1l1lll1_opy_.SETUP_FIXTURE, bstack1llll111ll1_opy_.POST, fixturedef, request, outcome)
        return # skip all existing bstack1111l11l1ll_opy_
    start_time = datetime.datetime.now()
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lll1l1lll1_opy_.SETUP_FIXTURE, bstack1llll111ll1_opy_.PRE, fixturedef, request)
    outcome = yield
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lll1l1lll1_opy_.SETUP_FIXTURE, bstack1llll111ll1_opy_.POST, fixturedef, request, outcome)
        return # skip all existing bstack1111l11l1ll_opy_
    try:
        fixture = {
            bstack1l1_opy_ (u"ࠪࡲࡦࡳࡥࠨῬ"): fixturedef.argname,
            bstack1l1_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫ῭"): bstack11l1ll1l111_opy_(outcome),
            bstack1l1_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴࠧ΅"): (datetime.datetime.now() - start_time).total_seconds() * 1000
        }
        current_test_item = store[bstack1l1_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡴࡦ࡯ࠪ`")]
        if not _111llll111_opy_.get(current_test_item.nodeid, None):
            _111llll111_opy_[current_test_item.nodeid] = {bstack1l1_opy_ (u"ࠧࡧ࡫ࡻࡸࡺࡸࡥࡴࠩ῰"): []}
        _111llll111_opy_[current_test_item.nodeid][bstack1l1_opy_ (u"ࠨࡨ࡬ࡼࡹࡻࡲࡦࡵࠪ῱")].append(fixture)
    except Exception as err:
        logger.debug(bstack1l1_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲࡼࡸࡪࡹࡴࡠࡨ࡬ࡼࡹࡻࡲࡦࡡࡶࡩࡹࡻࡰ࠻ࠢࡾࢁࠬῲ"), str(err))
if bstack11111l1l1_opy_() and bstack111111l1_opy_.on():
    def pytest_bdd_before_step(request, step):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1lll1l1lll1_opy_.STEP, bstack1llll111ll1_opy_.PRE, request, step)
            return
        try:
            _111llll111_opy_[request.node.nodeid][bstack1l1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ῳ")].bstack1lllllll1_opy_(id(step))
        except Exception as err:
            print(bstack1l1_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶࡢࡦࡩࡪ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡴࡶࡨࡴ࠿ࠦࡻࡾࠩῴ"), str(err))
    def pytest_bdd_step_error(request, step, exception):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1lll1l1lll1_opy_.STEP, bstack1llll111ll1_opy_.POST, request, step, exception)
            return
        try:
            _111llll111_opy_[request.node.nodeid][bstack1l1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨ῵")].bstack11l111111l_opy_(id(step), Result.failed(exception=exception))
        except Exception as err:
            print(bstack1l1_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶࡹࡵࡧࡶࡸࡤࡨࡤࡥࡡࡶࡸࡪࡶ࡟ࡦࡴࡵࡳࡷࡀࠠࡼࡿࠪῶ"), str(err))
    def pytest_bdd_after_step(request, step):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1lll1l1lll1_opy_.STEP, bstack1llll111ll1_opy_.POST, request, step)
            return
        try:
            bstack111lllll11_opy_: bstack11l11111l1_opy_ = _111llll111_opy_[request.node.nodeid][bstack1l1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪῷ")]
            bstack111lllll11_opy_.bstack11l111111l_opy_(id(step), Result.passed())
        except Exception as err:
            print(bstack1l1_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࡟ࡣࡦࡧࡣࡸࡺࡥࡱࡡࡨࡶࡷࡵࡲ࠻ࠢࡾࢁࠬῸ"), str(err))
    def pytest_bdd_before_scenario(request, feature, scenario):
        global bstack1111l111ll1_opy_
        try:
            if not bstack111111l1_opy_.on() or bstack1111l111ll1_opy_ != bstack1l1_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩ࠭Ό"):
                return
            if cli.is_running():
                cli.test_framework.track_event(cli_context, bstack1lll1l1lll1_opy_.TEST, bstack1llll111ll1_opy_.PRE, request, feature, scenario)
                return
            driver = bstack1l1l11l1l_opy_(threading.current_thread(), bstack1l1_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩῺ"), None)
            if not _111llll111_opy_.get(request.node.nodeid, None):
                _111llll111_opy_[request.node.nodeid] = {}
            bstack111lllll11_opy_ = bstack11l11111l1_opy_.bstack111l111l11l_opy_(
                scenario, feature, request.node,
                name=bstack111l1l1l11l_opy_(request.node, scenario),
                started_at=bstack11l1l11ll1_opy_(),
                file_path=feature.filename,
                scope=[feature.name],
                framework=bstack1l1_opy_ (u"ࠫࡕࡿࡴࡦࡵࡷ࠱ࡨࡻࡣࡶ࡯ࡥࡩࡷ࠭Ώ"),
                tags=bstack111l1l1l1l1_opy_(feature, scenario),
                bstack11l111l11l_opy_=bstack111111l1_opy_.bstack11l111ll11_opy_(driver) if driver and driver.session_id else {}
            )
            _111llll111_opy_[request.node.nodeid][bstack1l1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨῼ")] = bstack111lllll11_opy_
            bstack1111l11l111_opy_(bstack111lllll11_opy_.uuid)
            bstack111111l1_opy_.bstack11l1111l1l_opy_(bstack1l1_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧ´"), bstack111lllll11_opy_)
        except Exception as err:
            print(bstack1l1_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡺࡶࡨࡷࡹࡥࡢࡥࡦࡢࡦࡪ࡬࡯ࡳࡧࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳ࠿ࠦࡻࡾࠩ῾"), str(err))
def bstack11111llll11_opy_(bstack111llllll1_opy_):
    if bstack111llllll1_opy_ in store[bstack1l1_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬ῿")]:
        store[bstack1l1_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭ ")].remove(bstack111llllll1_opy_)
def bstack1111l11l111_opy_(test_uuid):
    store[bstack1l1_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧ ")] = test_uuid
    threading.current_thread().current_test_uuid = test_uuid
@bstack111111l1_opy_.bstack1111ll1l1l1_opy_
def bstack11111ll1ll1_opy_(item, call, report):
    logger.debug(bstack1l1_opy_ (u"ࠫ࡭ࡧ࡮ࡥ࡮ࡨࡣࡴ࠷࠱ࡺࡡࡷࡩࡸࡺ࡟ࡦࡸࡨࡲࡹࡀࠠࡴࡶࡤࡶࡹ࠭ "))
    global bstack1111l111ll1_opy_
    bstack11l1llll11_opy_ = bstack11l1l11ll1_opy_()
    if hasattr(report, bstack1l1_opy_ (u"ࠬࡹࡴࡰࡲࠪ ")):
        bstack11l1llll11_opy_ = bstack11l1l11l1ll_opy_(report.stop)
    elif hasattr(report, bstack1l1_opy_ (u"࠭ࡳࡵࡣࡵࡸࠬ ")):
        bstack11l1llll11_opy_ = bstack11l1l11l1ll_opy_(report.start)
    try:
        if getattr(report, bstack1l1_opy_ (u"ࠧࡸࡪࡨࡲࠬ "), bstack1l1_opy_ (u"ࠨࠩ ")) == bstack1l1_opy_ (u"ࠩࡦࡥࡱࡲࠧ "):
            logger.debug(bstack1l1_opy_ (u"ࠪ࡬ࡦࡴࡤ࡭ࡧࡢࡳ࠶࠷ࡹࡠࡶࡨࡷࡹࡥࡥࡷࡧࡱࡸ࠿ࠦࡳࡵࡣࡷࡩࠥ࠳ࠠࡼࡿ࠯ࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠠ࠮ࠢࡾࢁࠬ ").format(getattr(report, bstack1l1_opy_ (u"ࠫࡼ࡮ࡥ࡯ࠩ "), bstack1l1_opy_ (u"ࠬ࠭ ")).__str__(), bstack1111l111ll1_opy_))
            if bstack1111l111ll1_opy_ == bstack1l1_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭​"):
                _111llll111_opy_[item.nodeid][bstack1l1_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬ‌")] = bstack11l1llll11_opy_
                bstack1111l111lll_opy_(item, _111llll111_opy_[item.nodeid], bstack1l1_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪ‍"), report, call)
                store[bstack1l1_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭‎")] = None
            elif bstack1111l111ll1_opy_ == bstack1l1_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠢ‏"):
                bstack111lllll11_opy_ = _111llll111_opy_[item.nodeid][bstack1l1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧ‐")]
                bstack111lllll11_opy_.set(hooks=_111llll111_opy_[item.nodeid].get(bstack1l1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫ‑"), []))
                exception, bstack11l111lll1_opy_ = None, None
                if call.excinfo:
                    exception = call.excinfo.value
                    bstack11l111lll1_opy_ = [call.excinfo.exconly(), getattr(report, bstack1l1_opy_ (u"࠭࡬ࡰࡰࡪࡶࡪࡶࡲࡵࡧࡻࡸࠬ‒"), bstack1l1_opy_ (u"ࠧࠨ–"))]
                bstack111lllll11_opy_.stop(time=bstack11l1llll11_opy_, result=Result(result=getattr(report, bstack1l1_opy_ (u"ࠨࡱࡸࡸࡨࡵ࡭ࡦࠩ—"), bstack1l1_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩ―")), exception=exception, bstack11l111lll1_opy_=bstack11l111lll1_opy_))
                bstack111111l1_opy_.bstack11l1111l1l_opy_(bstack1l1_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬ‖"), _111llll111_opy_[item.nodeid][bstack1l1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧ‗")])
        elif getattr(report, bstack1l1_opy_ (u"ࠬࡽࡨࡦࡰࠪ‘"), bstack1l1_opy_ (u"࠭ࠧ’")) in [bstack1l1_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭‚"), bstack1l1_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࠪ‛")]:
            logger.debug(bstack1l1_opy_ (u"ࠩ࡫ࡥࡳࡪ࡬ࡦࡡࡲ࠵࠶ࡿ࡟ࡵࡧࡶࡸࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡹࡴࡢࡶࡨࠤ࠲ࠦࡻࡾ࠮ࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࠦ࠭ࠡࡽࢀࠫ“").format(getattr(report, bstack1l1_opy_ (u"ࠪࡻ࡭࡫࡮ࠨ”"), bstack1l1_opy_ (u"ࠫࠬ„")).__str__(), bstack1111l111ll1_opy_))
            bstack11l111l111_opy_ = item.nodeid + bstack1l1_opy_ (u"ࠬ࠳ࠧ‟") + getattr(report, bstack1l1_opy_ (u"࠭ࡷࡩࡧࡱࠫ†"), bstack1l1_opy_ (u"ࠧࠨ‡"))
            if getattr(report, bstack1l1_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩ•"), False):
                hook_type = bstack1l1_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡈࡅࡈࡎࠧ‣") if getattr(report, bstack1l1_opy_ (u"ࠪࡻ࡭࡫࡮ࠨ․"), bstack1l1_opy_ (u"ࠫࠬ‥")) == bstack1l1_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫ…") else bstack1l1_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡋࡁࡄࡊࠪ‧")
                _111llll111_opy_[bstack11l111l111_opy_] = {
                    bstack1l1_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ "): uuid4().__str__(),
                    bstack1l1_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬ "): bstack11l1llll11_opy_,
                    bstack1l1_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡵࡻࡳࡩࠬ‪"): hook_type
                }
            _111llll111_opy_[bstack11l111l111_opy_][bstack1l1_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨ‫")] = bstack11l1llll11_opy_
            bstack11111llll11_opy_(_111llll111_opy_[bstack11l111l111_opy_][bstack1l1_opy_ (u"ࠫࡺࡻࡩࡥࠩ‬")])
            bstack11111lllll1_opy_(item, _111llll111_opy_[bstack11l111l111_opy_], bstack1l1_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧ‭"), report, call)
            if getattr(report, bstack1l1_opy_ (u"࠭ࡷࡩࡧࡱࠫ‮"), bstack1l1_opy_ (u"ࠧࠨ ")) == bstack1l1_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧ‰"):
                if getattr(report, bstack1l1_opy_ (u"ࠩࡲࡹࡹࡩ࡯࡮ࡧࠪ‱"), bstack1l1_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪ′")) == bstack1l1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ″"):
                    bstack111lll1111_opy_ = {
                        bstack1l1_opy_ (u"ࠬࡻࡵࡪࡦࠪ‴"): uuid4().__str__(),
                        bstack1l1_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪ‵"): bstack11l1l11ll1_opy_(),
                        bstack1l1_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬ‶"): bstack11l1l11ll1_opy_()
                    }
                    _111llll111_opy_[item.nodeid] = {**_111llll111_opy_[item.nodeid], **bstack111lll1111_opy_}
                    bstack1111l111lll_opy_(item, _111llll111_opy_[item.nodeid], bstack1l1_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩ‷"))
                    bstack1111l111lll_opy_(item, _111llll111_opy_[item.nodeid], bstack1l1_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫ‸"), report, call)
    except Exception as err:
        print(bstack1l1_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢ࡫ࡥࡳࡪ࡬ࡦࡡࡲ࠵࠶ࡿ࡟ࡵࡧࡶࡸࡤ࡫ࡶࡦࡰࡷ࠾ࠥࢁࡽࠨ‹"), str(err))
def bstack11111llllll_opy_(test, bstack111lll1111_opy_, result=None, call=None, bstack1lll1llll1_opy_=None, outcome=None):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    bstack111lllll11_opy_ = {
        bstack1l1_opy_ (u"ࠫࡺࡻࡩࡥࠩ›"): bstack111lll1111_opy_[bstack1l1_opy_ (u"ࠬࡻࡵࡪࡦࠪ※")],
        bstack1l1_opy_ (u"࠭ࡴࡺࡲࡨࠫ‼"): bstack1l1_opy_ (u"ࠧࡵࡧࡶࡸࠬ‽"),
        bstack1l1_opy_ (u"ࠨࡰࡤࡱࡪ࠭‾"): test.name,
        bstack1l1_opy_ (u"ࠩࡥࡳࡩࡿࠧ‿"): {
            bstack1l1_opy_ (u"ࠪࡰࡦࡴࡧࠨ⁀"): bstack1l1_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫ⁁"),
            bstack1l1_opy_ (u"ࠬࡩ࡯ࡥࡧࠪ⁂"): inspect.getsource(test.obj)
        },
        bstack1l1_opy_ (u"࠭ࡩࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ⁃"): test.name,
        bstack1l1_opy_ (u"ࠧࡴࡥࡲࡴࡪ࠭⁄"): test.name,
        bstack1l1_opy_ (u"ࠨࡵࡦࡳࡵ࡫ࡳࠨ⁅"): bstack11llll111l_opy_.bstack111lll11ll_opy_(test),
        bstack1l1_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬ⁆"): file_path,
        bstack1l1_opy_ (u"ࠪࡰࡴࡩࡡࡵ࡫ࡲࡲࠬ⁇"): file_path,
        bstack1l1_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫ⁈"): bstack1l1_opy_ (u"ࠬࡶࡥ࡯ࡦ࡬ࡲ࡬࠭⁉"),
        bstack1l1_opy_ (u"࠭ࡶࡤࡡࡩ࡭ࡱ࡫ࡰࡢࡶ࡫ࠫ⁊"): file_path,
        bstack1l1_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫ⁋"): bstack111lll1111_opy_[bstack1l1_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬ⁌")],
        bstack1l1_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬ⁍"): bstack1l1_opy_ (u"ࠪࡔࡾࡺࡥࡴࡶࠪ⁎"),
        bstack1l1_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰࡖࡪࡸࡵ࡯ࡒࡤࡶࡦࡳࠧ⁏"): {
            bstack1l1_opy_ (u"ࠬࡸࡥࡳࡷࡱࡣࡳࡧ࡭ࡦࠩ⁐"): test.nodeid
        },
        bstack1l1_opy_ (u"࠭ࡴࡢࡩࡶࠫ⁑"): bstack11ll1111l11_opy_(test.own_markers)
    }
    if bstack1lll1llll1_opy_ in [bstack1l1_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔ࡭࡬ࡴࡵ࡫ࡤࠨ⁒"), bstack1l1_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪ⁓")]:
        bstack111lllll11_opy_[bstack1l1_opy_ (u"ࠩࡰࡩࡹࡧࠧ⁔")] = {
            bstack1l1_opy_ (u"ࠪࡪ࡮ࡾࡴࡶࡴࡨࡷࠬ⁕"): bstack111lll1111_opy_.get(bstack1l1_opy_ (u"ࠫ࡫࡯ࡸࡵࡷࡵࡩࡸ࠭⁖"), [])
        }
    if bstack1lll1llll1_opy_ == bstack1l1_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙࡫ࡪࡲࡳࡩࡩ࠭⁗"):
        bstack111lllll11_opy_[bstack1l1_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭⁘")] = bstack1l1_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨ⁙")
        bstack111lllll11_opy_[bstack1l1_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧ⁚")] = bstack111lll1111_opy_[bstack1l1_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨ⁛")]
        bstack111lllll11_opy_[bstack1l1_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨ⁜")] = bstack111lll1111_opy_[bstack1l1_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ⁝")]
    if result:
        bstack111lllll11_opy_[bstack1l1_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬ⁞")] = result.outcome
        bstack111lllll11_opy_[bstack1l1_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࡠ࡫ࡱࡣࡲࡹࠧ ")] = result.duration * 1000
        bstack111lllll11_opy_[bstack1l1_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬ⁠")] = bstack111lll1111_opy_[bstack1l1_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭⁡")]
        if result.failed:
            bstack111lllll11_opy_[bstack1l1_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࡢࡸࡾࡶࡥࠨ⁢")] = bstack111111l1_opy_.bstack1111ll11l1_opy_(call.excinfo.typename)
            bstack111lllll11_opy_[bstack1l1_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࠫ⁣")] = bstack111111l1_opy_.bstack1111lll1ll1_opy_(call.excinfo, result)
        bstack111lllll11_opy_[bstack1l1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪ⁤")] = bstack111lll1111_opy_[bstack1l1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫ⁥")]
    if outcome:
        bstack111lllll11_opy_[bstack1l1_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭⁦")] = bstack11l1ll1l111_opy_(outcome)
        bstack111lllll11_opy_[bstack1l1_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࡡ࡬ࡲࡤࡳࡳࠨ⁧")] = 0
        bstack111lllll11_opy_[bstack1l1_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭⁨")] = bstack111lll1111_opy_[bstack1l1_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧ⁩")]
        if bstack111lllll11_opy_[bstack1l1_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪ⁪")] == bstack1l1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ⁫"):
            bstack111lllll11_opy_[bstack1l1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪࡥࡴࡺࡲࡨࠫ⁬")] = bstack1l1_opy_ (u"࠭ࡕ࡯ࡪࡤࡲࡩࡲࡥࡥࡇࡵࡶࡴࡸࠧ⁭")  # bstack1111l11ll1l_opy_
            bstack111lllll11_opy_[bstack1l1_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࠨ⁮")] = [{bstack1l1_opy_ (u"ࠨࡤࡤࡧࡰࡺࡲࡢࡥࡨࠫ⁯"): [bstack1l1_opy_ (u"ࠩࡶࡳࡲ࡫ࠠࡦࡴࡵࡳࡷ࠭⁰")]}]
        bstack111lllll11_opy_[bstack1l1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩⁱ")] = bstack111lll1111_opy_[bstack1l1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪ⁲")]
    return bstack111lllll11_opy_
def bstack1111l111111_opy_(test, bstack111l1ll111_opy_, bstack1lll1llll1_opy_, result, call, outcome, bstack1111l11l11l_opy_):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    hook_type = bstack111l1ll111_opy_[bstack1l1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡸࡾࡶࡥࠨ⁳")]
    hook_name = bstack111l1ll111_opy_[bstack1l1_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡳࡧ࡭ࡦࠩ⁴")]
    hook_data = {
        bstack1l1_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ⁵"): bstack111l1ll111_opy_[bstack1l1_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭⁶")],
        bstack1l1_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ⁷"): bstack1l1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࠨ⁸"),
        bstack1l1_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ⁹"): bstack1l1_opy_ (u"ࠬࢁࡽࠨ⁺").format(bstack111l1l1lll1_opy_(hook_name)),
        bstack1l1_opy_ (u"࠭ࡢࡰࡦࡼࠫ⁻"): {
            bstack1l1_opy_ (u"ࠧ࡭ࡣࡱ࡫ࠬ⁼"): bstack1l1_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨ⁽"),
            bstack1l1_opy_ (u"ࠩࡦࡳࡩ࡫ࠧ⁾"): None
        },
        bstack1l1_opy_ (u"ࠪࡷࡨࡵࡰࡦࠩⁿ"): test.name,
        bstack1l1_opy_ (u"ࠫࡸࡩ࡯ࡱࡧࡶࠫ₀"): bstack11llll111l_opy_.bstack111lll11ll_opy_(test, hook_name),
        bstack1l1_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨ₁"): file_path,
        bstack1l1_opy_ (u"࠭࡬ࡰࡥࡤࡸ࡮ࡵ࡮ࠨ₂"): file_path,
        bstack1l1_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ₃"): bstack1l1_opy_ (u"ࠨࡲࡨࡲࡩ࡯࡮ࡨࠩ₄"),
        bstack1l1_opy_ (u"ࠩࡹࡧࡤ࡬ࡩ࡭ࡧࡳࡥࡹ࡮ࠧ₅"): file_path,
        bstack1l1_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧ₆"): bstack111l1ll111_opy_[bstack1l1_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨ₇")],
        bstack1l1_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨ₈"): bstack1l1_opy_ (u"࠭ࡐࡺࡶࡨࡷࡹ࠳ࡣࡶࡥࡸࡱࡧ࡫ࡲࠨ₉") if bstack1111l111ll1_opy_ == bstack1l1_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠫ₊") else bstack1l1_opy_ (u"ࠨࡒࡼࡸࡪࡹࡴࠨ₋"),
        bstack1l1_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡵࡻࡳࡩࠬ₌"): hook_type
    }
    bstack111l111l1ll_opy_ = bstack111l1l1lll_opy_(_111llll111_opy_.get(test.nodeid, None))
    if bstack111l111l1ll_opy_:
        hook_data[bstack1l1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤ࡯ࡤࠨ₍")] = bstack111l111l1ll_opy_
    if result:
        hook_data[bstack1l1_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫ₎")] = result.outcome
        hook_data[bstack1l1_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴ࡟ࡪࡰࡢࡱࡸ࠭₏")] = result.duration * 1000
        hook_data[bstack1l1_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫₐ")] = bstack111l1ll111_opy_[bstack1l1_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬₑ")]
        if result.failed:
            hook_data[bstack1l1_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࡡࡷࡽࡵ࡫ࠧₒ")] = bstack111111l1_opy_.bstack1111ll11l1_opy_(call.excinfo.typename)
            hook_data[bstack1l1_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࠪₓ")] = bstack111111l1_opy_.bstack1111lll1ll1_opy_(call.excinfo, result)
    if outcome:
        hook_data[bstack1l1_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪₔ")] = bstack11l1ll1l111_opy_(outcome)
        hook_data[bstack1l1_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳࡥࡩ࡯ࡡࡰࡷࠬₕ")] = 100
        hook_data[bstack1l1_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪₖ")] = bstack111l1ll111_opy_[bstack1l1_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫₗ")]
        if hook_data[bstack1l1_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧₘ")] == bstack1l1_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨₙ"):
            hook_data[bstack1l1_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࡢࡸࡾࡶࡥࠨₚ")] = bstack1l1_opy_ (u"࡙ࠪࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࡋࡲࡳࡱࡵࠫₛ")  # bstack1111l11ll1l_opy_
            hook_data[bstack1l1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࠬₜ")] = [{bstack1l1_opy_ (u"ࠬࡨࡡࡤ࡭ࡷࡶࡦࡩࡥࠨ₝"): [bstack1l1_opy_ (u"࠭ࡳࡰ࡯ࡨࠤࡪࡸࡲࡰࡴࠪ₞")]}]
    if bstack1111l11l11l_opy_:
        hook_data[bstack1l1_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ₟")] = bstack1111l11l11l_opy_.result
        hook_data[bstack1l1_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࡢ࡭ࡳࡥ࡭ࡴࠩ₠")] = bstack11l1l111ll1_opy_(bstack111l1ll111_opy_[bstack1l1_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭₡")], bstack111l1ll111_opy_[bstack1l1_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨ₢")])
        hook_data[bstack1l1_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ₣")] = bstack111l1ll111_opy_[bstack1l1_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ₤")]
        if hook_data[bstack1l1_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭₥")] == bstack1l1_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ₦"):
            hook_data[bstack1l1_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࡡࡷࡽࡵ࡫ࠧ₧")] = bstack111111l1_opy_.bstack1111ll11l1_opy_(bstack1111l11l11l_opy_.exception_type)
            hook_data[bstack1l1_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࠪ₨")] = [{bstack1l1_opy_ (u"ࠪࡦࡦࡩ࡫ࡵࡴࡤࡧࡪ࠭₩"): bstack11l1ll1ll11_opy_(bstack1111l11l11l_opy_.exception)}]
    return hook_data
def bstack1111l111lll_opy_(test, bstack111lll1111_opy_, bstack1lll1llll1_opy_, result=None, call=None, outcome=None):
    logger.debug(bstack1l1_opy_ (u"ࠫࡸ࡫࡮ࡥࡡࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡆࡺࡴࡦ࡯ࡳࡸ࡮ࡴࡧࠡࡶࡲࠤ࡬࡫࡮ࡦࡴࡤࡸࡪࠦࡴࡦࡵࡷࠤࡩࡧࡴࡢࠢࡩࡳࡷࠦࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠣ࠱ࠥࢁࡽࠨ₪").format(bstack1lll1llll1_opy_))
    bstack111lllll11_opy_ = bstack11111llllll_opy_(test, bstack111lll1111_opy_, result, call, bstack1lll1llll1_opy_, outcome)
    driver = getattr(test, bstack1l1_opy_ (u"ࠬࡥࡤࡳ࡫ࡹࡩࡷ࠭₫"), None)
    if bstack1lll1llll1_opy_ == bstack1l1_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧ€") and driver:
        bstack111lllll11_opy_[bstack1l1_opy_ (u"ࠧࡪࡰࡷࡩ࡬ࡸࡡࡵ࡫ࡲࡲࡸ࠭₭")] = bstack111111l1_opy_.bstack11l111ll11_opy_(driver)
    if bstack1lll1llll1_opy_ == bstack1l1_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕ࡮࡭ࡵࡶࡥࡥࠩ₮"):
        bstack1lll1llll1_opy_ = bstack1l1_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫ₯")
    bstack111l1ll1ll_opy_ = {
        bstack1l1_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧ₰"): bstack1lll1llll1_opy_,
        bstack1l1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳ࠭₱"): bstack111lllll11_opy_
    }
    bstack111111l1_opy_.bstack1l111lll1l_opy_(bstack111l1ll1ll_opy_)
    if bstack1lll1llll1_opy_ == bstack1l1_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭₲"):
        threading.current_thread().bstackTestMeta = {bstack1l1_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭₳"): bstack1l1_opy_ (u"ࠧࡱࡧࡱࡨ࡮ࡴࡧࠨ₴")}
    elif bstack1lll1llll1_opy_ == bstack1l1_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪ₵"):
        threading.current_thread().bstackTestMeta = {bstack1l1_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩ₶"): getattr(result, bstack1l1_opy_ (u"ࠪࡳࡺࡺࡣࡰ࡯ࡨࠫ₷"), bstack1l1_opy_ (u"ࠫࠬ₸"))}
def bstack11111lllll1_opy_(test, bstack111lll1111_opy_, bstack1lll1llll1_opy_, result=None, call=None, outcome=None, bstack1111l11l11l_opy_=None):
    logger.debug(bstack1l1_opy_ (u"ࠬࡹࡥ࡯ࡦࡢ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡇࡴࡵࡧࡰࡴࡹ࡯࡮ࡨࠢࡷࡳࠥ࡭ࡥ࡯ࡧࡵࡥࡹ࡫ࠠࡩࡱࡲ࡯ࠥࡪࡡࡵࡣ࠯ࠤࡪࡼࡥ࡯ࡶࡗࡽࡵ࡫ࠠ࠮ࠢࡾࢁࠬ₹").format(bstack1lll1llll1_opy_))
    hook_data = bstack1111l111111_opy_(test, bstack111lll1111_opy_, bstack1lll1llll1_opy_, result, call, outcome, bstack1111l11l11l_opy_)
    bstack111l1ll1ll_opy_ = {
        bstack1l1_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪ₺"): bstack1lll1llll1_opy_,
        bstack1l1_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࠩ₻"): hook_data
    }
    bstack111111l1_opy_.bstack1l111lll1l_opy_(bstack111l1ll1ll_opy_)
def bstack111l1l1lll_opy_(bstack111lll1111_opy_):
    if not bstack111lll1111_opy_:
        return None
    if bstack111lll1111_opy_.get(bstack1l1_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫ₼"), None):
        return getattr(bstack111lll1111_opy_[bstack1l1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬ₽")], bstack1l1_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ₾"), None)
    return bstack111lll1111_opy_.get(bstack1l1_opy_ (u"ࠫࡺࡻࡩࡥࠩ₿"), None)
@pytest.fixture(autouse=True)
def second_fixture(caplog, request):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lll1l1lll1_opy_.LOG, bstack1llll111ll1_opy_.PRE, request, caplog)
    yield
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lll1l1lll1_opy_.LOG, bstack1llll111ll1_opy_.POST, request, caplog)
        return # skip all existing bstack1111l11l1ll_opy_
    try:
        if not bstack111111l1_opy_.on():
            return
        places = [bstack1l1_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫ⃀"), bstack1l1_opy_ (u"࠭ࡣࡢ࡮࡯ࠫ⃁"), bstack1l1_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࠩ⃂")]
        logs = []
        for bstack1111l11111l_opy_ in places:
            records = caplog.get_records(bstack1111l11111l_opy_)
            bstack11111ll1111_opy_ = bstack1l1_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ⃃") if bstack1111l11111l_opy_ == bstack1l1_opy_ (u"ࠩࡦࡥࡱࡲࠧ⃄") else bstack1l1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ⃅")
            bstack11111lll11l_opy_ = request.node.nodeid + (bstack1l1_opy_ (u"ࠫࠬ⃆") if bstack1111l11111l_opy_ == bstack1l1_opy_ (u"ࠬࡩࡡ࡭࡮ࠪ⃇") else bstack1l1_opy_ (u"࠭࠭ࠨ⃈") + bstack1111l11111l_opy_)
            test_uuid = bstack111l1l1lll_opy_(_111llll111_opy_.get(bstack11111lll11l_opy_, None))
            if not test_uuid:
                continue
            for record in records:
                if bstack11l1l1lll1l_opy_(record.message):
                    continue
                logs.append({
                    bstack1l1_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪ⃉"): bstack11l1l111lll_opy_(record.created).isoformat() + bstack1l1_opy_ (u"ࠨ࡜ࠪ⃊"),
                    bstack1l1_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨ⃋"): record.levelname,
                    bstack1l1_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ⃌"): record.message,
                    bstack11111ll1111_opy_: test_uuid
                })
        if len(logs) > 0:
            bstack111111l1_opy_.bstack1ll1l1l1l1_opy_(logs)
    except Exception as err:
        print(bstack1l1_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡷࡪࡩ࡯࡯ࡦࡢࡪ࡮ࡾࡴࡶࡴࡨ࠾ࠥࢁࡽࠨ⃍"), str(err))
def bstack1ll1ll1ll_opy_(sequence, driver_command, response=None, driver = None, args = None):
    global bstack1l111111l_opy_
    bstack11l1l1ll1l_opy_ = bstack1l1l11l1l_opy_(threading.current_thread(), bstack1l1_opy_ (u"ࠬ࡯ࡳࡂ࠳࠴ࡽ࡙࡫ࡳࡵࠩ⃎"), None) and bstack1l1l11l1l_opy_(
            threading.current_thread(), bstack1l1_opy_ (u"࠭ࡡ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬ⃏"), None)
    bstack1l1ll11l11_opy_ = getattr(driver, bstack1l1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡁ࠲࠳ࡼࡗ࡭ࡵࡵ࡭ࡦࡖࡧࡦࡴࠧ⃐"), None) != None and getattr(driver, bstack1l1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡂ࠳࠴ࡽࡘ࡮࡯ࡶ࡮ࡧࡗࡨࡧ࡮ࠨ⃑"), None) == True
    if sequence == bstack1l1_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦ⃒ࠩ") and driver != None:
      if not bstack1l111111l_opy_ and bstack1ll111l1ll1_opy_() and bstack1l1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻ⃓ࠪ") in CONFIG and CONFIG[bstack1l1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ⃔")] == True and bstack11ll111l1_opy_.bstack111l1ll1_opy_(driver_command) and (bstack1l1ll11l11_opy_ or bstack11l1l1ll1l_opy_) and not bstack1l111l111l_opy_(args):
        try:
          bstack1l111111l_opy_ = True
          logger.debug(bstack1l1_opy_ (u"ࠬࡖࡥࡳࡨࡲࡶࡲ࡯࡮ࡨࠢࡶࡧࡦࡴࠠࡧࡱࡵࠤࢀࢃࠧ⃕").format(driver_command))
          logger.debug(perform_scan(driver, driver_command=driver_command))
        except Exception as err:
          logger.debug(bstack1l1_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡳࡩࡷ࡬࡯ࡳ࡯ࠣࡷࡨࡧ࡮ࠡࡽࢀࠫ⃖").format(str(err)))
        bstack1l111111l_opy_ = False
    if sequence == bstack1l1_opy_ (u"ࠧࡢࡨࡷࡩࡷ࠭⃗"):
        if driver_command == bstack1l1_opy_ (u"ࠨࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸ⃘ࠬ"):
            bstack111111l1_opy_.bstack1ll1lll11_opy_({
                bstack1l1_opy_ (u"ࠩ࡬ࡱࡦ࡭ࡥࠨ⃙"): response[bstack1l1_opy_ (u"ࠪࡺࡦࡲࡵࡦ⃚ࠩ")],
                bstack1l1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ⃛"): store[bstack1l1_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩ⃜")]
            })
def bstack11111l1l_opy_():
    global bstack1l11lll111_opy_
    bstack1l11l11lll_opy_.bstack1ll1l1l11_opy_()
    logging.shutdown()
    bstack111111l1_opy_.bstack111l1l11l1_opy_()
    for driver in bstack1l11lll111_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack11111ll1lll_opy_(*args):
    global bstack1l11lll111_opy_
    bstack111111l1_opy_.bstack111l1l11l1_opy_()
    for driver in bstack1l11lll111_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack1llll1111_opy_, stage=STAGE.bstack1llll11l1_opy_, bstack1lll11ll_opy_=bstack11l1l11l11_opy_)
def bstack1l11l1111_opy_(self, *args, **kwargs):
    bstack1ll1l1ll_opy_ = bstack11l11llll_opy_(self, *args, **kwargs)
    bstack1l11lll1_opy_ = getattr(threading.current_thread(), bstack1l1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡚ࡥࡴࡶࡐࡩࡹࡧࠧ⃝"), None)
    if bstack1l11lll1_opy_ and bstack1l11lll1_opy_.get(bstack1l1_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧ⃞"), bstack1l1_opy_ (u"ࠨࠩ⃟")) == bstack1l1_opy_ (u"ࠩࡳࡩࡳࡪࡩ࡯ࡩࠪ⃠"):
        bstack111111l1_opy_.bstack1lll11lll1_opy_(self)
    return bstack1ll1l1ll_opy_
@measure(event_name=EVENTS.bstack1l1l1ll11l_opy_, stage=STAGE.bstack11l1llll1_opy_, bstack1lll11ll_opy_=bstack11l1l11l11_opy_)
def bstack11l1l1l111_opy_(framework_name):
    from bstack_utils.config import Config
    bstack11llllll1_opy_ = Config.bstack111111ll_opy_()
    if bstack11llllll1_opy_.get_property(bstack1l1_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡱࡴࡪ࡟ࡤࡣ࡯ࡰࡪࡪࠧ⃡")):
        return
    bstack11llllll1_opy_.bstack1llllll1l1_opy_(bstack1l1_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡲࡵࡤࡠࡥࡤࡰࡱ࡫ࡤࠨ⃢"), True)
    global bstack111l1l1l_opy_
    global bstack11ll1111l1_opy_
    bstack111l1l1l_opy_ = framework_name
    logger.info(bstack1ll1ll1lll_opy_.format(bstack111l1l1l_opy_.split(bstack1l1_opy_ (u"ࠬ࠳ࠧ⃣"))[0]))
    try:
        from selenium import webdriver
        from selenium.webdriver.common.service import Service
        from selenium.webdriver.remote.webdriver import WebDriver
        if bstack1ll111l1ll1_opy_():
            Service.start = bstack111lll1ll_opy_
            Service.stop = bstack111l11ll1_opy_
            webdriver.Remote.get = bstack1l11l11ll_opy_
            webdriver.Remote.__init__ = bstack1l1111lll_opy_
            if not isinstance(os.getenv(bstack1l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖ࡙ࡕࡇࡖࡘࡤࡖࡁࡓࡃࡏࡐࡊࡒࠧ⃤")), str):
                return
            WebDriver.close = bstack1l1lll11l1_opy_
            WebDriver.quit = bstack11ll1llll1_opy_
            WebDriver.getAccessibilityResults = getAccessibilityResults
            WebDriver.get_accessibility_results = getAccessibilityResults
            WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
            WebDriver.get_accessibility_results_summary = getAccessibilityResultsSummary
            WebDriver.performScan = perform_scan
            WebDriver.perform_scan = perform_scan
        elif bstack111111l1_opy_.on():
            webdriver.Remote.__init__ = bstack1l11l1111_opy_
        bstack11ll1111l1_opy_ = True
    except Exception as e:
        pass
    if os.environ.get(bstack1l1_opy_ (u"ࠧࡔࡇࡏࡉࡓࡏࡕࡎࡡࡒࡖࡤࡖࡌࡂ࡛࡚ࡖࡎࡍࡈࡕࡡࡌࡒࡘ࡚ࡁࡍࡎࡈࡈ⃥ࠬ")):
        bstack11ll1111l1_opy_ = eval(os.environ.get(bstack1l1_opy_ (u"ࠨࡕࡈࡐࡊࡔࡉࡖࡏࡢࡓࡗࡥࡐࡍࡃ࡜࡛ࡗࡏࡇࡉࡖࡢࡍࡓ࡙ࡔࡂࡎࡏࡉࡉ⃦࠭")))
    if not bstack11ll1111l1_opy_:
        bstack11llllll1l_opy_(bstack1l1_opy_ (u"ࠤࡓࡥࡨࡱࡡࡨࡧࡶࠤࡳࡵࡴࠡ࡫ࡱࡷࡹࡧ࡬࡭ࡧࡧࠦ⃧"), bstack11l1l11l_opy_)
    if bstack11ll1l11_opy_():
        try:
            from selenium.webdriver.remote.remote_connection import RemoteConnection
            RemoteConnection._1l1lll1ll_opy_ = bstack11l1l111l1_opy_
        except Exception as e:
            logger.error(bstack1111ll1ll_opy_.format(str(e)))
    if bstack1l1_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶ⃨ࠪ") in str(framework_name).lower():
        if not bstack1ll111l1ll1_opy_():
            return
        try:
            from pytest_selenium import pytest_selenium
            from _pytest.config import Config
            pytest_selenium.pytest_report_header = bstack11l1l1l1_opy_
            from pytest_selenium.drivers import browserstack
            browserstack.pytest_selenium_runtest_makereport = bstack111l1l11_opy_
            Config.getoption = bstack11l1lll111_opy_
        except Exception as e:
            pass
        try:
            from pytest_bdd import reporting
            reporting.runtest_makereport = bstack1l1l1ll1ll_opy_
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack1l1ll111l1_opy_, stage=STAGE.bstack1llll11l1_opy_, bstack1lll11ll_opy_=bstack11l1l11l11_opy_)
def bstack11ll1llll1_opy_(self):
    global bstack111l1l1l_opy_
    global bstack1l1l1l1l1l_opy_
    global bstack11l1lllll_opy_
    try:
        if bstack1l1_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ⃩") in bstack111l1l1l_opy_ and self.session_id != None and bstack1l1l11l1l_opy_(threading.current_thread(), bstack1l1_opy_ (u"ࠬࡺࡥࡴࡶࡖࡸࡦࡺࡵࡴ⃪ࠩ"), bstack1l1_opy_ (u"⃫࠭ࠧ")) != bstack1l1_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨ⃬"):
            bstack1lllllll11_opy_ = bstack1l1_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨ⃭") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack1l1_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥ⃮ࠩ")
            bstack11llll1111_opy_(logger, True)
            if self != None:
                bstack1ll1llll1_opy_(self, bstack1lllllll11_opy_, bstack1l1_opy_ (u"ࠪ࠰⃯ࠥ࠭").join(threading.current_thread().bstackTestErrorMessages))
        if not cli.bstack1lll1lll11l_opy_(bstack1lll11l1l1l_opy_):
            item = store.get(bstack1l1_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡹ࡫࡭ࠨ⃰"), None)
            if item is not None and bstack1l1l11l1l_opy_(threading.current_thread(), bstack1l1_opy_ (u"ࠬࡧ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫ⃱"), None):
                bstack111111l11_opy_.bstack1lll11ll11_opy_(self, bstack1l111ll11l_opy_, logger, item)
        threading.current_thread().testStatus = bstack1l1_opy_ (u"࠭ࠧ⃲")
    except Exception as e:
        logger.debug(bstack1l1_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡳࡡࡳ࡭࡬ࡲ࡬ࠦࡳࡵࡣࡷࡹࡸࡀࠠࠣ⃳") + str(e))
    bstack11l1lllll_opy_(self)
    self.session_id = None
@measure(event_name=EVENTS.bstack1l11ll11l_opy_, stage=STAGE.bstack1llll11l1_opy_, bstack1lll11ll_opy_=bstack11l1l11l11_opy_)
def bstack1l1111lll_opy_(self, command_executor,
             desired_capabilities=None, bstack11llll11l1_opy_=None, proxy=None,
             keep_alive=True, file_detector=None, options=None):
    global CONFIG
    global bstack1l1l1l1l1l_opy_
    global bstack11l1l11l11_opy_
    global bstack1l11l1ll1_opy_
    global bstack111l1l1l_opy_
    global bstack11l11llll_opy_
    global bstack1l11lll111_opy_
    global bstack1lll11l1l_opy_
    global bstack1lll11l1_opy_
    global bstack1l111ll11l_opy_
    CONFIG[bstack1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪ⃴")] = str(bstack111l1l1l_opy_) + str(__version__)
    command_executor = bstack1l1ll1l1ll_opy_(bstack1lll11l1l_opy_, CONFIG)
    logger.debug(bstack11ll1l1ll1_opy_.format(command_executor))
    proxy = bstack1l1ll11ll1_opy_(CONFIG, proxy)
    bstack11ll11ll11_opy_ = 0
    try:
        if bstack1l11l1ll1_opy_ is True:
            bstack11ll11ll11_opy_ = int(os.environ.get(bstack1l1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩ⃵")))
    except:
        bstack11ll11ll11_opy_ = 0
    bstack1l111lllll_opy_ = bstack1111l1l11_opy_(CONFIG, bstack11ll11ll11_opy_)
    logger.debug(bstack1l11llll11_opy_.format(str(bstack1l111lllll_opy_)))
    bstack1l111ll11l_opy_ = CONFIG.get(bstack1l1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭⃶"))[bstack11ll11ll11_opy_]
    if bstack1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨ⃷") in CONFIG and CONFIG[bstack1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩ⃸")]:
        bstack1ll111llll_opy_(bstack1l111lllll_opy_, bstack1lll11l1_opy_)
    if bstack1l1l11l11_opy_.bstack11lll11111_opy_(CONFIG, bstack11ll11ll11_opy_) and bstack1l1l11l11_opy_.bstack11lll11l11_opy_(bstack1l111lllll_opy_, options, desired_capabilities):
        threading.current_thread().a11yPlatform = True
        if not cli.bstack1lll1lll11l_opy_(bstack1lll11l1l1l_opy_):
            bstack1l1l11l11_opy_.set_capabilities(bstack1l111lllll_opy_, CONFIG)
    if desired_capabilities:
        bstack11l1l11l1_opy_ = bstack1lll1l1lll_opy_(desired_capabilities)
        bstack11l1l11l1_opy_[bstack1l1_opy_ (u"࠭ࡵࡴࡧ࡚࠷ࡈ࠭⃹")] = bstack1lll1l1l11_opy_(CONFIG)
        bstack1ll1l1111l_opy_ = bstack1111l1l11_opy_(bstack11l1l11l1_opy_)
        if bstack1ll1l1111l_opy_:
            bstack1l111lllll_opy_ = update(bstack1ll1l1111l_opy_, bstack1l111lllll_opy_)
        desired_capabilities = None
    if options:
        bstack1ll1l1l11l_opy_(options, bstack1l111lllll_opy_)
    if not options:
        options = bstack1l1l1l1ll1_opy_(bstack1l111lllll_opy_)
    if proxy and bstack11ll1ll11l_opy_() >= version.parse(bstack1l1_opy_ (u"ࠧ࠵࠰࠴࠴࠳࠶ࠧ⃺")):
        options.proxy(proxy)
    if options and bstack11ll1ll11l_opy_() >= version.parse(bstack1l1_opy_ (u"ࠨ࠵࠱࠼࠳࠶ࠧ⃻")):
        desired_capabilities = None
    if (
            not options and not desired_capabilities
    ) or (
            bstack11ll1ll11l_opy_() < version.parse(bstack1l1_opy_ (u"ࠩ࠶࠲࠽࠴࠰ࠨ⃼")) and not desired_capabilities
    ):
        desired_capabilities = {}
        desired_capabilities.update(bstack1l111lllll_opy_)
    logger.info(bstack1l1l1lllll_opy_)
    bstack1l11l111l1_opy_.end(EVENTS.bstack1l1l1ll11l_opy_.value, EVENTS.bstack1l1l1ll11l_opy_.value + bstack1l1_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥ⃽"),
                               EVENTS.bstack1l1l1ll11l_opy_.value + bstack1l1_opy_ (u"ࠦ࠿࡫࡮ࡥࠤ⃾"), True, None)
    if bstack11ll1ll11l_opy_() >= version.parse(bstack1l1_opy_ (u"ࠬ࠺࠮࠲࠲࠱࠴ࠬ⃿")):
        bstack11l11llll_opy_(self, command_executor=command_executor,
                  options=options, keep_alive=keep_alive, file_detector=file_detector)
    elif bstack11ll1ll11l_opy_() >= version.parse(bstack1l1_opy_ (u"࠭࠳࠯࠺࠱࠴ࠬ℀")):
        bstack11l11llll_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities, options=options,
                  bstack11llll11l1_opy_=bstack11llll11l1_opy_, proxy=proxy,
                  keep_alive=keep_alive, file_detector=file_detector)
    elif bstack11ll1ll11l_opy_() >= version.parse(bstack1l1_opy_ (u"ࠧ࠳࠰࠸࠷࠳࠶ࠧ℁")):
        bstack11l11llll_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities,
                  bstack11llll11l1_opy_=bstack11llll11l1_opy_, proxy=proxy,
                  keep_alive=keep_alive, file_detector=file_detector)
    else:
        bstack11l11llll_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities,
                  bstack11llll11l1_opy_=bstack11llll11l1_opy_, proxy=proxy,
                  keep_alive=keep_alive)
    try:
        bstack1ll1111ll_opy_ = bstack1l1_opy_ (u"ࠨࠩℂ")
        if bstack11ll1ll11l_opy_() >= version.parse(bstack1l1_opy_ (u"ࠩ࠷࠲࠵࠴࠰ࡣ࠳ࠪ℃")):
            bstack1ll1111ll_opy_ = self.caps.get(bstack1l1_opy_ (u"ࠥࡳࡵࡺࡩ࡮ࡣ࡯ࡌࡺࡨࡕࡳ࡮ࠥ℄"))
        else:
            bstack1ll1111ll_opy_ = self.capabilities.get(bstack1l1_opy_ (u"ࠦࡴࡶࡴࡪ࡯ࡤࡰࡍࡻࡢࡖࡴ࡯ࠦ℅"))
        if bstack1ll1111ll_opy_:
            bstack1ll1lll1_opy_(bstack1ll1111ll_opy_)
            if bstack11ll1ll11l_opy_() <= version.parse(bstack1l1_opy_ (u"ࠬ࠹࠮࠲࠵࠱࠴ࠬ℆")):
                self.command_executor._url = bstack1l1_opy_ (u"ࠨࡨࡵࡶࡳ࠾࠴࠵ࠢℇ") + bstack1lll11l1l_opy_ + bstack1l1_opy_ (u"ࠢ࠻࠺࠳࠳ࡼࡪ࠯ࡩࡷࡥࠦ℈")
            else:
                self.command_executor._url = bstack1l1_opy_ (u"ࠣࡪࡷࡸࡵࡹ࠺࠰࠱ࠥ℉") + bstack1ll1111ll_opy_ + bstack1l1_opy_ (u"ࠤ࠲ࡻࡩ࠵ࡨࡶࡤࠥℊ")
            logger.debug(bstack1l1l11ll1l_opy_.format(bstack1ll1111ll_opy_))
        else:
            logger.debug(bstack1ll11111l_opy_.format(bstack1l1_opy_ (u"ࠥࡓࡵࡺࡩ࡮ࡣ࡯ࠤࡍࡻࡢࠡࡰࡲࡸࠥ࡬࡯ࡶࡰࡧࠦℋ")))
    except Exception as e:
        logger.debug(bstack1ll11111l_opy_.format(e))
    bstack1l1l1l1l1l_opy_ = self.session_id
    if bstack1l1_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫℌ") in bstack111l1l1l_opy_:
        threading.current_thread().bstackSessionId = self.session_id
        threading.current_thread().bstackSessionDriver = self
        threading.current_thread().bstackTestErrorMessages = []
        item = store.get(bstack1l1_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡺࡥ࡮ࠩℍ"), None)
        if item:
            bstack11111llll1l_opy_ = getattr(item, bstack1l1_opy_ (u"࠭࡟ࡵࡧࡶࡸࡤࡩࡡࡴࡧࡢࡷࡹࡧࡲࡵࡧࡧࠫℎ"), False)
            if not getattr(item, bstack1l1_opy_ (u"ࠧࡠࡦࡵ࡭ࡻ࡫ࡲࠨℏ"), None) and bstack11111llll1l_opy_:
                setattr(store[bstack1l1_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡪࡶࡨࡱࠬℐ")], bstack1l1_opy_ (u"ࠩࡢࡨࡷ࡯ࡶࡦࡴࠪℑ"), self)
        bstack1l11lll1_opy_ = getattr(threading.current_thread(), bstack1l1_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡗࡩࡸࡺࡍࡦࡶࡤࠫℒ"), None)
        if bstack1l11lll1_opy_ and bstack1l11lll1_opy_.get(bstack1l1_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫℓ"), bstack1l1_opy_ (u"ࠬ࠭℔")) == bstack1l1_opy_ (u"࠭ࡰࡦࡰࡧ࡭ࡳ࡭ࠧℕ"):
            bstack111111l1_opy_.bstack1lll11lll1_opy_(self)
    bstack1l11lll111_opy_.append(self)
    if bstack1l1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ№") in CONFIG and bstack1l1_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭℗") in CONFIG[bstack1l1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ℘")][bstack11ll11ll11_opy_]:
        bstack11l1l11l11_opy_ = CONFIG[bstack1l1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ℙ")][bstack11ll11ll11_opy_][bstack1l1_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩℚ")]
    logger.debug(bstack1111ll111_opy_.format(bstack1l1l1l1l1l_opy_))
@measure(event_name=EVENTS.bstack1l11ll1111_opy_, stage=STAGE.bstack1llll11l1_opy_, bstack1lll11ll_opy_=bstack11l1l11l11_opy_)
def bstack1l11l11ll_opy_(self, url):
    global bstack1ll1l11ll1_opy_
    global CONFIG
    try:
        bstack11l11l11_opy_(url, CONFIG, logger)
    except Exception as err:
        logger.debug(bstack11l1l111ll_opy_.format(str(err)))
    try:
        bstack1ll1l11ll1_opy_(self, url)
    except Exception as e:
        try:
            bstack1l1111ll1_opy_ = str(e)
            if any(err_msg in bstack1l1111ll1_opy_ for err_msg in bstack1l11ll1lll_opy_):
                bstack11l11l11_opy_(url, CONFIG, logger, True)
        except Exception as err:
            logger.debug(bstack11l1l111ll_opy_.format(str(err)))
        raise e
def bstack11ll11l1_opy_(item, when):
    global bstack11ll1l111_opy_
    try:
        bstack11ll1l111_opy_(item, when)
    except Exception as e:
        pass
def bstack1l1l1ll1ll_opy_(item, call, rep):
    global bstack1l11llll1l_opy_
    global bstack1l11lll111_opy_
    name = bstack1l1_opy_ (u"ࠬ࠭ℛ")
    try:
        if rep.when == bstack1l1_opy_ (u"࠭ࡣࡢ࡮࡯ࠫℜ"):
            bstack1l1l1l1l1l_opy_ = threading.current_thread().bstackSessionId
            bstack11111ll11ll_opy_ = item.config.getoption(bstack1l1_opy_ (u"ࠧࡴ࡭࡬ࡴࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩℝ"))
            try:
                if (str(bstack11111ll11ll_opy_).lower() != bstack1l1_opy_ (u"ࠨࡶࡵࡹࡪ࠭℞")):
                    name = str(rep.nodeid)
                    bstack111ll11ll_opy_ = bstack11ll1lll1_opy_(bstack1l1_opy_ (u"ࠩࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ℟"), name, bstack1l1_opy_ (u"ࠪࠫ℠"), bstack1l1_opy_ (u"ࠫࠬ℡"), bstack1l1_opy_ (u"ࠬ࠭™"), bstack1l1_opy_ (u"࠭ࠧ℣"))
                    os.environ[bstack1l1_opy_ (u"ࠧࡑ࡛ࡗࡉࡘ࡚࡟ࡕࡇࡖࡘࡤࡔࡁࡎࡇࠪℤ")] = name
                    for driver in bstack1l11lll111_opy_:
                        if bstack1l1l1l1l1l_opy_ == driver.session_id:
                            driver.execute_script(bstack111ll11ll_opy_)
            except Exception as e:
                logger.debug(bstack1l1_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡷࡪࡺࡴࡪࡰࡪࠤࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠢࡩࡳࡷࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡷࡪࡹࡳࡪࡱࡱ࠾ࠥࢁࡽࠨ℥").format(str(e)))
            try:
                bstack11lll1l1ll_opy_(rep.outcome.lower())
                if rep.outcome.lower() != bstack1l1_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪΩ"):
                    status = bstack1l1_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ℧") if rep.outcome.lower() == bstack1l1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫℨ") else bstack1l1_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬ℩")
                    reason = bstack1l1_opy_ (u"࠭ࠧK")
                    if status == bstack1l1_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧÅ"):
                        reason = rep.longrepr.reprcrash.message
                        if (not threading.current_thread().bstackTestErrorMessages):
                            threading.current_thread().bstackTestErrorMessages = []
                        threading.current_thread().bstackTestErrorMessages.append(reason)
                    level = bstack1l1_opy_ (u"ࠨ࡫ࡱࡪࡴ࠭ℬ") if status == bstack1l1_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩℭ") else bstack1l1_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩ℮")
                    data = name + bstack1l1_opy_ (u"ࠫࠥࡶࡡࡴࡵࡨࡨࠦ࠭ℯ") if status == bstack1l1_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬℰ") else name + bstack1l1_opy_ (u"࠭ࠠࡧࡣ࡬ࡰࡪࡪࠡࠡࠩℱ") + reason
                    bstack1l1111l1l_opy_ = bstack11ll1lll1_opy_(bstack1l1_opy_ (u"ࠧࡢࡰࡱࡳࡹࡧࡴࡦࠩℲ"), bstack1l1_opy_ (u"ࠨࠩℳ"), bstack1l1_opy_ (u"ࠩࠪℴ"), bstack1l1_opy_ (u"ࠪࠫℵ"), level, data)
                    for driver in bstack1l11lll111_opy_:
                        if bstack1l1l1l1l1l_opy_ == driver.session_id:
                            driver.execute_script(bstack1l1111l1l_opy_)
            except Exception as e:
                logger.debug(bstack1l1_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡳࡦࡶࡷ࡭ࡳ࡭ࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡥࡲࡲࡹ࡫ࡸࡵࠢࡩࡳࡷࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡷࡪࡹࡳࡪࡱࡱ࠾ࠥࢁࡽࠨℶ").format(str(e)))
    except Exception as e:
        logger.debug(bstack1l1_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡨࡧࡷࡸ࡮ࡴࡧࠡࡵࡷࡥࡹ࡫ࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡵࡧࡶࡸࠥࡹࡴࡢࡶࡸࡷ࠿ࠦࡻࡾࠩℷ").format(str(e)))
    bstack1l11llll1l_opy_(item, call, rep)
notset = Notset()
def bstack11l1lll111_opy_(self, name: str, default=notset, skip: bool = False):
    global bstack1l1ll1111_opy_
    if str(name).lower() == bstack1l1_opy_ (u"࠭ࡤࡳ࡫ࡹࡩࡷ࠭ℸ"):
        return bstack1l1_opy_ (u"ࠢࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠨℹ")
    else:
        return bstack1l1ll1111_opy_(self, name, default, skip)
def bstack11l1l111l1_opy_(self):
    global CONFIG
    global bstack1l111lll1_opy_
    try:
        proxy = bstack1lll11l111_opy_(CONFIG)
        if proxy:
            if proxy.endswith(bstack1l1_opy_ (u"ࠨ࠰ࡳࡥࡨ࠭℺")):
                proxies = bstack1l111ll1_opy_(proxy, bstack1l1ll1l1ll_opy_())
                if len(proxies) > 0:
                    protocol, bstack1lll1lll_opy_ = proxies.popitem()
                    if bstack1l1_opy_ (u"ࠤ࠽࠳࠴ࠨ℻") in bstack1lll1lll_opy_:
                        return bstack1lll1lll_opy_
                    else:
                        return bstack1l1_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻࠱࠲ࠦℼ") + bstack1lll1lll_opy_
            else:
                return proxy
    except Exception as e:
        logger.error(bstack1l1_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡳࡦࡶࡷ࡭ࡳ࡭ࠠࡱࡴࡲࡼࡾࠦࡵࡳ࡮ࠣ࠾ࠥࢁࡽࠣℽ").format(str(e)))
    return bstack1l111lll1_opy_(self)
def bstack11ll1l11_opy_():
    return (bstack1l1_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨℾ") in CONFIG or bstack1l1_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪℿ") in CONFIG) and bstack1l11l1l1_opy_() and bstack11ll1ll11l_opy_() >= version.parse(
        bstack11llll11ll_opy_)
def bstack1111ll1l_opy_(self,
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
    global bstack11l1l11l11_opy_
    global bstack1l11l1ll1_opy_
    global bstack111l1l1l_opy_
    CONFIG[bstack1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࡙ࡄࡌࠩ⅀")] = str(bstack111l1l1l_opy_) + str(__version__)
    bstack11ll11ll11_opy_ = 0
    try:
        if bstack1l11l1ll1_opy_ is True:
            bstack11ll11ll11_opy_ = int(os.environ.get(bstack1l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨ⅁")))
    except:
        bstack11ll11ll11_opy_ = 0
    CONFIG[bstack1l1_opy_ (u"ࠤ࡬ࡷࡕࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣ⅂")] = True
    bstack1l111lllll_opy_ = bstack1111l1l11_opy_(CONFIG, bstack11ll11ll11_opy_)
    logger.debug(bstack1l11llll11_opy_.format(str(bstack1l111lllll_opy_)))
    if CONFIG.get(bstack1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧ⅃")):
        bstack1ll111llll_opy_(bstack1l111lllll_opy_, bstack1lll11l1_opy_)
    if bstack1l1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ⅄") in CONFIG and bstack1l1_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪⅅ") in CONFIG[bstack1l1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩⅆ")][bstack11ll11ll11_opy_]:
        bstack11l1l11l11_opy_ = CONFIG[bstack1l1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪⅇ")][bstack11ll11ll11_opy_][bstack1l1_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ⅈ")]
    import urllib
    import json
    if bstack1l1_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭ⅉ") in CONFIG and str(CONFIG[bstack1l1_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧ⅊")]).lower() != bstack1l1_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪ⅋"):
        bstack1ll11l1l_opy_ = bstack1ll1ll11l_opy_()
        bstack111l1l11l_opy_ = bstack1ll11l1l_opy_ + urllib.parse.quote(json.dumps(bstack1l111lllll_opy_))
    else:
        bstack111l1l11l_opy_ = bstack1l1_opy_ (u"ࠬࡽࡳࡴ࠼࠲࠳ࡨࡪࡰ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࡀࡥࡤࡴࡸࡃࠧ⅌") + urllib.parse.quote(json.dumps(bstack1l111lllll_opy_))
    browser = self.connect(bstack111l1l11l_opy_)
    return browser
def bstack1l1l111ll1_opy_():
    global bstack11ll1111l1_opy_
    global bstack111l1l1l_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        from bstack_utils.helper import bstack1l11l1lll1_opy_
        if not bstack1ll111l1ll1_opy_():
            global bstack1111ll11l_opy_
            if not bstack1111ll11l_opy_:
                from bstack_utils.helper import bstack1ll1lll11l_opy_, bstack11lll1ll1l_opy_
                bstack1111ll11l_opy_ = bstack1ll1lll11l_opy_()
                bstack11lll1ll1l_opy_(bstack111l1l1l_opy_)
            BrowserType.connect = bstack1l11l1lll1_opy_
            return
        BrowserType.launch = bstack1111ll1l_opy_
        bstack11ll1111l1_opy_ = True
    except Exception as e:
        pass
def bstack1111l1111l1_opy_():
    global CONFIG
    global bstack11lll1ll1_opy_
    global bstack1lll11l1l_opy_
    global bstack1lll11l1_opy_
    global bstack1l11l1ll1_opy_
    global bstack1l11l1lll_opy_
    CONFIG = json.loads(os.environ.get(bstack1l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡉࡏࡏࡈࡌࡋࠬ⅍")))
    bstack11lll1ll1_opy_ = eval(os.environ.get(bstack1l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡉࡔࡡࡄࡔࡕࡥࡁࡖࡖࡒࡑࡆ࡚ࡅࠨⅎ")))
    bstack1lll11l1l_opy_ = os.environ.get(bstack1l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡉࡗࡅࡣ࡚ࡘࡌࠨ⅏"))
    bstack11l1l1l1l1_opy_(CONFIG, bstack11lll1ll1_opy_)
    bstack1l11l1lll_opy_ = bstack1l11l11lll_opy_.bstack1ll11l11ll_opy_(CONFIG, bstack1l11l1lll_opy_)
    if cli.bstack1ll1lll1ll_opy_():
        bstack1llll1l111_opy_.invoke(bstack1lll111l11_opy_.CONNECT, bstack1l1ll1lll_opy_())
        cli_context.platform_index = int(os.environ.get(bstack1l1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩ⅐"), bstack1l1_opy_ (u"ࠪ࠴ࠬ⅑")))
        cli.bstack1llllll11l1_opy_(cli_context.platform_index)
        cli.bstack1lll111l111_opy_(bstack1l1ll1l1ll_opy_(bstack1lll11l1l_opy_, CONFIG), cli_context.platform_index, bstack1l1l1l1ll1_opy_)
        cli.bstack1lllllll11l_opy_()
        logger.debug(bstack1l1_opy_ (u"ࠦࡈࡒࡉࠡ࡫ࡶࠤࡦࡩࡴࡪࡸࡨࠤ࡫ࡵࡲࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢ࡭ࡳࡪࡥࡹ࠿ࠥ⅒") + str(cli_context.platform_index) + bstack1l1_opy_ (u"ࠧࠨ⅓"))
        return # skip all existing bstack1111l11l1ll_opy_
    global bstack11l11llll_opy_
    global bstack11l1lllll_opy_
    global bstack11ll1l11ll_opy_
    global bstack111ll111l_opy_
    global bstack1l1ll11lll_opy_
    global bstack11l1l1l11_opy_
    global bstack1ll11llll1_opy_
    global bstack1ll1l11ll1_opy_
    global bstack1l111lll1_opy_
    global bstack1l1ll1111_opy_
    global bstack11ll1l111_opy_
    global bstack1l11llll1l_opy_
    try:
        from selenium import webdriver
        from selenium.webdriver.remote.webdriver import WebDriver
        bstack11l11llll_opy_ = webdriver.Remote.__init__
        bstack11l1lllll_opy_ = WebDriver.quit
        bstack1ll11llll1_opy_ = WebDriver.close
        bstack1ll1l11ll1_opy_ = WebDriver.get
    except Exception as e:
        pass
    if (bstack1l1_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩ⅔") in CONFIG or bstack1l1_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫ⅕") in CONFIG) and bstack1l11l1l1_opy_():
        if bstack11ll1ll11l_opy_() < version.parse(bstack11llll11ll_opy_):
            logger.error(bstack1111lll1l_opy_.format(bstack11ll1ll11l_opy_()))
        else:
            try:
                from selenium.webdriver.remote.remote_connection import RemoteConnection
                bstack1l111lll1_opy_ = RemoteConnection._1l1lll1ll_opy_
            except Exception as e:
                logger.error(bstack1111ll1ll_opy_.format(str(e)))
    try:
        from _pytest.config import Config
        bstack1l1ll1111_opy_ = Config.getoption
        from _pytest import runner
        bstack11ll1l111_opy_ = runner._update_current_test_var
    except Exception as e:
        logger.warn(e, bstack1lllll111_opy_)
    try:
        from pytest_bdd import reporting
        bstack1l11llll1l_opy_ = reporting.runtest_makereport
    except Exception as e:
        logger.debug(bstack1l1_opy_ (u"ࠨࡒ࡯ࡩࡦࡹࡥࠡ࡫ࡱࡷࡹࡧ࡬࡭ࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡴࡰࠢࡵࡹࡳࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡸࡪࡹࡴࡴࠩ⅖"))
    bstack1lll11l1_opy_ = CONFIG.get(bstack1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭⅗"), {}).get(bstack1l1_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ⅘"))
    bstack1l11l1ll1_opy_ = True
    bstack11l1l1l111_opy_(bstack11l1ll111l_opy_)
if (bstack11l1l1l1l11_opy_()):
    bstack1111l1111l1_opy_()
@bstack111l1ll1l1_opy_(class_method=False)
def bstack1111l111l1l_opy_(hook_name, event, bstack1l11l111l1l_opy_=None):
    if hook_name not in [bstack1l1_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࠬ⅙"), bstack1l1_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࠩ⅚"), bstack1l1_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡳ࡯ࡥࡷ࡯ࡩࠬ⅛"), bstack1l1_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡳࡩࡻ࡬ࡦࠩ⅜"), bstack1l1_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟ࡤ࡮ࡤࡷࡸ࠭⅝"), bstack1l1_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡨࡲࡡࡴࡵࠪ⅞"), bstack1l1_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡰࡩࡹ࡮࡯ࡥࠩ⅟"), bstack1l1_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡦࡶ࡫ࡳࡩ࠭Ⅰ")]:
        return
    node = store[bstack1l1_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡺࡥ࡮ࠩⅡ")]
    if hook_name in [bstack1l1_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡳ࡯ࡥࡷ࡯ࡩࠬⅢ"), bstack1l1_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡳࡩࡻ࡬ࡦࠩⅣ")]:
        node = store[bstack1l1_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡰࡳࡩࡻ࡬ࡦࡡ࡬ࡸࡪࡳࠧⅤ")]
    elif hook_name in [bstack1l1_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠࡥ࡯ࡥࡸࡹࠧⅥ"), bstack1l1_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡩ࡬ࡢࡵࡶࠫⅦ")]:
        node = store[bstack1l1_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡩ࡬ࡢࡵࡶࡣ࡮ࡺࡥ࡮ࠩⅧ")]
    hook_type = bstack111l1l1ll1l_opy_(hook_name)
    if event == bstack1l1_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩࠬⅨ"):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1lll1l1lll1_opy_[hook_type], bstack1llll111ll1_opy_.PRE, node, hook_name)
            return
        uuid = uuid4().__str__()
        bstack111l1ll111_opy_ = {
            bstack1l1_opy_ (u"࠭ࡵࡶ࡫ࡧࠫⅩ"): uuid,
            bstack1l1_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫⅪ"): bstack11l1l11ll1_opy_(),
            bstack1l1_opy_ (u"ࠨࡶࡼࡴࡪ࠭Ⅻ"): bstack1l1_opy_ (u"ࠩ࡫ࡳࡴࡱࠧⅬ"),
            bstack1l1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡶࡼࡴࡪ࠭Ⅽ"): hook_type,
            bstack1l1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡱࡥࡲ࡫ࠧⅮ"): hook_name
        }
        store[bstack1l1_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩⅯ")].append(uuid)
        bstack1111l111l11_opy_ = node.nodeid
        if hook_type == bstack1l1_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡅࡂࡅࡋࠫⅰ"):
            if not _111llll111_opy_.get(bstack1111l111l11_opy_, None):
                _111llll111_opy_[bstack1111l111l11_opy_] = {bstack1l1_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭ⅱ"): []}
            _111llll111_opy_[bstack1111l111l11_opy_][bstack1l1_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧⅲ")].append(bstack111l1ll111_opy_[bstack1l1_opy_ (u"ࠩࡸࡹ࡮ࡪࠧⅳ")])
        _111llll111_opy_[bstack1111l111l11_opy_ + bstack1l1_opy_ (u"ࠪ࠱ࠬⅴ") + hook_name] = bstack111l1ll111_opy_
        bstack11111lllll1_opy_(node, bstack111l1ll111_opy_, bstack1l1_opy_ (u"ࠫࡍࡵ࡯࡬ࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬⅵ"))
    elif event == bstack1l1_opy_ (u"ࠬࡧࡦࡵࡧࡵࠫⅶ"):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1lll1l1lll1_opy_[hook_type], bstack1llll111ll1_opy_.POST, node, None, bstack1l11l111l1l_opy_)
            return
        bstack11l111l111_opy_ = node.nodeid + bstack1l1_opy_ (u"࠭࠭ࠨⅷ") + hook_name
        _111llll111_opy_[bstack11l111l111_opy_][bstack1l1_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬⅸ")] = bstack11l1l11ll1_opy_()
        bstack11111llll11_opy_(_111llll111_opy_[bstack11l111l111_opy_][bstack1l1_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ⅹ")])
        bstack11111lllll1_opy_(node, _111llll111_opy_[bstack11l111l111_opy_], bstack1l1_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫⅺ"), bstack1111l11l11l_opy_=bstack1l11l111l1l_opy_)
def bstack11111ll1l11_opy_():
    global bstack1111l111ll1_opy_
    if bstack11111l1l1_opy_():
        bstack1111l111ll1_opy_ = bstack1l1_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠧⅻ")
    else:
        bstack1111l111ll1_opy_ = bstack1l1_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫⅼ")
@bstack111111l1_opy_.bstack1111ll1l1l1_opy_
def bstack1111l11ll11_opy_():
    bstack11111ll1l11_opy_()
    if cli.is_running():
        try:
            bstack11l11lll1l1_opy_(bstack1111l111l1l_opy_)
        except Exception as e:
            logger.debug(bstack1l1_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤ࡭ࡵ࡯࡬ࡵࠣࡴࡦࡺࡣࡩ࠼ࠣࡿࢂࠨⅽ").format(e))
        return
    if bstack1l11l1l1_opy_():
        bstack11llllll1_opy_ = Config.bstack111111ll_opy_()
        bstack1l1_opy_ (u"࠭ࠧࠨࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡇࡱࡵࠤࡵࡶࡰࠡ࠿ࠣ࠵࠱ࠦ࡭ࡰࡦࡢࡩࡽ࡫ࡣࡶࡶࡨࠤ࡬࡫ࡴࡴࠢࡸࡷࡪࡪࠠࡧࡱࡵࠤࡦ࠷࠱ࡺࠢࡦࡳࡲࡳࡡ࡯ࡦࡶ࠱ࡼࡸࡡࡱࡲ࡬ࡲ࡬ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡋࡵࡲࠡࡲࡳࡴࠥࡄࠠ࠲࠮ࠣࡱࡴࡪ࡟ࡦࡺࡨࡧࡺࡺࡥࠡࡦࡲࡩࡸࠦ࡮ࡰࡶࠣࡶࡺࡴࠠࡣࡧࡦࡥࡺࡹࡥࠡ࡫ࡷࠤ࡮ࡹࠠࡱࡣࡷࡧ࡭࡫ࡤࠡ࡫ࡱࠤࡦࠦࡤࡪࡨࡩࡩࡷ࡫࡮ࡵࠢࡳࡶࡴࡩࡥࡴࡵࠣ࡭ࡩࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࡙࡮ࡵࡴࠢࡺࡩࠥࡴࡥࡦࡦࠣࡸࡴࠦࡵࡴࡧࠣࡗࡪࡲࡥ࡯࡫ࡸࡱࡕࡧࡴࡤࡪࠫࡷࡪࡲࡥ࡯࡫ࡸࡱࡤ࡮ࡡ࡯ࡦ࡯ࡩࡷ࠯ࠠࡧࡱࡵࠤࡵࡶࡰࠡࡀࠣ࠵ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠧࠨࠩⅾ")
        if bstack11llllll1_opy_.get_property(bstack1l1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟࡮ࡱࡧࡣࡨࡧ࡬࡭ࡧࡧࠫⅿ")):
            if CONFIG.get(bstack1l1_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨↀ")) is not None and int(CONFIG[bstack1l1_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩↁ")]) > 1:
                bstack1ll1l1l111_opy_(bstack1ll1ll1ll_opy_)
            return
        bstack1ll1l1l111_opy_(bstack1ll1ll1ll_opy_)
    try:
        bstack11l11lll1l1_opy_(bstack1111l111l1l_opy_)
    except Exception as e:
        logger.debug(bstack1l1_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢ࡫ࡳࡴࡱࡳࠡࡲࡤࡸࡨ࡮࠺ࠡࡽࢀࠦↂ").format(e))
bstack1111l11ll11_opy_()