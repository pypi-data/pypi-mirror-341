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
import os
import re
import sys
import json
import time
import shutil
import tempfile
import requests
import subprocess
from threading import Thread
from os.path import expanduser
from bstack_utils.constants import *
from requests.auth import HTTPBasicAuth
from bstack_utils.helper import bstack11l1lll1l_opy_, bstack1l1ll11lll_opy_
from bstack_utils.measure import measure
class bstack11ll111ll1_opy_:
  working_dir = os.getcwd()
  bstack1l1111ll_opy_ = False
  config = {}
  bstack11ll11ll11l_opy_ = bstack1l1ll11_opy_ (u"ࠪࠫᱥ")
  binary_path = bstack1l1ll11_opy_ (u"ࠫࠬᱦ")
  bstack11l11111l11_opy_ = bstack1l1ll11_opy_ (u"ࠬ࠭ᱧ")
  bstack1llll11ll_opy_ = False
  bstack111ll1llll1_opy_ = None
  bstack111llll111l_opy_ = {}
  bstack111ll1ll1ll_opy_ = 300
  bstack111ll1lllll_opy_ = False
  logger = None
  bstack11l1111l1ll_opy_ = False
  bstack1lll11l1_opy_ = False
  percy_build_id = None
  bstack111ll1ll11l_opy_ = bstack1l1ll11_opy_ (u"࠭ࠧᱨ")
  bstack11l11111111_opy_ = {
    bstack1l1ll11_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࠧᱩ") : 1,
    bstack1l1ll11_opy_ (u"ࠨࡨ࡬ࡶࡪ࡬࡯ࡹࠩᱪ") : 2,
    bstack1l1ll11_opy_ (u"ࠩࡨࡨ࡬࡫ࠧᱫ") : 3,
    bstack1l1ll11_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫ࠪᱬ") : 4
  }
  def __init__(self) -> None: pass
  def bstack111ll1ll1l1_opy_(self):
    bstack111llll1111_opy_ = bstack1l1ll11_opy_ (u"ࠫࠬᱭ")
    bstack11l1111llll_opy_ = sys.platform
    bstack111ll1ll111_opy_ = bstack1l1ll11_opy_ (u"ࠬࡶࡥࡳࡥࡼࠫᱮ")
    if re.match(bstack1l1ll11_opy_ (u"ࠨࡤࡢࡴࡺ࡭ࡳࢂ࡭ࡢࡥࠣࡳࡸࠨᱯ"), bstack11l1111llll_opy_) != None:
      bstack111llll1111_opy_ = bstack11ll1ll11l1_opy_ + bstack1l1ll11_opy_ (u"ࠢ࠰ࡲࡨࡶࡨࡿ࠭ࡰࡵࡻ࠲ࡿ࡯ࡰࠣᱰ")
      self.bstack111ll1ll11l_opy_ = bstack1l1ll11_opy_ (u"ࠨ࡯ࡤࡧࠬᱱ")
    elif re.match(bstack1l1ll11_opy_ (u"ࠤࡰࡷࡼ࡯࡮ࡽ࡯ࡶࡽࡸࢂ࡭ࡪࡰࡪࡻࢁࡩࡹࡨࡹ࡬ࡲࢁࡨࡣࡤࡹ࡬ࡲࢁࡽࡩ࡯ࡥࡨࢀࡪࡳࡣࡽࡹ࡬ࡲ࠸࠸ࠢᱲ"), bstack11l1111llll_opy_) != None:
      bstack111llll1111_opy_ = bstack11ll1ll11l1_opy_ + bstack1l1ll11_opy_ (u"ࠥ࠳ࡵ࡫ࡲࡤࡻ࠰ࡻ࡮ࡴ࠮ࡻ࡫ࡳࠦᱳ")
      bstack111ll1ll111_opy_ = bstack1l1ll11_opy_ (u"ࠦࡵ࡫ࡲࡤࡻ࠱ࡩࡽ࡫ࠢᱴ")
      self.bstack111ll1ll11l_opy_ = bstack1l1ll11_opy_ (u"ࠬࡽࡩ࡯ࠩᱵ")
    else:
      bstack111llll1111_opy_ = bstack11ll1ll11l1_opy_ + bstack1l1ll11_opy_ (u"ࠨ࠯ࡱࡧࡵࡧࡾ࠳࡬ࡪࡰࡸࡼ࠳ࢀࡩࡱࠤᱶ")
      self.bstack111ll1ll11l_opy_ = bstack1l1ll11_opy_ (u"ࠧ࡭࡫ࡱࡹࡽ࠭ᱷ")
    return bstack111llll1111_opy_, bstack111ll1ll111_opy_
  def bstack11l11111ll1_opy_(self):
    try:
      bstack11l1111lll1_opy_ = [os.path.join(expanduser(bstack1l1ll11_opy_ (u"ࠣࢀࠥᱸ")), bstack1l1ll11_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩᱹ")), self.working_dir, tempfile.gettempdir()]
      for path in bstack11l1111lll1_opy_:
        if(self.bstack11l11111lll_opy_(path)):
          return path
      raise bstack1l1ll11_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡤࡰࡹࡱࡰࡴࡧࡤࠡࡲࡨࡶࡨࡿࠠࡣ࡫ࡱࡥࡷࡿࠢᱺ")
    except Exception as e:
      self.logger.error(bstack1l1ll11_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡧ࡫ࡱࡨࠥࡧࡶࡢ࡫࡯ࡥࡧࡲࡥࠡࡲࡤࡸ࡭ࠦࡦࡰࡴࠣࡴࡪࡸࡣࡺࠢࡧࡳࡼࡴ࡬ࡰࡣࡧ࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࠯ࠣࡿࢂࠨᱻ").format(e))
  def bstack11l11111lll_opy_(self, path):
    try:
      if not os.path.exists(path):
        os.makedirs(path)
      return True
    except:
      return False
  def bstack111ll1lll11_opy_(self, bstack11l1111ll11_opy_):
    return os.path.join(bstack11l1111ll11_opy_, self.bstack11ll11ll11l_opy_ + bstack1l1ll11_opy_ (u"ࠧ࠴ࡥࡵࡣࡪࠦᱼ"))
  def bstack111llllll11_opy_(self, bstack11l1111ll11_opy_, bstack111lll1l111_opy_):
    if not bstack111lll1l111_opy_: return
    try:
      bstack111lllll111_opy_ = self.bstack111ll1lll11_opy_(bstack11l1111ll11_opy_)
      with open(bstack111lllll111_opy_, bstack1l1ll11_opy_ (u"ࠨࡷࠣᱽ")) as f:
        f.write(bstack111lll1l111_opy_)
        self.logger.debug(bstack1l1ll11_opy_ (u"ࠢࡔࡣࡹࡩࡩࠦ࡮ࡦࡹࠣࡉ࡙ࡧࡧࠡࡨࡲࡶࠥࡶࡥࡳࡥࡼࠦ᱾"))
    except Exception as e:
      self.logger.error(bstack1l1ll11_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸࡧࡶࡦࠢࡷ࡬ࡪࠦࡥࡵࡣࡪ࠰ࠥ࡫ࡲࡳࡱࡵ࠾ࠥࢁࡽࠣ᱿").format(e))
  def bstack111lll11111_opy_(self, bstack11l1111ll11_opy_):
    try:
      bstack111lllll111_opy_ = self.bstack111ll1lll11_opy_(bstack11l1111ll11_opy_)
      if os.path.exists(bstack111lllll111_opy_):
        with open(bstack111lllll111_opy_, bstack1l1ll11_opy_ (u"ࠤࡵࠦᲀ")) as f:
          bstack111lll1l111_opy_ = f.read().strip()
          return bstack111lll1l111_opy_ if bstack111lll1l111_opy_ else None
    except Exception as e:
      self.logger.error(bstack1l1ll11_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡰࡴࡧࡤࡪࡰࡪࠤࡊ࡚ࡡࡨ࠮ࠣࡩࡷࡸ࡯ࡳ࠼ࠣࡿࢂࠨᲁ").format(e))
  def bstack111lll11ll1_opy_(self, bstack11l1111ll11_opy_, bstack111llll1111_opy_):
    bstack111ll1l1ll1_opy_ = self.bstack111lll11111_opy_(bstack11l1111ll11_opy_)
    if bstack111ll1l1ll1_opy_:
      try:
        bstack111llllll1l_opy_ = self.bstack111lll1lll1_opy_(bstack111ll1l1ll1_opy_, bstack111llll1111_opy_)
        if not bstack111llllll1l_opy_:
          self.logger.debug(bstack1l1ll11_opy_ (u"ࠦࡕ࡫ࡲࡤࡻࠣࡦ࡮ࡴࡡࡳࡻࠣ࡭ࡸࠦࡵࡱࠢࡷࡳࠥࡪࡡࡵࡧࠣࠬࡊ࡚ࡡࡨࠢࡸࡲࡨ࡮ࡡ࡯ࡩࡨࡨ࠮ࠨᲂ"))
          return True
        self.logger.debug(bstack1l1ll11_opy_ (u"ࠧࡔࡥࡸࠢࡓࡩࡷࡩࡹࠡࡤ࡬ࡲࡦࡸࡹࠡࡸࡨࡶࡸ࡯࡯࡯ࠢࡤࡺࡦ࡯࡬ࡢࡤ࡯ࡩ࠱ࠦࡤࡰࡹࡱࡰࡴࡧࡤࡪࡰࡪࠤࡺࡶࡤࡢࡶࡨࠦᲃ"))
        return False
      except Exception as e:
        self.logger.warn(bstack1l1ll11_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡦ࡬ࡪࡩ࡫ࠡࡨࡲࡶࠥࡨࡩ࡯ࡣࡵࡽࠥࡻࡰࡥࡣࡷࡩࡸ࠲ࠠࡶࡵ࡬ࡲ࡬ࠦࡥࡹ࡫ࡶࡸ࡮ࡴࡧࠡࡤ࡬ࡲࡦࡸࡹ࠻ࠢࡾࢁࠧᲄ").format(e))
    return False
  def bstack111lll1lll1_opy_(self, bstack111ll1l1ll1_opy_, bstack111llll1111_opy_):
    try:
      headers = {
        bstack1l1ll11_opy_ (u"ࠢࡊࡨ࠰ࡒࡴࡴࡥ࠮ࡏࡤࡸࡨ࡮ࠢᲅ"): bstack111ll1l1ll1_opy_
      }
      response = bstack1l1ll11lll_opy_(bstack1l1ll11_opy_ (u"ࠨࡉࡈࡘࠬᲆ"), bstack111llll1111_opy_, {}, {bstack1l1ll11_opy_ (u"ࠤ࡫ࡩࡦࡪࡥࡳࡵࠥᲇ"): headers})
      if response.status_code == 304:
        return False
      return True
    except Exception as e:
      raise(bstack1l1ll11_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡦ࡬ࡪࡩ࡫ࡪࡰࡪࠤ࡫ࡵࡲࠡࡒࡨࡶࡨࡿࠠࡣ࡫ࡱࡥࡷࡿࠠࡶࡲࡧࡥࡹ࡫ࡳ࠻ࠢࡾࢁࠧᲈ").format(e))
  @measure(event_name=EVENTS.bstack11ll11lllll_opy_, stage=STAGE.bstack1ll1111ll1_opy_)
  def bstack111llll1lll_opy_(self, bstack111llll1111_opy_, bstack111ll1ll111_opy_):
    try:
      bstack111lll1l1ll_opy_ = self.bstack11l11111ll1_opy_()
      bstack111ll1l1l1l_opy_ = os.path.join(bstack111lll1l1ll_opy_, bstack1l1ll11_opy_ (u"ࠫࡵ࡫ࡲࡤࡻ࠱ࡾ࡮ࡶࠧᲉ"))
      bstack111lllll1ll_opy_ = os.path.join(bstack111lll1l1ll_opy_, bstack111ll1ll111_opy_)
      if self.bstack111lll11ll1_opy_(bstack111lll1l1ll_opy_, bstack111llll1111_opy_):
        if os.path.exists(bstack111lllll1ll_opy_):
          self.logger.info(bstack1l1ll11_opy_ (u"ࠧࡖࡥࡳࡥࡼࠤࡧ࡯࡮ࡢࡴࡼࠤ࡫ࡵࡵ࡯ࡦࠣ࡭ࡳࠦࡻࡾ࠮ࠣࡷࡰ࡯ࡰࡱ࡫ࡱ࡫ࠥࡪ࡯ࡸࡰ࡯ࡳࡦࡪࠢᲊ").format(bstack111lllll1ll_opy_))
          return bstack111lllll1ll_opy_
        if os.path.exists(bstack111ll1l1l1l_opy_):
          self.logger.info(bstack1l1ll11_opy_ (u"ࠨࡐࡦࡴࡦࡽࠥࢀࡩࡱࠢࡩࡳࡺࡴࡤࠡ࡫ࡱࠤࢀࢃࠬࠡࡷࡱࡾ࡮ࡶࡰࡪࡰࡪࠦ᲋").format(bstack111ll1l1l1l_opy_))
          return self.bstack111llll1l1l_opy_(bstack111ll1l1l1l_opy_, bstack111ll1ll111_opy_)
      self.logger.info(bstack1l1ll11_opy_ (u"ࠢࡅࡱࡺࡲࡱࡵࡡࡥ࡫ࡱ࡫ࠥࡶࡥࡳࡥࡼࠤࡧ࡯࡮ࡢࡴࡼࠤ࡫ࡸ࡯࡮ࠢࡾࢁࠧ᲌").format(bstack111llll1111_opy_))
      response = bstack1l1ll11lll_opy_(bstack1l1ll11_opy_ (u"ࠨࡉࡈࡘࠬ᲍"), bstack111llll1111_opy_, {}, {})
      if response.status_code == 200:
        bstack11l1111l111_opy_ = response.headers.get(bstack1l1ll11_opy_ (u"ࠤࡈࡘࡦ࡭ࠢ᲎"), bstack1l1ll11_opy_ (u"ࠥࠦ᲏"))
        if bstack11l1111l111_opy_:
          self.bstack111llllll11_opy_(bstack111lll1l1ll_opy_, bstack11l1111l111_opy_)
        with open(bstack111ll1l1l1l_opy_, bstack1l1ll11_opy_ (u"ࠫࡼࡨࠧᲐ")) as file:
          file.write(response.content)
        self.logger.info(bstack1l1ll11_opy_ (u"ࠧࡊ࡯ࡸࡰ࡯ࡳࡦࡪࡥࡥࠢࡳࡩࡷࡩࡹࠡࡤ࡬ࡲࡦࡸࡹࠡࡣࡱࡨࠥࡹࡡࡷࡧࡧࠤࡦࡺࠠࡼࡿࠥᲑ").format(bstack111ll1l1l1l_opy_))
        return self.bstack111llll1l1l_opy_(bstack111ll1l1l1l_opy_, bstack111ll1ll111_opy_)
      else:
        raise(bstack1l1ll11_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡧࡳࡼࡴ࡬ࡰࡣࡧࠤࡹ࡮ࡥࠡࡨ࡬ࡰࡪ࠴ࠠࡔࡶࡤࡸࡺࡹࠠࡤࡱࡧࡩ࠿ࠦࡻࡾࠤᲒ").format(response.status_code))
    except Exception as e:
      self.logger.error(bstack1l1ll11_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡨࡴࡽ࡮࡭ࡱࡤࡨࠥࡶࡥࡳࡥࡼࠤࡧ࡯࡮ࡢࡴࡼ࠾ࠥࢁࡽࠣᲓ").format(e))
  def bstack111ll1l111l_opy_(self, bstack111llll1111_opy_, bstack111ll1ll111_opy_):
    try:
      retry = 2
      bstack111lllll1ll_opy_ = None
      bstack111lll1ll1l_opy_ = False
      while retry > 0:
        bstack111lllll1ll_opy_ = self.bstack111llll1lll_opy_(bstack111llll1111_opy_, bstack111ll1ll111_opy_)
        bstack111lll1ll1l_opy_ = self.bstack111ll1l1lll_opy_(bstack111llll1111_opy_, bstack111ll1ll111_opy_, bstack111lllll1ll_opy_)
        if bstack111lll1ll1l_opy_:
          break
        retry -= 1
      return bstack111lllll1ll_opy_, bstack111lll1ll1l_opy_
    except Exception as e:
      self.logger.error(bstack1l1ll11_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤ࡬࡫ࡴࠡࡲࡨࡶࡨࡿࠠࡣ࡫ࡱࡥࡷࡿࠠࡱࡣࡷ࡬ࠧᲔ").format(e))
    return bstack111lllll1ll_opy_, False
  def bstack111ll1l1lll_opy_(self, bstack111llll1111_opy_, bstack111ll1ll111_opy_, bstack111lllll1ll_opy_, bstack111llll11ll_opy_ = 0):
    if bstack111llll11ll_opy_ > 1:
      return False
    if bstack111lllll1ll_opy_ == None or os.path.exists(bstack111lllll1ll_opy_) == False:
      self.logger.warn(bstack1l1ll11_opy_ (u"ࠤࡓࡩࡷࡩࡹࠡࡲࡤࡸ࡭ࠦ࡮ࡰࡶࠣࡪࡴࡻ࡮ࡥ࠮ࠣࡶࡪࡺࡲࡺ࡫ࡱ࡫ࠥࡪ࡯ࡸࡰ࡯ࡳࡦࡪࠢᲕ"))
      return False
    bstack111lll111l1_opy_ = bstack1l1ll11_opy_ (u"ࠥࡢ࠳࠰ࡀࡱࡧࡵࡧࡾࡢ࠯ࡤ࡮࡬ࠤࡡࡪ࠮࡝ࡦ࠮࠲ࡡࡪࠫࠣᲖ")
    command = bstack1l1ll11_opy_ (u"ࠫࢀࢃࠠ࠮࠯ࡹࡩࡷࡹࡩࡰࡰࠪᲗ").format(bstack111lllll1ll_opy_)
    bstack111llll11l1_opy_ = subprocess.check_output(command, shell=True, text=True)
    if re.match(bstack111lll111l1_opy_, bstack111llll11l1_opy_) != None:
      return True
    else:
      self.logger.error(bstack1l1ll11_opy_ (u"ࠧࡖࡥࡳࡥࡼࠤࡻ࡫ࡲࡴ࡫ࡲࡲࠥࡩࡨࡦࡥ࡮ࠤ࡫ࡧࡩ࡭ࡧࡧࠦᲘ"))
      return False
  def bstack111llll1l1l_opy_(self, bstack111ll1l1l1l_opy_, bstack111ll1ll111_opy_):
    try:
      working_dir = os.path.dirname(bstack111ll1l1l1l_opy_)
      shutil.unpack_archive(bstack111ll1l1l1l_opy_, working_dir)
      bstack111lllll1ll_opy_ = os.path.join(working_dir, bstack111ll1ll111_opy_)
      os.chmod(bstack111lllll1ll_opy_, 0o755)
      return bstack111lllll1ll_opy_
    except Exception as e:
      self.logger.error(bstack1l1ll11_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡸࡲࡿ࡯ࡰࠡࡲࡨࡶࡨࡿࠠࡣ࡫ࡱࡥࡷࡿࠢᲙ"))
  def bstack11l1111l1l1_opy_(self):
    try:
      bstack111lllll11l_opy_ = self.config.get(bstack1l1ll11_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠭Ლ"))
      bstack11l1111l1l1_opy_ = bstack111lllll11l_opy_ or (bstack111lllll11l_opy_ is None and self.bstack1l1111ll_opy_)
      if not bstack11l1111l1l1_opy_ or self.config.get(bstack1l1ll11_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫᲛ"), None) not in bstack11ll1l11111_opy_:
        return False
      self.bstack1llll11ll_opy_ = True
      return True
    except Exception as e:
      self.logger.error(bstack1l1ll11_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡪࡥࡵࡧࡦࡸࠥࡶࡥࡳࡥࡼ࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡽࢀࠦᲜ").format(e))
  def bstack11l1111ll1l_opy_(self):
    try:
      bstack11l1111ll1l_opy_ = self.percy_capture_mode
      return bstack11l1111ll1l_opy_
    except Exception as e:
      self.logger.error(bstack1l1ll11_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡤࡦࡶࡨࡧࡹࠦࡰࡦࡴࡦࡽࠥࡩࡡࡱࡶࡸࡶࡪࠦ࡭ࡰࡦࡨ࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡽࢀࠦᲝ").format(e))
  def init(self, bstack1l1111ll_opy_, config, logger):
    self.bstack1l1111ll_opy_ = bstack1l1111ll_opy_
    self.config = config
    self.logger = logger
    if not self.bstack11l1111l1l1_opy_():
      return
    self.bstack111llll111l_opy_ = config.get(bstack1l1ll11_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࡒࡴࡹ࡯࡯࡯ࡵࠪᲞ"), {})
    self.percy_capture_mode = config.get(bstack1l1ll11_opy_ (u"ࠬࡶࡥࡳࡥࡼࡇࡦࡶࡴࡶࡴࡨࡑࡴࡪࡥࠨᲟ"))
    try:
      bstack111llll1111_opy_, bstack111ll1ll111_opy_ = self.bstack111ll1ll1l1_opy_()
      self.bstack11ll11ll11l_opy_ = bstack111ll1ll111_opy_
      bstack111lllll1ll_opy_, bstack111lll1ll1l_opy_ = self.bstack111ll1l111l_opy_(bstack111llll1111_opy_, bstack111ll1ll111_opy_)
      if bstack111lll1ll1l_opy_:
        self.binary_path = bstack111lllll1ll_opy_
        thread = Thread(target=self.bstack111ll1lll1l_opy_)
        thread.start()
      else:
        self.bstack11l1111l1ll_opy_ = True
        self.logger.error(bstack1l1ll11_opy_ (u"ࠨࡉ࡯ࡸࡤࡰ࡮ࡪࠠࡱࡧࡵࡧࡾࠦࡰࡢࡶ࡫ࠤ࡫ࡵࡵ࡯ࡦࠣ࠱ࠥࢁࡽ࠭ࠢࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡹࡴࡢࡴࡷࠤࡕ࡫ࡲࡤࡻࠥᲠ").format(bstack111lllll1ll_opy_))
    except Exception as e:
      self.logger.error(bstack1l1ll11_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡷࡹࡧࡲࡵࠢࡳࡩࡷࡩࡹ࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࢁࡽࠣᲡ").format(e))
  def bstack111lll11l11_opy_(self):
    try:
      logfile = os.path.join(self.working_dir, bstack1l1ll11_opy_ (u"ࠨ࡮ࡲ࡫ࠬᲢ"), bstack1l1ll11_opy_ (u"ࠩࡳࡩࡷࡩࡹ࠯࡮ࡲ࡫ࠬᲣ"))
      os.makedirs(os.path.dirname(logfile)) if not os.path.exists(os.path.dirname(logfile)) else None
      self.logger.debug(bstack1l1ll11_opy_ (u"ࠥࡔࡺࡹࡨࡪࡰࡪࠤࡵ࡫ࡲࡤࡻࠣࡰࡴ࡭ࡳࠡࡣࡷࠤࢀࢃࠢᲤ").format(logfile))
      self.bstack11l11111l11_opy_ = logfile
    except Exception as e:
      self.logger.error(bstack1l1ll11_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡴࡧࡷࠤࡵ࡫ࡲࡤࡻࠣࡰࡴ࡭ࠠࡱࡣࡷ࡬࠱ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡾࢁࠧᲥ").format(e))
  @measure(event_name=EVENTS.bstack11ll1l1ll1l_opy_, stage=STAGE.bstack1ll1111ll1_opy_)
  def bstack111ll1lll1l_opy_(self):
    bstack111ll1l11ll_opy_ = self.bstack111lll11l1l_opy_()
    if bstack111ll1l11ll_opy_ == None:
      self.bstack11l1111l1ll_opy_ = True
      self.logger.error(bstack1l1ll11_opy_ (u"ࠧࡖࡥࡳࡥࡼࠤࡹࡵ࡫ࡦࡰࠣࡲࡴࡺࠠࡧࡱࡸࡲࡩ࠲ࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡹࡧࡲࡵࠢࡳࡩࡷࡩࡹࠣᲦ"))
      return False
    command_args = [bstack1l1ll11_opy_ (u"ࠨࡡࡱࡲ࠽ࡩࡽ࡫ࡣ࠻ࡵࡷࡥࡷࡺࠢᲧ") if self.bstack1l1111ll_opy_ else bstack1l1ll11_opy_ (u"ࠧࡦࡺࡨࡧ࠿ࡹࡴࡢࡴࡷࠫᲨ")]
    bstack11l11l11l1l_opy_ = self.bstack111llll1ll1_opy_()
    if bstack11l11l11l1l_opy_ != None:
      command_args.append(bstack1l1ll11_opy_ (u"ࠣ࠯ࡦࠤࢀࢃࠢᲩ").format(bstack11l11l11l1l_opy_))
    env = os.environ.copy()
    env[bstack1l1ll11_opy_ (u"ࠤࡓࡉࡗࡉ࡙ࡠࡖࡒࡏࡊࡔࠢᲪ")] = bstack111ll1l11ll_opy_
    env[bstack1l1ll11_opy_ (u"ࠥࡘࡍࡥࡂࡖࡋࡏࡈࡤ࡛ࡕࡊࡆࠥᲫ")] = os.environ.get(bstack1l1ll11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩᲬ"), bstack1l1ll11_opy_ (u"ࠬ࠭Ჭ"))
    bstack11l1111111l_opy_ = [self.binary_path]
    self.bstack111lll11l11_opy_()
    self.bstack111ll1llll1_opy_ = self.bstack111lll1l11l_opy_(bstack11l1111111l_opy_ + command_args, env)
    self.logger.debug(bstack1l1ll11_opy_ (u"ࠨࡓࡵࡣࡵࡸ࡮ࡴࡧࠡࡊࡨࡥࡱࡺࡨࠡࡅ࡫ࡩࡨࡱࠢᲮ"))
    bstack111llll11ll_opy_ = 0
    while self.bstack111ll1llll1_opy_.poll() == None:
      bstack11l1111l11l_opy_ = self.bstack111lll1llll_opy_()
      if bstack11l1111l11l_opy_:
        self.logger.debug(bstack1l1ll11_opy_ (u"ࠢࡉࡧࡤࡰࡹ࡮ࠠࡄࡪࡨࡧࡰࠦࡳࡶࡥࡦࡩࡸࡹࡦࡶ࡮ࠥᲯ"))
        self.bstack111ll1lllll_opy_ = True
        return True
      bstack111llll11ll_opy_ += 1
      self.logger.debug(bstack1l1ll11_opy_ (u"ࠣࡊࡨࡥࡱࡺࡨࠡࡅ࡫ࡩࡨࡱࠠࡓࡧࡷࡶࡾࠦ࠭ࠡࡽࢀࠦᲰ").format(bstack111llll11ll_opy_))
      time.sleep(2)
    self.logger.error(bstack1l1ll11_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡴࡢࡴࡷࠤࡵ࡫ࡲࡤࡻ࠯ࠤࡍ࡫ࡡ࡭ࡶ࡫ࠤࡈ࡮ࡥࡤ࡭ࠣࡊࡦ࡯࡬ࡦࡦࠣࡥ࡫ࡺࡥࡳࠢࡾࢁࠥࡧࡴࡵࡧࡰࡴࡹࡹࠢᲱ").format(bstack111llll11ll_opy_))
    self.bstack11l1111l1ll_opy_ = True
    return False
  def bstack111lll1llll_opy_(self, bstack111llll11ll_opy_ = 0):
    if bstack111llll11ll_opy_ > 10:
      return False
    try:
      bstack111lll1111l_opy_ = os.environ.get(bstack1l1ll11_opy_ (u"ࠪࡔࡊࡘࡃ࡚ࡡࡖࡉࡗ࡜ࡅࡓࡡࡄࡈࡉࡘࡅࡔࡕࠪᲲ"), bstack1l1ll11_opy_ (u"ࠫ࡭ࡺࡴࡱ࠼࠲࠳ࡱࡵࡣࡢ࡮࡫ࡳࡸࡺ࠺࠶࠵࠶࠼ࠬᲳ"))
      bstack111lll1ll11_opy_ = bstack111lll1111l_opy_ + bstack11ll1ll111l_opy_
      response = requests.get(bstack111lll1ll11_opy_)
      data = response.json()
      self.percy_build_id = data.get(bstack1l1ll11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࠫᲴ"), {}).get(bstack1l1ll11_opy_ (u"࠭ࡩࡥࠩᲵ"), None)
      return True
    except:
      self.logger.debug(bstack1l1ll11_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦ࡯ࡤࡥࡸࡶࡷ࡫ࡤࠡࡹ࡫࡭ࡱ࡫ࠠࡱࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤ࡭࡫ࡡ࡭ࡶ࡫ࠤࡨ࡮ࡥࡤ࡭ࠣࡶࡪࡹࡰࡰࡰࡶࡩࠧᲶ"))
      return False
  def bstack111lll11l1l_opy_(self):
    bstack111lll11lll_opy_ = bstack1l1ll11_opy_ (u"ࠨࡣࡳࡴࠬᲷ") if self.bstack1l1111ll_opy_ else bstack1l1ll11_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶࡨࠫᲸ")
    bstack11l11111l1l_opy_ = bstack1l1ll11_opy_ (u"ࠥࡹࡳࡪࡥࡧ࡫ࡱࡩࡩࠨᲹ") if self.config.get(bstack1l1ll11_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࠪᲺ")) is None else True
    bstack11l1l111l1l_opy_ = bstack1l1ll11_opy_ (u"ࠧࡧࡰࡪ࠱ࡤࡴࡵࡥࡰࡦࡴࡦࡽ࠴࡭ࡥࡵࡡࡳࡶࡴࡰࡥࡤࡶࡢࡸࡴࡱࡥ࡯ࡁࡱࡥࡲ࡫࠽ࡼࡿࠩࡸࡾࡶࡥ࠾ࡽࢀࠪࡵ࡫ࡲࡤࡻࡀࡿࢂࠨ᲻").format(self.config[bstack1l1ll11_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠫ᲼")], bstack111lll11lll_opy_, bstack11l11111l1l_opy_)
    if self.percy_capture_mode:
      bstack11l1l111l1l_opy_ += bstack1l1ll11_opy_ (u"ࠢࠧࡲࡨࡶࡨࡿ࡟ࡤࡣࡳࡸࡺࡸࡥࡠ࡯ࡲࡨࡪࡃࡻࡾࠤᲽ").format(self.percy_capture_mode)
    uri = bstack11l1lll1l_opy_(bstack11l1l111l1l_opy_)
    try:
      response = bstack1l1ll11lll_opy_(bstack1l1ll11_opy_ (u"ࠨࡉࡈࡘࠬᲾ"), uri, {}, {bstack1l1ll11_opy_ (u"ࠩࡤࡹࡹ࡮ࠧᲿ"): (self.config[bstack1l1ll11_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬ᳀")], self.config[bstack1l1ll11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧ᳁")])})
      if response.status_code == 200:
        data = response.json()
        self.bstack1llll11ll_opy_ = data.get(bstack1l1ll11_opy_ (u"ࠬࡹࡵࡤࡥࡨࡷࡸ࠭᳂"))
        self.percy_capture_mode = data.get(bstack1l1ll11_opy_ (u"࠭ࡰࡦࡴࡦࡽࡤࡩࡡࡱࡶࡸࡶࡪࡥ࡭ࡰࡦࡨࠫ᳃"))
        os.environ[bstack1l1ll11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡆࡔࡆ࡝ࠬ᳄")] = str(self.bstack1llll11ll_opy_)
        os.environ[bstack1l1ll11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡇࡕࡇ࡞ࡥࡃࡂࡒࡗ࡙ࡗࡋ࡟ࡎࡑࡇࡉࠬ᳅")] = str(self.percy_capture_mode)
        if bstack11l11111l1l_opy_ == bstack1l1ll11_opy_ (u"ࠤࡸࡲࡩ࡫ࡦࡪࡰࡨࡨࠧ᳆") and str(self.bstack1llll11ll_opy_).lower() == bstack1l1ll11_opy_ (u"ࠥࡸࡷࡻࡥࠣ᳇"):
          self.bstack1lll11l1_opy_ = True
        if bstack1l1ll11_opy_ (u"ࠦࡹࡵ࡫ࡦࡰࠥ᳈") in data:
          return data[bstack1l1ll11_opy_ (u"ࠧࡺ࡯࡬ࡧࡱࠦ᳉")]
        else:
          raise bstack1l1ll11_opy_ (u"࠭ࡔࡰ࡭ࡨࡲࠥࡔ࡯ࡵࠢࡉࡳࡺࡴࡤࠡ࠯ࠣࡿࢂ࠭᳊").format(data)
      else:
        raise bstack1l1ll11_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡪࡪࡺࡣࡩࠢࡳࡩࡷࡩࡹࠡࡶࡲ࡯ࡪࡴࠬࠡࡔࡨࡷࡵࡵ࡮ࡴࡧࠣࡷࡹࡧࡴࡶࡵࠣ࠱ࠥࢁࡽ࠭ࠢࡕࡩࡸࡶ࡯࡯ࡵࡨࠤࡇࡵࡤࡺࠢ࠰ࠤࢀࢃࠢ᳋").format(response.status_code, response.json())
    except Exception as e:
      self.logger.error(bstack1l1ll11_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡤࡴࡨࡥࡹ࡯࡮ࡨࠢࡳࡩࡷࡩࡹࠡࡲࡵࡳ࡯࡫ࡣࡵࠤ᳌").format(e))
  def bstack111llll1ll1_opy_(self):
    bstack111llllllll_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1ll11_opy_ (u"ࠤࡳࡩࡷࡩࡹࡄࡱࡱࡪ࡮࡭࠮࡫ࡵࡲࡲࠧ᳍"))
    try:
      if bstack1l1ll11_opy_ (u"ࠪࡺࡪࡸࡳࡪࡱࡱࠫ᳎") not in self.bstack111llll111l_opy_:
        self.bstack111llll111l_opy_[bstack1l1ll11_opy_ (u"ࠫࡻ࡫ࡲࡴ࡫ࡲࡲࠬ᳏")] = 2
      with open(bstack111llllllll_opy_, bstack1l1ll11_opy_ (u"ࠬࡽࠧ᳐")) as fp:
        json.dump(self.bstack111llll111l_opy_, fp)
      return bstack111llllllll_opy_
    except Exception as e:
      self.logger.error(bstack1l1ll11_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡦࡶࡪࡧࡴࡦࠢࡳࡩࡷࡩࡹࠡࡥࡲࡲ࡫࠲ࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡿࢂࠨ᳑").format(e))
  def bstack111lll1l11l_opy_(self, cmd, env = os.environ.copy()):
    try:
      if self.bstack111ll1ll11l_opy_ == bstack1l1ll11_opy_ (u"ࠧࡸ࡫ࡱࠫ᳒"):
        bstack111lll1l1l1_opy_ = [bstack1l1ll11_opy_ (u"ࠨࡥࡰࡨ࠳࡫ࡸࡦࠩ᳓"), bstack1l1ll11_opy_ (u"ࠩ࠲ࡧ᳔ࠬ")]
        cmd = bstack111lll1l1l1_opy_ + cmd
      cmd = bstack1l1ll11_opy_ (u"ࠪࠤ᳕ࠬ").join(cmd)
      self.logger.debug(bstack1l1ll11_opy_ (u"ࠦࡗࡻ࡮࡯࡫ࡱ࡫ࠥࢁࡽ᳖ࠣ").format(cmd))
      with open(self.bstack11l11111l11_opy_, bstack1l1ll11_opy_ (u"ࠧࡧ᳗ࠢ")) as bstack111ll1l1111_opy_:
        process = subprocess.Popen(cmd, shell=True, stdout=bstack111ll1l1111_opy_, text=True, stderr=bstack111ll1l1111_opy_, env=env, universal_newlines=True)
      return process
    except Exception as e:
      self.bstack11l1111l1ll_opy_ = True
      self.logger.error(bstack1l1ll11_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡸࡦࡸࡴࠡࡲࡨࡶࡨࡿࠠࡸ࡫ࡷ࡬ࠥࡩ࡭ࡥࠢ࠰ࠤࢀࢃࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱ࠾ࠥࢁࡽ᳘ࠣ").format(cmd, e))
  def shutdown(self):
    try:
      if self.bstack111ll1lllll_opy_:
        self.logger.info(bstack1l1ll11_opy_ (u"ࠢࡔࡶࡲࡴࡵ࡯࡮ࡨࠢࡓࡩࡷࡩࡹ᳙ࠣ"))
        cmd = [self.binary_path, bstack1l1ll11_opy_ (u"ࠣࡧࡻࡩࡨࡀࡳࡵࡱࡳࠦ᳚")]
        self.bstack111lll1l11l_opy_(cmd)
        self.bstack111ll1lllll_opy_ = False
    except Exception as e:
      self.logger.error(bstack1l1ll11_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡴࡰࡲࠣࡷࡪࡹࡳࡪࡱࡱࠤࡼ࡯ࡴࡩࠢࡦࡳࡲࡳࡡ࡯ࡦࠣ࠱ࠥࢁࡽ࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲ࠿ࠦࡻࡾࠤ᳛").format(cmd, e))
  def bstack1l1111l11_opy_(self):
    if not self.bstack1llll11ll_opy_:
      return
    try:
      bstack111lll111ll_opy_ = 0
      while not self.bstack111ll1lllll_opy_ and bstack111lll111ll_opy_ < self.bstack111ll1ll1ll_opy_:
        if self.bstack11l1111l1ll_opy_:
          self.logger.info(bstack1l1ll11_opy_ (u"ࠥࡔࡪࡸࡣࡺࠢࡶࡩࡹࡻࡰࠡࡨࡤ࡭ࡱ࡫ࡤ᳜ࠣ"))
          return
        time.sleep(1)
        bstack111lll111ll_opy_ += 1
      os.environ[bstack1l1ll11_opy_ (u"ࠫࡕࡋࡒࡄ࡛ࡢࡆࡊ࡙ࡔࡠࡒࡏࡅ࡙ࡌࡏࡓࡏ᳝ࠪ")] = str(self.bstack11l111111ll_opy_())
      self.logger.info(bstack1l1ll11_opy_ (u"ࠧࡖࡥࡳࡥࡼࠤࡸ࡫ࡴࡶࡲࠣࡧࡴࡳࡰ࡭ࡧࡷࡩࡩࠨ᳞"))
    except Exception as e:
      self.logger.error(bstack1l1ll11_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡶࡩࡹࡻࡰࠡࡲࡨࡶࡨࡿࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࢀࢃ᳟ࠢ").format(e))
  def bstack11l111111ll_opy_(self):
    if self.bstack1l1111ll_opy_:
      return
    try:
      bstack111ll1l11l1_opy_ = [platform[bstack1l1ll11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬ᳠")].lower() for platform in self.config.get(bstack1l1ll11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ᳡"), [])]
      bstack111ll1l1l11_opy_ = sys.maxsize
      bstack111lllllll1_opy_ = bstack1l1ll11_opy_ (u"᳢ࠩࠪ")
      for browser in bstack111ll1l11l1_opy_:
        if browser in self.bstack11l11111111_opy_:
          bstack111lllll1l1_opy_ = self.bstack11l11111111_opy_[browser]
        if bstack111lllll1l1_opy_ < bstack111ll1l1l11_opy_:
          bstack111ll1l1l11_opy_ = bstack111lllll1l1_opy_
          bstack111lllllll1_opy_ = browser
      return bstack111lllllll1_opy_
    except Exception as e:
      self.logger.error(bstack1l1ll11_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡦࡪࡰࡧࠤࡧ࡫ࡳࡵࠢࡳࡰࡦࡺࡦࡰࡴࡰ࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡽࢀ᳣ࠦ").format(e))
  @classmethod
  def bstack1lll111111_opy_(self):
    return os.getenv(bstack1l1ll11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡊࡘࡃ᳤࡚ࠩ"), bstack1l1ll11_opy_ (u"ࠬࡌࡡ࡭ࡵࡨ᳥ࠫ")).lower()
  @classmethod
  def bstack1ll1111l1l_opy_(self):
    return os.getenv(bstack1l1ll11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡅࡓࡅ࡜ࡣࡈࡇࡐࡕࡗࡕࡉࡤࡓࡏࡅࡇ᳦ࠪ"), bstack1l1ll11_opy_ (u"ࠧࠨ᳧"))
  @classmethod
  def bstack1l1ll1l11ll_opy_(cls, value):
    cls.bstack1lll11l1_opy_ = value
  @classmethod
  def bstack11l111111l1_opy_(cls):
    return cls.bstack1lll11l1_opy_
  @classmethod
  def bstack1l1ll1l11l1_opy_(cls, value):
    cls.percy_build_id = value
  @classmethod
  def bstack111llll1l11_opy_(cls):
    return cls.percy_build_id