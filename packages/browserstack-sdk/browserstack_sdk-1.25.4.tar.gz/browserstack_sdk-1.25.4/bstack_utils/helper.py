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
import collections
import datetime
import json
import os
import platform
import re
import subprocess
import traceback
import tempfile
import multiprocessing
import threading
import sys
import logging
from math import ceil
import urllib
from urllib.parse import urlparse
import copy
import zipfile
import git
import requests
from packaging import version
from bstack_utils.config import Config
from bstack_utils.constants import (bstack11ll1l1l111_opy_, bstack1l1llll1l1_opy_, bstack1ll11l11ll_opy_, bstack11l1ll1l11_opy_,
                                    bstack11ll1ll1l1l_opy_, bstack11ll1l111ll_opy_, bstack11ll1l11lll_opy_, bstack11ll1lllll1_opy_)
from bstack_utils.measure import measure
from bstack_utils.messages import bstack11l1ll1l_opy_, bstack1ll1l11lll_opy_
from bstack_utils.proxy import bstack1l1lll11l1_opy_, bstack1lll1l1l_opy_
from bstack_utils.constants import *
from bstack_utils import bstack111l1l111_opy_
from browserstack_sdk._version import __version__
bstack11llllllll_opy_ = Config.bstack1l1111llll_opy_()
logger = bstack111l1l111_opy_.get_logger(__name__, bstack111l1l111_opy_.bstack1llll111l1l_opy_())
def bstack11llll11ll1_opy_(config):
    return config[bstack1l1ll11_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ᦜ")]
def bstack11lllll111l_opy_(config):
    return config[bstack1l1ll11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨᦝ")]
def bstack11lll111_opy_():
    try:
        import playwright
        return True
    except ImportError:
        return False
def bstack11l1l1111ll_opy_(obj):
    values = []
    bstack11l1lll11ll_opy_ = re.compile(bstack1l1ll11_opy_ (u"ࡸࠢ࡟ࡅࡘࡗ࡙ࡕࡍࡠࡖࡄࡋࡤࡢࡤࠬࠦࠥᦞ"), re.I)
    for key in obj.keys():
        if bstack11l1lll11ll_opy_.match(key):
            values.append(obj[key])
    return values
def bstack11l1ll1llll_opy_(config):
    tags = []
    tags.extend(bstack11l1l1111ll_opy_(os.environ))
    tags.extend(bstack11l1l1111ll_opy_(config))
    return tags
def bstack11l1l11ll1l_opy_(markers):
    tags = []
    for marker in markers:
        tags.append(marker.name)
    return tags
def bstack11l1lll1lll_opy_(bstack11l1llll1l1_opy_):
    if not bstack11l1llll1l1_opy_:
        return bstack1l1ll11_opy_ (u"ࠧࠨᦟ")
    return bstack1l1ll11_opy_ (u"ࠣࡽࢀࠤ࠭ࢁࡽࠪࠤᦠ").format(bstack11l1llll1l1_opy_.name, bstack11l1llll1l1_opy_.email)
def bstack11llll11l11_opy_():
    try:
        repo = git.Repo(search_parent_directories=True)
        bstack11l1lll1111_opy_ = repo.common_dir
        info = {
            bstack1l1ll11_opy_ (u"ࠤࡶ࡬ࡦࠨᦡ"): repo.head.commit.hexsha,
            bstack1l1ll11_opy_ (u"ࠥࡷ࡭ࡵࡲࡵࡡࡶ࡬ࡦࠨᦢ"): repo.git.rev_parse(repo.head.commit, short=True),
            bstack1l1ll11_opy_ (u"ࠦࡧࡸࡡ࡯ࡥ࡫ࠦᦣ"): repo.active_branch.name,
            bstack1l1ll11_opy_ (u"ࠧࡺࡡࡨࠤᦤ"): repo.git.describe(all=True, tags=True, exact_match=True),
            bstack1l1ll11_opy_ (u"ࠨࡣࡰ࡯ࡰ࡭ࡹࡺࡥࡳࠤᦥ"): bstack11l1lll1lll_opy_(repo.head.commit.committer),
            bstack1l1ll11_opy_ (u"ࠢࡤࡱࡰࡱ࡮ࡺࡴࡦࡴࡢࡨࡦࡺࡥࠣᦦ"): repo.head.commit.committed_datetime.isoformat(),
            bstack1l1ll11_opy_ (u"ࠣࡣࡸࡸ࡭ࡵࡲࠣᦧ"): bstack11l1lll1lll_opy_(repo.head.commit.author),
            bstack1l1ll11_opy_ (u"ࠤࡤࡹࡹ࡮࡯ࡳࡡࡧࡥࡹ࡫ࠢᦨ"): repo.head.commit.authored_datetime.isoformat(),
            bstack1l1ll11_opy_ (u"ࠥࡧࡴࡳ࡭ࡪࡶࡢࡱࡪࡹࡳࡢࡩࡨࠦᦩ"): repo.head.commit.message,
            bstack1l1ll11_opy_ (u"ࠦࡷࡵ࡯ࡵࠤᦪ"): repo.git.rev_parse(bstack1l1ll11_opy_ (u"ࠧ࠳࠭ࡴࡪࡲࡻ࠲ࡺ࡯ࡱ࡮ࡨࡺࡪࡲࠢᦫ")),
            bstack1l1ll11_opy_ (u"ࠨࡣࡰ࡯ࡰࡳࡳࡥࡧࡪࡶࡢࡨ࡮ࡸࠢ᦬"): bstack11l1lll1111_opy_,
            bstack1l1ll11_opy_ (u"ࠢࡸࡱࡵ࡯ࡹࡸࡥࡦࡡࡪ࡭ࡹࡥࡤࡪࡴࠥ᦭"): subprocess.check_output([bstack1l1ll11_opy_ (u"ࠣࡩ࡬ࡸࠧ᦮"), bstack1l1ll11_opy_ (u"ࠤࡵࡩࡻ࠳ࡰࡢࡴࡶࡩࠧ᦯"), bstack1l1ll11_opy_ (u"ࠥ࠱࠲࡭ࡩࡵ࠯ࡦࡳࡲࡳ࡯࡯࠯ࡧ࡭ࡷࠨᦰ")]).strip().decode(
                bstack1l1ll11_opy_ (u"ࠫࡺࡺࡦ࠮࠺ࠪᦱ")),
            bstack1l1ll11_opy_ (u"ࠧࡲࡡࡴࡶࡢࡸࡦ࡭ࠢᦲ"): repo.git.describe(tags=True, abbrev=0, always=True),
            bstack1l1ll11_opy_ (u"ࠨࡣࡰ࡯ࡰ࡭ࡹࡹ࡟ࡴ࡫ࡱࡧࡪࡥ࡬ࡢࡵࡷࡣࡹࡧࡧࠣᦳ"): repo.git.rev_list(
                bstack1l1ll11_opy_ (u"ࠢࡼࡿ࠱࠲ࢀࢃࠢᦴ").format(repo.head.commit, repo.git.describe(tags=True, abbrev=0, always=True)), count=True)
        }
        remotes = repo.remotes
        bstack11ll1111ll1_opy_ = []
        for remote in remotes:
            bstack11ll111l1ll_opy_ = {
                bstack1l1ll11_opy_ (u"ࠣࡰࡤࡱࡪࠨᦵ"): remote.name,
                bstack1l1ll11_opy_ (u"ࠤࡸࡶࡱࠨᦶ"): remote.url,
            }
            bstack11ll1111ll1_opy_.append(bstack11ll111l1ll_opy_)
        bstack11ll11ll1ll_opy_ = {
            bstack1l1ll11_opy_ (u"ࠥࡲࡦࡳࡥࠣᦷ"): bstack1l1ll11_opy_ (u"ࠦ࡬࡯ࡴࠣᦸ"),
            **info,
            bstack1l1ll11_opy_ (u"ࠧࡸࡥ࡮ࡱࡷࡩࡸࠨᦹ"): bstack11ll1111ll1_opy_
        }
        bstack11ll11ll1ll_opy_ = bstack11l1llll111_opy_(bstack11ll11ll1ll_opy_)
        return bstack11ll11ll1ll_opy_
    except git.InvalidGitRepositoryError:
        return {}
    except Exception as err:
        print(bstack1l1ll11_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶ࡯ࡱࡷ࡯ࡥࡹ࡯࡮ࡨࠢࡊ࡭ࡹࠦ࡭ࡦࡶࡤࡨࡦࡺࡡࠡࡹ࡬ࡸ࡭ࠦࡥࡳࡴࡲࡶ࠿ࠦࡻࡾࠤᦺ").format(err))
        return {}
def bstack11l1llll111_opy_(bstack11ll11ll1ll_opy_):
    bstack11l1lll1l1l_opy_ = bstack11ll111ll1l_opy_(bstack11ll11ll1ll_opy_)
    if bstack11l1lll1l1l_opy_ and bstack11l1lll1l1l_opy_ > bstack11ll1ll1l1l_opy_:
        bstack11l1llll11l_opy_ = bstack11l1lll1l1l_opy_ - bstack11ll1ll1l1l_opy_
        bstack11l1ll1ll1l_opy_ = bstack11l1l1lllll_opy_(bstack11ll11ll1ll_opy_[bstack1l1ll11_opy_ (u"ࠢࡤࡱࡰࡱ࡮ࡺ࡟࡮ࡧࡶࡷࡦ࡭ࡥࠣᦻ")], bstack11l1llll11l_opy_)
        bstack11ll11ll1ll_opy_[bstack1l1ll11_opy_ (u"ࠣࡥࡲࡱࡲ࡯ࡴࡠ࡯ࡨࡷࡸࡧࡧࡦࠤᦼ")] = bstack11l1ll1ll1l_opy_
        logger.info(bstack1l1ll11_opy_ (u"ࠤࡗ࡬ࡪࠦࡣࡰ࡯ࡰ࡭ࡹࠦࡨࡢࡵࠣࡦࡪ࡫࡮ࠡࡶࡵࡹࡳࡩࡡࡵࡧࡧ࠲࡙ࠥࡩࡻࡧࠣࡳ࡫ࠦࡣࡰ࡯ࡰ࡭ࡹࠦࡡࡧࡶࡨࡶࠥࡺࡲࡶࡰࡦࡥࡹ࡯࡯࡯ࠢ࡬ࡷࠥࢁࡽࠡࡍࡅࠦᦽ")
                    .format(bstack11ll111ll1l_opy_(bstack11ll11ll1ll_opy_) / 1024))
    return bstack11ll11ll1ll_opy_
def bstack11ll111ll1l_opy_(bstack1l1l1l111l_opy_):
    try:
        if bstack1l1l1l111l_opy_:
            bstack11ll111l111_opy_ = json.dumps(bstack1l1l1l111l_opy_)
            bstack11l1l1ll111_opy_ = sys.getsizeof(bstack11ll111l111_opy_)
            return bstack11l1l1ll111_opy_
    except Exception as e:
        logger.debug(bstack1l1ll11_opy_ (u"ࠥࡗࡴࡳࡥࡵࡪ࡬ࡲ࡬ࠦࡷࡦࡰࡷࠤࡼࡸ࡯࡯ࡩࠣࡻ࡭࡯࡬ࡦࠢࡦࡥࡱࡩࡵ࡭ࡣࡷ࡭ࡳ࡭ࠠࡴ࡫ࡽࡩࠥࡵࡦࠡࡌࡖࡓࡓࠦ࡯ࡣ࡬ࡨࡧࡹࡀࠠࡼࡿࠥᦾ").format(e))
    return -1
def bstack11l1l1lllll_opy_(field, bstack11l1l1lll1l_opy_):
    try:
        bstack11l1l1lll11_opy_ = len(bytes(bstack11ll1l111ll_opy_, bstack1l1ll11_opy_ (u"ࠫࡺࡺࡦ࠮࠺ࠪᦿ")))
        bstack11l1l11l11l_opy_ = bytes(field, bstack1l1ll11_opy_ (u"ࠬࡻࡴࡧ࠯࠻ࠫᧀ"))
        bstack11l1l11l1l1_opy_ = len(bstack11l1l11l11l_opy_)
        bstack11ll1111lll_opy_ = ceil(bstack11l1l11l1l1_opy_ - bstack11l1l1lll1l_opy_ - bstack11l1l1lll11_opy_)
        if bstack11ll1111lll_opy_ > 0:
            bstack11l1l1l11l1_opy_ = bstack11l1l11l11l_opy_[:bstack11ll1111lll_opy_].decode(bstack1l1ll11_opy_ (u"࠭ࡵࡵࡨ࠰࠼ࠬᧁ"), errors=bstack1l1ll11_opy_ (u"ࠧࡪࡩࡱࡳࡷ࡫ࠧᧂ")) + bstack11ll1l111ll_opy_
            return bstack11l1l1l11l1_opy_
    except Exception as e:
        logger.debug(bstack1l1ll11_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦࡴࡳࡷࡱࡧࡦࡺࡩ࡯ࡩࠣࡪ࡮࡫࡬ࡥ࠮ࠣࡲࡴࡺࡨࡪࡰࡪࠤࡼࡧࡳࠡࡶࡵࡹࡳࡩࡡࡵࡧࡧࠤ࡭࡫ࡲࡦ࠼ࠣࡿࢂࠨᧃ").format(e))
    return field
def bstack11111ll1_opy_():
    env = os.environ
    if (bstack1l1ll11_opy_ (u"ࠤࡍࡉࡓࡑࡉࡏࡕࡢ࡙ࡗࡒࠢᧄ") in env and len(env[bstack1l1ll11_opy_ (u"ࠥࡎࡊࡔࡋࡊࡐࡖࡣ࡚ࡘࡌࠣᧅ")]) > 0) or (
            bstack1l1ll11_opy_ (u"ࠦࡏࡋࡎࡌࡋࡑࡗࡤࡎࡏࡎࡇࠥᧆ") in env and len(env[bstack1l1ll11_opy_ (u"ࠧࡐࡅࡏࡍࡌࡒࡘࡥࡈࡐࡏࡈࠦᧇ")]) > 0):
        return {
            bstack1l1ll11_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᧈ"): bstack1l1ll11_opy_ (u"ࠢࡋࡧࡱ࡯࡮ࡴࡳࠣᧉ"),
            bstack1l1ll11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦ᧊"): env.get(bstack1l1ll11_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡗࡕࡐࠧ᧋")),
            bstack1l1ll11_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧ᧌"): env.get(bstack1l1ll11_opy_ (u"ࠦࡏࡕࡂࡠࡐࡄࡑࡊࠨ᧍")),
            bstack1l1ll11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ᧎"): env.get(bstack1l1ll11_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࠧ᧏"))
        }
    if env.get(bstack1l1ll11_opy_ (u"ࠢࡄࡋࠥ᧐")) == bstack1l1ll11_opy_ (u"ࠣࡶࡵࡹࡪࠨ᧑") and bstack11111ll1l_opy_(env.get(bstack1l1ll11_opy_ (u"ࠤࡆࡍࡗࡉࡌࡆࡅࡌࠦ᧒"))):
        return {
            bstack1l1ll11_opy_ (u"ࠥࡲࡦࡳࡥࠣ᧓"): bstack1l1ll11_opy_ (u"ࠦࡈ࡯ࡲࡤ࡮ࡨࡇࡎࠨ᧔"),
            bstack1l1ll11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣ᧕"): env.get(bstack1l1ll11_opy_ (u"ࠨࡃࡊࡔࡆࡐࡊࡥࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠤ᧖")),
            bstack1l1ll11_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤ᧗"): env.get(bstack1l1ll11_opy_ (u"ࠣࡅࡌࡖࡈࡒࡅࡠࡌࡒࡆࠧ᧘")),
            bstack1l1ll11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣ᧙"): env.get(bstack1l1ll11_opy_ (u"ࠥࡇࡎࡘࡃࡍࡇࡢࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࠨ᧚"))
        }
    if env.get(bstack1l1ll11_opy_ (u"ࠦࡈࡏࠢ᧛")) == bstack1l1ll11_opy_ (u"ࠧࡺࡲࡶࡧࠥ᧜") and bstack11111ll1l_opy_(env.get(bstack1l1ll11_opy_ (u"ࠨࡔࡓࡃ࡙ࡍࡘࠨ᧝"))):
        return {
            bstack1l1ll11_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ᧞"): bstack1l1ll11_opy_ (u"ࠣࡖࡵࡥࡻ࡯ࡳࠡࡅࡌࠦ᧟"),
            bstack1l1ll11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧ᧠"): env.get(bstack1l1ll11_opy_ (u"ࠥࡘࡗࡇࡖࡊࡕࡢࡆ࡚ࡏࡌࡅࡡ࡚ࡉࡇࡥࡕࡓࡎࠥ᧡")),
            bstack1l1ll11_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨ᧢"): env.get(bstack1l1ll11_opy_ (u"࡚ࠧࡒࡂࡘࡌࡗࡤࡐࡏࡃࡡࡑࡅࡒࡋࠢ᧣")),
            bstack1l1ll11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧ᧤"): env.get(bstack1l1ll11_opy_ (u"ࠢࡕࡔࡄ࡚ࡎ࡙࡟ࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࠨ᧥"))
        }
    if env.get(bstack1l1ll11_opy_ (u"ࠣࡅࡌࠦ᧦")) == bstack1l1ll11_opy_ (u"ࠤࡷࡶࡺ࡫ࠢ᧧") and env.get(bstack1l1ll11_opy_ (u"ࠥࡇࡎࡥࡎࡂࡏࡈࠦ᧨")) == bstack1l1ll11_opy_ (u"ࠦࡨࡵࡤࡦࡵ࡫࡭ࡵࠨ᧩"):
        return {
            bstack1l1ll11_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ᧪"): bstack1l1ll11_opy_ (u"ࠨࡃࡰࡦࡨࡷ࡭࡯ࡰࠣ᧫"),
            bstack1l1ll11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥ᧬"): None,
            bstack1l1ll11_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥ᧭"): None,
            bstack1l1ll11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣ᧮"): None
        }
    if env.get(bstack1l1ll11_opy_ (u"ࠥࡆࡎ࡚ࡂࡖࡅࡎࡉ࡙ࡥࡂࡓࡃࡑࡇࡍࠨ᧯")) and env.get(bstack1l1ll11_opy_ (u"ࠦࡇࡏࡔࡃࡗࡆࡏࡊ࡚࡟ࡄࡑࡐࡑࡎ࡚ࠢ᧰")):
        return {
            bstack1l1ll11_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ᧱"): bstack1l1ll11_opy_ (u"ࠨࡂࡪࡶࡥࡹࡨࡱࡥࡵࠤ᧲"),
            bstack1l1ll11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥ᧳"): env.get(bstack1l1ll11_opy_ (u"ࠣࡄࡌࡘࡇ࡛ࡃࡌࡇࡗࡣࡌࡏࡔࡠࡊࡗࡘࡕࡥࡏࡓࡋࡊࡍࡓࠨ᧴")),
            bstack1l1ll11_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦ᧵"): None,
            bstack1l1ll11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ᧶"): env.get(bstack1l1ll11_opy_ (u"ࠦࡇࡏࡔࡃࡗࡆࡏࡊ࡚࡟ࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࠨ᧷"))
        }
    if env.get(bstack1l1ll11_opy_ (u"ࠧࡉࡉࠣ᧸")) == bstack1l1ll11_opy_ (u"ࠨࡴࡳࡷࡨࠦ᧹") and bstack11111ll1l_opy_(env.get(bstack1l1ll11_opy_ (u"ࠢࡅࡔࡒࡒࡊࠨ᧺"))):
        return {
            bstack1l1ll11_opy_ (u"ࠣࡰࡤࡱࡪࠨ᧻"): bstack1l1ll11_opy_ (u"ࠤࡇࡶࡴࡴࡥࠣ᧼"),
            bstack1l1ll11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨ᧽"): env.get(bstack1l1ll11_opy_ (u"ࠦࡉࡘࡏࡏࡇࡢࡆ࡚ࡏࡌࡅࡡࡏࡍࡓࡑࠢ᧾")),
            bstack1l1ll11_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢ᧿"): None,
            bstack1l1ll11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᨀ"): env.get(bstack1l1ll11_opy_ (u"ࠢࡅࡔࡒࡒࡊࡥࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࠧᨁ"))
        }
    if env.get(bstack1l1ll11_opy_ (u"ࠣࡅࡌࠦᨂ")) == bstack1l1ll11_opy_ (u"ࠤࡷࡶࡺ࡫ࠢᨃ") and bstack11111ll1l_opy_(env.get(bstack1l1ll11_opy_ (u"ࠥࡗࡊࡓࡁࡑࡊࡒࡖࡊࠨᨄ"))):
        return {
            bstack1l1ll11_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᨅ"): bstack1l1ll11_opy_ (u"࡙ࠧࡥ࡮ࡣࡳ࡬ࡴࡸࡥࠣᨆ"),
            bstack1l1ll11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᨇ"): env.get(bstack1l1ll11_opy_ (u"ࠢࡔࡇࡐࡅࡕࡎࡏࡓࡇࡢࡓࡗࡍࡁࡏࡋ࡝ࡅ࡙ࡏࡏࡏࡡࡘࡖࡑࠨᨈ")),
            bstack1l1ll11_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᨉ"): env.get(bstack1l1ll11_opy_ (u"ࠤࡖࡉࡒࡇࡐࡉࡑࡕࡉࡤࡐࡏࡃࡡࡑࡅࡒࡋࠢᨊ")),
            bstack1l1ll11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᨋ"): env.get(bstack1l1ll11_opy_ (u"ࠦࡘࡋࡍࡂࡒࡋࡓࡗࡋ࡟ࡋࡑࡅࡣࡎࡊࠢᨌ"))
        }
    if env.get(bstack1l1ll11_opy_ (u"ࠧࡉࡉࠣᨍ")) == bstack1l1ll11_opy_ (u"ࠨࡴࡳࡷࡨࠦᨎ") and bstack11111ll1l_opy_(env.get(bstack1l1ll11_opy_ (u"ࠢࡈࡋࡗࡐࡆࡈ࡟ࡄࡋࠥᨏ"))):
        return {
            bstack1l1ll11_opy_ (u"ࠣࡰࡤࡱࡪࠨᨐ"): bstack1l1ll11_opy_ (u"ࠤࡊ࡭ࡹࡒࡡࡣࠤᨑ"),
            bstack1l1ll11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᨒ"): env.get(bstack1l1ll11_opy_ (u"ࠦࡈࡏ࡟ࡋࡑࡅࡣ࡚ࡘࡌࠣᨓ")),
            bstack1l1ll11_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᨔ"): env.get(bstack1l1ll11_opy_ (u"ࠨࡃࡊࡡࡍࡓࡇࡥࡎࡂࡏࡈࠦᨕ")),
            bstack1l1ll11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᨖ"): env.get(bstack1l1ll11_opy_ (u"ࠣࡅࡌࡣࡏࡕࡂࡠࡋࡇࠦᨗ"))
        }
    if env.get(bstack1l1ll11_opy_ (u"ࠤࡆࡍᨘࠧ")) == bstack1l1ll11_opy_ (u"ࠥࡸࡷࡻࡥࠣᨙ") and bstack11111ll1l_opy_(env.get(bstack1l1ll11_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡎࡍ࡙ࡋࠢᨚ"))):
        return {
            bstack1l1ll11_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᨛ"): bstack1l1ll11_opy_ (u"ࠨࡂࡶ࡫࡯ࡨࡰ࡯ࡴࡦࠤ᨜"),
            bstack1l1ll11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥ᨝"): env.get(bstack1l1ll11_opy_ (u"ࠣࡄࡘࡍࡑࡊࡋࡊࡖࡈࡣࡇ࡛ࡉࡍࡆࡢ࡙ࡗࡒࠢ᨞")),
            bstack1l1ll11_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦ᨟"): env.get(bstack1l1ll11_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡍࡌࡘࡊࡥࡌࡂࡄࡈࡐࠧᨠ")) or env.get(bstack1l1ll11_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡎࡍ࡙ࡋ࡟ࡑࡋࡓࡉࡑࡏࡎࡆࡡࡑࡅࡒࡋࠢᨡ")),
            bstack1l1ll11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᨢ"): env.get(bstack1l1ll11_opy_ (u"ࠨࡂࡖࡋࡏࡈࡐࡏࡔࡆࡡࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࠣᨣ"))
        }
    if bstack11111ll1l_opy_(env.get(bstack1l1ll11_opy_ (u"ࠢࡕࡈࡢࡆ࡚ࡏࡌࡅࠤᨤ"))):
        return {
            bstack1l1ll11_opy_ (u"ࠣࡰࡤࡱࡪࠨᨥ"): bstack1l1ll11_opy_ (u"ࠤ࡙࡭ࡸࡻࡡ࡭ࠢࡖࡸࡺࡪࡩࡰࠢࡗࡩࡦࡳࠠࡔࡧࡵࡺ࡮ࡩࡥࡴࠤᨦ"),
            bstack1l1ll11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᨧ"): bstack1l1ll11_opy_ (u"ࠦࢀࢃࡻࡾࠤᨨ").format(env.get(bstack1l1ll11_opy_ (u"࡙࡙ࠬࡔࡖࡈࡑࡤ࡚ࡅࡂࡏࡉࡓ࡚ࡔࡄࡂࡖࡌࡓࡓ࡙ࡅࡓࡘࡈࡖ࡚ࡘࡉࠨᨩ")), env.get(bstack1l1ll11_opy_ (u"࠭ࡓ࡚ࡕࡗࡉࡒࡥࡔࡆࡃࡐࡔࡗࡕࡊࡆࡅࡗࡍࡉ࠭ᨪ"))),
            bstack1l1ll11_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᨫ"): env.get(bstack1l1ll11_opy_ (u"ࠣࡕ࡜ࡗ࡙ࡋࡍࡠࡆࡈࡊࡎࡔࡉࡕࡋࡒࡒࡎࡊࠢᨬ")),
            bstack1l1ll11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᨭ"): env.get(bstack1l1ll11_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡅ࡙ࡎࡒࡄࡊࡆࠥᨮ"))
        }
    if bstack11111ll1l_opy_(env.get(bstack1l1ll11_opy_ (u"ࠦࡆࡖࡐࡗࡇ࡜ࡓࡗࠨᨯ"))):
        return {
            bstack1l1ll11_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᨰ"): bstack1l1ll11_opy_ (u"ࠨࡁࡱࡲࡹࡩࡾࡵࡲࠣᨱ"),
            bstack1l1ll11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᨲ"): bstack1l1ll11_opy_ (u"ࠣࡽࢀ࠳ࡵࡸ࡯࡫ࡧࡦࡸ࠴ࢁࡽ࠰ࡽࢀ࠳ࡧࡻࡩ࡭ࡦࡶ࠳ࢀࢃࠢᨳ").format(env.get(bstack1l1ll11_opy_ (u"ࠩࡄࡔࡕ࡜ࡅ࡚ࡑࡕࡣ࡚ࡘࡌࠨᨴ")), env.get(bstack1l1ll11_opy_ (u"ࠪࡅࡕࡖࡖࡆ࡛ࡒࡖࡤࡇࡃࡄࡑࡘࡒ࡙ࡥࡎࡂࡏࡈࠫᨵ")), env.get(bstack1l1ll11_opy_ (u"ࠫࡆࡖࡐࡗࡇ࡜ࡓࡗࡥࡐࡓࡑࡍࡉࡈ࡚࡟ࡔࡎࡘࡋࠬᨶ")), env.get(bstack1l1ll11_opy_ (u"ࠬࡇࡐࡑࡘࡈ࡝ࡔࡘ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࠩᨷ"))),
            bstack1l1ll11_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᨸ"): env.get(bstack1l1ll11_opy_ (u"ࠢࡂࡒࡓ࡚ࡊ࡟ࡏࡓࡡࡍࡓࡇࡥࡎࡂࡏࡈࠦᨹ")),
            bstack1l1ll11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᨺ"): env.get(bstack1l1ll11_opy_ (u"ࠤࡄࡔࡕ࡜ࡅ࡚ࡑࡕࡣࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥᨻ"))
        }
    if env.get(bstack1l1ll11_opy_ (u"ࠥࡅ࡟࡛ࡒࡆࡡࡋࡘ࡙ࡖ࡟ࡖࡕࡈࡖࡤࡇࡇࡆࡐࡗࠦᨼ")) and env.get(bstack1l1ll11_opy_ (u"࡙ࠦࡌ࡟ࡃࡗࡌࡐࡉࠨᨽ")):
        return {
            bstack1l1ll11_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᨾ"): bstack1l1ll11_opy_ (u"ࠨࡁࡻࡷࡵࡩࠥࡉࡉࠣᨿ"),
            bstack1l1ll11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᩀ"): bstack1l1ll11_opy_ (u"ࠣࡽࢀࡿࢂ࠵࡟ࡣࡷ࡬ࡰࡩ࠵ࡲࡦࡵࡸࡰࡹࡹ࠿ࡣࡷ࡬ࡰࡩࡏࡤ࠾ࡽࢀࠦᩁ").format(env.get(bstack1l1ll11_opy_ (u"ࠩࡖ࡝ࡘ࡚ࡅࡎࡡࡗࡉࡆࡓࡆࡐࡗࡑࡈࡆ࡚ࡉࡐࡐࡖࡉࡗ࡜ࡅࡓࡗࡕࡍࠬᩂ")), env.get(bstack1l1ll11_opy_ (u"ࠪࡗ࡞࡙ࡔࡆࡏࡢࡘࡊࡇࡍࡑࡔࡒࡎࡊࡉࡔࠨᩃ")), env.get(bstack1l1ll11_opy_ (u"ࠫࡇ࡛ࡉࡍࡆࡢࡆ࡚ࡏࡌࡅࡋࡇࠫᩄ"))),
            bstack1l1ll11_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᩅ"): env.get(bstack1l1ll11_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤࡈࡕࡊࡎࡇࡍࡉࠨᩆ")),
            bstack1l1ll11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᩇ"): env.get(bstack1l1ll11_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡃࡗࡌࡐࡉࡏࡄࠣᩈ"))
        }
    if any([env.get(bstack1l1ll11_opy_ (u"ࠤࡆࡓࡉࡋࡂࡖࡋࡏࡈࡤࡈࡕࡊࡎࡇࡣࡎࡊࠢᩉ")), env.get(bstack1l1ll11_opy_ (u"ࠥࡇࡔࡊࡅࡃࡗࡌࡐࡉࡥࡒࡆࡕࡒࡐ࡛ࡋࡄࡠࡕࡒ࡙ࡗࡉࡅࡠࡘࡈࡖࡘࡏࡏࡏࠤᩊ")), env.get(bstack1l1ll11_opy_ (u"ࠦࡈࡕࡄࡆࡄࡘࡍࡑࡊ࡟ࡔࡑࡘࡖࡈࡋ࡟ࡗࡇࡕࡗࡎࡕࡎࠣᩋ"))]):
        return {
            bstack1l1ll11_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᩌ"): bstack1l1ll11_opy_ (u"ࠨࡁࡘࡕࠣࡇࡴࡪࡥࡃࡷ࡬ࡰࡩࠨᩍ"),
            bstack1l1ll11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᩎ"): env.get(bstack1l1ll11_opy_ (u"ࠣࡅࡒࡈࡊࡈࡕࡊࡎࡇࡣࡕ࡛ࡂࡍࡋࡆࡣࡇ࡛ࡉࡍࡆࡢ࡙ࡗࡒࠢᩏ")),
            bstack1l1ll11_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᩐ"): env.get(bstack1l1ll11_opy_ (u"ࠥࡇࡔࡊࡅࡃࡗࡌࡐࡉࡥࡂࡖࡋࡏࡈࡤࡏࡄࠣᩑ")),
            bstack1l1ll11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᩒ"): env.get(bstack1l1ll11_opy_ (u"ࠧࡉࡏࡅࡇࡅ࡙ࡎࡒࡄࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠥᩓ"))
        }
    if env.get(bstack1l1ll11_opy_ (u"ࠨࡢࡢ࡯ࡥࡳࡴࡥࡢࡶ࡫࡯ࡨࡓࡻ࡭ࡣࡧࡵࠦᩔ")):
        return {
            bstack1l1ll11_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᩕ"): bstack1l1ll11_opy_ (u"ࠣࡄࡤࡱࡧࡵ࡯ࠣᩖ"),
            bstack1l1ll11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᩗ"): env.get(bstack1l1ll11_opy_ (u"ࠥࡦࡦࡳࡢࡰࡱࡢࡦࡺ࡯࡬ࡥࡔࡨࡷࡺࡲࡴࡴࡗࡵࡰࠧᩘ")),
            bstack1l1ll11_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᩙ"): env.get(bstack1l1ll11_opy_ (u"ࠧࡨࡡ࡮ࡤࡲࡳࡤࡹࡨࡰࡴࡷࡎࡴࡨࡎࡢ࡯ࡨࠦᩚ")),
            bstack1l1ll11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᩛ"): env.get(bstack1l1ll11_opy_ (u"ࠢࡣࡣࡰࡦࡴࡵ࡟ࡣࡷ࡬ࡰࡩࡔࡵ࡮ࡤࡨࡶࠧᩜ"))
        }
    if env.get(bstack1l1ll11_opy_ (u"࡙ࠣࡈࡖࡈࡑࡅࡓࠤᩝ")) or env.get(bstack1l1ll11_opy_ (u"ࠤ࡚ࡉࡗࡉࡋࡆࡔࡢࡑࡆࡏࡎࡠࡒࡌࡔࡊࡒࡉࡏࡇࡢࡗ࡙ࡇࡒࡕࡇࡇࠦᩞ")):
        return {
            bstack1l1ll11_opy_ (u"ࠥࡲࡦࡳࡥࠣ᩟"): bstack1l1ll11_opy_ (u"ࠦ࡜࡫ࡲࡤ࡭ࡨࡶ᩠ࠧ"),
            bstack1l1ll11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᩡ"): env.get(bstack1l1ll11_opy_ (u"ࠨࡗࡆࡔࡆࡏࡊࡘ࡟ࡃࡗࡌࡐࡉࡥࡕࡓࡎࠥᩢ")),
            bstack1l1ll11_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᩣ"): bstack1l1ll11_opy_ (u"ࠣࡏࡤ࡭ࡳࠦࡐࡪࡲࡨࡰ࡮ࡴࡥࠣᩤ") if env.get(bstack1l1ll11_opy_ (u"ࠤ࡚ࡉࡗࡉࡋࡆࡔࡢࡑࡆࡏࡎࡠࡒࡌࡔࡊࡒࡉࡏࡇࡢࡗ࡙ࡇࡒࡕࡇࡇࠦᩥ")) else None,
            bstack1l1ll11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᩦ"): env.get(bstack1l1ll11_opy_ (u"ࠦ࡜ࡋࡒࡄࡍࡈࡖࡤࡍࡉࡕࡡࡆࡓࡒࡓࡉࡕࠤᩧ"))
        }
    if any([env.get(bstack1l1ll11_opy_ (u"ࠧࡍࡃࡑࡡࡓࡖࡔࡐࡅࡄࡖࠥᩨ")), env.get(bstack1l1ll11_opy_ (u"ࠨࡇࡄࡎࡒ࡙ࡉࡥࡐࡓࡑࡍࡉࡈ࡚ࠢᩩ")), env.get(bstack1l1ll11_opy_ (u"ࠢࡈࡑࡒࡋࡑࡋ࡟ࡄࡎࡒ࡙ࡉࡥࡐࡓࡑࡍࡉࡈ࡚ࠢᩪ"))]):
        return {
            bstack1l1ll11_opy_ (u"ࠣࡰࡤࡱࡪࠨᩫ"): bstack1l1ll11_opy_ (u"ࠤࡊࡳࡴ࡭࡬ࡦࠢࡆࡰࡴࡻࡤࠣᩬ"),
            bstack1l1ll11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᩭ"): None,
            bstack1l1ll11_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᩮ"): env.get(bstack1l1ll11_opy_ (u"ࠧࡖࡒࡐࡌࡈࡇ࡙ࡥࡉࡅࠤᩯ")),
            bstack1l1ll11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᩰ"): env.get(bstack1l1ll11_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡉࡅࠤᩱ"))
        }
    if env.get(bstack1l1ll11_opy_ (u"ࠣࡕࡋࡍࡕࡖࡁࡃࡎࡈࠦᩲ")):
        return {
            bstack1l1ll11_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᩳ"): bstack1l1ll11_opy_ (u"ࠥࡗ࡭࡯ࡰࡱࡣࡥࡰࡪࠨᩴ"),
            bstack1l1ll11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢ᩵"): env.get(bstack1l1ll11_opy_ (u"࡙ࠧࡈࡊࡒࡓࡅࡇࡒࡅࡠࡄࡘࡍࡑࡊ࡟ࡖࡔࡏࠦ᩶")),
            bstack1l1ll11_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣ᩷"): bstack1l1ll11_opy_ (u"ࠢࡋࡱࡥࠤࠨࢁࡽࠣ᩸").format(env.get(bstack1l1ll11_opy_ (u"ࠨࡕࡋࡍࡕࡖࡁࡃࡎࡈࡣࡏࡕࡂࡠࡋࡇࠫ᩹"))) if env.get(bstack1l1ll11_opy_ (u"ࠤࡖࡌࡎࡖࡐࡂࡄࡏࡉࡤࡐࡏࡃࡡࡌࡈࠧ᩺")) else None,
            bstack1l1ll11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ᩻"): env.get(bstack1l1ll11_opy_ (u"ࠦࡘࡎࡉࡑࡒࡄࡆࡑࡋ࡟ࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࠨ᩼"))
        }
    if bstack11111ll1l_opy_(env.get(bstack1l1ll11_opy_ (u"ࠧࡔࡅࡕࡎࡌࡊ࡞ࠨ᩽"))):
        return {
            bstack1l1ll11_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ᩾"): bstack1l1ll11_opy_ (u"ࠢࡏࡧࡷࡰ࡮࡬ࡹ᩿ࠣ"),
            bstack1l1ll11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦ᪀"): env.get(bstack1l1ll11_opy_ (u"ࠤࡇࡉࡕࡒࡏ࡚ࡡࡘࡖࡑࠨ᪁")),
            bstack1l1ll11_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧ᪂"): env.get(bstack1l1ll11_opy_ (u"ࠦࡘࡏࡔࡆࡡࡑࡅࡒࡋࠢ᪃")),
            bstack1l1ll11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ᪄"): env.get(bstack1l1ll11_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤࡏࡄࠣ᪅"))
        }
    if bstack11111ll1l_opy_(env.get(bstack1l1ll11_opy_ (u"ࠢࡈࡋࡗࡌ࡚ࡈ࡟ࡂࡅࡗࡍࡔࡔࡓࠣ᪆"))):
        return {
            bstack1l1ll11_opy_ (u"ࠣࡰࡤࡱࡪࠨ᪇"): bstack1l1ll11_opy_ (u"ࠤࡊ࡭ࡹࡎࡵࡣࠢࡄࡧࡹ࡯࡯࡯ࡵࠥ᪈"),
            bstack1l1ll11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨ᪉"): bstack1l1ll11_opy_ (u"ࠦࢀࢃ࠯ࡼࡿ࠲ࡥࡨࡺࡩࡰࡰࡶ࠳ࡷࡻ࡮ࡴ࠱ࡾࢁࠧ᪊").format(env.get(bstack1l1ll11_opy_ (u"ࠬࡍࡉࡕࡊࡘࡆࡤ࡙ࡅࡓࡘࡈࡖࡤ࡛ࡒࡍࠩ᪋")), env.get(bstack1l1ll11_opy_ (u"࠭ࡇࡊࡖࡋ࡙ࡇࡥࡒࡆࡒࡒࡗࡎ࡚ࡏࡓ࡛ࠪ᪌")), env.get(bstack1l1ll11_opy_ (u"ࠧࡈࡋࡗࡌ࡚ࡈ࡟ࡓࡗࡑࡣࡎࡊࠧ᪍"))),
            bstack1l1ll11_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥ᪎"): env.get(bstack1l1ll11_opy_ (u"ࠤࡊࡍ࡙ࡎࡕࡃࡡ࡚ࡓࡗࡑࡆࡍࡑ࡚ࠦ᪏")),
            bstack1l1ll11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ᪐"): env.get(bstack1l1ll11_opy_ (u"ࠦࡌࡏࡔࡉࡗࡅࡣࡗ࡛ࡎࡠࡋࡇࠦ᪑"))
        }
    if env.get(bstack1l1ll11_opy_ (u"ࠧࡉࡉࠣ᪒")) == bstack1l1ll11_opy_ (u"ࠨࡴࡳࡷࡨࠦ᪓") and env.get(bstack1l1ll11_opy_ (u"ࠢࡗࡇࡕࡇࡊࡒࠢ᪔")) == bstack1l1ll11_opy_ (u"ࠣ࠳ࠥ᪕"):
        return {
            bstack1l1ll11_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ᪖"): bstack1l1ll11_opy_ (u"࡚ࠥࡪࡸࡣࡦ࡮ࠥ᪗"),
            bstack1l1ll11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢ᪘"): bstack1l1ll11_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽࠳࠴ࢁࡽࠣ᪙").format(env.get(bstack1l1ll11_opy_ (u"࠭ࡖࡆࡔࡆࡉࡑࡥࡕࡓࡎࠪ᪚"))),
            bstack1l1ll11_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤ᪛"): None,
            bstack1l1ll11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢ᪜"): None,
        }
    if env.get(bstack1l1ll11_opy_ (u"ࠤࡗࡉࡆࡓࡃࡊࡖ࡜ࡣ࡛ࡋࡒࡔࡋࡒࡒࠧ᪝")):
        return {
            bstack1l1ll11_opy_ (u"ࠥࡲࡦࡳࡥࠣ᪞"): bstack1l1ll11_opy_ (u"࡙ࠦ࡫ࡡ࡮ࡥ࡬ࡸࡾࠨ᪟"),
            bstack1l1ll11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣ᪠"): None,
            bstack1l1ll11_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣ᪡"): env.get(bstack1l1ll11_opy_ (u"ࠢࡕࡇࡄࡑࡈࡏࡔ࡚ࡡࡓࡖࡔࡐࡅࡄࡖࡢࡒࡆࡓࡅࠣ᪢")),
            bstack1l1ll11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢ᪣"): env.get(bstack1l1ll11_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࠣ᪤"))
        }
    if any([env.get(bstack1l1ll11_opy_ (u"ࠥࡇࡔࡔࡃࡐࡗࡕࡗࡊࠨ᪥")), env.get(bstack1l1ll11_opy_ (u"ࠦࡈࡕࡎࡄࡑࡘࡖࡘࡋ࡟ࡖࡔࡏࠦ᪦")), env.get(bstack1l1ll11_opy_ (u"ࠧࡉࡏࡏࡅࡒ࡙ࡗ࡙ࡅࡠࡗࡖࡉࡗࡔࡁࡎࡇࠥᪧ")), env.get(bstack1l1ll11_opy_ (u"ࠨࡃࡐࡐࡆࡓ࡚ࡘࡓࡆࡡࡗࡉࡆࡓࠢ᪨"))]):
        return {
            bstack1l1ll11_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ᪩"): bstack1l1ll11_opy_ (u"ࠣࡅࡲࡲࡨࡵࡵࡳࡵࡨࠦ᪪"),
            bstack1l1ll11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧ᪫"): None,
            bstack1l1ll11_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧ᪬"): env.get(bstack1l1ll11_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡎࡔࡈ࡟ࡏࡃࡐࡉࠧ᪭")) or None,
            bstack1l1ll11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ᪮"): env.get(bstack1l1ll11_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤࡏࡄࠣ᪯"), 0)
        }
    if env.get(bstack1l1ll11_opy_ (u"ࠢࡈࡑࡢࡎࡔࡈ࡟ࡏࡃࡐࡉࠧ᪰")):
        return {
            bstack1l1ll11_opy_ (u"ࠣࡰࡤࡱࡪࠨ᪱"): bstack1l1ll11_opy_ (u"ࠤࡊࡳࡈࡊࠢ᪲"),
            bstack1l1ll11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨ᪳"): None,
            bstack1l1ll11_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨ᪴"): env.get(bstack1l1ll11_opy_ (u"ࠧࡍࡏࡠࡌࡒࡆࡤࡔࡁࡎࡇ᪵ࠥ")),
            bstack1l1ll11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶ᪶ࠧ"): env.get(bstack1l1ll11_opy_ (u"ࠢࡈࡑࡢࡔࡎࡖࡅࡍࡋࡑࡉࡤࡉࡏࡖࡐࡗࡉࡗࠨ᪷"))
        }
    if env.get(bstack1l1ll11_opy_ (u"ࠣࡅࡉࡣࡇ࡛ࡉࡍࡆࡢࡍࡉࠨ᪸")):
        return {
            bstack1l1ll11_opy_ (u"ࠤࡱࡥࡲ࡫᪹ࠢ"): bstack1l1ll11_opy_ (u"ࠥࡇࡴࡪࡥࡇࡴࡨࡷ࡭ࠨ᪺"),
            bstack1l1ll11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢ᪻"): env.get(bstack1l1ll11_opy_ (u"ࠧࡉࡆࡠࡄࡘࡍࡑࡊ࡟ࡖࡔࡏࠦ᪼")),
            bstack1l1ll11_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥ᪽ࠣ"): env.get(bstack1l1ll11_opy_ (u"ࠢࡄࡈࡢࡔࡎࡖࡅࡍࡋࡑࡉࡤࡔࡁࡎࡇࠥ᪾")),
            bstack1l1ll11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸᪿࠢ"): env.get(bstack1l1ll11_opy_ (u"ࠤࡆࡊࡤࡈࡕࡊࡎࡇࡣࡎࡊᫀࠢ"))
        }
    return {bstack1l1ll11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ᫁"): None}
def get_host_info():
    return {
        bstack1l1ll11_opy_ (u"ࠦ࡭ࡵࡳࡵࡰࡤࡱࡪࠨ᫂"): platform.node(),
        bstack1l1ll11_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳ᫃ࠢ"): platform.system(),
        bstack1l1ll11_opy_ (u"ࠨࡴࡺࡲࡨ᫄ࠦ"): platform.machine(),
        bstack1l1ll11_opy_ (u"ࠢࡷࡧࡵࡷ࡮ࡵ࡮ࠣ᫅"): platform.version(),
        bstack1l1ll11_opy_ (u"ࠣࡣࡵࡧ࡭ࠨ᫆"): platform.architecture()[0]
    }
def bstack1l1l1lll11_opy_():
    try:
        import selenium
        return True
    except ImportError:
        return False
def bstack11l1lllll11_opy_():
    if bstack11llllllll_opy_.get_property(bstack1l1ll11_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡶࡩࡸࡹࡩࡰࡰࠪ᫇")):
        return bstack1l1ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩ᫈")
    return bstack1l1ll11_opy_ (u"ࠫࡺࡴ࡫࡯ࡱࡺࡲࡤ࡭ࡲࡪࡦࠪ᫉")
def bstack11l1l1l1ll1_opy_(driver):
    info = {
        bstack1l1ll11_opy_ (u"ࠬࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶ᫊ࠫ"): driver.capabilities,
        bstack1l1ll11_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡪࡦࠪ᫋"): driver.session_id,
        bstack1l1ll11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࠨᫌ"): driver.capabilities.get(bstack1l1ll11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ᫍ"), None),
        bstack1l1ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡢࡺࡪࡸࡳࡪࡱࡱࠫᫎ"): driver.capabilities.get(bstack1l1ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫ᫏"), None),
        bstack1l1ll11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲ࠭᫐"): driver.capabilities.get(bstack1l1ll11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡎࡢ࡯ࡨࠫ᫑"), None),
        bstack1l1ll11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ᫒"):driver.capabilities.get(bstack1l1ll11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩ᫓"), None),
    }
    if bstack11l1lllll11_opy_() == bstack1l1ll11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧ᫔"):
        if bstack1l1111ll_opy_():
            info[bstack1l1ll11_opy_ (u"ࠩࡳࡶࡴࡪࡵࡤࡶࠪ᫕")] = bstack1l1ll11_opy_ (u"ࠪࡥࡵࡶ࠭ࡢࡷࡷࡳࡲࡧࡴࡦࠩ᫖")
        elif driver.capabilities.get(bstack1l1ll11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬ᫗"), {}).get(bstack1l1ll11_opy_ (u"ࠬࡺࡵࡳࡤࡲࡷࡨࡧ࡬ࡦࠩ᫘"), False):
            info[bstack1l1ll11_opy_ (u"࠭ࡰࡳࡱࡧࡹࡨࡺࠧ᫙")] = bstack1l1ll11_opy_ (u"ࠧࡵࡷࡵࡦࡴࡹࡣࡢ࡮ࡨࠫ᫚")
        else:
            info[bstack1l1ll11_opy_ (u"ࠨࡲࡵࡳࡩࡻࡣࡵࠩ᫛")] = bstack1l1ll11_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶࡨࠫ᫜")
    return info
def bstack1l1111ll_opy_():
    if bstack11llllllll_opy_.get_property(bstack1l1ll11_opy_ (u"ࠪࡥࡵࡶ࡟ࡢࡷࡷࡳࡲࡧࡴࡦࠩ᫝")):
        return True
    if bstack11111ll1l_opy_(os.environ.get(bstack1l1ll11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡍࡘࡥࡁࡑࡒࡢࡅ࡚࡚ࡏࡎࡃࡗࡉࠬ᫞"), None)):
        return True
    return False
def bstack1l1ll11lll_opy_(bstack11l1l1ll11l_opy_, url, data, config):
    headers = config.get(bstack1l1ll11_opy_ (u"ࠬ࡮ࡥࡢࡦࡨࡶࡸ࠭᫟"), None)
    proxies = bstack1l1lll11l1_opy_(config, url)
    auth = config.get(bstack1l1ll11_opy_ (u"࠭ࡡࡶࡶ࡫ࠫ᫠"), None)
    response = requests.request(
            bstack11l1l1ll11l_opy_,
            url=url,
            headers=headers,
            auth=auth,
            json=data,
            proxies=proxies
        )
    return response
def bstack11lll1l11_opy_(bstack1ll11111ll_opy_, size):
    bstack1ll1l1ll1l_opy_ = []
    while len(bstack1ll11111ll_opy_) > size:
        bstack11l11ll1ll_opy_ = bstack1ll11111ll_opy_[:size]
        bstack1ll1l1ll1l_opy_.append(bstack11l11ll1ll_opy_)
        bstack1ll11111ll_opy_ = bstack1ll11111ll_opy_[size:]
    bstack1ll1l1ll1l_opy_.append(bstack1ll11111ll_opy_)
    return bstack1ll1l1ll1l_opy_
def bstack11l1lllll1l_opy_(message, bstack11l1ll111l1_opy_=False):
    os.write(1, bytes(message, bstack1l1ll11_opy_ (u"ࠧࡶࡶࡩ࠱࠽࠭᫡")))
    os.write(1, bytes(bstack1l1ll11_opy_ (u"ࠨ࡞ࡱࠫ᫢"), bstack1l1ll11_opy_ (u"ࠩࡸࡸ࡫࠳࠸ࠨ᫣")))
    if bstack11l1ll111l1_opy_:
        with open(bstack1l1ll11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠰ࡳ࠶࠷ࡹ࠮ࠩ᫤") + os.environ[bstack1l1ll11_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡄࡘࡍࡑࡊ࡟ࡉࡃࡖࡌࡊࡊ࡟ࡊࡆࠪ᫥")] + bstack1l1ll11_opy_ (u"ࠬ࠴࡬ࡰࡩࠪ᫦"), bstack1l1ll11_opy_ (u"࠭ࡡࠨ᫧")) as f:
            f.write(message + bstack1l1ll11_opy_ (u"ࠧ࡝ࡰࠪ᫨"))
def bstack1ll11111111_opy_():
    return os.environ[bstack1l1ll11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡗࡗࡓࡒࡇࡔࡊࡑࡑࠫ᫩")].lower() == bstack1l1ll11_opy_ (u"ࠩࡷࡶࡺ࡫ࠧ᫪")
def bstack11l1lll1l_opy_(bstack11l1l111l1l_opy_):
    return bstack1l1ll11_opy_ (u"ࠪࡿࢂ࠵ࡻࡾࠩ᫫").format(bstack11ll1l1l111_opy_, bstack11l1l111l1l_opy_)
def bstack1l11111ll_opy_():
    return bstack111l11l11l_opy_().replace(tzinfo=None).isoformat() + bstack1l1ll11_opy_ (u"ࠫ࡟࠭᫬")
def bstack11l1l111ll1_opy_(start, finish):
    return (datetime.datetime.fromisoformat(finish.rstrip(bstack1l1ll11_opy_ (u"ࠬࡠࠧ᫭"))) - datetime.datetime.fromisoformat(start.rstrip(bstack1l1ll11_opy_ (u"࡚࠭ࠨ᫮")))).total_seconds() * 1000
def bstack11ll11llll1_opy_(timestamp):
    return bstack11ll11111ll_opy_(timestamp).isoformat() + bstack1l1ll11_opy_ (u"࡛ࠧࠩ᫯")
def bstack11l1l1l11ll_opy_(bstack11l1ll1l1ll_opy_):
    date_format = bstack1l1ll11_opy_ (u"ࠨࠧ࡜ࠩࡲࠫࡤࠡࠧࡋ࠾ࠪࡓ࠺ࠦࡕ࠱ࠩ࡫࠭᫰")
    bstack11ll11l1ll1_opy_ = datetime.datetime.strptime(bstack11l1ll1l1ll_opy_, date_format)
    return bstack11ll11l1ll1_opy_.isoformat() + bstack1l1ll11_opy_ (u"ࠩ࡝ࠫ᫱")
def bstack11l1l1111l1_opy_(outcome):
    _, exception, _ = outcome.excinfo or (None, None, None)
    if exception:
        return bstack1l1ll11_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ᫲")
    else:
        return bstack1l1ll11_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫ᫳")
def bstack11111ll1l_opy_(val):
    if val is None:
        return False
    return val.__str__().lower() == bstack1l1ll11_opy_ (u"ࠬࡺࡲࡶࡧࠪ᫴")
def bstack11l1l11llll_opy_(val):
    return val.__str__().lower() == bstack1l1ll11_opy_ (u"࠭ࡦࡢ࡮ࡶࡩࠬ᫵")
def bstack111l11ll1l_opy_(bstack11l1lll1ll1_opy_=Exception, class_method=False, default_value=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except bstack11l1lll1ll1_opy_ as e:
                print(bstack1l1ll11_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠡࡽࢀࠤ࠲ࡄࠠࡼࡿ࠽ࠤࢀࢃࠢ᫶").format(func.__name__, bstack11l1lll1ll1_opy_.__name__, str(e)))
                return default_value
        return wrapper
    def bstack11l1ll11ll1_opy_(bstack11l1ll1l111_opy_):
        def wrapped(cls, *args, **kwargs):
            try:
                return bstack11l1ll1l111_opy_(cls, *args, **kwargs)
            except bstack11l1lll1ll1_opy_ as e:
                print(bstack1l1ll11_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡧࡷࡱࡧࡹ࡯࡯࡯ࠢࡾࢁࠥ࠳࠾ࠡࡽࢀ࠾ࠥࢁࡽࠣ᫷").format(bstack11l1ll1l111_opy_.__name__, bstack11l1lll1ll1_opy_.__name__, str(e)))
                return default_value
        return wrapped
    if class_method:
        return bstack11l1ll11ll1_opy_
    else:
        return decorator
def bstack11l1l1l1_opy_(bstack111l11111l_opy_):
    if os.getenv(bstack1l1ll11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡘࡘࡔࡓࡁࡕࡋࡒࡒࠬ᫸")) is not None:
        return bstack11111ll1l_opy_(os.getenv(bstack1l1ll11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄ࡙࡙ࡕࡍࡂࡖࡌࡓࡓ࠭᫹")))
    if bstack1l1ll11_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨ᫺") in bstack111l11111l_opy_ and bstack11l1l11llll_opy_(bstack111l11111l_opy_[bstack1l1ll11_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩ᫻")]):
        return False
    if bstack1l1ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨ᫼") in bstack111l11111l_opy_ and bstack11l1l11llll_opy_(bstack111l11111l_opy_[bstack1l1ll11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩ᫽")]):
        return False
    return True
def bstack1lll111ll_opy_():
    try:
        from pytest_bdd import reporting
        bstack11l11llll1l_opy_ = os.environ.get(bstack1l1ll11_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡖࡕࡈࡖࡤࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࠣ᫾"), None)
        return bstack11l11llll1l_opy_ is None or bstack11l11llll1l_opy_ == bstack1l1ll11_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠨ᫿")
    except Exception as e:
        return False
def bstack11l1lll11_opy_(hub_url, CONFIG):
    if bstack1l1llll1l_opy_() <= version.parse(bstack1l1ll11_opy_ (u"ࠪ࠷࠳࠷࠳࠯࠲ࠪᬀ")):
        if hub_url:
            return bstack1l1ll11_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳ࠧᬁ") + hub_url + bstack1l1ll11_opy_ (u"ࠧࡀ࠸࠱࠱ࡺࡨ࠴࡮ࡵࡣࠤᬂ")
        return bstack1ll11l11ll_opy_
    if hub_url:
        return bstack1l1ll11_opy_ (u"ࠨࡨࡵࡶࡳࡷ࠿࠵࠯ࠣᬃ") + hub_url + bstack1l1ll11_opy_ (u"ࠢ࠰ࡹࡧ࠳࡭ࡻࡢࠣᬄ")
    return bstack11l1ll1l11_opy_
def bstack11l1l11ll11_opy_():
    return isinstance(os.getenv(bstack1l1ll11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑ࡛ࡗࡉࡘ࡚࡟ࡑࡎࡘࡋࡎࡔࠧᬅ")), str)
def bstack11111111l_opy_(url):
    return urlparse(url).hostname
def bstack1llllllll_opy_(hostname):
    for bstack111lll111_opy_ in bstack1l1llll1l1_opy_:
        regex = re.compile(bstack111lll111_opy_)
        if regex.match(hostname):
            return True
    return False
def bstack11ll11lll1l_opy_(bstack11ll11l1l1l_opy_, file_name, logger):
    bstack1ll1l111ll_opy_ = os.path.join(os.path.expanduser(bstack1l1ll11_opy_ (u"ࠩࢁࠫᬆ")), bstack11ll11l1l1l_opy_)
    try:
        if not os.path.exists(bstack1ll1l111ll_opy_):
            os.makedirs(bstack1ll1l111ll_opy_)
        file_path = os.path.join(os.path.expanduser(bstack1l1ll11_opy_ (u"ࠪࢂࠬᬇ")), bstack11ll11l1l1l_opy_, file_name)
        if not os.path.isfile(file_path):
            with open(file_path, bstack1l1ll11_opy_ (u"ࠫࡼ࠭ᬈ")):
                pass
            with open(file_path, bstack1l1ll11_opy_ (u"ࠧࡽࠫࠣᬉ")) as outfile:
                json.dump({}, outfile)
        return file_path
    except Exception as e:
        logger.debug(bstack11l1ll1l_opy_.format(str(e)))
def bstack11l1l1l1111_opy_(file_name, key, value, logger):
    file_path = bstack11ll11lll1l_opy_(bstack1l1ll11_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ᬊ"), file_name, logger)
    if file_path != None:
        if os.path.exists(file_path):
            bstack1l11llll_opy_ = json.load(open(file_path, bstack1l1ll11_opy_ (u"ࠧࡳࡤࠪᬋ")))
        else:
            bstack1l11llll_opy_ = {}
        bstack1l11llll_opy_[key] = value
        with open(file_path, bstack1l1ll11_opy_ (u"ࠣࡹ࠮ࠦᬌ")) as outfile:
            json.dump(bstack1l11llll_opy_, outfile)
def bstack11l11l1ll_opy_(file_name, logger):
    file_path = bstack11ll11lll1l_opy_(bstack1l1ll11_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩᬍ"), file_name, logger)
    bstack1l11llll_opy_ = {}
    if file_path != None and os.path.exists(file_path):
        with open(file_path, bstack1l1ll11_opy_ (u"ࠪࡶࠬᬎ")) as bstack1ll1ll11l1_opy_:
            bstack1l11llll_opy_ = json.load(bstack1ll1ll11l1_opy_)
    return bstack1l11llll_opy_
def bstack1l11llllll_opy_(file_path, logger):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        logger.debug(bstack1l1ll11_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡤࡦ࡮ࡨࡸ࡮ࡴࡧࠡࡨ࡬ࡰࡪࡀࠠࠨᬏ") + file_path + bstack1l1ll11_opy_ (u"ࠬࠦࠧᬐ") + str(e))
def bstack1l1llll1l_opy_():
    from selenium import webdriver
    return version.parse(webdriver.__version__)
class Notset:
    def __repr__(self):
        return bstack1l1ll11_opy_ (u"ࠨ࠼ࡏࡑࡗࡗࡊ࡚࠾ࠣᬑ")
def bstack1ll1l11ll_opy_(config):
    if bstack1l1ll11_opy_ (u"ࠧࡪࡵࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠭ᬒ") in config:
        del (config[bstack1l1ll11_opy_ (u"ࠨ࡫ࡶࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠧᬓ")])
        return False
    if bstack1l1llll1l_opy_() < version.parse(bstack1l1ll11_opy_ (u"ࠩ࠶࠲࠹࠴࠰ࠨᬔ")):
        return False
    if bstack1l1llll1l_opy_() >= version.parse(bstack1l1ll11_opy_ (u"ࠪ࠸࠳࠷࠮࠶ࠩᬕ")):
        return True
    if bstack1l1ll11_opy_ (u"ࠫࡺࡹࡥࡘ࠵ࡆࠫᬖ") in config and config[bstack1l1ll11_opy_ (u"ࠬࡻࡳࡦ࡙࠶ࡇࠬᬗ")] is False:
        return False
    else:
        return True
def bstack1lll1l1l1l_opy_(args_list, bstack11l1llllll1_opy_):
    index = -1
    for value in bstack11l1llllll1_opy_:
        try:
            index = args_list.index(value)
            return index
        except Exception as e:
            return index
    return index
class Result:
    def __init__(self, result=None, duration=None, exception=None, bstack11l11111l1_opy_=None):
        self.result = result
        self.duration = duration
        self.exception = exception
        self.exception_type = type(self.exception).__name__ if exception else None
        self.bstack11l11111l1_opy_ = bstack11l11111l1_opy_
    @classmethod
    def passed(cls):
        return Result(result=bstack1l1ll11_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ᬘ"))
    @classmethod
    def failed(cls, exception=None):
        return Result(result=bstack1l1ll11_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧᬙ"), exception=exception)
    def bstack1111ll111l_opy_(self):
        if self.result != bstack1l1ll11_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨᬚ"):
            return None
        if isinstance(self.exception_type, str) and bstack1l1ll11_opy_ (u"ࠤࡄࡷࡸ࡫ࡲࡵ࡫ࡲࡲࠧᬛ") in self.exception_type:
            return bstack1l1ll11_opy_ (u"ࠥࡅࡸࡹࡥࡳࡶ࡬ࡳࡳࡋࡲࡳࡱࡵࠦᬜ")
        return bstack1l1ll11_opy_ (u"࡚ࠦࡴࡨࡢࡰࡧࡰࡪࡪࡅࡳࡴࡲࡶࠧᬝ")
    def bstack11l1l111lll_opy_(self):
        if self.result != bstack1l1ll11_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᬞ"):
            return None
        if self.bstack11l11111l1_opy_:
            return self.bstack11l11111l1_opy_
        return bstack11l11llll11_opy_(self.exception)
def bstack11l11llll11_opy_(exc):
    return [traceback.format_exception(exc)]
def bstack11ll1111l11_opy_(message):
    if isinstance(message, str):
        return not bool(message and message.strip())
    return True
def bstack1lllll11_opy_(object, key, default_value):
    if not object or not object.__dict__:
        return default_value
    if key in object.__dict__.keys():
        return object.__dict__.get(key)
    return default_value
def bstack1ll1ll11ll_opy_(config, logger):
    try:
        import playwright
        bstack11l1l1l111l_opy_ = playwright.__file__
        bstack11ll111ll11_opy_ = os.path.split(bstack11l1l1l111l_opy_)
        bstack11l1ll111ll_opy_ = bstack11ll111ll11_opy_[0] + bstack1l1ll11_opy_ (u"࠭࠯ࡥࡴ࡬ࡺࡪࡸ࠯ࡱࡣࡦ࡯ࡦ࡭ࡥ࠰࡮࡬ࡦ࠴ࡩ࡬ࡪ࠱ࡦࡰ࡮࠴ࡪࡴࠩᬟ")
        os.environ[bstack1l1ll11_opy_ (u"ࠧࡈࡎࡒࡆࡆࡒ࡟ࡂࡉࡈࡒ࡙ࡥࡈࡕࡖࡓࡣࡕࡘࡏ࡙࡛ࠪᬠ")] = bstack1lll1l1l_opy_(config)
        with open(bstack11l1ll111ll_opy_, bstack1l1ll11_opy_ (u"ࠨࡴࠪᬡ")) as f:
            bstack11ll11ll1_opy_ = f.read()
            bstack11l1ll1l1l1_opy_ = bstack1l1ll11_opy_ (u"ࠩࡪࡰࡴࡨࡡ࡭࠯ࡤ࡫ࡪࡴࡴࠨᬢ")
            bstack11l1ll1lll1_opy_ = bstack11ll11ll1_opy_.find(bstack11l1ll1l1l1_opy_)
            if bstack11l1ll1lll1_opy_ == -1:
              process = subprocess.Popen(bstack1l1ll11_opy_ (u"ࠥࡲࡵࡳࠠࡪࡰࡶࡸࡦࡲ࡬ࠡࡩ࡯ࡳࡧࡧ࡬࠮ࡣࡪࡩࡳࡺࠢᬣ"), shell=True, cwd=bstack11ll111ll11_opy_[0])
              process.wait()
              bstack11l1l1ll1ll_opy_ = bstack1l1ll11_opy_ (u"ࠫࠧࡻࡳࡦࠢࡶࡸࡷ࡯ࡣࡵࠤ࠾ࠫᬤ")
              bstack11l1ll11lll_opy_ = bstack1l1ll11_opy_ (u"ࠧࠨࠢࠡ࡞ࠥࡹࡸ࡫ࠠࡴࡶࡵ࡭ࡨࡺ࡜ࠣ࠽ࠣࡧࡴࡴࡳࡵࠢࡾࠤࡧࡵ࡯ࡵࡵࡷࡶࡦࡶࠠࡾࠢࡀࠤࡷ࡫ࡱࡶ࡫ࡵࡩ࠭࠭ࡧ࡭ࡱࡥࡥࡱ࠳ࡡࡨࡧࡱࡸࠬ࠯࠻ࠡ࡫ࡩࠤ࠭ࡶࡲࡰࡥࡨࡷࡸ࠴ࡥ࡯ࡸ࠱ࡋࡑࡕࡂࡂࡎࡢࡅࡌࡋࡎࡕࡡࡋࡘ࡙ࡖ࡟ࡑࡔࡒ࡜࡞࠯ࠠࡣࡱࡲࡸࡸࡺࡲࡢࡲࠫ࠭ࡀࠦࠢࠣࠤᬥ")
              bstack11l1l1l1lll_opy_ = bstack11ll11ll1_opy_.replace(bstack11l1l1ll1ll_opy_, bstack11l1ll11lll_opy_)
              with open(bstack11l1ll111ll_opy_, bstack1l1ll11_opy_ (u"࠭ࡷࠨᬦ")) as f:
                f.write(bstack11l1l1l1lll_opy_)
    except Exception as e:
        logger.error(bstack1ll1l11lll_opy_.format(str(e)))
def bstack11l1ll11l1_opy_():
  try:
    bstack11l1lll111l_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1ll11_opy_ (u"ࠧࡰࡲࡷ࡭ࡲࡧ࡬ࡠࡪࡸࡦࡤࡻࡲ࡭࠰࡭ࡷࡴࡴࠧᬧ"))
    bstack11ll11l11l1_opy_ = []
    if os.path.exists(bstack11l1lll111l_opy_):
      with open(bstack11l1lll111l_opy_) as f:
        bstack11ll11l11l1_opy_ = json.load(f)
      os.remove(bstack11l1lll111l_opy_)
    return bstack11ll11l11l1_opy_
  except:
    pass
  return []
def bstack1l11111lll_opy_(bstack11ll1111ll_opy_):
  try:
    bstack11ll11l11l1_opy_ = []
    bstack11l1lll111l_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1ll11_opy_ (u"ࠨࡱࡳࡸ࡮ࡳࡡ࡭ࡡ࡫ࡹࡧࡥࡵࡳ࡮࠱࡮ࡸࡵ࡮ࠨᬨ"))
    if os.path.exists(bstack11l1lll111l_opy_):
      with open(bstack11l1lll111l_opy_) as f:
        bstack11ll11l11l1_opy_ = json.load(f)
    bstack11ll11l11l1_opy_.append(bstack11ll1111ll_opy_)
    with open(bstack11l1lll111l_opy_, bstack1l1ll11_opy_ (u"ࠩࡺࠫᬩ")) as f:
        json.dump(bstack11ll11l11l1_opy_, f)
  except:
    pass
def bstack1llll1111_opy_(logger, bstack11l1l11l1ll_opy_ = False):
  try:
    test_name = os.environ.get(bstack1l1ll11_opy_ (u"ࠪࡔ࡞࡚ࡅࡔࡖࡢࡘࡊ࡙ࡔࡠࡐࡄࡑࡊ࠭ᬪ"), bstack1l1ll11_opy_ (u"ࠫࠬᬫ"))
    if test_name == bstack1l1ll11_opy_ (u"ࠬ࠭ᬬ"):
        test_name = threading.current_thread().__dict__.get(bstack1l1ll11_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹࡈࡤࡥࡡࡷࡩࡸࡺ࡟࡯ࡣࡰࡩࠬᬭ"), bstack1l1ll11_opy_ (u"ࠧࠨᬮ"))
    bstack11ll11111l1_opy_ = bstack1l1ll11_opy_ (u"ࠨ࠮ࠣࠫᬯ").join(threading.current_thread().bstackTestErrorMessages)
    if bstack11l1l11l1ll_opy_:
        bstack11111l11l_opy_ = os.environ.get(bstack1l1ll11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩᬰ"), bstack1l1ll11_opy_ (u"ࠪ࠴ࠬᬱ"))
        bstack11llll1l1l_opy_ = {bstack1l1ll11_opy_ (u"ࠫࡳࡧ࡭ࡦࠩᬲ"): test_name, bstack1l1ll11_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫᬳ"): bstack11ll11111l1_opy_, bstack1l1ll11_opy_ (u"࠭ࡩ࡯ࡦࡨࡼ᬴ࠬ"): bstack11111l11l_opy_}
        bstack11ll11ll1l1_opy_ = []
        bstack11ll11lll11_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1ll11_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࡟ࡱࡲࡳࡣࡪࡸࡲࡰࡴࡢࡰ࡮ࡹࡴ࠯࡬ࡶࡳࡳ࠭ᬵ"))
        if os.path.exists(bstack11ll11lll11_opy_):
            with open(bstack11ll11lll11_opy_) as f:
                bstack11ll11ll1l1_opy_ = json.load(f)
        bstack11ll11ll1l1_opy_.append(bstack11llll1l1l_opy_)
        with open(bstack11ll11lll11_opy_, bstack1l1ll11_opy_ (u"ࠨࡹࠪᬶ")) as f:
            json.dump(bstack11ll11ll1l1_opy_, f)
    else:
        bstack11llll1l1l_opy_ = {bstack1l1ll11_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᬷ"): test_name, bstack1l1ll11_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩᬸ"): bstack11ll11111l1_opy_, bstack1l1ll11_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪᬹ"): str(multiprocessing.current_process().name)}
        if bstack1l1ll11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤ࡫ࡲࡳࡱࡵࡣࡱ࡯ࡳࡵࠩᬺ") not in multiprocessing.current_process().__dict__.keys():
            multiprocessing.current_process().bstack_error_list = []
        multiprocessing.current_process().bstack_error_list.append(bstack11llll1l1l_opy_)
  except Exception as e:
      logger.warn(bstack1l1ll11_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡶࡸࡴࡸࡥࠡࡲࡼࡸࡪࡹࡴࠡࡨࡸࡲࡳ࡫࡬ࠡࡦࡤࡸࡦࡀࠠࡼࡿࠥᬻ").format(e))
def bstack11111l111_opy_(error_message, test_name, index, logger):
  try:
    bstack11l1ll1111l_opy_ = []
    bstack11llll1l1l_opy_ = {bstack1l1ll11_opy_ (u"ࠧ࡯ࡣࡰࡩࠬᬼ"): test_name, bstack1l1ll11_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧᬽ"): error_message, bstack1l1ll11_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨᬾ"): index}
    bstack11l1l11111l_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1ll11_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࡡࡨࡶࡷࡵࡲࡠ࡮࡬ࡷࡹ࠴ࡪࡴࡱࡱࠫᬿ"))
    if os.path.exists(bstack11l1l11111l_opy_):
        with open(bstack11l1l11111l_opy_) as f:
            bstack11l1ll1111l_opy_ = json.load(f)
    bstack11l1ll1111l_opy_.append(bstack11llll1l1l_opy_)
    with open(bstack11l1l11111l_opy_, bstack1l1ll11_opy_ (u"ࠫࡼ࠭ᭀ")) as f:
        json.dump(bstack11l1ll1111l_opy_, f)
  except Exception as e:
    logger.warn(bstack1l1ll11_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡵࡷࡳࡷ࡫ࠠࡳࡱࡥࡳࡹࠦࡦࡶࡰࡱࡩࡱࠦࡤࡢࡶࡤ࠾ࠥࢁࡽࠣᭁ").format(e))
def bstack11ll1l1lll_opy_(bstack1lll11ll11_opy_, name, logger):
  try:
    bstack11llll1l1l_opy_ = {bstack1l1ll11_opy_ (u"࠭࡮ࡢ࡯ࡨࠫᭂ"): name, bstack1l1ll11_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ᭃ"): bstack1lll11ll11_opy_, bstack1l1ll11_opy_ (u"ࠨ࡫ࡱࡨࡪࡾ᭄ࠧ"): str(threading.current_thread()._name)}
    return bstack11llll1l1l_opy_
  except Exception as e:
    logger.warn(bstack1l1ll11_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡹࡴࡰࡴࡨࠤࡧ࡫ࡨࡢࡸࡨࠤ࡫ࡻ࡮࡯ࡧ࡯ࠤࡩࡧࡴࡢ࠼ࠣࡿࢂࠨᭅ").format(e))
  return
def bstack11l1l1l1l1l_opy_():
    return platform.system() == bstack1l1ll11_opy_ (u"࡛ࠪ࡮ࡴࡤࡰࡹࡶࠫᭆ")
def bstack11llll1l_opy_(bstack11l1l1ll1l1_opy_, config, logger):
    bstack11l1l1llll1_opy_ = {}
    try:
        return {key: config[key] for key in config if bstack11l1l1ll1l1_opy_.match(key)}
    except Exception as e:
        logger.debug(bstack1l1ll11_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡧ࡫࡯ࡸࡪࡸࠠࡤࡱࡱࡪ࡮࡭ࠠ࡬ࡧࡼࡷࠥࡨࡹࠡࡴࡨ࡫ࡪࡾࠠ࡮ࡣࡷࡧ࡭ࡀࠠࡼࡿࠥᭇ").format(e))
    return bstack11l1l1llll1_opy_
def bstack11ll1111l1l_opy_(bstack11l1l11lll1_opy_, bstack11ll11ll111_opy_):
    bstack11l1lllllll_opy_ = version.parse(bstack11l1l11lll1_opy_)
    bstack11l1lll1l11_opy_ = version.parse(bstack11ll11ll111_opy_)
    if bstack11l1lllllll_opy_ > bstack11l1lll1l11_opy_:
        return 1
    elif bstack11l1lllllll_opy_ < bstack11l1lll1l11_opy_:
        return -1
    else:
        return 0
def bstack111l11l11l_opy_():
    return datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
def bstack11ll11111ll_opy_(timestamp):
    return datetime.datetime.fromtimestamp(timestamp, datetime.timezone.utc).replace(tzinfo=None)
def bstack11l1ll1ll11_opy_(framework):
    from browserstack_sdk._version import __version__
    return str(framework) + str(__version__)
def bstack1l111ll111_opy_(options, framework, bstack1ll11ll11_opy_={}):
    if options is None:
        return
    if getattr(options, bstack1l1ll11_opy_ (u"ࠬ࡭ࡥࡵࠩᭈ"), None):
        caps = options
    else:
        caps = options.to_capabilities()
    bstack1lll1ll1l1_opy_ = caps.get(bstack1l1ll11_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧᭉ"))
    bstack11ll111l11l_opy_ = True
    bstack11lll1111l_opy_ = os.environ[bstack1l1ll11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬᭊ")]
    if bstack11l1l11llll_opy_(caps.get(bstack1l1ll11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡶࡵࡨ࡛࠸ࡉࠧᭋ"))) or bstack11l1l11llll_opy_(caps.get(bstack1l1ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡷࡶࡩࡤࡽ࠳ࡤࠩᭌ"))):
        bstack11ll111l11l_opy_ = False
    if bstack1ll1l11ll_opy_({bstack1l1ll11_opy_ (u"ࠥࡹࡸ࡫ࡗ࠴ࡅࠥ᭍"): bstack11ll111l11l_opy_}):
        bstack1lll1ll1l1_opy_ = bstack1lll1ll1l1_opy_ or {}
        bstack1lll1ll1l1_opy_[bstack1l1ll11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭᭎")] = bstack11l1ll1ll11_opy_(framework)
        bstack1lll1ll1l1_opy_[bstack1l1ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧ᭏")] = bstack1ll11111111_opy_()
        bstack1lll1ll1l1_opy_[bstack1l1ll11_opy_ (u"࠭ࡴࡦࡵࡷ࡬ࡺࡨࡂࡶ࡫࡯ࡨ࡚ࡻࡩࡥࠩ᭐")] = bstack11lll1111l_opy_
        bstack1lll1ll1l1_opy_[bstack1l1ll11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡖࡲࡰࡦࡸࡧࡹࡓࡡࡱࠩ᭑")] = bstack1ll11ll11_opy_
        if getattr(options, bstack1l1ll11_opy_ (u"ࠨࡵࡨࡸࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡺࠩ᭒"), None):
            options.set_capability(bstack1l1ll11_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪ᭓"), bstack1lll1ll1l1_opy_)
        else:
            options[bstack1l1ll11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫ᭔")] = bstack1lll1ll1l1_opy_
    else:
        if getattr(options, bstack1l1ll11_opy_ (u"ࠫࡸ࡫ࡴࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷࡽࠬ᭕"), None):
            options.set_capability(bstack1l1ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭᭖"), bstack11l1ll1ll11_opy_(framework))
            options.set_capability(bstack1l1ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧ᭗"), bstack1ll11111111_opy_())
            options.set_capability(bstack1l1ll11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡴࡦࡵࡷ࡬ࡺࡨࡂࡶ࡫࡯ࡨ࡚ࡻࡩࡥࠩ᭘"), bstack11lll1111l_opy_)
            options.set_capability(bstack1l1ll11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡷ࡬ࡰࡩࡖࡲࡰࡦࡸࡧࡹࡓࡡࡱࠩ᭙"), bstack1ll11ll11_opy_)
        else:
            options[bstack1l1ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪ᭚")] = bstack11l1ll1ll11_opy_(framework)
            options[bstack1l1ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫ᭛")] = bstack1ll11111111_opy_()
            options[bstack1l1ll11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡸࡪࡹࡴࡩࡷࡥࡆࡺ࡯࡬ࡥࡗࡸ࡭ࡩ࠭᭜")] = bstack11lll1111l_opy_
            options[bstack1l1ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡧࡻࡩ࡭ࡦࡓࡶࡴࡪࡵࡤࡶࡐࡥࡵ࠭᭝")] = bstack1ll11ll11_opy_
    return options
def bstack11ll11l1lll_opy_(bstack11l1l111l11_opy_, framework):
    bstack1ll11ll11_opy_ = bstack11llllllll_opy_.get_property(bstack1l1ll11_opy_ (u"ࠨࡐࡍࡃ࡜࡛ࡗࡏࡇࡉࡖࡢࡔࡗࡕࡄࡖࡅࡗࡣࡒࡇࡐࠣ᭞"))
    if bstack11l1l111l11_opy_ and len(bstack11l1l111l11_opy_.split(bstack1l1ll11_opy_ (u"ࠧࡤࡣࡳࡷࡂ࠭᭟"))) > 1:
        ws_url = bstack11l1l111l11_opy_.split(bstack1l1ll11_opy_ (u"ࠨࡥࡤࡴࡸࡃࠧ᭠"))[0]
        if bstack1l1ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱࠬ᭡") in ws_url:
            from browserstack_sdk._version import __version__
            bstack11l11lllll1_opy_ = json.loads(urllib.parse.unquote(bstack11l1l111l11_opy_.split(bstack1l1ll11_opy_ (u"ࠪࡧࡦࡶࡳ࠾ࠩ᭢"))[1]))
            bstack11l11lllll1_opy_ = bstack11l11lllll1_opy_ or {}
            bstack11lll1111l_opy_ = os.environ[bstack1l1ll11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩ᭣")]
            bstack11l11lllll1_opy_[bstack1l1ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭᭤")] = str(framework) + str(__version__)
            bstack11l11lllll1_opy_[bstack1l1ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧ᭥")] = bstack1ll11111111_opy_()
            bstack11l11lllll1_opy_[bstack1l1ll11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡴࡦࡵࡷ࡬ࡺࡨࡂࡶ࡫࡯ࡨ࡚ࡻࡩࡥࠩ᭦")] = bstack11lll1111l_opy_
            bstack11l11lllll1_opy_[bstack1l1ll11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡷ࡬ࡰࡩࡖࡲࡰࡦࡸࡧࡹࡓࡡࡱࠩ᭧")] = bstack1ll11ll11_opy_
            bstack11l1l111l11_opy_ = bstack11l1l111l11_opy_.split(bstack1l1ll11_opy_ (u"ࠩࡦࡥࡵࡹ࠽ࠨ᭨"))[0] + bstack1l1ll11_opy_ (u"ࠪࡧࡦࡶࡳ࠾ࠩ᭩") + urllib.parse.quote(json.dumps(bstack11l11lllll1_opy_))
    return bstack11l1l111l11_opy_
def bstack11ll1lll1l_opy_():
    global bstack1ll1ll111l_opy_
    from playwright._impl._browser_type import BrowserType
    bstack1ll1ll111l_opy_ = BrowserType.connect
    return bstack1ll1ll111l_opy_
def bstack11ll111l1_opy_(framework_name):
    global bstack1l1l1111l_opy_
    bstack1l1l1111l_opy_ = framework_name
    return framework_name
def bstack11l1l1ll_opy_(self, *args, **kwargs):
    global bstack1ll1ll111l_opy_
    try:
        global bstack1l1l1111l_opy_
        if bstack1l1ll11_opy_ (u"ࠫࡼࡹࡅ࡯ࡦࡳࡳ࡮ࡴࡴࠨ᭪") in kwargs:
            kwargs[bstack1l1ll11_opy_ (u"ࠬࡽࡳࡆࡰࡧࡴࡴ࡯࡮ࡵࠩ᭫")] = bstack11ll11l1lll_opy_(
                kwargs.get(bstack1l1ll11_opy_ (u"࠭ࡷࡴࡇࡱࡨࡵࡵࡩ࡯ࡶ᭬ࠪ"), None),
                bstack1l1l1111l_opy_
            )
    except Exception as e:
        logger.error(bstack1l1ll11_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩࡧࡱࠤࡵࡸ࡯ࡤࡧࡶࡷ࡮ࡴࡧࠡࡕࡇࡏࠥࡩࡡࡱࡵ࠽ࠤࢀࢃࠢ᭭").format(str(e)))
    return bstack1ll1ll111l_opy_(self, *args, **kwargs)
def bstack11ll11l11ll_opy_(bstack11ll111lll1_opy_, proxies):
    proxy_settings = {}
    try:
        if not proxies:
            proxies = bstack1l1lll11l1_opy_(bstack11ll111lll1_opy_, bstack1l1ll11_opy_ (u"ࠣࠤ᭮"))
        if proxies and proxies.get(bstack1l1ll11_opy_ (u"ࠤ࡫ࡸࡹࡶࡳࠣ᭯")):
            parsed_url = urlparse(proxies.get(bstack1l1ll11_opy_ (u"ࠥ࡬ࡹࡺࡰࡴࠤ᭰")))
            if parsed_url and parsed_url.hostname: proxy_settings[bstack1l1ll11_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡋࡳࡸࡺࠧ᭱")] = str(parsed_url.hostname)
            if parsed_url and parsed_url.port: proxy_settings[bstack1l1ll11_opy_ (u"ࠬࡶࡲࡰࡺࡼࡔࡴࡸࡴࠨ᭲")] = str(parsed_url.port)
            if parsed_url and parsed_url.username: proxy_settings[bstack1l1ll11_opy_ (u"࠭ࡰࡳࡱࡻࡽ࡚ࡹࡥࡳࠩ᭳")] = str(parsed_url.username)
            if parsed_url and parsed_url.password: proxy_settings[bstack1l1ll11_opy_ (u"ࠧࡱࡴࡲࡼࡾࡖࡡࡴࡵࠪ᭴")] = str(parsed_url.password)
        return proxy_settings
    except:
        return proxy_settings
def bstack1111l111_opy_(bstack11ll111lll1_opy_):
    bstack11l1l11l111_opy_ = {
        bstack11ll1lllll1_opy_[bstack11ll111111l_opy_]: bstack11ll111lll1_opy_[bstack11ll111111l_opy_]
        for bstack11ll111111l_opy_ in bstack11ll111lll1_opy_
        if bstack11ll111111l_opy_ in bstack11ll1lllll1_opy_
    }
    bstack11l1l11l111_opy_[bstack1l1ll11_opy_ (u"ࠣࡲࡵࡳࡽࡿࡓࡦࡶࡷ࡭ࡳ࡭ࡳࠣ᭵")] = bstack11ll11l11ll_opy_(bstack11ll111lll1_opy_, bstack11llllllll_opy_.get_property(bstack1l1ll11_opy_ (u"ࠤࡳࡶࡴࡾࡹࡔࡧࡷࡸ࡮ࡴࡧࡴࠤ᭶")))
    bstack11l1ll1l11l_opy_ = [element.lower() for element in bstack11ll1l11lll_opy_]
    bstack11ll1111111_opy_(bstack11l1l11l111_opy_, bstack11l1ll1l11l_opy_)
    return bstack11l1l11l111_opy_
def bstack11ll1111111_opy_(d, keys):
    for key in list(d.keys()):
        if key.lower() in keys:
            d[key] = bstack1l1ll11_opy_ (u"ࠥ࠮࠯࠰ࠪࠣ᭷")
    for value in d.values():
        if isinstance(value, dict):
            bstack11ll1111111_opy_(value, keys)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    bstack11ll1111111_opy_(item, keys)
def bstack1ll11l11111_opy_():
    bstack11l1ll11111_opy_ = [os.environ.get(bstack1l1ll11_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡊࡎࡒࡅࡔࡡࡇࡍࡗࠨ᭸")), os.path.join(os.path.expanduser(bstack1l1ll11_opy_ (u"ࠧࢄࠢ᭹")), bstack1l1ll11_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭᭺")), os.path.join(bstack1l1ll11_opy_ (u"ࠧ࠰ࡶࡰࡴࠬ᭻"), bstack1l1ll11_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨ᭼"))]
    for path in bstack11l1ll11111_opy_:
        if path is None:
            continue
        try:
            if os.path.exists(path):
                logger.debug(bstack1l1ll11_opy_ (u"ࠤࡉ࡭ࡱ࡫ࠠࠨࠤ᭽") + str(path) + bstack1l1ll11_opy_ (u"ࠥࠫࠥ࡫ࡸࡪࡵࡷࡷ࠳ࠨ᭾"))
                if not os.access(path, os.W_OK):
                    logger.debug(bstack1l1ll11_opy_ (u"ࠦࡌ࡯ࡶࡪࡰࡪࠤࡵ࡫ࡲ࡮࡫ࡶࡷ࡮ࡵ࡮ࡴࠢࡩࡳࡷࠦࠧࠣ᭿") + str(path) + bstack1l1ll11_opy_ (u"ࠧ࠭ࠢᮀ"))
                    os.chmod(path, 0o777)
                else:
                    logger.debug(bstack1l1ll11_opy_ (u"ࠨࡆࡪ࡮ࡨࠤࠬࠨᮁ") + str(path) + bstack1l1ll11_opy_ (u"ࠢࠨࠢࡤࡰࡷ࡫ࡡࡥࡻࠣ࡬ࡦࡹࠠࡵࡪࡨࠤࡷ࡫ࡱࡶ࡫ࡵࡩࡩࠦࡰࡦࡴࡰ࡭ࡸࡹࡩࡰࡰࡶ࠲ࠧᮂ"))
            else:
                logger.debug(bstack1l1ll11_opy_ (u"ࠣࡅࡵࡩࡦࡺࡩ࡯ࡩࠣࡪ࡮ࡲࡥࠡࠩࠥᮃ") + str(path) + bstack1l1ll11_opy_ (u"ࠤࠪࠤࡼ࡯ࡴࡩࠢࡺࡶ࡮ࡺࡥࠡࡲࡨࡶࡲ࡯ࡳࡴ࡫ࡲࡲ࠳ࠨᮄ"))
                os.makedirs(path, exist_ok=True)
                os.chmod(path, 0o777)
            logger.debug(bstack1l1ll11_opy_ (u"ࠥࡓࡵ࡫ࡲࡢࡶ࡬ࡳࡳࠦࡳࡶࡥࡦࡩࡪࡪࡥࡥࠢࡩࡳࡷࠦࠧࠣᮅ") + str(path) + bstack1l1ll11_opy_ (u"ࠦࠬ࠴ࠢᮆ"))
            return path
        except Exception as e:
            logger.debug(bstack1l1ll11_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡨࡸࠥࡻࡰࠡࡨ࡬ࡰࡪࠦࠧࡼࡲࡤࡸ࡭ࢃࠧ࠻ࠢࠥᮇ") + str(e) + bstack1l1ll11_opy_ (u"ࠨࠢᮈ"))
    logger.debug(bstack1l1ll11_opy_ (u"ࠢࡂ࡮࡯ࠤࡵࡧࡴࡩࡵࠣࡪࡦ࡯࡬ࡦࡦ࠱ࠦᮉ"))
    return None
@measure(event_name=EVENTS.bstack11lll1111l1_opy_, stage=STAGE.bstack1ll1111ll1_opy_)
def bstack1llll1l1111_opy_(binary_path, bstack1lllll11l1l_opy_, bs_config):
    logger.debug(bstack1l1ll11_opy_ (u"ࠣࡅࡸࡶࡷ࡫࡮ࡵࠢࡆࡐࡎࠦࡐࡢࡶ࡫ࠤ࡫ࡵࡵ࡯ࡦ࠽ࠤࢀࢃࠢᮊ").format(binary_path))
    bstack11ll111llll_opy_ = bstack1l1ll11_opy_ (u"ࠩࠪᮋ")
    bstack11l1ll11l11_opy_ = {
        bstack1l1ll11_opy_ (u"ࠪࡷࡩࡱ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨᮌ"): __version__,
        bstack1l1ll11_opy_ (u"ࠦࡴࡹࠢᮍ"): platform.system(),
        bstack1l1ll11_opy_ (u"ࠧࡵࡳࡠࡣࡵࡧ࡭ࠨᮎ"): platform.machine(),
        bstack1l1ll11_opy_ (u"ࠨࡣ࡭࡫ࡢࡺࡪࡸࡳࡪࡱࡱࠦᮏ"): bstack1l1ll11_opy_ (u"ࠧ࠱ࠩᮐ"),
        bstack1l1ll11_opy_ (u"ࠣࡵࡧ࡯ࡤࡲࡡ࡯ࡩࡸࡥ࡬࡫ࠢᮑ"): bstack1l1ll11_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩᮒ")
    }
    try:
        if binary_path:
            bstack11l1ll11l11_opy_[bstack1l1ll11_opy_ (u"ࠪࡧࡱ࡯࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨᮓ")] = subprocess.check_output([binary_path, bstack1l1ll11_opy_ (u"ࠦࡻ࡫ࡲࡴ࡫ࡲࡲࠧᮔ")]).strip().decode(bstack1l1ll11_opy_ (u"ࠬࡻࡴࡧ࠯࠻ࠫᮕ"))
        response = requests.request(
            bstack1l1ll11_opy_ (u"࠭ࡇࡆࡖࠪᮖ"),
            url=bstack11l1lll1l_opy_(bstack11ll1l11l1l_opy_),
            headers=None,
            auth=(bs_config[bstack1l1ll11_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩᮗ")], bs_config[bstack1l1ll11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫᮘ")]),
            json=None,
            params=bstack11l1ll11l11_opy_
        )
        data = response.json()
        if response.status_code == 200 and bstack1l1ll11_opy_ (u"ࠩࡸࡶࡱ࠭ᮙ") in data.keys() and bstack1l1ll11_opy_ (u"ࠪࡹࡵࡪࡡࡵࡧࡧࡣࡨࡲࡩࡠࡸࡨࡶࡸ࡯࡯࡯ࠩᮚ") in data.keys():
            logger.debug(bstack1l1ll11_opy_ (u"ࠦࡓ࡫ࡥࡥࠢࡷࡳࠥࡻࡰࡥࡣࡷࡩࠥࡨࡩ࡯ࡣࡵࡽ࠱ࠦࡣࡶࡴࡵࡩࡳࡺࠠࡣ࡫ࡱࡥࡷࡿࠠࡷࡧࡵࡷ࡮ࡵ࡮࠻ࠢࡾࢁࠧᮛ").format(bstack11l1ll11l11_opy_[bstack1l1ll11_opy_ (u"ࠬࡩ࡬ࡪࡡࡹࡩࡷࡹࡩࡰࡰࠪᮜ")]))
            bstack11ll11ll11l_opy_ = bstack11l1l111111_opy_(data[bstack1l1ll11_opy_ (u"࠭ࡵࡳ࡮ࠪᮝ")], bstack1lllll11l1l_opy_)
            bstack11ll111llll_opy_ = os.path.join(bstack1lllll11l1l_opy_, bstack11ll11ll11l_opy_)
            os.chmod(bstack11ll111llll_opy_, 0o777) # bstack11l1llll1ll_opy_ permission
            return bstack11ll111llll_opy_
    except Exception as e:
        logger.debug(bstack1l1ll11_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡪ࡯ࡸࡰ࡯ࡳࡦࡪࡩ࡯ࡩࠣࡲࡪࡽࠠࡔࡆࡎࠤࢀࢃࠢᮞ").format(e))
    return binary_path
@measure(event_name=EVENTS.bstack11ll1l111l1_opy_, stage=STAGE.bstack1ll1111ll1_opy_)
def bstack11l1l111111_opy_(bstack11l1ll11l1l_opy_, bstack11ll11l111l_opy_):
    logger.debug(bstack1l1ll11_opy_ (u"ࠣࡆࡲࡻࡳࡲ࡯ࡢࡦ࡬ࡲ࡬ࠦࡓࡅࡍࠣࡦ࡮ࡴࡡࡳࡻࠣࡪࡷࡵ࡭࠻ࠢࠥᮟ") + str(bstack11l1ll11l1l_opy_) + bstack1l1ll11_opy_ (u"ࠤࠥᮠ"))
    zip_path = os.path.join(bstack11ll11l111l_opy_, bstack1l1ll11_opy_ (u"ࠥࡨࡴࡽ࡮࡭ࡱࡤࡨࡪࡪ࡟ࡧ࡫࡯ࡩ࠳ࢀࡩࡱࠤᮡ"))
    bstack11ll11ll11l_opy_ = bstack1l1ll11_opy_ (u"ࠫࠬᮢ")
    with requests.get(bstack11l1ll11l1l_opy_, stream=True) as response:
        response.raise_for_status()
        with open(zip_path, bstack1l1ll11_opy_ (u"ࠧࡽࡢࠣᮣ")) as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
        logger.debug(bstack1l1ll11_opy_ (u"ࠨࡆࡪ࡮ࡨࠤࡩࡵࡷ࡯࡮ࡲࡥࡩ࡫ࡤࠡࡵࡸࡧࡨ࡫ࡳࡴࡨࡸࡰࡱࡿ࠮ࠣᮤ"))
    with zipfile.ZipFile(zip_path, bstack1l1ll11_opy_ (u"ࠧࡳࠩᮥ")) as zip_ref:
        bstack11ll11l1l11_opy_ = zip_ref.namelist()
        if len(bstack11ll11l1l11_opy_) > 0:
            bstack11ll11ll11l_opy_ = bstack11ll11l1l11_opy_[0] # bstack11l1lll11l1_opy_ bstack11ll1l1ll11_opy_ will be bstack11l1l1l1l11_opy_ 1 file i.e. the binary in the zip
        zip_ref.extractall(bstack11ll11l111l_opy_)
        logger.debug(bstack1l1ll11_opy_ (u"ࠣࡈ࡬ࡰࡪࡹࠠࡴࡷࡦࡧࡪࡹࡳࡧࡷ࡯ࡰࡾࠦࡥࡹࡶࡵࡥࡨࡺࡥࡥࠢࡷࡳࠥ࠭ࠢᮦ") + str(bstack11ll11l111l_opy_) + bstack1l1ll11_opy_ (u"ࠤࠪࠦᮧ"))
    os.remove(zip_path)
    return bstack11ll11ll11l_opy_
def get_cli_dir():
    bstack11ll11l1111_opy_ = bstack1ll11l11111_opy_()
    if bstack11ll11l1111_opy_:
        bstack1lllll11l1l_opy_ = os.path.join(bstack11ll11l1111_opy_, bstack1l1ll11_opy_ (u"ࠥࡧࡱ࡯ࠢᮨ"))
        if not os.path.exists(bstack1lllll11l1l_opy_):
            os.makedirs(bstack1lllll11l1l_opy_, mode=0o777, exist_ok=True)
        return bstack1lllll11l1l_opy_
    else:
        raise FileNotFoundError(bstack1l1ll11_opy_ (u"ࠦࡓࡵࠠࡸࡴ࡬ࡸࡦࡨ࡬ࡦࠢࡧ࡭ࡷ࡫ࡣࡵࡱࡵࡽࠥࡧࡶࡢ࡫࡯ࡥࡧࡲࡥࠡࡨࡲࡶࠥࡺࡨࡦࠢࡖࡈࡐࠦࡢࡪࡰࡤࡶࡾ࠴ࠢᮩ"))
def bstack1lll1llll11_opy_(bstack1lllll11l1l_opy_):
    bstack1l1ll11_opy_ (u"ࠧࠨࠢࡈࡧࡷࠤࡹ࡮ࡥࠡࡲࡤࡸ࡭ࠦࡦࡰࡴࠣࡸ࡭࡫ࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡓࡅࡍࠣࡦ࡮ࡴࡡࡳࡻࠣ࡭ࡳࠦࡡࠡࡹࡵ࡭ࡹࡧࡢ࡭ࡧࠣࡨ࡮ࡸࡥࡤࡶࡲࡶࡾ࠴ࠢࠣࠤ᮪")
    bstack11l11llllll_opy_ = [
        os.path.join(bstack1lllll11l1l_opy_, f)
        for f in os.listdir(bstack1lllll11l1l_opy_)
        if os.path.isfile(os.path.join(bstack1lllll11l1l_opy_, f)) and f.startswith(bstack1l1ll11_opy_ (u"ࠨࡢࡪࡰࡤࡶࡾ࠳᮫ࠢ"))
    ]
    if len(bstack11l11llllll_opy_) > 0:
        return max(bstack11l11llllll_opy_, key=os.path.getmtime) # get bstack11ll111l1l1_opy_ binary
    return bstack1l1ll11_opy_ (u"ࠢࠣᮬ")
def bstack1ll1l1llll1_opy_(d, u):
  for k, v in u.items():
    if isinstance(v, collections.abc.Mapping):
      d[k] = bstack1ll1l1llll1_opy_(d.get(k, {}), v)
    else:
      if isinstance(v, list):
        d[k] = d.get(k, []) + v
      else:
        d[k] = v
  return d