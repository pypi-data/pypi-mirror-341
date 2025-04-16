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
from bstack_utils.constants import (bstack11ll1l1ll1l_opy_, bstack1lllll1l1_opy_, bstack1ll111111_opy_, bstack11ll1lll11_opy_,
                                    bstack11ll1ll1lll_opy_, bstack11ll1ll1l11_opy_, bstack11lll11111l_opy_, bstack11ll1lll1l1_opy_)
from bstack_utils.measure import measure
from bstack_utils.messages import bstack11lll1l111_opy_, bstack1111ll1ll_opy_
from bstack_utils.proxy import bstack11ll1llll_opy_, bstack1lll11l111_opy_
from bstack_utils.constants import *
from bstack_utils import bstack1l11l11lll_opy_
from browserstack_sdk._version import __version__
bstack11llllll1_opy_ = Config.bstack111111ll_opy_()
logger = bstack1l11l11lll_opy_.get_logger(__name__, bstack1l11l11lll_opy_.bstack1lll1111lll_opy_())
def bstack11llll1l1l1_opy_(config):
    return config[bstack1l1_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬᦛ")]
def bstack11llll11l11_opy_(config):
    return config[bstack1l1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧᦜ")]
def bstack1l1l11l1l1_opy_():
    try:
        import playwright
        return True
    except ImportError:
        return False
def bstack11ll11l11l1_opy_(obj):
    values = []
    bstack11ll1111ll1_opy_ = re.compile(bstack1l1_opy_ (u"ࡷࠨ࡞ࡄࡗࡖࡘࡔࡓ࡟ࡕࡃࡊࡣࡡࡪࠫࠥࠤᦝ"), re.I)
    for key in obj.keys():
        if bstack11ll1111ll1_opy_.match(key):
            values.append(obj[key])
    return values
def bstack11ll111ll1l_opy_(config):
    tags = []
    tags.extend(bstack11ll11l11l1_opy_(os.environ))
    tags.extend(bstack11ll11l11l1_opy_(config))
    return tags
def bstack11ll1111l11_opy_(markers):
    tags = []
    for marker in markers:
        tags.append(marker.name)
    return tags
def bstack11ll11ll11l_opy_(bstack11ll1111lll_opy_):
    if not bstack11ll1111lll_opy_:
        return bstack1l1_opy_ (u"࠭ࠧᦞ")
    return bstack1l1_opy_ (u"ࠢࡼࡿࠣࠬࢀࢃࠩࠣᦟ").format(bstack11ll1111lll_opy_.name, bstack11ll1111lll_opy_.email)
def bstack11lll1lll1l_opy_():
    try:
        repo = git.Repo(search_parent_directories=True)
        bstack11l1lll1ll1_opy_ = repo.common_dir
        info = {
            bstack1l1_opy_ (u"ࠣࡵ࡫ࡥࠧᦠ"): repo.head.commit.hexsha,
            bstack1l1_opy_ (u"ࠤࡶ࡬ࡴࡸࡴࡠࡵ࡫ࡥࠧᦡ"): repo.git.rev_parse(repo.head.commit, short=True),
            bstack1l1_opy_ (u"ࠥࡦࡷࡧ࡮ࡤࡪࠥᦢ"): repo.active_branch.name,
            bstack1l1_opy_ (u"ࠦࡹࡧࡧࠣᦣ"): repo.git.describe(all=True, tags=True, exact_match=True),
            bstack1l1_opy_ (u"ࠧࡩ࡯࡮࡯࡬ࡸࡹ࡫ࡲࠣᦤ"): bstack11ll11ll11l_opy_(repo.head.commit.committer),
            bstack1l1_opy_ (u"ࠨࡣࡰ࡯ࡰ࡭ࡹࡺࡥࡳࡡࡧࡥࡹ࡫ࠢᦥ"): repo.head.commit.committed_datetime.isoformat(),
            bstack1l1_opy_ (u"ࠢࡢࡷࡷ࡬ࡴࡸࠢᦦ"): bstack11ll11ll11l_opy_(repo.head.commit.author),
            bstack1l1_opy_ (u"ࠣࡣࡸࡸ࡭ࡵࡲࡠࡦࡤࡸࡪࠨᦧ"): repo.head.commit.authored_datetime.isoformat(),
            bstack1l1_opy_ (u"ࠤࡦࡳࡲࡳࡩࡵࡡࡰࡩࡸࡹࡡࡨࡧࠥᦨ"): repo.head.commit.message,
            bstack1l1_opy_ (u"ࠥࡶࡴࡵࡴࠣᦩ"): repo.git.rev_parse(bstack1l1_opy_ (u"ࠦ࠲࠳ࡳࡩࡱࡺ࠱ࡹࡵࡰ࡭ࡧࡹࡩࡱࠨᦪ")),
            bstack1l1_opy_ (u"ࠧࡩ࡯࡮࡯ࡲࡲࡤ࡭ࡩࡵࡡࡧ࡭ࡷࠨᦫ"): bstack11l1lll1ll1_opy_,
            bstack1l1_opy_ (u"ࠨࡷࡰࡴ࡮ࡸࡷ࡫ࡥࡠࡩ࡬ࡸࡤࡪࡩࡳࠤ᦬"): subprocess.check_output([bstack1l1_opy_ (u"ࠢࡨ࡫ࡷࠦ᦭"), bstack1l1_opy_ (u"ࠣࡴࡨࡺ࠲ࡶࡡࡳࡵࡨࠦ᦮"), bstack1l1_opy_ (u"ࠤ࠰࠱࡬࡯ࡴ࠮ࡥࡲࡱࡲࡵ࡮࠮ࡦ࡬ࡶࠧ᦯")]).strip().decode(
                bstack1l1_opy_ (u"ࠪࡹࡹ࡬࠭࠹ࠩᦰ")),
            bstack1l1_opy_ (u"ࠦࡱࡧࡳࡵࡡࡷࡥ࡬ࠨᦱ"): repo.git.describe(tags=True, abbrev=0, always=True),
            bstack1l1_opy_ (u"ࠧࡩ࡯࡮࡯࡬ࡸࡸࡥࡳࡪࡰࡦࡩࡤࡲࡡࡴࡶࡢࡸࡦ࡭ࠢᦲ"): repo.git.rev_list(
                bstack1l1_opy_ (u"ࠨࡻࡾ࠰࠱ࡿࢂࠨᦳ").format(repo.head.commit, repo.git.describe(tags=True, abbrev=0, always=True)), count=True)
        }
        remotes = repo.remotes
        bstack11l1llll1ll_opy_ = []
        for remote in remotes:
            bstack11l1l1ll111_opy_ = {
                bstack1l1_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᦴ"): remote.name,
                bstack1l1_opy_ (u"ࠣࡷࡵࡰࠧᦵ"): remote.url,
            }
            bstack11l1llll1ll_opy_.append(bstack11l1l1ll111_opy_)
        bstack11ll11llll1_opy_ = {
            bstack1l1_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᦶ"): bstack1l1_opy_ (u"ࠥ࡫࡮ࡺࠢᦷ"),
            **info,
            bstack1l1_opy_ (u"ࠦࡷ࡫࡭ࡰࡶࡨࡷࠧᦸ"): bstack11l1llll1ll_opy_
        }
        bstack11ll11llll1_opy_ = bstack11ll11l1ll1_opy_(bstack11ll11llll1_opy_)
        return bstack11ll11llll1_opy_
    except git.InvalidGitRepositoryError:
        return {}
    except Exception as err:
        print(bstack1l1_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡵࡰࡶ࡮ࡤࡸ࡮ࡴࡧࠡࡉ࡬ࡸࠥࡳࡥࡵࡣࡧࡥࡹࡧࠠࡸ࡫ࡷ࡬ࠥ࡫ࡲࡳࡱࡵ࠾ࠥࢁࡽࠣᦹ").format(err))
        return {}
def bstack11ll11l1ll1_opy_(bstack11ll11llll1_opy_):
    bstack11l1lll1l11_opy_ = bstack11l1ll111ll_opy_(bstack11ll11llll1_opy_)
    if bstack11l1lll1l11_opy_ and bstack11l1lll1l11_opy_ > bstack11ll1ll1lll_opy_:
        bstack11ll11l111l_opy_ = bstack11l1lll1l11_opy_ - bstack11ll1ll1lll_opy_
        bstack11ll11l1lll_opy_ = bstack11ll1111l1l_opy_(bstack11ll11llll1_opy_[bstack1l1_opy_ (u"ࠨࡣࡰ࡯ࡰ࡭ࡹࡥ࡭ࡦࡵࡶࡥ࡬࡫ࠢᦺ")], bstack11ll11l111l_opy_)
        bstack11ll11llll1_opy_[bstack1l1_opy_ (u"ࠢࡤࡱࡰࡱ࡮ࡺ࡟࡮ࡧࡶࡷࡦ࡭ࡥࠣᦻ")] = bstack11ll11l1lll_opy_
        logger.info(bstack1l1_opy_ (u"ࠣࡖ࡫ࡩࠥࡩ࡯࡮࡯࡬ࡸࠥ࡮ࡡࡴࠢࡥࡩࡪࡴࠠࡵࡴࡸࡲࡨࡧࡴࡦࡦ࠱ࠤࡘ࡯ࡺࡦࠢࡲࡪࠥࡩ࡯࡮࡯࡬ࡸࠥࡧࡦࡵࡧࡵࠤࡹࡸࡵ࡯ࡥࡤࡸ࡮ࡵ࡮ࠡ࡫ࡶࠤࢀࢃࠠࡌࡄࠥᦼ")
                    .format(bstack11l1ll111ll_opy_(bstack11ll11llll1_opy_) / 1024))
    return bstack11ll11llll1_opy_
def bstack11l1ll111ll_opy_(bstack11l11l1ll_opy_):
    try:
        if bstack11l11l1ll_opy_:
            bstack11ll11lll11_opy_ = json.dumps(bstack11l11l1ll_opy_)
            bstack11l1lll11l1_opy_ = sys.getsizeof(bstack11ll11lll11_opy_)
            return bstack11l1lll11l1_opy_
    except Exception as e:
        logger.debug(bstack1l1_opy_ (u"ࠤࡖࡳࡲ࡫ࡴࡩ࡫ࡱ࡫ࠥࡽࡥ࡯ࡶࠣࡻࡷࡵ࡮ࡨࠢࡺ࡬࡮ࡲࡥࠡࡥࡤࡰࡨࡻ࡬ࡢࡶ࡬ࡲ࡬ࠦࡳࡪࡼࡨࠤࡴ࡬ࠠࡋࡕࡒࡒࠥࡵࡢ࡫ࡧࡦࡸ࠿ࠦࡻࡾࠤᦽ").format(e))
    return -1
def bstack11ll1111l1l_opy_(field, bstack11l1ll1l1l1_opy_):
    try:
        bstack11l1lll1111_opy_ = len(bytes(bstack11ll1ll1l11_opy_, bstack1l1_opy_ (u"ࠪࡹࡹ࡬࠭࠹ࠩᦾ")))
        bstack11ll11ll1ll_opy_ = bytes(field, bstack1l1_opy_ (u"ࠫࡺࡺࡦ࠮࠺ࠪᦿ"))
        bstack11l1ll1l1ll_opy_ = len(bstack11ll11ll1ll_opy_)
        bstack11ll111l1l1_opy_ = ceil(bstack11l1ll1l1ll_opy_ - bstack11l1ll1l1l1_opy_ - bstack11l1lll1111_opy_)
        if bstack11ll111l1l1_opy_ > 0:
            bstack11ll11ll1l1_opy_ = bstack11ll11ll1ll_opy_[:bstack11ll111l1l1_opy_].decode(bstack1l1_opy_ (u"ࠬࡻࡴࡧ࠯࠻ࠫᧀ"), errors=bstack1l1_opy_ (u"࠭ࡩࡨࡰࡲࡶࡪ࠭ᧁ")) + bstack11ll1ll1l11_opy_
            return bstack11ll11ll1l1_opy_
    except Exception as e:
        logger.debug(bstack1l1_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡺࡲࡶࡰࡦࡥࡹ࡯࡮ࡨࠢࡩ࡭ࡪࡲࡤ࠭ࠢࡱࡳࡹ࡮ࡩ࡯ࡩࠣࡻࡦࡹࠠࡵࡴࡸࡲࡨࡧࡴࡦࡦࠣ࡬ࡪࡸࡥ࠻ࠢࡾࢁࠧᧂ").format(e))
    return field
def bstack11ll111111_opy_():
    env = os.environ
    if (bstack1l1_opy_ (u"ࠣࡌࡈࡒࡐࡏࡎࡔࡡࡘࡖࡑࠨᧃ") in env and len(env[bstack1l1_opy_ (u"ࠤࡍࡉࡓࡑࡉࡏࡕࡢ࡙ࡗࡒࠢᧄ")]) > 0) or (
            bstack1l1_opy_ (u"ࠥࡎࡊࡔࡋࡊࡐࡖࡣࡍࡕࡍࡆࠤᧅ") in env and len(env[bstack1l1_opy_ (u"ࠦࡏࡋࡎࡌࡋࡑࡗࡤࡎࡏࡎࡇࠥᧆ")]) > 0):
        return {
            bstack1l1_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᧇ"): bstack1l1_opy_ (u"ࠨࡊࡦࡰ࡮࡭ࡳࡹࠢᧈ"),
            bstack1l1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᧉ"): env.get(bstack1l1_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡖࡔࡏࠦ᧊")),
            bstack1l1_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦ᧋"): env.get(bstack1l1_opy_ (u"ࠥࡎࡔࡈ࡟ࡏࡃࡐࡉࠧ᧌")),
            bstack1l1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥ᧍"): env.get(bstack1l1_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦ᧎"))
        }
    if env.get(bstack1l1_opy_ (u"ࠨࡃࡊࠤ᧏")) == bstack1l1_opy_ (u"ࠢࡵࡴࡸࡩࠧ᧐") and bstack111llll11_opy_(env.get(bstack1l1_opy_ (u"ࠣࡅࡌࡖࡈࡒࡅࡄࡋࠥ᧑"))):
        return {
            bstack1l1_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ᧒"): bstack1l1_opy_ (u"ࠥࡇ࡮ࡸࡣ࡭ࡧࡆࡍࠧ᧓"),
            bstack1l1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢ᧔"): env.get(bstack1l1_opy_ (u"ࠧࡉࡉࡓࡅࡏࡉࡤࡈࡕࡊࡎࡇࡣ࡚ࡘࡌࠣ᧕")),
            bstack1l1_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣ᧖"): env.get(bstack1l1_opy_ (u"ࠢࡄࡋࡕࡇࡑࡋ࡟ࡋࡑࡅࠦ᧗")),
            bstack1l1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢ᧘"): env.get(bstack1l1_opy_ (u"ࠤࡆࡍࡗࡉࡌࡆࡡࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࠧ᧙"))
        }
    if env.get(bstack1l1_opy_ (u"ࠥࡇࡎࠨ᧚")) == bstack1l1_opy_ (u"ࠦࡹࡸࡵࡦࠤ᧛") and bstack111llll11_opy_(env.get(bstack1l1_opy_ (u"࡚ࠧࡒࡂࡘࡌࡗࠧ᧜"))):
        return {
            bstack1l1_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ᧝"): bstack1l1_opy_ (u"ࠢࡕࡴࡤࡺ࡮ࡹࠠࡄࡋࠥ᧞"),
            bstack1l1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦ᧟"): env.get(bstack1l1_opy_ (u"ࠤࡗࡖࡆ࡜ࡉࡔࡡࡅ࡙ࡎࡒࡄࡠ࡙ࡈࡆࡤ࡛ࡒࡍࠤ᧠")),
            bstack1l1_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧ᧡"): env.get(bstack1l1_opy_ (u"࡙ࠦࡘࡁࡗࡋࡖࡣࡏࡕࡂࡠࡐࡄࡑࡊࠨ᧢")),
            bstack1l1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ᧣"): env.get(bstack1l1_opy_ (u"ࠨࡔࡓࡃ࡙ࡍࡘࡥࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࠧ᧤"))
        }
    if env.get(bstack1l1_opy_ (u"ࠢࡄࡋࠥ᧥")) == bstack1l1_opy_ (u"ࠣࡶࡵࡹࡪࠨ᧦") and env.get(bstack1l1_opy_ (u"ࠤࡆࡍࡤࡔࡁࡎࡇࠥ᧧")) == bstack1l1_opy_ (u"ࠥࡧࡴࡪࡥࡴࡪ࡬ࡴࠧ᧨"):
        return {
            bstack1l1_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ᧩"): bstack1l1_opy_ (u"ࠧࡉ࡯ࡥࡧࡶ࡬࡮ࡶࠢ᧪"),
            bstack1l1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤ᧫"): None,
            bstack1l1_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤ᧬"): None,
            bstack1l1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢ᧭"): None
        }
    if env.get(bstack1l1_opy_ (u"ࠤࡅࡍ࡙ࡈࡕࡄࡍࡈࡘࡤࡈࡒࡂࡐࡆࡌࠧ᧮")) and env.get(bstack1l1_opy_ (u"ࠥࡆࡎ࡚ࡂࡖࡅࡎࡉ࡙ࡥࡃࡐࡏࡐࡍ࡙ࠨ᧯")):
        return {
            bstack1l1_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ᧰"): bstack1l1_opy_ (u"ࠧࡈࡩࡵࡤࡸࡧࡰ࡫ࡴࠣ᧱"),
            bstack1l1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤ᧲"): env.get(bstack1l1_opy_ (u"ࠢࡃࡋࡗࡆ࡚ࡉࡋࡆࡖࡢࡋࡎ࡚࡟ࡉࡖࡗࡔࡤࡕࡒࡊࡉࡌࡒࠧ᧳")),
            bstack1l1_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥ᧴"): None,
            bstack1l1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣ᧵"): env.get(bstack1l1_opy_ (u"ࠥࡆࡎ࡚ࡂࡖࡅࡎࡉ࡙ࡥࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࠧ᧶"))
        }
    if env.get(bstack1l1_opy_ (u"ࠦࡈࡏࠢ᧷")) == bstack1l1_opy_ (u"ࠧࡺࡲࡶࡧࠥ᧸") and bstack111llll11_opy_(env.get(bstack1l1_opy_ (u"ࠨࡄࡓࡑࡑࡉࠧ᧹"))):
        return {
            bstack1l1_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ᧺"): bstack1l1_opy_ (u"ࠣࡆࡵࡳࡳ࡫ࠢ᧻"),
            bstack1l1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧ᧼"): env.get(bstack1l1_opy_ (u"ࠥࡈࡗࡕࡎࡆࡡࡅ࡙ࡎࡒࡄࡠࡎࡌࡒࡐࠨ᧽")),
            bstack1l1_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨ᧾"): None,
            bstack1l1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ᧿"): env.get(bstack1l1_opy_ (u"ࠨࡄࡓࡑࡑࡉࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦᨀ"))
        }
    if env.get(bstack1l1_opy_ (u"ࠢࡄࡋࠥᨁ")) == bstack1l1_opy_ (u"ࠣࡶࡵࡹࡪࠨᨂ") and bstack111llll11_opy_(env.get(bstack1l1_opy_ (u"ࠤࡖࡉࡒࡇࡐࡉࡑࡕࡉࠧᨃ"))):
        return {
            bstack1l1_opy_ (u"ࠥࡲࡦࡳࡥࠣᨄ"): bstack1l1_opy_ (u"ࠦࡘ࡫࡭ࡢࡲ࡫ࡳࡷ࡫ࠢᨅ"),
            bstack1l1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᨆ"): env.get(bstack1l1_opy_ (u"ࠨࡓࡆࡏࡄࡔࡍࡕࡒࡆࡡࡒࡖࡌࡇࡎࡊ࡜ࡄࡘࡎࡕࡎࡠࡗࡕࡐࠧᨇ")),
            bstack1l1_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᨈ"): env.get(bstack1l1_opy_ (u"ࠣࡕࡈࡑࡆࡖࡈࡐࡔࡈࡣࡏࡕࡂࡠࡐࡄࡑࡊࠨᨉ")),
            bstack1l1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᨊ"): env.get(bstack1l1_opy_ (u"ࠥࡗࡊࡓࡁࡑࡊࡒࡖࡊࡥࡊࡐࡄࡢࡍࡉࠨᨋ"))
        }
    if env.get(bstack1l1_opy_ (u"ࠦࡈࡏࠢᨌ")) == bstack1l1_opy_ (u"ࠧࡺࡲࡶࡧࠥᨍ") and bstack111llll11_opy_(env.get(bstack1l1_opy_ (u"ࠨࡇࡊࡖࡏࡅࡇࡥࡃࡊࠤᨎ"))):
        return {
            bstack1l1_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᨏ"): bstack1l1_opy_ (u"ࠣࡉ࡬ࡸࡑࡧࡢࠣᨐ"),
            bstack1l1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᨑ"): env.get(bstack1l1_opy_ (u"ࠥࡇࡎࡥࡊࡐࡄࡢ࡙ࡗࡒࠢᨒ")),
            bstack1l1_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᨓ"): env.get(bstack1l1_opy_ (u"ࠧࡉࡉࡠࡌࡒࡆࡤࡔࡁࡎࡇࠥᨔ")),
            bstack1l1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᨕ"): env.get(bstack1l1_opy_ (u"ࠢࡄࡋࡢࡎࡔࡈ࡟ࡊࡆࠥᨖ"))
        }
    if env.get(bstack1l1_opy_ (u"ࠣࡅࡌࠦᨗ")) == bstack1l1_opy_ (u"ࠤࡷࡶࡺ࡫ᨘࠢ") and bstack111llll11_opy_(env.get(bstack1l1_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡍࡌࡘࡊࠨᨙ"))):
        return {
            bstack1l1_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᨚ"): bstack1l1_opy_ (u"ࠧࡈࡵࡪ࡮ࡧ࡯࡮ࡺࡥࠣᨛ"),
            bstack1l1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤ᨜"): env.get(bstack1l1_opy_ (u"ࠢࡃࡗࡌࡐࡉࡑࡉࡕࡇࡢࡆ࡚ࡏࡌࡅࡡࡘࡖࡑࠨ᨝")),
            bstack1l1_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥ᨞"): env.get(bstack1l1_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡌࡋࡗࡉࡤࡒࡁࡃࡇࡏࠦ᨟")) or env.get(bstack1l1_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡍࡌࡘࡊࡥࡐࡊࡒࡈࡐࡎࡔࡅࡠࡐࡄࡑࡊࠨᨠ")),
            bstack1l1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᨡ"): env.get(bstack1l1_opy_ (u"ࠧࡈࡕࡊࡎࡇࡏࡎ࡚ࡅࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠢᨢ"))
        }
    if bstack111llll11_opy_(env.get(bstack1l1_opy_ (u"ࠨࡔࡇࡡࡅ࡙ࡎࡒࡄࠣᨣ"))):
        return {
            bstack1l1_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᨤ"): bstack1l1_opy_ (u"ࠣࡘ࡬ࡷࡺࡧ࡬ࠡࡕࡷࡹࡩ࡯࡯ࠡࡖࡨࡥࡲࠦࡓࡦࡴࡹ࡭ࡨ࡫ࡳࠣᨥ"),
            bstack1l1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᨦ"): bstack1l1_opy_ (u"ࠥࡿࢂࢁࡽࠣᨧ").format(env.get(bstack1l1_opy_ (u"ࠫࡘ࡟ࡓࡕࡇࡐࡣ࡙ࡋࡁࡎࡈࡒ࡙ࡓࡊࡁࡕࡋࡒࡒࡘࡋࡒࡗࡇࡕ࡙ࡗࡏࠧᨨ")), env.get(bstack1l1_opy_ (u"࡙࡙ࠬࡔࡖࡈࡑࡤ࡚ࡅࡂࡏࡓࡖࡔࡐࡅࡄࡖࡌࡈࠬᨩ"))),
            bstack1l1_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᨪ"): env.get(bstack1l1_opy_ (u"ࠢࡔ࡛ࡖࡘࡊࡓ࡟ࡅࡇࡉࡍࡓࡏࡔࡊࡑࡑࡍࡉࠨᨫ")),
            bstack1l1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᨬ"): env.get(bstack1l1_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡄࡘࡍࡑࡊࡉࡅࠤᨭ"))
        }
    if bstack111llll11_opy_(env.get(bstack1l1_opy_ (u"ࠥࡅࡕࡖࡖࡆ࡛ࡒࡖࠧᨮ"))):
        return {
            bstack1l1_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᨯ"): bstack1l1_opy_ (u"ࠧࡇࡰࡱࡸࡨࡽࡴࡸࠢᨰ"),
            bstack1l1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᨱ"): bstack1l1_opy_ (u"ࠢࡼࡿ࠲ࡴࡷࡵࡪࡦࡥࡷ࠳ࢀࢃ࠯ࡼࡿ࠲ࡦࡺ࡯࡬ࡥࡵ࠲ࡿࢂࠨᨲ").format(env.get(bstack1l1_opy_ (u"ࠨࡃࡓࡔ࡛ࡋ࡙ࡐࡔࡢ࡙ࡗࡒࠧᨳ")), env.get(bstack1l1_opy_ (u"ࠩࡄࡔࡕ࡜ࡅ࡚ࡑࡕࡣࡆࡉࡃࡐࡗࡑࡘࡤࡔࡁࡎࡇࠪᨴ")), env.get(bstack1l1_opy_ (u"ࠪࡅࡕࡖࡖࡆ࡛ࡒࡖࡤࡖࡒࡐࡌࡈࡇ࡙ࡥࡓࡍࡗࡊࠫᨵ")), env.get(bstack1l1_opy_ (u"ࠫࡆࡖࡐࡗࡇ࡜ࡓࡗࡥࡂࡖࡋࡏࡈࡤࡏࡄࠨᨶ"))),
            bstack1l1_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᨷ"): env.get(bstack1l1_opy_ (u"ࠨࡁࡑࡒ࡙ࡉ࡞ࡕࡒࡠࡌࡒࡆࡤࡔࡁࡎࡇࠥᨸ")),
            bstack1l1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᨹ"): env.get(bstack1l1_opy_ (u"ࠣࡃࡓࡔ࡛ࡋ࡙ࡐࡔࡢࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࠤᨺ"))
        }
    if env.get(bstack1l1_opy_ (u"ࠤࡄ࡞࡚ࡘࡅࡠࡊࡗࡘࡕࡥࡕࡔࡇࡕࡣࡆࡍࡅࡏࡖࠥᨻ")) and env.get(bstack1l1_opy_ (u"ࠥࡘࡋࡥࡂࡖࡋࡏࡈࠧᨼ")):
        return {
            bstack1l1_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᨽ"): bstack1l1_opy_ (u"ࠧࡇࡺࡶࡴࡨࠤࡈࡏࠢᨾ"),
            bstack1l1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᨿ"): bstack1l1_opy_ (u"ࠢࡼࡿࡾࢁ࠴ࡥࡢࡶ࡫࡯ࡨ࠴ࡸࡥࡴࡷ࡯ࡸࡸࡅࡢࡶ࡫࡯ࡨࡎࡪ࠽ࡼࡿࠥᩀ").format(env.get(bstack1l1_opy_ (u"ࠨࡕ࡜ࡗ࡙ࡋࡍࡠࡖࡈࡅࡒࡌࡏࡖࡐࡇࡅ࡙ࡏࡏࡏࡕࡈࡖ࡛ࡋࡒࡖࡔࡌࠫᩁ")), env.get(bstack1l1_opy_ (u"ࠩࡖ࡝ࡘ࡚ࡅࡎࡡࡗࡉࡆࡓࡐࡓࡑࡍࡉࡈ࡚ࠧᩂ")), env.get(bstack1l1_opy_ (u"ࠪࡆ࡚ࡏࡌࡅࡡࡅ࡙ࡎࡒࡄࡊࡆࠪᩃ"))),
            bstack1l1_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᩄ"): env.get(bstack1l1_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡇ࡛ࡉࡍࡆࡌࡈࠧᩅ")),
            bstack1l1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᩆ"): env.get(bstack1l1_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡂࡖࡋࡏࡈࡎࡊࠢᩇ"))
        }
    if any([env.get(bstack1l1_opy_ (u"ࠣࡅࡒࡈࡊࡈࡕࡊࡎࡇࡣࡇ࡛ࡉࡍࡆࡢࡍࡉࠨᩈ")), env.get(bstack1l1_opy_ (u"ࠤࡆࡓࡉࡋࡂࡖࡋࡏࡈࡤࡘࡅࡔࡑࡏ࡚ࡊࡊ࡟ࡔࡑࡘࡖࡈࡋ࡟ࡗࡇࡕࡗࡎࡕࡎࠣᩉ")), env.get(bstack1l1_opy_ (u"ࠥࡇࡔࡊࡅࡃࡗࡌࡐࡉࡥࡓࡐࡗࡕࡇࡊࡥࡖࡆࡔࡖࡍࡔࡔࠢᩊ"))]):
        return {
            bstack1l1_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᩋ"): bstack1l1_opy_ (u"ࠧࡇࡗࡔࠢࡆࡳࡩ࡫ࡂࡶ࡫࡯ࡨࠧᩌ"),
            bstack1l1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᩍ"): env.get(bstack1l1_opy_ (u"ࠢࡄࡑࡇࡉࡇ࡛ࡉࡍࡆࡢࡔ࡚ࡈࡌࡊࡅࡢࡆ࡚ࡏࡌࡅࡡࡘࡖࡑࠨᩎ")),
            bstack1l1_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᩏ"): env.get(bstack1l1_opy_ (u"ࠤࡆࡓࡉࡋࡂࡖࡋࡏࡈࡤࡈࡕࡊࡎࡇࡣࡎࡊࠢᩐ")),
            bstack1l1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᩑ"): env.get(bstack1l1_opy_ (u"ࠦࡈࡕࡄࡆࡄࡘࡍࡑࡊ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࠤᩒ"))
        }
    if env.get(bstack1l1_opy_ (u"ࠧࡨࡡ࡮ࡤࡲࡳࡤࡨࡵࡪ࡮ࡧࡒࡺࡳࡢࡦࡴࠥᩓ")):
        return {
            bstack1l1_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᩔ"): bstack1l1_opy_ (u"ࠢࡃࡣࡰࡦࡴࡵࠢᩕ"),
            bstack1l1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᩖ"): env.get(bstack1l1_opy_ (u"ࠤࡥࡥࡲࡨ࡯ࡰࡡࡥࡹ࡮ࡲࡤࡓࡧࡶࡹࡱࡺࡳࡖࡴ࡯ࠦᩗ")),
            bstack1l1_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᩘ"): env.get(bstack1l1_opy_ (u"ࠦࡧࡧ࡭ࡣࡱࡲࡣࡸ࡮࡯ࡳࡶࡍࡳࡧࡔࡡ࡮ࡧࠥᩙ")),
            bstack1l1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᩚ"): env.get(bstack1l1_opy_ (u"ࠨࡢࡢ࡯ࡥࡳࡴࡥࡢࡶ࡫࡯ࡨࡓࡻ࡭ࡣࡧࡵࠦᩛ"))
        }
    if env.get(bstack1l1_opy_ (u"ࠢࡘࡇࡕࡇࡐࡋࡒࠣᩜ")) or env.get(bstack1l1_opy_ (u"࡙ࠣࡈࡖࡈࡑࡅࡓࡡࡐࡅࡎࡔ࡟ࡑࡋࡓࡉࡑࡏࡎࡆࡡࡖࡘࡆࡘࡔࡆࡆࠥᩝ")):
        return {
            bstack1l1_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᩞ"): bstack1l1_opy_ (u"࡛ࠥࡪࡸࡣ࡬ࡧࡵࠦ᩟"),
            bstack1l1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲ᩠ࠢ"): env.get(bstack1l1_opy_ (u"ࠧ࡝ࡅࡓࡅࡎࡉࡗࡥࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠤᩡ")),
            bstack1l1_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᩢ"): bstack1l1_opy_ (u"ࠢࡎࡣ࡬ࡲࠥࡖࡩࡱࡧ࡯࡭ࡳ࡫ࠢᩣ") if env.get(bstack1l1_opy_ (u"࡙ࠣࡈࡖࡈࡑࡅࡓࡡࡐࡅࡎࡔ࡟ࡑࡋࡓࡉࡑࡏࡎࡆࡡࡖࡘࡆࡘࡔࡆࡆࠥᩤ")) else None,
            bstack1l1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᩥ"): env.get(bstack1l1_opy_ (u"࡛ࠥࡊࡘࡃࡌࡇࡕࡣࡌࡏࡔࡠࡅࡒࡑࡒࡏࡔࠣᩦ"))
        }
    if any([env.get(bstack1l1_opy_ (u"ࠦࡌࡉࡐࡠࡒࡕࡓࡏࡋࡃࡕࠤᩧ")), env.get(bstack1l1_opy_ (u"ࠧࡍࡃࡍࡑࡘࡈࡤࡖࡒࡐࡌࡈࡇ࡙ࠨᩨ")), env.get(bstack1l1_opy_ (u"ࠨࡇࡐࡑࡊࡐࡊࡥࡃࡍࡑࡘࡈࡤࡖࡒࡐࡌࡈࡇ࡙ࠨᩩ"))]):
        return {
            bstack1l1_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᩪ"): bstack1l1_opy_ (u"ࠣࡉࡲࡳ࡬ࡲࡥࠡࡅ࡯ࡳࡺࡪࠢᩫ"),
            bstack1l1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᩬ"): None,
            bstack1l1_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᩭ"): env.get(bstack1l1_opy_ (u"ࠦࡕࡘࡏࡋࡇࡆࡘࡤࡏࡄࠣᩮ")),
            bstack1l1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᩯ"): env.get(bstack1l1_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤࡏࡄࠣᩰ"))
        }
    if env.get(bstack1l1_opy_ (u"ࠢࡔࡊࡌࡔࡕࡇࡂࡍࡇࠥᩱ")):
        return {
            bstack1l1_opy_ (u"ࠣࡰࡤࡱࡪࠨᩲ"): bstack1l1_opy_ (u"ࠤࡖ࡬࡮ࡶࡰࡢࡤ࡯ࡩࠧᩳ"),
            bstack1l1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᩴ"): env.get(bstack1l1_opy_ (u"ࠦࡘࡎࡉࡑࡒࡄࡆࡑࡋ࡟ࡃࡗࡌࡐࡉࡥࡕࡓࡎࠥ᩵")),
            bstack1l1_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢ᩶"): bstack1l1_opy_ (u"ࠨࡊࡰࡤࠣࠧࢀࢃࠢ᩷").format(env.get(bstack1l1_opy_ (u"ࠧࡔࡊࡌࡔࡕࡇࡂࡍࡇࡢࡎࡔࡈ࡟ࡊࡆࠪ᩸"))) if env.get(bstack1l1_opy_ (u"ࠣࡕࡋࡍࡕࡖࡁࡃࡎࡈࡣࡏࡕࡂࡠࡋࡇࠦ᩹")) else None,
            bstack1l1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣ᩺"): env.get(bstack1l1_opy_ (u"ࠥࡗࡍࡏࡐࡑࡃࡅࡐࡊࡥࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࠧ᩻"))
        }
    if bstack111llll11_opy_(env.get(bstack1l1_opy_ (u"ࠦࡓࡋࡔࡍࡋࡉ࡝ࠧ᩼"))):
        return {
            bstack1l1_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ᩽"): bstack1l1_opy_ (u"ࠨࡎࡦࡶ࡯࡭࡫ࡿࠢ᩾"),
            bstack1l1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮᩿ࠥ"): env.get(bstack1l1_opy_ (u"ࠣࡆࡈࡔࡑࡕ࡙ࡠࡗࡕࡐࠧ᪀")),
            bstack1l1_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦ᪁"): env.get(bstack1l1_opy_ (u"ࠥࡗࡎ࡚ࡅࡠࡐࡄࡑࡊࠨ᪂")),
            bstack1l1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥ᪃"): env.get(bstack1l1_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡎࡊࠢ᪄"))
        }
    if bstack111llll11_opy_(env.get(bstack1l1_opy_ (u"ࠨࡇࡊࡖࡋ࡙ࡇࡥࡁࡄࡖࡌࡓࡓ࡙ࠢ᪅"))):
        return {
            bstack1l1_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ᪆"): bstack1l1_opy_ (u"ࠣࡉ࡬ࡸࡍࡻࡢࠡࡃࡦࡸ࡮ࡵ࡮ࡴࠤ᪇"),
            bstack1l1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧ᪈"): bstack1l1_opy_ (u"ࠥࡿࢂ࠵ࡻࡾ࠱ࡤࡧࡹ࡯࡯࡯ࡵ࠲ࡶࡺࡴࡳ࠰ࡽࢀࠦ᪉").format(env.get(bstack1l1_opy_ (u"ࠫࡌࡏࡔࡉࡗࡅࡣࡘࡋࡒࡗࡇࡕࡣ࡚ࡘࡌࠨ᪊")), env.get(bstack1l1_opy_ (u"ࠬࡍࡉࡕࡊࡘࡆࡤࡘࡅࡑࡑࡖࡍ࡙ࡕࡒ࡚ࠩ᪋")), env.get(bstack1l1_opy_ (u"࠭ࡇࡊࡖࡋ࡙ࡇࡥࡒࡖࡐࡢࡍࡉ࠭᪌"))),
            bstack1l1_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤ᪍"): env.get(bstack1l1_opy_ (u"ࠣࡉࡌࡘࡍ࡛ࡂࡠ࡙ࡒࡖࡐࡌࡌࡐ࡙ࠥ᪎")),
            bstack1l1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣ᪏"): env.get(bstack1l1_opy_ (u"ࠥࡋࡎ࡚ࡈࡖࡄࡢࡖ࡚ࡔ࡟ࡊࡆࠥ᪐"))
        }
    if env.get(bstack1l1_opy_ (u"ࠦࡈࡏࠢ᪑")) == bstack1l1_opy_ (u"ࠧࡺࡲࡶࡧࠥ᪒") and env.get(bstack1l1_opy_ (u"ࠨࡖࡆࡔࡆࡉࡑࠨ᪓")) == bstack1l1_opy_ (u"ࠢ࠲ࠤ᪔"):
        return {
            bstack1l1_opy_ (u"ࠣࡰࡤࡱࡪࠨ᪕"): bstack1l1_opy_ (u"ࠤ࡙ࡩࡷࡩࡥ࡭ࠤ᪖"),
            bstack1l1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨ᪗"): bstack1l1_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳ࢀࢃࠢ᪘").format(env.get(bstack1l1_opy_ (u"ࠬ࡜ࡅࡓࡅࡈࡐࡤ࡛ࡒࡍࠩ᪙"))),
            bstack1l1_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣ᪚"): None,
            bstack1l1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ᪛"): None,
        }
    if env.get(bstack1l1_opy_ (u"ࠣࡖࡈࡅࡒࡉࡉࡕ࡛ࡢ࡚ࡊࡘࡓࡊࡑࡑࠦ᪜")):
        return {
            bstack1l1_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ᪝"): bstack1l1_opy_ (u"ࠥࡘࡪࡧ࡭ࡤ࡫ࡷࡽࠧ᪞"),
            bstack1l1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢ᪟"): None,
            bstack1l1_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢ᪠"): env.get(bstack1l1_opy_ (u"ࠨࡔࡆࡃࡐࡇࡎ࡚࡙ࡠࡒࡕࡓࡏࡋࡃࡕࡡࡑࡅࡒࡋࠢ᪡")),
            bstack1l1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ᪢"): env.get(bstack1l1_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠢ᪣"))
        }
    if any([env.get(bstack1l1_opy_ (u"ࠤࡆࡓࡓࡉࡏࡖࡔࡖࡉࠧ᪤")), env.get(bstack1l1_opy_ (u"ࠥࡇࡔࡔࡃࡐࡗࡕࡗࡊࡥࡕࡓࡎࠥ᪥")), env.get(bstack1l1_opy_ (u"ࠦࡈࡕࡎࡄࡑࡘࡖࡘࡋ࡟ࡖࡕࡈࡖࡓࡇࡍࡆࠤ᪦")), env.get(bstack1l1_opy_ (u"ࠧࡉࡏࡏࡅࡒ࡙ࡗ࡙ࡅࡠࡖࡈࡅࡒࠨᪧ"))]):
        return {
            bstack1l1_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ᪨"): bstack1l1_opy_ (u"ࠢࡄࡱࡱࡧࡴࡻࡲࡴࡧࠥ᪩"),
            bstack1l1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦ᪪"): None,
            bstack1l1_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦ᪫"): env.get(bstack1l1_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡍࡓࡇࡥࡎࡂࡏࡈࠦ᪬")) or None,
            bstack1l1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥ᪭"): env.get(bstack1l1_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡎࡊࠢ᪮"), 0)
        }
    if env.get(bstack1l1_opy_ (u"ࠨࡇࡐࡡࡍࡓࡇࡥࡎࡂࡏࡈࠦ᪯")):
        return {
            bstack1l1_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ᪰"): bstack1l1_opy_ (u"ࠣࡉࡲࡇࡉࠨ᪱"),
            bstack1l1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧ᪲"): None,
            bstack1l1_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧ᪳"): env.get(bstack1l1_opy_ (u"ࠦࡌࡕ࡟ࡋࡑࡅࡣࡓࡇࡍࡆࠤ᪴")),
            bstack1l1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵ᪵ࠦ"): env.get(bstack1l1_opy_ (u"ࠨࡇࡐࡡࡓࡍࡕࡋࡌࡊࡐࡈࡣࡈࡕࡕࡏࡖࡈࡖ᪶ࠧ"))
        }
    if env.get(bstack1l1_opy_ (u"ࠢࡄࡈࡢࡆ࡚ࡏࡌࡅࡡࡌࡈ᪷ࠧ")):
        return {
            bstack1l1_opy_ (u"ࠣࡰࡤࡱࡪࠨ᪸"): bstack1l1_opy_ (u"ࠤࡆࡳࡩ࡫ࡆࡳࡧࡶ࡬᪹ࠧ"),
            bstack1l1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨ᪺"): env.get(bstack1l1_opy_ (u"ࠦࡈࡌ࡟ࡃࡗࡌࡐࡉࡥࡕࡓࡎࠥ᪻")),
            bstack1l1_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢ᪼"): env.get(bstack1l1_opy_ (u"ࠨࡃࡇࡡࡓࡍࡕࡋࡌࡊࡐࡈࡣࡓࡇࡍࡆࠤ᪽")),
            bstack1l1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ᪾"): env.get(bstack1l1_opy_ (u"ࠣࡅࡉࡣࡇ࡛ࡉࡍࡆࡢࡍࡉࠨᪿ"))
        }
    return {bstack1l1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲᫀࠣ"): None}
def get_host_info():
    return {
        bstack1l1_opy_ (u"ࠥ࡬ࡴࡹࡴ࡯ࡣࡰࡩࠧ᫁"): platform.node(),
        bstack1l1_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲࠨ᫂"): platform.system(),
        bstack1l1_opy_ (u"ࠧࡺࡹࡱࡧ᫃ࠥ"): platform.machine(),
        bstack1l1_opy_ (u"ࠨࡶࡦࡴࡶ࡭ࡴࡴ᫄ࠢ"): platform.version(),
        bstack1l1_opy_ (u"ࠢࡢࡴࡦ࡬ࠧ᫅"): platform.architecture()[0]
    }
def bstack1l11l1l1_opy_():
    try:
        import selenium
        return True
    except ImportError:
        return False
def bstack11l1l1l1l1l_opy_():
    if bstack11llllll1_opy_.get_property(bstack1l1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡵࡨࡷࡸ࡯࡯࡯ࠩ᫆")):
        return bstack1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨ᫇")
    return bstack1l1_opy_ (u"ࠪࡹࡳࡱ࡮ࡰࡹࡱࡣ࡬ࡸࡩࡥࠩ᫈")
def bstack11l1llllll1_opy_(driver):
    info = {
        bstack1l1_opy_ (u"ࠫࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪ᫉"): driver.capabilities,
        bstack1l1_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡥࡩࡥ᫊ࠩ"): driver.session_id,
        bstack1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࠧ᫋"): driver.capabilities.get(bstack1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬᫌ"), None),
        bstack1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠪᫍ"): driver.capabilities.get(bstack1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪᫎ"), None),
        bstack1l1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࠬ᫏"): driver.capabilities.get(bstack1l1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡔࡡ࡮ࡧࠪ᫐"), None),
        bstack1l1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ᫑"):driver.capabilities.get(bstack1l1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨ᫒"), None),
    }
    if bstack11l1l1l1l1l_opy_() == bstack1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭᫓"):
        if bstack1ll1l1ll11_opy_():
            info[bstack1l1_opy_ (u"ࠨࡲࡵࡳࡩࡻࡣࡵࠩ᫔")] = bstack1l1_opy_ (u"ࠩࡤࡴࡵ࠳ࡡࡶࡶࡲࡱࡦࡺࡥࠨ᫕")
        elif driver.capabilities.get(bstack1l1_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫ᫖"), {}).get(bstack1l1_opy_ (u"ࠫࡹࡻࡲࡣࡱࡶࡧࡦࡲࡥࠨ᫗"), False):
            info[bstack1l1_opy_ (u"ࠬࡶࡲࡰࡦࡸࡧࡹ࠭᫘")] = bstack1l1_opy_ (u"࠭ࡴࡶࡴࡥࡳࡸࡩࡡ࡭ࡧࠪ᫙")
        else:
            info[bstack1l1_opy_ (u"ࠧࡱࡴࡲࡨࡺࡩࡴࠨ᫚")] = bstack1l1_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵࡧࠪ᫛")
    return info
def bstack1ll1l1ll11_opy_():
    if bstack11llllll1_opy_.get_property(bstack1l1_opy_ (u"ࠩࡤࡴࡵࡥࡡࡶࡶࡲࡱࡦࡺࡥࠨ᫜")):
        return True
    if bstack111llll11_opy_(os.environ.get(bstack1l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡌࡗࡤࡇࡐࡑࡡࡄ࡙࡙ࡕࡍࡂࡖࡈࠫ᫝"), None)):
        return True
    return False
def bstack111lll111_opy_(bstack11l1lllllll_opy_, url, data, config):
    headers = config.get(bstack1l1_opy_ (u"ࠫ࡭࡫ࡡࡥࡧࡵࡷࠬ᫞"), None)
    proxies = bstack11ll1llll_opy_(config, url)
    auth = config.get(bstack1l1_opy_ (u"ࠬࡧࡵࡵࡪࠪ᫟"), None)
    response = requests.request(
            bstack11l1lllllll_opy_,
            url=url,
            headers=headers,
            auth=auth,
            json=data,
            proxies=proxies
        )
    return response
def bstack11ll11lll_opy_(bstack1l111l1l1_opy_, size):
    bstack111l11ll_opy_ = []
    while len(bstack1l111l1l1_opy_) > size:
        bstack1l111ll1l1_opy_ = bstack1l111l1l1_opy_[:size]
        bstack111l11ll_opy_.append(bstack1l111ll1l1_opy_)
        bstack1l111l1l1_opy_ = bstack1l111l1l1_opy_[size:]
    bstack111l11ll_opy_.append(bstack1l111l1l1_opy_)
    return bstack111l11ll_opy_
def bstack11l1l111l11_opy_(message, bstack11l1l1ll1l1_opy_=False):
    os.write(1, bytes(message, bstack1l1_opy_ (u"࠭ࡵࡵࡨ࠰࠼ࠬ᫠")))
    os.write(1, bytes(bstack1l1_opy_ (u"ࠧ࡝ࡰࠪ᫡"), bstack1l1_opy_ (u"ࠨࡷࡷࡪ࠲࠾ࠧ᫢")))
    if bstack11l1l1ll1l1_opy_:
        with open(bstack1l1_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠯ࡲ࠵࠶ࡿ࠭ࠨ᫣") + os.environ[bstack1l1_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡃࡗࡌࡐࡉࡥࡈࡂࡕࡋࡉࡉࡥࡉࡅࠩ᫤")] + bstack1l1_opy_ (u"ࠫ࠳ࡲ࡯ࡨࠩ᫥"), bstack1l1_opy_ (u"ࠬࡧࠧ᫦")) as f:
            f.write(message + bstack1l1_opy_ (u"࠭࡜࡯ࠩ᫧"))
def bstack1ll111l1ll1_opy_():
    return os.environ[bstack1l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡖࡖࡒࡑࡆ࡚ࡉࡐࡐࠪ᫨")].lower() == bstack1l1_opy_ (u"ࠨࡶࡵࡹࡪ࠭᫩")
def bstack1l11111ll1_opy_(bstack11l1l1l1lll_opy_):
    return bstack1l1_opy_ (u"ࠩࡾࢁ࠴ࢁࡽࠨ᫪").format(bstack11ll1l1ll1l_opy_, bstack11l1l1l1lll_opy_)
def bstack11l1l11ll1_opy_():
    return bstack111ll11ll1_opy_().replace(tzinfo=None).isoformat() + bstack1l1_opy_ (u"ࠪ࡞ࠬ᫫")
def bstack11l1l111ll1_opy_(start, finish):
    return (datetime.datetime.fromisoformat(finish.rstrip(bstack1l1_opy_ (u"ࠫ࡟࠭᫬"))) - datetime.datetime.fromisoformat(start.rstrip(bstack1l1_opy_ (u"ࠬࡠࠧ᫭")))).total_seconds() * 1000
def bstack11l1l11l1ll_opy_(timestamp):
    return bstack11l1l111lll_opy_(timestamp).isoformat() + bstack1l1_opy_ (u"࡚࠭ࠨ᫮")
def bstack11l1l11llll_opy_(bstack11ll11l1l11_opy_):
    date_format = bstack1l1_opy_ (u"࡛ࠧࠦࠨࡱࠪࡪࠠࠦࡊ࠽ࠩࡒࡀࠥࡔ࠰ࠨࡪࠬ᫯")
    bstack11l1l1ll1ll_opy_ = datetime.datetime.strptime(bstack11ll11l1l11_opy_, date_format)
    return bstack11l1l1ll1ll_opy_.isoformat() + bstack1l1_opy_ (u"ࠨ࡜ࠪ᫰")
def bstack11l1ll1l111_opy_(outcome):
    _, exception, _ = outcome.excinfo or (None, None, None)
    if exception:
        return bstack1l1_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ᫱")
    else:
        return bstack1l1_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪ᫲")
def bstack111llll11_opy_(val):
    if val is None:
        return False
    return val.__str__().lower() == bstack1l1_opy_ (u"ࠫࡹࡸࡵࡦࠩ᫳")
def bstack11ll111l1ll_opy_(val):
    return val.__str__().lower() == bstack1l1_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫ᫴")
def bstack111l1ll1l1_opy_(bstack11l1lll11ll_opy_=Exception, class_method=False, default_value=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except bstack11l1lll11ll_opy_ as e:
                print(bstack1l1_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠠࡼࡿࠣ࠱ࡃࠦࡻࡾ࠼ࠣࡿࢂࠨ᫵").format(func.__name__, bstack11l1lll11ll_opy_.__name__, str(e)))
                return default_value
        return wrapper
    def bstack11ll111ll11_opy_(bstack11ll11111l1_opy_):
        def wrapped(cls, *args, **kwargs):
            try:
                return bstack11ll11111l1_opy_(cls, *args, **kwargs)
            except bstack11l1lll11ll_opy_ as e:
                print(bstack1l1_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠡࡽࢀࠤ࠲ࡄࠠࡼࡿ࠽ࠤࢀࢃࠢ᫶").format(bstack11ll11111l1_opy_.__name__, bstack11l1lll11ll_opy_.__name__, str(e)))
                return default_value
        return wrapped
    if class_method:
        return bstack11ll111ll11_opy_
    else:
        return decorator
def bstack1lll1lll1l_opy_(bstack1111lll1ll_opy_):
    if os.getenv(bstack1l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡗࡗࡓࡒࡇࡔࡊࡑࡑࠫ᫷")) is not None:
        return bstack111llll11_opy_(os.getenv(bstack1l1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡘࡘࡔࡓࡁࡕࡋࡒࡒࠬ᫸")))
    if bstack1l1_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧ᫹") in bstack1111lll1ll_opy_ and bstack11ll111l1ll_opy_(bstack1111lll1ll_opy_[bstack1l1_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨ᫺")]):
        return False
    if bstack1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧ᫻") in bstack1111lll1ll_opy_ and bstack11ll111l1ll_opy_(bstack1111lll1ll_opy_[bstack1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨ᫼")]):
        return False
    return True
def bstack11111l1l1_opy_():
    try:
        from pytest_bdd import reporting
        bstack11l1llll111_opy_ = os.environ.get(bstack1l1_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡕࡔࡇࡕࡣࡋࡘࡁࡎࡇ࡚ࡓࡗࡑࠢ᫽"), None)
        return bstack11l1llll111_opy_ is None or bstack11l1llll111_opy_ == bstack1l1_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠧ᫾")
    except Exception as e:
        return False
def bstack1l1ll1l1ll_opy_(hub_url, CONFIG):
    if bstack11ll1ll11l_opy_() <= version.parse(bstack1l1_opy_ (u"ࠩ࠶࠲࠶࠹࠮࠱ࠩ᫿")):
        if hub_url:
            return bstack1l1_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻࠱࠲ࠦᬀ") + hub_url + bstack1l1_opy_ (u"ࠦ࠿࠾࠰࠰ࡹࡧ࠳࡭ࡻࡢࠣᬁ")
        return bstack1ll111111_opy_
    if hub_url:
        return bstack1l1_opy_ (u"ࠧ࡮ࡴࡵࡲࡶ࠾࠴࠵ࠢᬂ") + hub_url + bstack1l1_opy_ (u"ࠨ࠯ࡸࡦ࠲࡬ࡺࡨࠢᬃ")
    return bstack11ll1lll11_opy_
def bstack11l1l1l1l11_opy_():
    return isinstance(os.getenv(bstack1l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐ࡚ࡖࡈࡗ࡙ࡥࡐࡍࡗࡊࡍࡓ࠭ᬄ")), str)
def bstack1l1l1111_opy_(url):
    return urlparse(url).hostname
def bstack1lll111l1_opy_(hostname):
    for bstack11ll1ll1l1_opy_ in bstack1lllll1l1_opy_:
        regex = re.compile(bstack11ll1ll1l1_opy_)
        if regex.match(hostname):
            return True
    return False
def bstack11l1l11lll1_opy_(bstack11ll1111111_opy_, file_name, logger):
    bstack1llll111l1_opy_ = os.path.join(os.path.expanduser(bstack1l1_opy_ (u"ࠨࢀࠪᬅ")), bstack11ll1111111_opy_)
    try:
        if not os.path.exists(bstack1llll111l1_opy_):
            os.makedirs(bstack1llll111l1_opy_)
        file_path = os.path.join(os.path.expanduser(bstack1l1_opy_ (u"ࠩࢁࠫᬆ")), bstack11ll1111111_opy_, file_name)
        if not os.path.isfile(file_path):
            with open(file_path, bstack1l1_opy_ (u"ࠪࡻࠬᬇ")):
                pass
            with open(file_path, bstack1l1_opy_ (u"ࠦࡼ࠱ࠢᬈ")) as outfile:
                json.dump({}, outfile)
        return file_path
    except Exception as e:
        logger.debug(bstack11lll1l111_opy_.format(str(e)))
def bstack11l1ll11lll_opy_(file_name, key, value, logger):
    file_path = bstack11l1l11lll1_opy_(bstack1l1_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬᬉ"), file_name, logger)
    if file_path != None:
        if os.path.exists(file_path):
            bstack1ll1l11ll_opy_ = json.load(open(file_path, bstack1l1_opy_ (u"࠭ࡲࡣࠩᬊ")))
        else:
            bstack1ll1l11ll_opy_ = {}
        bstack1ll1l11ll_opy_[key] = value
        with open(file_path, bstack1l1_opy_ (u"ࠢࡸ࠭ࠥᬋ")) as outfile:
            json.dump(bstack1ll1l11ll_opy_, outfile)
def bstack1111l1ll1_opy_(file_name, logger):
    file_path = bstack11l1l11lll1_opy_(bstack1l1_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨᬌ"), file_name, logger)
    bstack1ll1l11ll_opy_ = {}
    if file_path != None and os.path.exists(file_path):
        with open(file_path, bstack1l1_opy_ (u"ࠩࡵࠫᬍ")) as bstack1l1l111lll_opy_:
            bstack1ll1l11ll_opy_ = json.load(bstack1l1l111lll_opy_)
    return bstack1ll1l11ll_opy_
def bstack1lll1l1l_opy_(file_path, logger):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        logger.debug(bstack1l1_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡪࡥ࡭ࡧࡷ࡭ࡳ࡭ࠠࡧ࡫࡯ࡩ࠿ࠦࠧᬎ") + file_path + bstack1l1_opy_ (u"ࠫࠥ࠭ᬏ") + str(e))
def bstack11ll1ll11l_opy_():
    from selenium import webdriver
    return version.parse(webdriver.__version__)
class Notset:
    def __repr__(self):
        return bstack1l1_opy_ (u"ࠧࡂࡎࡐࡖࡖࡉ࡙ࡄࠢᬐ")
def bstack1lll1l1l11_opy_(config):
    if bstack1l1_opy_ (u"࠭ࡩࡴࡒ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠬᬑ") in config:
        del (config[bstack1l1_opy_ (u"ࠧࡪࡵࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠭ᬒ")])
        return False
    if bstack11ll1ll11l_opy_() < version.parse(bstack1l1_opy_ (u"ࠨ࠵࠱࠸࠳࠶ࠧᬓ")):
        return False
    if bstack11ll1ll11l_opy_() >= version.parse(bstack1l1_opy_ (u"ࠩ࠷࠲࠶࠴࠵ࠨᬔ")):
        return True
    if bstack1l1_opy_ (u"ࠪࡹࡸ࡫ࡗ࠴ࡅࠪᬕ") in config and config[bstack1l1_opy_ (u"ࠫࡺࡹࡥࡘ࠵ࡆࠫᬖ")] is False:
        return False
    else:
        return True
def bstack1lllll1111_opy_(args_list, bstack11l1l1l1ll1_opy_):
    index = -1
    for value in bstack11l1l1l1ll1_opy_:
        try:
            index = args_list.index(value)
            return index
        except Exception as e:
            return index
    return index
class Result:
    def __init__(self, result=None, duration=None, exception=None, bstack11l111lll1_opy_=None):
        self.result = result
        self.duration = duration
        self.exception = exception
        self.exception_type = type(self.exception).__name__ if exception else None
        self.bstack11l111lll1_opy_ = bstack11l111lll1_opy_
    @classmethod
    def passed(cls):
        return Result(result=bstack1l1_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬᬗ"))
    @classmethod
    def failed(cls, exception=None):
        return Result(result=bstack1l1_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ᬘ"), exception=exception)
    def bstack1111ll11l1_opy_(self):
        if self.result != bstack1l1_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧᬙ"):
            return None
        if isinstance(self.exception_type, str) and bstack1l1_opy_ (u"ࠣࡃࡶࡷࡪࡸࡴࡪࡱࡱࠦᬚ") in self.exception_type:
            return bstack1l1_opy_ (u"ࠤࡄࡷࡸ࡫ࡲࡵ࡫ࡲࡲࡊࡸࡲࡰࡴࠥᬛ")
        return bstack1l1_opy_ (u"࡙ࠥࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࡋࡲࡳࡱࡵࠦᬜ")
    def bstack11l1l11111l_opy_(self):
        if self.result != bstack1l1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᬝ"):
            return None
        if self.bstack11l111lll1_opy_:
            return self.bstack11l111lll1_opy_
        return bstack11l1ll1ll11_opy_(self.exception)
def bstack11l1ll1ll11_opy_(exc):
    return [traceback.format_exception(exc)]
def bstack11l1l1lll1l_opy_(message):
    if isinstance(message, str):
        return not bool(message and message.strip())
    return True
def bstack1l1l11l1l_opy_(object, key, default_value):
    if not object or not object.__dict__:
        return default_value
    if key in object.__dict__.keys():
        return object.__dict__.get(key)
    return default_value
def bstack11l111l1_opy_(config, logger):
    try:
        import playwright
        bstack11l1l1111l1_opy_ = playwright.__file__
        bstack11l11llllll_opy_ = os.path.split(bstack11l1l1111l1_opy_)
        bstack11ll111llll_opy_ = bstack11l11llllll_opy_[0] + bstack1l1_opy_ (u"ࠬ࠵ࡤࡳ࡫ࡹࡩࡷ࠵ࡰࡢࡥ࡮ࡥ࡬࡫࠯࡭࡫ࡥ࠳ࡨࡲࡩ࠰ࡥ࡯࡭࠳ࡰࡳࠨᬞ")
        os.environ[bstack1l1_opy_ (u"࠭ࡇࡍࡑࡅࡅࡑࡥࡁࡈࡇࡑࡘࡤࡎࡔࡕࡒࡢࡔࡗࡕࡘ࡚ࠩᬟ")] = bstack1lll11l111_opy_(config)
        with open(bstack11ll111llll_opy_, bstack1l1_opy_ (u"ࠧࡳࠩᬠ")) as f:
            bstack1l1ll11l1_opy_ = f.read()
            bstack11ll11l1l1l_opy_ = bstack1l1_opy_ (u"ࠨࡩ࡯ࡳࡧࡧ࡬࠮ࡣࡪࡩࡳࡺࠧᬡ")
            bstack11l1l1l111l_opy_ = bstack1l1ll11l1_opy_.find(bstack11ll11l1l1l_opy_)
            if bstack11l1l1l111l_opy_ == -1:
              process = subprocess.Popen(bstack1l1_opy_ (u"ࠤࡱࡴࡲࠦࡩ࡯ࡵࡷࡥࡱࡲࠠࡨ࡮ࡲࡦࡦࡲ࠭ࡢࡩࡨࡲࡹࠨᬢ"), shell=True, cwd=bstack11l11llllll_opy_[0])
              process.wait()
              bstack11l1l1lll11_opy_ = bstack1l1_opy_ (u"ࠪࠦࡺࡹࡥࠡࡵࡷࡶ࡮ࡩࡴࠣ࠽ࠪᬣ")
              bstack11ll11111ll_opy_ = bstack1l1_opy_ (u"ࠦࠧࠨࠠ࡝ࠤࡸࡷࡪࠦࡳࡵࡴ࡬ࡧࡹࡢࠢ࠼ࠢࡦࡳࡳࡹࡴࠡࡽࠣࡦࡴࡵࡴࡴࡶࡵࡥࡵࠦࡽࠡ࠿ࠣࡶࡪࡷࡵࡪࡴࡨࠬࠬ࡭࡬ࡰࡤࡤࡰ࠲ࡧࡧࡦࡰࡷࠫ࠮ࡁࠠࡪࡨࠣࠬࡵࡸ࡯ࡤࡧࡶࡷ࠳࡫࡮ࡷ࠰ࡊࡐࡔࡈࡁࡍࡡࡄࡋࡊࡔࡔࡠࡊࡗࡘࡕࡥࡐࡓࡑ࡛࡝࠮ࠦࡢࡰࡱࡷࡷࡹࡸࡡࡱࠪࠬ࠿ࠥࠨࠢࠣᬤ")
              bstack11l1l11l111_opy_ = bstack1l1ll11l1_opy_.replace(bstack11l1l1lll11_opy_, bstack11ll11111ll_opy_)
              with open(bstack11ll111llll_opy_, bstack1l1_opy_ (u"ࠬࡽࠧᬥ")) as f:
                f.write(bstack11l1l11l111_opy_)
    except Exception as e:
        logger.error(bstack1111ll1ll_opy_.format(str(e)))
def bstack11l1l11ll_opy_():
  try:
    bstack11l1lllll1l_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1_opy_ (u"࠭࡯ࡱࡶ࡬ࡱࡦࡲ࡟ࡩࡷࡥࡣࡺࡸ࡬࠯࡬ࡶࡳࡳ࠭ᬦ"))
    bstack11l1ll1111l_opy_ = []
    if os.path.exists(bstack11l1lllll1l_opy_):
      with open(bstack11l1lllll1l_opy_) as f:
        bstack11l1ll1111l_opy_ = json.load(f)
      os.remove(bstack11l1lllll1l_opy_)
    return bstack11l1ll1111l_opy_
  except:
    pass
  return []
def bstack1ll1lll1_opy_(bstack1ll1111ll_opy_):
  try:
    bstack11l1ll1111l_opy_ = []
    bstack11l1lllll1l_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1_opy_ (u"ࠧࡰࡲࡷ࡭ࡲࡧ࡬ࡠࡪࡸࡦࡤࡻࡲ࡭࠰࡭ࡷࡴࡴࠧᬧ"))
    if os.path.exists(bstack11l1lllll1l_opy_):
      with open(bstack11l1lllll1l_opy_) as f:
        bstack11l1ll1111l_opy_ = json.load(f)
    bstack11l1ll1111l_opy_.append(bstack1ll1111ll_opy_)
    with open(bstack11l1lllll1l_opy_, bstack1l1_opy_ (u"ࠨࡹࠪᬨ")) as f:
        json.dump(bstack11l1ll1111l_opy_, f)
  except:
    pass
def bstack11llll1111_opy_(logger, bstack11ll11ll111_opy_ = False):
  try:
    test_name = os.environ.get(bstack1l1_opy_ (u"ࠩࡓ࡝࡙ࡋࡓࡕࡡࡗࡉࡘ࡚࡟ࡏࡃࡐࡉࠬᬩ"), bstack1l1_opy_ (u"ࠪࠫᬪ"))
    if test_name == bstack1l1_opy_ (u"ࠫࠬᬫ"):
        test_name = threading.current_thread().__dict__.get(bstack1l1_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࡇࡪࡤࡠࡶࡨࡷࡹࡥ࡮ࡢ࡯ࡨࠫᬬ"), bstack1l1_opy_ (u"࠭ࠧᬭ"))
    bstack11ll11l11ll_opy_ = bstack1l1_opy_ (u"ࠧ࠭ࠢࠪᬮ").join(threading.current_thread().bstackTestErrorMessages)
    if bstack11ll11ll111_opy_:
        bstack11ll11ll11_opy_ = os.environ.get(bstack1l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨᬯ"), bstack1l1_opy_ (u"ࠩ࠳ࠫᬰ"))
        bstack11lll111_opy_ = {bstack1l1_opy_ (u"ࠪࡲࡦࡳࡥࠨᬱ"): test_name, bstack1l1_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪᬲ"): bstack11ll11l11ll_opy_, bstack1l1_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫᬳ"): bstack11ll11ll11_opy_}
        bstack11l1l111l1l_opy_ = []
        bstack11l11llll11_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹࡥࡰࡱࡲࡢࡩࡷࡸ࡯ࡳࡡ࡯࡭ࡸࡺ࠮࡫ࡵࡲࡲ᬴ࠬ"))
        if os.path.exists(bstack11l11llll11_opy_):
            with open(bstack11l11llll11_opy_) as f:
                bstack11l1l111l1l_opy_ = json.load(f)
        bstack11l1l111l1l_opy_.append(bstack11lll111_opy_)
        with open(bstack11l11llll11_opy_, bstack1l1_opy_ (u"ࠧࡸࠩᬵ")) as f:
            json.dump(bstack11l1l111l1l_opy_, f)
    else:
        bstack11lll111_opy_ = {bstack1l1_opy_ (u"ࠨࡰࡤࡱࡪ࠭ᬶ"): test_name, bstack1l1_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨᬷ"): bstack11ll11l11ll_opy_, bstack1l1_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩᬸ"): str(multiprocessing.current_process().name)}
        if bstack1l1_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡪࡸࡲࡰࡴࡢࡰ࡮ࡹࡴࠨᬹ") not in multiprocessing.current_process().__dict__.keys():
            multiprocessing.current_process().bstack_error_list = []
        multiprocessing.current_process().bstack_error_list.append(bstack11lll111_opy_)
  except Exception as e:
      logger.warn(bstack1l1_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡵࡷࡳࡷ࡫ࠠࡱࡻࡷࡩࡸࡺࠠࡧࡷࡱࡲࡪࡲࠠࡥࡣࡷࡥ࠿ࠦࡻࡾࠤᬺ").format(e))
def bstack111lllll_opy_(error_message, test_name, index, logger):
  try:
    bstack11l1l111111_opy_ = []
    bstack11lll111_opy_ = {bstack1l1_opy_ (u"࠭࡮ࡢ࡯ࡨࠫᬻ"): test_name, bstack1l1_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ᬼ"): error_message, bstack1l1_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧᬽ"): index}
    bstack11ll111111l_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1_opy_ (u"ࠩࡵࡳࡧࡵࡴࡠࡧࡵࡶࡴࡸ࡟࡭࡫ࡶࡸ࠳ࡰࡳࡰࡰࠪᬾ"))
    if os.path.exists(bstack11ll111111l_opy_):
        with open(bstack11ll111111l_opy_) as f:
            bstack11l1l111111_opy_ = json.load(f)
    bstack11l1l111111_opy_.append(bstack11lll111_opy_)
    with open(bstack11ll111111l_opy_, bstack1l1_opy_ (u"ࠪࡻࠬᬿ")) as f:
        json.dump(bstack11l1l111111_opy_, f)
  except Exception as e:
    logger.warn(bstack1l1_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡴࡶࡲࡶࡪࠦࡲࡰࡤࡲࡸࠥ࡬ࡵ࡯ࡰࡨࡰࠥࡪࡡࡵࡣ࠽ࠤࢀࢃࠢᭀ").format(e))
def bstack1l11l1ll1l_opy_(bstack11ll1ll111_opy_, name, logger):
  try:
    bstack11lll111_opy_ = {bstack1l1_opy_ (u"ࠬࡴࡡ࡮ࡧࠪᭁ"): name, bstack1l1_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬᭂ"): bstack11ll1ll111_opy_, bstack1l1_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭ᭃ"): str(threading.current_thread()._name)}
    return bstack11lll111_opy_
  except Exception as e:
    logger.warn(bstack1l1_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸࡺ࡯ࡳࡧࠣࡦࡪ࡮ࡡࡷࡧࠣࡪࡺࡴ࡮ࡦ࡮ࠣࡨࡦࡺࡡ࠻ࠢࡾࢁ᭄ࠧ").format(e))
  return
def bstack11l1lllll11_opy_():
    return platform.system() == bstack1l1_opy_ (u"࡚ࠩ࡭ࡳࡪ࡯ࡸࡵࠪᭅ")
def bstack11l11l1lll_opy_(bstack11l1l1ll11l_opy_, config, logger):
    bstack11ll111l11l_opy_ = {}
    try:
        return {key: config[key] for key in config if bstack11l1l1ll11l_opy_.match(key)}
    except Exception as e:
        logger.debug(bstack1l1_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡦࡪ࡮ࡷࡩࡷࠦࡣࡰࡰࡩ࡭࡬ࠦ࡫ࡦࡻࡶࠤࡧࡿࠠࡳࡧࡪࡩࡽࠦ࡭ࡢࡶࡦ࡬࠿ࠦࡻࡾࠤᭆ").format(e))
    return bstack11ll111l11l_opy_
def bstack11l1l1111ll_opy_(bstack11l1lll111l_opy_, bstack11ll11lll1l_opy_):
    bstack11ll11l1111_opy_ = version.parse(bstack11l1lll111l_opy_)
    bstack11ll111l111_opy_ = version.parse(bstack11ll11lll1l_opy_)
    if bstack11ll11l1111_opy_ > bstack11ll111l111_opy_:
        return 1
    elif bstack11ll11l1111_opy_ < bstack11ll111l111_opy_:
        return -1
    else:
        return 0
def bstack111ll11ll1_opy_():
    return datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
def bstack11l1l111lll_opy_(timestamp):
    return datetime.datetime.fromtimestamp(timestamp, datetime.timezone.utc).replace(tzinfo=None)
def bstack11l1l1l11ll_opy_(framework):
    from browserstack_sdk._version import __version__
    return str(framework) + str(__version__)
def bstack1l11111l1_opy_(options, framework, bstack1lll11l1ll_opy_={}):
    if options is None:
        return
    if getattr(options, bstack1l1_opy_ (u"ࠫ࡬࡫ࡴࠨᭇ"), None):
        caps = options
    else:
        caps = options.to_capabilities()
    bstack1111lll11_opy_ = caps.get(bstack1l1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᭈ"))
    bstack11l11llll1l_opy_ = True
    bstack1ll11ll1l_opy_ = os.environ[bstack1l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫᭉ")]
    if bstack11ll111l1ll_opy_(caps.get(bstack1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡵࡴࡧ࡚࠷ࡈ࠭ᭊ"))) or bstack11ll111l1ll_opy_(caps.get(bstack1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡶࡵࡨࡣࡼ࠹ࡣࠨᭋ"))):
        bstack11l11llll1l_opy_ = False
    if bstack1lll1l1l11_opy_({bstack1l1_opy_ (u"ࠤࡸࡷࡪ࡝࠳ࡄࠤᭌ"): bstack11l11llll1l_opy_}):
        bstack1111lll11_opy_ = bstack1111lll11_opy_ or {}
        bstack1111lll11_opy_[bstack1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏࠬ᭍")] = bstack11l1l1l11ll_opy_(framework)
        bstack1111lll11_opy_[bstack1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭᭎")] = bstack1ll111l1ll1_opy_()
        bstack1111lll11_opy_[bstack1l1_opy_ (u"ࠬࡺࡥࡴࡶ࡫ࡹࡧࡈࡵࡪ࡮ࡧ࡙ࡺ࡯ࡤࠨ᭏")] = bstack1ll11ll1l_opy_
        bstack1111lll11_opy_[bstack1l1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡕࡸ࡯ࡥࡷࡦࡸࡒࡧࡰࠨ᭐")] = bstack1lll11l1ll_opy_
        if getattr(options, bstack1l1_opy_ (u"ࠧࡴࡧࡷࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡹࠨ᭑"), None):
            options.set_capability(bstack1l1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩ᭒"), bstack1111lll11_opy_)
        else:
            options[bstack1l1_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪ᭓")] = bstack1111lll11_opy_
    else:
        if getattr(options, bstack1l1_opy_ (u"ࠪࡷࡪࡺ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶࡼࠫ᭔"), None):
            options.set_capability(bstack1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏࠬ᭕"), bstack11l1l1l11ll_opy_(framework))
            options.set_capability(bstack1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭᭖"), bstack1ll111l1ll1_opy_())
            options.set_capability(bstack1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡺࡥࡴࡶ࡫ࡹࡧࡈࡵࡪ࡮ࡧ࡙ࡺ࡯ࡤࠨ᭗"), bstack1ll11ll1l_opy_)
            options.set_capability(bstack1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡶ࡫࡯ࡨࡕࡸ࡯ࡥࡷࡦࡸࡒࡧࡰࠨ᭘"), bstack1lll11l1ll_opy_)
        else:
            options[bstack1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࡙ࡄࡌࠩ᭙")] = bstack11l1l1l11ll_opy_(framework)
            options[bstack1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪ᭚")] = bstack1ll111l1ll1_opy_()
            options[bstack1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡷࡩࡸࡺࡨࡶࡤࡅࡹ࡮ࡲࡤࡖࡷ࡬ࡨࠬ᭛")] = bstack1ll11ll1l_opy_
            options[bstack1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡺ࡯࡬ࡥࡒࡵࡳࡩࡻࡣࡵࡏࡤࡴࠬ᭜")] = bstack1lll11l1ll_opy_
    return options
def bstack11l1l11ll1l_opy_(bstack11l1lll1l1l_opy_, framework):
    bstack1lll11l1ll_opy_ = bstack11llllll1_opy_.get_property(bstack1l1_opy_ (u"ࠧࡖࡌࡂ࡛࡚ࡖࡎࡍࡈࡕࡡࡓࡖࡔࡊࡕࡄࡖࡢࡑࡆࡖࠢ᭝"))
    if bstack11l1lll1l1l_opy_ and len(bstack11l1lll1l1l_opy_.split(bstack1l1_opy_ (u"࠭ࡣࡢࡲࡶࡁࠬ᭞"))) > 1:
        ws_url = bstack11l1lll1l1l_opy_.split(bstack1l1_opy_ (u"ࠧࡤࡣࡳࡷࡂ࠭᭟"))[0]
        if bstack1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰࠫ᭠") in ws_url:
            from browserstack_sdk._version import __version__
            bstack11l1l1lllll_opy_ = json.loads(urllib.parse.unquote(bstack11l1lll1l1l_opy_.split(bstack1l1_opy_ (u"ࠩࡦࡥࡵࡹ࠽ࠨ᭡"))[1]))
            bstack11l1l1lllll_opy_ = bstack11l1l1lllll_opy_ or {}
            bstack1ll11ll1l_opy_ = os.environ[bstack1l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨ᭢")]
            bstack11l1l1lllll_opy_[bstack1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏࠬ᭣")] = str(framework) + str(__version__)
            bstack11l1l1lllll_opy_[bstack1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭᭤")] = bstack1ll111l1ll1_opy_()
            bstack11l1l1lllll_opy_[bstack1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡺࡥࡴࡶ࡫ࡹࡧࡈࡵࡪ࡮ࡧ࡙ࡺ࡯ࡤࠨ᭥")] = bstack1ll11ll1l_opy_
            bstack11l1l1lllll_opy_[bstack1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡶ࡫࡯ࡨࡕࡸ࡯ࡥࡷࡦࡸࡒࡧࡰࠨ᭦")] = bstack1lll11l1ll_opy_
            bstack11l1lll1l1l_opy_ = bstack11l1lll1l1l_opy_.split(bstack1l1_opy_ (u"ࠨࡥࡤࡴࡸࡃࠧ᭧"))[0] + bstack1l1_opy_ (u"ࠩࡦࡥࡵࡹ࠽ࠨ᭨") + urllib.parse.quote(json.dumps(bstack11l1l1lllll_opy_))
    return bstack11l1lll1l1l_opy_
def bstack1ll1lll11l_opy_():
    global bstack1111ll11l_opy_
    from playwright._impl._browser_type import BrowserType
    bstack1111ll11l_opy_ = BrowserType.connect
    return bstack1111ll11l_opy_
def bstack11lll1ll1l_opy_(framework_name):
    global bstack111l1l1l_opy_
    bstack111l1l1l_opy_ = framework_name
    return framework_name
def bstack1l11l1lll1_opy_(self, *args, **kwargs):
    global bstack1111ll11l_opy_
    try:
        global bstack111l1l1l_opy_
        if bstack1l1_opy_ (u"ࠪࡻࡸࡋ࡮ࡥࡲࡲ࡭ࡳࡺࠧ᭩") in kwargs:
            kwargs[bstack1l1_opy_ (u"ࠫࡼࡹࡅ࡯ࡦࡳࡳ࡮ࡴࡴࠨ᭪")] = bstack11l1l11ll1l_opy_(
                kwargs.get(bstack1l1_opy_ (u"ࠬࡽࡳࡆࡰࡧࡴࡴ࡯࡮ࡵࠩ᭫"), None),
                bstack111l1l1l_opy_
            )
    except Exception as e:
        logger.error(bstack1l1_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡦࡰࠣࡴࡷࡵࡣࡦࡵࡶ࡭ࡳ࡭ࠠࡔࡆࡎࠤࡨࡧࡰࡴ࠼ࠣࡿࢂࠨ᭬").format(str(e)))
    return bstack1111ll11l_opy_(self, *args, **kwargs)
def bstack11l1ll11ll1_opy_(bstack11l1llll1l1_opy_, proxies):
    proxy_settings = {}
    try:
        if not proxies:
            proxies = bstack11ll1llll_opy_(bstack11l1llll1l1_opy_, bstack1l1_opy_ (u"ࠢࠣ᭭"))
        if proxies and proxies.get(bstack1l1_opy_ (u"ࠣࡪࡷࡸࡵࡹࠢ᭮")):
            parsed_url = urlparse(proxies.get(bstack1l1_opy_ (u"ࠤ࡫ࡸࡹࡶࡳࠣ᭯")))
            if parsed_url and parsed_url.hostname: proxy_settings[bstack1l1_opy_ (u"ࠪࡴࡷࡵࡸࡺࡊࡲࡷࡹ࠭᭰")] = str(parsed_url.hostname)
            if parsed_url and parsed_url.port: proxy_settings[bstack1l1_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡓࡳࡷࡺࠧ᭱")] = str(parsed_url.port)
            if parsed_url and parsed_url.username: proxy_settings[bstack1l1_opy_ (u"ࠬࡶࡲࡰࡺࡼ࡙ࡸ࡫ࡲࠨ᭲")] = str(parsed_url.username)
            if parsed_url and parsed_url.password: proxy_settings[bstack1l1_opy_ (u"࠭ࡰࡳࡱࡻࡽࡕࡧࡳࡴࠩ᭳")] = str(parsed_url.password)
        return proxy_settings
    except:
        return proxy_settings
def bstack1ll11l1l1l_opy_(bstack11l1llll1l1_opy_):
    bstack11l1l1llll1_opy_ = {
        bstack11ll1lll1l1_opy_[bstack11l1l1l11l1_opy_]: bstack11l1llll1l1_opy_[bstack11l1l1l11l1_opy_]
        for bstack11l1l1l11l1_opy_ in bstack11l1llll1l1_opy_
        if bstack11l1l1l11l1_opy_ in bstack11ll1lll1l1_opy_
    }
    bstack11l1l1llll1_opy_[bstack1l1_opy_ (u"ࠢࡱࡴࡲࡼࡾ࡙ࡥࡵࡶ࡬ࡲ࡬ࡹࠢ᭴")] = bstack11l1ll11ll1_opy_(bstack11l1llll1l1_opy_, bstack11llllll1_opy_.get_property(bstack1l1_opy_ (u"ࠣࡲࡵࡳࡽࡿࡓࡦࡶࡷ࡭ࡳ࡭ࡳࠣ᭵")))
    bstack11l1llll11l_opy_ = [element.lower() for element in bstack11lll11111l_opy_]
    bstack11l1l11l1l1_opy_(bstack11l1l1llll1_opy_, bstack11l1llll11l_opy_)
    return bstack11l1l1llll1_opy_
def bstack11l1l11l1l1_opy_(d, keys):
    for key in list(d.keys()):
        if key.lower() in keys:
            d[key] = bstack1l1_opy_ (u"ࠤ࠭࠮࠯࠰ࠢ᭶")
    for value in d.values():
        if isinstance(value, dict):
            bstack11l1l11l1l1_opy_(value, keys)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    bstack11l1l11l1l1_opy_(item, keys)
def bstack1l1lllll1ll_opy_():
    bstack11l1ll11l1l_opy_ = [os.environ.get(bstack1l1_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡉࡍࡑࡋࡓࡠࡆࡌࡖࠧ᭷")), os.path.join(os.path.expanduser(bstack1l1_opy_ (u"ࠦࢃࠨ᭸")), bstack1l1_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬ᭹")), os.path.join(bstack1l1_opy_ (u"࠭࠯ࡵ࡯ࡳࠫ᭺"), bstack1l1_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧ᭻"))]
    for path in bstack11l1ll11l1l_opy_:
        if path is None:
            continue
        try:
            if os.path.exists(path):
                logger.debug(bstack1l1_opy_ (u"ࠣࡈ࡬ࡰࡪࠦࠧࠣ᭼") + str(path) + bstack1l1_opy_ (u"ࠤࠪࠤࡪࡾࡩࡴࡶࡶ࠲ࠧ᭽"))
                if not os.access(path, os.W_OK):
                    logger.debug(bstack1l1_opy_ (u"ࠥࡋ࡮ࡼࡩ࡯ࡩࠣࡴࡪࡸ࡭ࡪࡵࡶ࡭ࡴࡴࡳࠡࡨࡲࡶࠥ࠭ࠢ᭾") + str(path) + bstack1l1_opy_ (u"ࠦࠬࠨ᭿"))
                    os.chmod(path, 0o777)
                else:
                    logger.debug(bstack1l1_opy_ (u"ࠧࡌࡩ࡭ࡧࠣࠫࠧᮀ") + str(path) + bstack1l1_opy_ (u"ࠨࠧࠡࡣ࡯ࡶࡪࡧࡤࡺࠢ࡫ࡥࡸࠦࡴࡩࡧࠣࡶࡪࡷࡵࡪࡴࡨࡨࠥࡶࡥࡳ࡯࡬ࡷࡸ࡯࡯࡯ࡵ࠱ࠦᮁ"))
            else:
                logger.debug(bstack1l1_opy_ (u"ࠢࡄࡴࡨࡥࡹ࡯࡮ࡨࠢࡩ࡭ࡱ࡫ࠠࠨࠤᮂ") + str(path) + bstack1l1_opy_ (u"ࠣࠩࠣࡻ࡮ࡺࡨࠡࡹࡵ࡭ࡹ࡫ࠠࡱࡧࡵࡱ࡮ࡹࡳࡪࡱࡱ࠲ࠧᮃ"))
                os.makedirs(path, exist_ok=True)
                os.chmod(path, 0o777)
            logger.debug(bstack1l1_opy_ (u"ࠤࡒࡴࡪࡸࡡࡵ࡫ࡲࡲࠥࡹࡵࡤࡥࡨࡩࡩ࡫ࡤࠡࡨࡲࡶࠥ࠭ࠢᮄ") + str(path) + bstack1l1_opy_ (u"ࠥࠫ࠳ࠨᮅ"))
            return path
        except Exception as e:
            logger.debug(bstack1l1_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡧࡷࠤࡺࡶࠠࡧ࡫࡯ࡩࠥ࠭ࡻࡱࡣࡷ࡬ࢂ࠭࠺ࠡࠤᮆ") + str(e) + bstack1l1_opy_ (u"ࠧࠨᮇ"))
    logger.debug(bstack1l1_opy_ (u"ࠨࡁ࡭࡮ࠣࡴࡦࡺࡨࡴࠢࡩࡥ࡮ࡲࡥࡥ࠰ࠥᮈ"))
    return None
@measure(event_name=EVENTS.bstack11ll1lll11l_opy_, stage=STAGE.bstack1llll11l1_opy_)
def bstack1llll1ll11l_opy_(binary_path, bstack1lll11l1111_opy_, bs_config):
    logger.debug(bstack1l1_opy_ (u"ࠢࡄࡷࡵࡶࡪࡴࡴࠡࡅࡏࡍࠥࡖࡡࡵࡪࠣࡪࡴࡻ࡮ࡥ࠼ࠣࡿࢂࠨᮉ").format(binary_path))
    bstack11l1lll1lll_opy_ = bstack1l1_opy_ (u"ࠨࠩᮊ")
    bstack11l1ll11l11_opy_ = {
        bstack1l1_opy_ (u"ࠩࡶࡨࡰࡥࡶࡦࡴࡶ࡭ࡴࡴࠧᮋ"): __version__,
        bstack1l1_opy_ (u"ࠥࡳࡸࠨᮌ"): platform.system(),
        bstack1l1_opy_ (u"ࠦࡴࡹ࡟ࡢࡴࡦ࡬ࠧᮍ"): platform.machine(),
        bstack1l1_opy_ (u"ࠧࡩ࡬ࡪࡡࡹࡩࡷࡹࡩࡰࡰࠥᮎ"): bstack1l1_opy_ (u"࠭࠰ࠨᮏ"),
        bstack1l1_opy_ (u"ࠢࡴࡦ࡮ࡣࡱࡧ࡮ࡨࡷࡤ࡫ࡪࠨᮐ"): bstack1l1_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨᮑ")
    }
    try:
        if binary_path:
            bstack11l1ll11l11_opy_[bstack1l1_opy_ (u"ࠩࡦࡰ࡮ࡥࡶࡦࡴࡶ࡭ࡴࡴࠧᮒ")] = subprocess.check_output([binary_path, bstack1l1_opy_ (u"ࠥࡺࡪࡸࡳࡪࡱࡱࠦᮓ")]).strip().decode(bstack1l1_opy_ (u"ࠫࡺࡺࡦ࠮࠺ࠪᮔ"))
        response = requests.request(
            bstack1l1_opy_ (u"ࠬࡍࡅࡕࠩᮕ"),
            url=bstack1l11111ll1_opy_(bstack11ll1ll11l1_opy_),
            headers=None,
            auth=(bs_config[bstack1l1_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨᮖ")], bs_config[bstack1l1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪᮗ")]),
            json=None,
            params=bstack11l1ll11l11_opy_
        )
        data = response.json()
        if response.status_code == 200 and bstack1l1_opy_ (u"ࠨࡷࡵࡰࠬᮘ") in data.keys() and bstack1l1_opy_ (u"ࠩࡸࡴࡩࡧࡴࡦࡦࡢࡧࡱ࡯࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨᮙ") in data.keys():
            logger.debug(bstack1l1_opy_ (u"ࠥࡒࡪ࡫ࡤࠡࡶࡲࠤࡺࡶࡤࡢࡶࡨࠤࡧ࡯࡮ࡢࡴࡼ࠰ࠥࡩࡵࡳࡴࡨࡲࡹࠦࡢࡪࡰࡤࡶࡾࠦࡶࡦࡴࡶ࡭ࡴࡴ࠺ࠡࡽࢀࠦᮚ").format(bstack11l1ll11l11_opy_[bstack1l1_opy_ (u"ࠫࡨࡲࡩࡠࡸࡨࡶࡸ࡯࡯࡯ࠩᮛ")]))
            bstack11l1l11l11l_opy_ = bstack11l1ll1l11l_opy_(data[bstack1l1_opy_ (u"ࠬࡻࡲ࡭ࠩᮜ")], bstack1lll11l1111_opy_)
            bstack11l1lll1lll_opy_ = os.path.join(bstack1lll11l1111_opy_, bstack11l1l11l11l_opy_)
            os.chmod(bstack11l1lll1lll_opy_, 0o777) # bstack11l1ll1ll1l_opy_ permission
            return bstack11l1lll1lll_opy_
    except Exception as e:
        logger.debug(bstack1l1_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤࡩࡵࡷ࡯࡮ࡲࡥࡩ࡯࡮ࡨࠢࡱࡩࡼࠦࡓࡅࡍࠣࡿࢂࠨᮝ").format(e))
    return binary_path
@measure(event_name=EVENTS.bstack11ll1l1l1l1_opy_, stage=STAGE.bstack1llll11l1_opy_)
def bstack11l1ll1l11l_opy_(bstack11l1ll1lll1_opy_, bstack11l11lllll1_opy_):
    logger.debug(bstack1l1_opy_ (u"ࠢࡅࡱࡺࡲࡱࡵࡡࡥ࡫ࡱ࡫࡙ࠥࡄࡌࠢࡥ࡭ࡳࡧࡲࡺࠢࡩࡶࡴࡳ࠺ࠡࠤᮞ") + str(bstack11l1ll1lll1_opy_) + bstack1l1_opy_ (u"ࠣࠤᮟ"))
    zip_path = os.path.join(bstack11l11lllll1_opy_, bstack1l1_opy_ (u"ࠤࡧࡳࡼࡴ࡬ࡰࡣࡧࡩࡩࡥࡦࡪ࡮ࡨ࠲ࡿ࡯ࡰࠣᮠ"))
    bstack11l1l11l11l_opy_ = bstack1l1_opy_ (u"ࠪࠫᮡ")
    with requests.get(bstack11l1ll1lll1_opy_, stream=True) as response:
        response.raise_for_status()
        with open(zip_path, bstack1l1_opy_ (u"ࠦࡼࡨࠢᮢ")) as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
        logger.debug(bstack1l1_opy_ (u"ࠧࡌࡩ࡭ࡧࠣࡨࡴࡽ࡮࡭ࡱࡤࡨࡪࡪࠠࡴࡷࡦࡧࡪࡹࡳࡧࡷ࡯ࡰࡾ࠴ࠢᮣ"))
    with zipfile.ZipFile(zip_path, bstack1l1_opy_ (u"࠭ࡲࠨᮤ")) as zip_ref:
        bstack11l1l1l1111_opy_ = zip_ref.namelist()
        if len(bstack11l1l1l1111_opy_) > 0:
            bstack11l1l11l11l_opy_ = bstack11l1l1l1111_opy_[0] # bstack11l1ll1llll_opy_ bstack11ll1llll1l_opy_ will be bstack11l1l11ll11_opy_ 1 file i.e. the binary in the zip
        zip_ref.extractall(bstack11l11lllll1_opy_)
        logger.debug(bstack1l1_opy_ (u"ࠢࡇ࡫࡯ࡩࡸࠦࡳࡶࡥࡦࡩࡸࡹࡦࡶ࡮࡯ࡽࠥ࡫ࡸࡵࡴࡤࡧࡹ࡫ࡤࠡࡶࡲࠤࠬࠨᮥ") + str(bstack11l11lllll1_opy_) + bstack1l1_opy_ (u"ࠣࠩࠥᮦ"))
    os.remove(zip_path)
    return bstack11l1l11l11l_opy_
def get_cli_dir():
    bstack11ll111lll1_opy_ = bstack1l1lllll1ll_opy_()
    if bstack11ll111lll1_opy_:
        bstack1lll11l1111_opy_ = os.path.join(bstack11ll111lll1_opy_, bstack1l1_opy_ (u"ࠤࡦࡰ࡮ࠨᮧ"))
        if not os.path.exists(bstack1lll11l1111_opy_):
            os.makedirs(bstack1lll11l1111_opy_, mode=0o777, exist_ok=True)
        return bstack1lll11l1111_opy_
    else:
        raise FileNotFoundError(bstack1l1_opy_ (u"ࠥࡒࡴࠦࡷࡳ࡫ࡷࡥࡧࡲࡥࠡࡦ࡬ࡶࡪࡩࡴࡰࡴࡼࠤࡦࡼࡡࡪ࡮ࡤࡦࡱ࡫ࠠࡧࡱࡵࠤࡹ࡮ࡥࠡࡕࡇࡏࠥࡨࡩ࡯ࡣࡵࡽ࠳ࠨᮨ"))
def bstack1llll1l111l_opy_(bstack1lll11l1111_opy_):
    bstack1l1_opy_ (u"ࠦࠧࠨࡇࡦࡶࠣࡸ࡭࡫ࠠࡱࡣࡷ࡬ࠥ࡬࡯ࡳࠢࡷ࡬ࡪࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯࡙ࠥࡄࡌࠢࡥ࡭ࡳࡧࡲࡺࠢ࡬ࡲࠥࡧࠠࡸࡴ࡬ࡸࡦࡨ࡬ࡦࠢࡧ࡭ࡷ࡫ࡣࡵࡱࡵࡽ࠳ࠨࠢࠣᮩ")
    bstack11l1ll11111_opy_ = [
        os.path.join(bstack1lll11l1111_opy_, f)
        for f in os.listdir(bstack1lll11l1111_opy_)
        if os.path.isfile(os.path.join(bstack1lll11l1111_opy_, f)) and f.startswith(bstack1l1_opy_ (u"ࠧࡨࡩ࡯ࡣࡵࡽ࠲ࠨ᮪"))
    ]
    if len(bstack11l1ll11111_opy_) > 0:
        return max(bstack11l1ll11111_opy_, key=os.path.getmtime) # get bstack11l1ll111l1_opy_ binary
    return bstack1l1_opy_ (u"ࠨ᮫ࠢ")
def bstack1ll1l1l11ll_opy_(d, u):
  for k, v in u.items():
    if isinstance(v, collections.abc.Mapping):
      d[k] = bstack1ll1l1l11ll_opy_(d.get(k, {}), v)
    else:
      if isinstance(v, list):
        d[k] = d.get(k, []) + v
      else:
        d[k] = v
  return d