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
import sys
import logging
import tarfile
import io
import os
import time
import requests
import re
from requests_toolbelt.multipart.encoder import MultipartEncoder
from bstack_utils.constants import bstack11ll1l11l1l_opy_, bstack11lll11111l_opy_
import tempfile
import json
bstack11l111ll11l_opy_ = os.getenv(bstack1l1_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡍࡑࡊࡣࡋࡏࡌࡆࠤᯗ"), None) or os.path.join(tempfile.gettempdir(), bstack1l1_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡦࡨࡦࡺ࡭࠮࡭ࡱࡪࠦᯘ"))
bstack11l11l11l11_opy_ = os.path.join(bstack1l1_opy_ (u"ࠥࡰࡴ࡭ࠢᯙ"), bstack1l1_opy_ (u"ࠫࡸࡪ࡫࠮ࡥ࡯࡭࠲ࡪࡥࡣࡷࡪ࠲ࡱࡵࡧࠨᯚ"))
logging.Formatter.converter = time.gmtime
def get_logger(name=__name__, level=None):
  logger = logging.getLogger(name)
  if level:
    logging.basicConfig(
      level=level,
      format=bstack1l1_opy_ (u"ࠬࠫࠨࡢࡵࡦࡸ࡮ࡳࡥࠪࡵࠣ࡟ࠪ࠮࡮ࡢ࡯ࡨ࠭ࡸࡣ࡛ࠦࠪ࡯ࡩࡻ࡫࡬࡯ࡣࡰࡩ࠮ࡹ࡝ࠡ࠯ࠣࠩ࠭ࡳࡥࡴࡵࡤ࡫ࡪ࠯ࡳࠨᯛ"),
      datefmt=bstack1l1_opy_ (u"࡚࠭ࠥ࠯ࠨࡱ࠲ࠫࡤࡕࠧࡋ࠾ࠪࡓ࠺ࠦࡕ࡝ࠫᯜ"),
      stream=sys.stdout
    )
  return logger
def bstack1lll1111lll_opy_():
  bstack11l111l1l1l_opy_ = os.environ.get(bstack1l1_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡂࡊࡐࡄࡖ࡞ࡥࡄࡆࡄࡘࡋࠧᯝ"), bstack1l1_opy_ (u"ࠣࡨࡤࡰࡸ࡫ࠢᯞ"))
  return logging.DEBUG if bstack11l111l1l1l_opy_.lower() == bstack1l1_opy_ (u"ࠤࡷࡶࡺ࡫ࠢᯟ") else logging.INFO
def bstack1ll111l1l1l_opy_():
  global bstack11l111ll11l_opy_
  if os.path.exists(bstack11l111ll11l_opy_):
    os.remove(bstack11l111ll11l_opy_)
  if os.path.exists(bstack11l11l11l11_opy_):
    os.remove(bstack11l11l11l11_opy_)
def bstack1ll1l1l11_opy_():
  for handler in logging.getLogger().handlers:
    logging.getLogger().removeHandler(handler)
def bstack1ll11l11ll_opy_(config, log_level):
  bstack11l111l1lll_opy_ = log_level
  if bstack1l1_opy_ (u"ࠪࡰࡴ࡭ࡌࡦࡸࡨࡰࠬᯠ") in config and config[bstack1l1_opy_ (u"ࠫࡱࡵࡧࡍࡧࡹࡩࡱ࠭ᯡ")] in bstack11ll1l11l1l_opy_:
    bstack11l111l1lll_opy_ = bstack11ll1l11l1l_opy_[config[bstack1l1_opy_ (u"ࠬࡲ࡯ࡨࡎࡨࡺࡪࡲࠧᯢ")]]
  if config.get(bstack1l1_opy_ (u"࠭ࡤࡪࡵࡤࡦࡱ࡫ࡁࡶࡶࡲࡇࡦࡶࡴࡶࡴࡨࡐࡴ࡭ࡳࠨᯣ"), False):
    logging.getLogger().setLevel(bstack11l111l1lll_opy_)
    return bstack11l111l1lll_opy_
  global bstack11l111ll11l_opy_
  bstack1ll1l1l11_opy_()
  bstack11l11l11lll_opy_ = logging.Formatter(
    fmt=bstack1l1_opy_ (u"ࠧࠦࠪࡤࡷࡨࡺࡩ࡮ࡧࠬࡷࠥࡡࠥࠩࡰࡤࡱࡪ࠯ࡳ࡞࡝ࠨࠬࡱ࡫ࡶࡦ࡮ࡱࡥࡲ࡫ࠩࡴ࡟ࠣ࠱ࠥࠫࠨ࡮ࡧࡶࡷࡦ࡭ࡥࠪࡵࠪᯤ"),
    datefmt=bstack1l1_opy_ (u"ࠨࠧ࡜࠱ࠪࡳ࠭ࠦࡦࡗࠩࡍࡀࠥࡎ࠼ࠨࡗ࡟࠭ᯥ"),
  )
  bstack11l11l1l1ll_opy_ = logging.StreamHandler(sys.stdout)
  file_handler = logging.FileHandler(bstack11l111ll11l_opy_)
  file_handler.setFormatter(bstack11l11l11lll_opy_)
  bstack11l11l1l1ll_opy_.setFormatter(bstack11l11l11lll_opy_)
  file_handler.setLevel(logging.DEBUG)
  bstack11l11l1l1ll_opy_.setLevel(log_level)
  file_handler.addFilter(lambda r: r.name != bstack1l1_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰ࠲ࡼ࡫ࡢࡥࡴ࡬ࡺࡪࡸ࠮ࡳࡧࡰࡳࡹ࡫࠮ࡳࡧࡰࡳࡹ࡫࡟ࡤࡱࡱࡲࡪࡩࡴࡪࡱࡱ᯦ࠫ"))
  logging.getLogger().setLevel(logging.DEBUG)
  bstack11l11l1l1ll_opy_.setLevel(bstack11l111l1lll_opy_)
  logging.getLogger().addHandler(bstack11l11l1l1ll_opy_)
  logging.getLogger().addHandler(file_handler)
  return bstack11l111l1lll_opy_
def bstack11l11l11l1l_opy_(config):
  try:
    bstack11l11l1l1l1_opy_ = set(bstack11lll11111l_opy_)
    bstack11l111lll11_opy_ = bstack1l1_opy_ (u"ࠪࠫᯧ")
    with open(bstack1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡽࡲࡲࠧᯨ")) as bstack11l111ll1ll_opy_:
      bstack11l111l1ll1_opy_ = bstack11l111ll1ll_opy_.read()
      bstack11l111lll11_opy_ = re.sub(bstack1l1_opy_ (u"ࡷ࠭࡞ࠩ࡞ࡶ࠯࠮ࡅࠣ࠯ࠬࠧࡠࡳ࠭ᯩ"), bstack1l1_opy_ (u"࠭ࠧᯪ"), bstack11l111l1ll1_opy_, flags=re.M)
      bstack11l111lll11_opy_ = re.sub(
        bstack1l1_opy_ (u"ࡲࠨࡠࠫࡠࡸ࠱ࠩࡀࠪࠪᯫ") + bstack1l1_opy_ (u"ࠨࡾࠪᯬ").join(bstack11l11l1l1l1_opy_) + bstack1l1_opy_ (u"ࠩࠬ࠲࠯ࠪࠧᯭ"),
        bstack1l1_opy_ (u"ࡵࠫࡡ࠸࠺ࠡ࡝ࡕࡉࡉࡇࡃࡕࡇࡇࡡࠬᯮ"),
        bstack11l111lll11_opy_, flags=re.M | re.I
      )
    def bstack11l111llll1_opy_(dic):
      bstack11l11l1l111_opy_ = {}
      for key, value in dic.items():
        if key in bstack11l11l1l1l1_opy_:
          bstack11l11l1l111_opy_[key] = bstack1l1_opy_ (u"ࠫࡠࡘࡅࡅࡃࡆࡘࡊࡊ࡝ࠨᯯ")
        else:
          if isinstance(value, dict):
            bstack11l11l1l111_opy_[key] = bstack11l111llll1_opy_(value)
          else:
            bstack11l11l1l111_opy_[key] = value
      return bstack11l11l1l111_opy_
    bstack11l11l1l111_opy_ = bstack11l111llll1_opy_(config)
    return {
      bstack1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡾࡳ࡬ࠨᯰ"): bstack11l111lll11_opy_,
      bstack1l1_opy_ (u"࠭ࡦࡪࡰࡤࡰࡨࡵ࡮ࡧ࡫ࡪ࠲࡯ࡹ࡯࡯ࠩᯱ"): json.dumps(bstack11l11l1l111_opy_)
    }
  except Exception as e:
    return {}
def bstack11l111lll1l_opy_(inipath, rootpath):
  log_dir = os.path.join(os.getcwd(), bstack1l1_opy_ (u"ࠧ࡭ࡱࡪ᯲ࠫ"))
  if not os.path.exists(log_dir):
    os.makedirs(log_dir)
  bstack11l11l111ll_opy_ = os.path.join(log_dir, bstack1l1_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡠࡥࡲࡲ࡫࡯ࡧࡴ᯳ࠩ"))
  if not os.path.exists(bstack11l11l111ll_opy_):
    bstack11l111ll111_opy_ = {
      bstack1l1_opy_ (u"ࠤ࡬ࡲ࡮ࡶࡡࡵࡪࠥ᯴"): str(inipath),
      bstack1l1_opy_ (u"ࠥࡶࡴࡵࡴࡱࡣࡷ࡬ࠧ᯵"): str(rootpath)
    }
    with open(os.path.join(log_dir, bstack1l1_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࡣࡨࡵ࡮ࡧ࡫ࡪࡷ࠳ࡰࡳࡰࡰࠪ᯶")), bstack1l1_opy_ (u"ࠬࡽࠧ᯷")) as bstack11l11l1l11l_opy_:
      bstack11l11l1l11l_opy_.write(json.dumps(bstack11l111ll111_opy_))
def bstack11l11l111l1_opy_():
  try:
    bstack11l11l111ll_opy_ = os.path.join(os.getcwd(), bstack1l1_opy_ (u"࠭࡬ࡰࡩࠪ᯸"), bstack1l1_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࡟ࡤࡱࡱࡪ࡮࡭ࡳ࠯࡬ࡶࡳࡳ࠭᯹"))
    if os.path.exists(bstack11l11l111ll_opy_):
      with open(bstack11l11l111ll_opy_, bstack1l1_opy_ (u"ࠨࡴࠪ᯺")) as bstack11l11l1l11l_opy_:
        bstack11l11l1111l_opy_ = json.load(bstack11l11l1l11l_opy_)
      return bstack11l11l1111l_opy_.get(bstack1l1_opy_ (u"ࠩ࡬ࡲ࡮ࡶࡡࡵࡪࠪ᯻"), bstack1l1_opy_ (u"ࠪࠫ᯼")), bstack11l11l1111l_opy_.get(bstack1l1_opy_ (u"ࠫࡷࡵ࡯ࡵࡲࡤࡸ࡭࠭᯽"), bstack1l1_opy_ (u"ࠬ࠭᯾"))
  except:
    pass
  return None, None
def bstack11l111ll1l1_opy_():
  try:
    bstack11l11l111ll_opy_ = os.path.join(os.getcwd(), bstack1l1_opy_ (u"࠭࡬ࡰࡩࠪ᯿"), bstack1l1_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࡟ࡤࡱࡱࡪ࡮࡭ࡳ࠯࡬ࡶࡳࡳ࠭ᰀ"))
    if os.path.exists(bstack11l11l111ll_opy_):
      os.remove(bstack11l11l111ll_opy_)
  except:
    pass
def bstack1ll1l1l1l1_opy_(config):
  from bstack_utils.helper import bstack11llllll1_opy_
  global bstack11l111ll11l_opy_
  try:
    if config.get(bstack1l1_opy_ (u"ࠨࡦ࡬ࡷࡦࡨ࡬ࡦࡃࡸࡸࡴࡉࡡࡱࡶࡸࡶࡪࡒ࡯ࡨࡵࠪᰁ"), False):
      return
    uuid = os.getenv(bstack1l1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧᰂ")) if os.getenv(bstack1l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨᰃ")) else bstack11llllll1_opy_.get_property(bstack1l1_opy_ (u"ࠦࡸࡪ࡫ࡓࡷࡱࡍࡩࠨᰄ"))
    if not uuid or uuid == bstack1l1_opy_ (u"ࠬࡴࡵ࡭࡮ࠪᰅ"):
      return
    bstack11l111lllll_opy_ = [bstack1l1_opy_ (u"࠭ࡲࡦࡳࡸ࡭ࡷ࡫࡭ࡦࡰࡷࡷ࠳ࡺࡸࡵࠩᰆ"), bstack1l1_opy_ (u"ࠧࡑ࡫ࡳࡪ࡮ࡲࡥࠨᰇ"), bstack1l1_opy_ (u"ࠨࡲࡼࡴࡷࡵࡪࡦࡥࡷ࠲ࡹࡵ࡭࡭ࠩᰈ"), bstack11l111ll11l_opy_, bstack11l11l11l11_opy_]
    bstack11l11l11ll1_opy_, root_path = bstack11l11l111l1_opy_()
    if bstack11l11l11ll1_opy_ != None:
      bstack11l111lllll_opy_.append(bstack11l11l11ll1_opy_)
    if root_path != None:
      bstack11l111lllll_opy_.append(os.path.join(root_path, bstack1l1_opy_ (u"ࠩࡦࡳࡳ࡬ࡴࡦࡵࡷ࠲ࡵࡿࠧᰉ")))
    bstack1ll1l1l11_opy_()
    logging.shutdown()
    output_file = os.path.join(tempfile.gettempdir(), bstack1l1_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠰ࡰࡴ࡭ࡳ࠮ࠩᰊ") + uuid + bstack1l1_opy_ (u"ࠫ࠳ࡺࡡࡳ࠰ࡪࡾࠬᰋ"))
    with tarfile.open(output_file, bstack1l1_opy_ (u"ࠧࡽ࠺ࡨࡼࠥᰌ")) as archive:
      for file in filter(lambda f: os.path.exists(f), bstack11l111lllll_opy_):
        try:
          archive.add(file,  arcname=os.path.basename(file))
        except:
          pass
      for name, data in bstack11l11l11l1l_opy_(config).items():
        tarinfo = tarfile.TarInfo(name)
        bstack11l11l11111_opy_ = data.encode()
        tarinfo.size = len(bstack11l11l11111_opy_)
        archive.addfile(tarinfo, io.BytesIO(bstack11l11l11111_opy_))
    bstack111ll111_opy_ = MultipartEncoder(
      fields= {
        bstack1l1_opy_ (u"࠭ࡤࡢࡶࡤࠫᰍ"): (os.path.basename(output_file), open(os.path.abspath(output_file), bstack1l1_opy_ (u"ࠧࡳࡤࠪᰎ")), bstack1l1_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡸ࠮ࡩࡽ࡭ࡵ࠭ᰏ")),
        bstack1l1_opy_ (u"ࠩࡦࡰ࡮࡫࡮ࡵࡄࡸ࡭ࡱࡪࡕࡶ࡫ࡧࠫᰐ"): uuid
      }
    )
    response = requests.post(
      bstack1l1_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳ࡺࡶ࡬ࡰࡣࡧ࠱ࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡤ࡮࡬ࡩࡳࡺ࠭࡭ࡱࡪࡷ࠴ࡻࡰ࡭ࡱࡤࡨࠧᰑ"),
      data=bstack111ll111_opy_,
      headers={bstack1l1_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲࡚ࡹࡱࡧࠪᰒ"): bstack111ll111_opy_.content_type},
      auth=(config[bstack1l1_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧᰓ")], config[bstack1l1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩᰔ")])
    )
    os.remove(output_file)
    if response.status_code != 200:
      get_logger().debug(bstack1l1_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡵࡱ࡮ࡲࡥࡩࠦ࡬ࡰࡩࡶ࠾ࠥ࠭ᰕ") + response.status_code)
  except Exception as e:
    get_logger().debug(bstack1l1_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡴࡧࡱࡨ࡮ࡴࡧࠡ࡮ࡲ࡫ࡸࡀࠧᰖ") + str(e))
  finally:
    try:
      bstack1ll111l1l1l_opy_()
      bstack11l111ll1l1_opy_()
    except:
      pass