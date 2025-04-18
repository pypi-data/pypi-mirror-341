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
import sys
import logging
import tarfile
import io
import os
import time
import requests
import re
from requests_toolbelt.multipart.encoder import MultipartEncoder
from bstack_utils.constants import bstack11ll1ll11ll_opy_, bstack11ll1l11lll_opy_
import tempfile
import json
bstack11l111ll11l_opy_ = os.getenv(bstack1l1ll11_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡎࡒࡋࡤࡌࡉࡍࡇࠥᯘ"), None) or os.path.join(tempfile.gettempdir(), bstack1l1ll11_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡧࡩࡧࡻࡧ࠯࡮ࡲ࡫ࠧᯙ"))
bstack11l11l1l111_opy_ = os.path.join(bstack1l1ll11_opy_ (u"ࠦࡱࡵࡧࠣᯚ"), bstack1l1ll11_opy_ (u"ࠬࡹࡤ࡬࠯ࡦࡰ࡮࠳ࡤࡦࡤࡸ࡫࠳ࡲ࡯ࡨࠩᯛ"))
logging.Formatter.converter = time.gmtime
def get_logger(name=__name__, level=None):
  logger = logging.getLogger(name)
  if level:
    logging.basicConfig(
      level=level,
      format=bstack1l1ll11_opy_ (u"࠭ࠥࠩࡣࡶࡧࡹ࡯࡭ࡦࠫࡶࠤࡠࠫࠨ࡯ࡣࡰࡩ࠮ࡹ࡝࡜ࠧࠫࡰࡪࡼࡥ࡭ࡰࡤࡱࡪ࠯ࡳ࡞ࠢ࠰ࠤࠪ࠮࡭ࡦࡵࡶࡥ࡬࡫ࠩࡴࠩᯜ"),
      datefmt=bstack1l1ll11_opy_ (u"࡛ࠧࠦ࠰ࠩࡲ࠳ࠥࡥࡖࠨࡌ࠿ࠫࡍ࠻ࠧࡖ࡞ࠬᯝ"),
      stream=sys.stdout
    )
  return logger
def bstack1llll111l1l_opy_():
  bstack11l111ll1ll_opy_ = os.environ.get(bstack1l1ll11_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡃࡋࡑࡅࡗ࡟࡟ࡅࡇࡅ࡙ࡌࠨᯞ"), bstack1l1ll11_opy_ (u"ࠤࡩࡥࡱࡹࡥࠣᯟ"))
  return logging.DEBUG if bstack11l111ll1ll_opy_.lower() == bstack1l1ll11_opy_ (u"ࠥࡸࡷࡻࡥࠣᯠ") else logging.INFO
def bstack1ll111l111l_opy_():
  global bstack11l111ll11l_opy_
  if os.path.exists(bstack11l111ll11l_opy_):
    os.remove(bstack11l111ll11l_opy_)
  if os.path.exists(bstack11l11l1l111_opy_):
    os.remove(bstack11l11l1l111_opy_)
def bstack1lllllll11_opy_():
  for handler in logging.getLogger().handlers:
    logging.getLogger().removeHandler(handler)
def bstack11l11l11_opy_(config, log_level):
  bstack11l111ll111_opy_ = log_level
  if bstack1l1ll11_opy_ (u"ࠫࡱࡵࡧࡍࡧࡹࡩࡱ࠭ᯡ") in config and config[bstack1l1ll11_opy_ (u"ࠬࡲ࡯ࡨࡎࡨࡺࡪࡲࠧᯢ")] in bstack11ll1ll11ll_opy_:
    bstack11l111ll111_opy_ = bstack11ll1ll11ll_opy_[config[bstack1l1ll11_opy_ (u"࠭࡬ࡰࡩࡏࡩࡻ࡫࡬ࠨᯣ")]]
  if config.get(bstack1l1ll11_opy_ (u"ࠧࡥ࡫ࡶࡥࡧࡲࡥࡂࡷࡷࡳࡈࡧࡰࡵࡷࡵࡩࡑࡵࡧࡴࠩᯤ"), False):
    logging.getLogger().setLevel(bstack11l111ll111_opy_)
    return bstack11l111ll111_opy_
  global bstack11l111ll11l_opy_
  bstack1lllllll11_opy_()
  bstack11l11l1l1l1_opy_ = logging.Formatter(
    fmt=bstack1l1ll11_opy_ (u"ࠨࠧࠫࡥࡸࡩࡴࡪ࡯ࡨ࠭ࡸ࡛ࠦࠦࠪࡱࡥࡲ࡫ࠩࡴ࡟࡞ࠩ࠭ࡲࡥࡷࡧ࡯ࡲࡦࡳࡥࠪࡵࡠࠤ࠲ࠦࠥࠩ࡯ࡨࡷࡸࡧࡧࡦࠫࡶࠫᯥ"),
    datefmt=bstack1l1ll11_opy_ (u"ࠩࠨ࡝࠲ࠫ࡭࠮ࠧࡧࡘࠪࡎ࠺ࠦࡏ࠽ࠩࡘࡠ᯦ࠧ"),
  )
  bstack11l111l1lll_opy_ = logging.StreamHandler(sys.stdout)
  file_handler = logging.FileHandler(bstack11l111ll11l_opy_)
  file_handler.setFormatter(bstack11l11l1l1l1_opy_)
  bstack11l111l1lll_opy_.setFormatter(bstack11l11l1l1l1_opy_)
  file_handler.setLevel(logging.DEBUG)
  bstack11l111l1lll_opy_.setLevel(log_level)
  file_handler.addFilter(lambda r: r.name != bstack1l1ll11_opy_ (u"ࠪࡷࡪࡲࡥ࡯࡫ࡸࡱ࠳ࡽࡥࡣࡦࡵ࡭ࡻ࡫ࡲ࠯ࡴࡨࡱࡴࡺࡥ࠯ࡴࡨࡱࡴࡺࡥࡠࡥࡲࡲࡳ࡫ࡣࡵ࡫ࡲࡲࠬᯧ"))
  logging.getLogger().setLevel(logging.DEBUG)
  bstack11l111l1lll_opy_.setLevel(bstack11l111ll111_opy_)
  logging.getLogger().addHandler(bstack11l111l1lll_opy_)
  logging.getLogger().addHandler(file_handler)
  return bstack11l111ll111_opy_
def bstack11l11l11l11_opy_(config):
  try:
    bstack11l11l1l11l_opy_ = set(bstack11ll1l11lll_opy_)
    bstack11l111l1l1l_opy_ = bstack1l1ll11_opy_ (u"ࠫࠬᯨ")
    with open(bstack1l1ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡾࡳ࡬ࠨᯩ")) as bstack11l111lll1l_opy_:
      bstack11l11l11111_opy_ = bstack11l111lll1l_opy_.read()
      bstack11l111l1l1l_opy_ = re.sub(bstack1l1ll11_opy_ (u"ࡸࠧ࡟ࠪ࡟ࡷ࠰࠯࠿ࠤ࠰࠭ࠨࡡࡴࠧᯪ"), bstack1l1ll11_opy_ (u"ࠧࠨᯫ"), bstack11l11l11111_opy_, flags=re.M)
      bstack11l111l1l1l_opy_ = re.sub(
        bstack1l1ll11_opy_ (u"ࡳࠩࡡࠬࡡࡹࠫࠪࡁࠫࠫᯬ") + bstack1l1ll11_opy_ (u"ࠩࡿࠫᯭ").join(bstack11l11l1l11l_opy_) + bstack1l1ll11_opy_ (u"ࠪ࠭࠳࠰ࠤࠨᯮ"),
        bstack1l1ll11_opy_ (u"ࡶࠬࡢ࠲࠻ࠢ࡞ࡖࡊࡊࡁࡄࡖࡈࡈࡢ࠭ᯯ"),
        bstack11l111l1l1l_opy_, flags=re.M | re.I
      )
    def bstack11l11l111ll_opy_(dic):
      bstack11l111lll11_opy_ = {}
      for key, value in dic.items():
        if key in bstack11l11l1l11l_opy_:
          bstack11l111lll11_opy_[key] = bstack1l1ll11_opy_ (u"ࠬࡡࡒࡆࡆࡄࡇ࡙ࡋࡄ࡞ࠩᯰ")
        else:
          if isinstance(value, dict):
            bstack11l111lll11_opy_[key] = bstack11l11l111ll_opy_(value)
          else:
            bstack11l111lll11_opy_[key] = value
      return bstack11l111lll11_opy_
    bstack11l111lll11_opy_ = bstack11l11l111ll_opy_(config)
    return {
      bstack1l1ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡿ࡭࡭ࠩᯱ"): bstack11l111l1l1l_opy_,
      bstack1l1ll11_opy_ (u"ࠧࡧ࡫ࡱࡥࡱࡩ࡯࡯ࡨ࡬࡫࠳ࡰࡳࡰࡰ᯲ࠪ"): json.dumps(bstack11l111lll11_opy_)
    }
  except Exception as e:
    return {}
def bstack11l11l111l1_opy_(inipath, rootpath):
  log_dir = os.path.join(os.getcwd(), bstack1l1ll11_opy_ (u"ࠨ࡮ࡲ࡫᯳ࠬ"))
  if not os.path.exists(log_dir):
    os.makedirs(log_dir)
  bstack11l11l11l1l_opy_ = os.path.join(log_dir, bstack1l1ll11_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࡡࡦࡳࡳ࡬ࡩࡨࡵࠪ᯴"))
  if not os.path.exists(bstack11l11l11l1l_opy_):
    bstack11l11l11lll_opy_ = {
      bstack1l1ll11_opy_ (u"ࠥ࡭ࡳ࡯ࡰࡢࡶ࡫ࠦ᯵"): str(inipath),
      bstack1l1ll11_opy_ (u"ࠦࡷࡵ࡯ࡵࡲࡤࡸ࡭ࠨ᯶"): str(rootpath)
    }
    with open(os.path.join(log_dir, bstack1l1ll11_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࡤࡩ࡯࡯ࡨ࡬࡫ࡸ࠴ࡪࡴࡱࡱࠫ᯷")), bstack1l1ll11_opy_ (u"࠭ࡷࠨ᯸")) as bstack11l111llll1_opy_:
      bstack11l111llll1_opy_.write(json.dumps(bstack11l11l11lll_opy_))
def bstack11l11l1111l_opy_():
  try:
    bstack11l11l11l1l_opy_ = os.path.join(os.getcwd(), bstack1l1ll11_opy_ (u"ࠧ࡭ࡱࡪࠫ᯹"), bstack1l1ll11_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡠࡥࡲࡲ࡫࡯ࡧࡴ࠰࡭ࡷࡴࡴࠧ᯺"))
    if os.path.exists(bstack11l11l11l1l_opy_):
      with open(bstack11l11l11l1l_opy_, bstack1l1ll11_opy_ (u"ࠩࡵࠫ᯻")) as bstack11l111llll1_opy_:
        bstack11l111l1ll1_opy_ = json.load(bstack11l111llll1_opy_)
      return bstack11l111l1ll1_opy_.get(bstack1l1ll11_opy_ (u"ࠪ࡭ࡳ࡯ࡰࡢࡶ࡫ࠫ᯼"), bstack1l1ll11_opy_ (u"ࠫࠬ᯽")), bstack11l111l1ll1_opy_.get(bstack1l1ll11_opy_ (u"ࠬࡸ࡯ࡰࡶࡳࡥࡹ࡮ࠧ᯾"), bstack1l1ll11_opy_ (u"࠭ࠧ᯿"))
  except:
    pass
  return None, None
def bstack11l111lllll_opy_():
  try:
    bstack11l11l11l1l_opy_ = os.path.join(os.getcwd(), bstack1l1ll11_opy_ (u"ࠧ࡭ࡱࡪࠫᰀ"), bstack1l1ll11_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡠࡥࡲࡲ࡫࡯ࡧࡴ࠰࡭ࡷࡴࡴࠧᰁ"))
    if os.path.exists(bstack11l11l11l1l_opy_):
      os.remove(bstack11l11l11l1l_opy_)
  except:
    pass
def bstack1l11lll1_opy_(config):
  from bstack_utils.helper import bstack11llllllll_opy_
  global bstack11l111ll11l_opy_
  try:
    if config.get(bstack1l1ll11_opy_ (u"ࠩࡧ࡭ࡸࡧࡢ࡭ࡧࡄࡹࡹࡵࡃࡢࡲࡷࡹࡷ࡫ࡌࡰࡩࡶࠫᰂ"), False):
      return
    uuid = os.getenv(bstack1l1ll11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨᰃ")) if os.getenv(bstack1l1ll11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩᰄ")) else bstack11llllllll_opy_.get_property(bstack1l1ll11_opy_ (u"ࠧࡹࡤ࡬ࡔࡸࡲࡎࡪࠢᰅ"))
    if not uuid or uuid == bstack1l1ll11_opy_ (u"࠭࡮ࡶ࡮࡯ࠫᰆ"):
      return
    bstack11l11l11ll1_opy_ = [bstack1l1ll11_opy_ (u"ࠧࡳࡧࡴࡹ࡮ࡸࡥ࡮ࡧࡱࡸࡸ࠴ࡴࡹࡶࠪᰇ"), bstack1l1ll11_opy_ (u"ࠨࡒ࡬ࡴ࡫࡯࡬ࡦࠩᰈ"), bstack1l1ll11_opy_ (u"ࠩࡳࡽࡵࡸ࡯࡫ࡧࡦࡸ࠳ࡺ࡯࡮࡮ࠪᰉ"), bstack11l111ll11l_opy_, bstack11l11l1l111_opy_]
    bstack11l11l1l1ll_opy_, root_path = bstack11l11l1111l_opy_()
    if bstack11l11l1l1ll_opy_ != None:
      bstack11l11l11ll1_opy_.append(bstack11l11l1l1ll_opy_)
    if root_path != None:
      bstack11l11l11ll1_opy_.append(os.path.join(root_path, bstack1l1ll11_opy_ (u"ࠪࡧࡴࡴࡦࡵࡧࡶࡸ࠳ࡶࡹࠨᰊ")))
    bstack1lllllll11_opy_()
    logging.shutdown()
    output_file = os.path.join(tempfile.gettempdir(), bstack1l1ll11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠱ࡱࡵࡧࡴ࠯ࠪᰋ") + uuid + bstack1l1ll11_opy_ (u"ࠬ࠴ࡴࡢࡴ࠱࡫ࡿ࠭ᰌ"))
    with tarfile.open(output_file, bstack1l1ll11_opy_ (u"ࠨࡷ࠻ࡩࡽࠦᰍ")) as archive:
      for file in filter(lambda f: os.path.exists(f), bstack11l11l11ll1_opy_):
        try:
          archive.add(file,  arcname=os.path.basename(file))
        except:
          pass
      for name, data in bstack11l11l11l11_opy_(config).items():
        tarinfo = tarfile.TarInfo(name)
        bstack11l111ll1l1_opy_ = data.encode()
        tarinfo.size = len(bstack11l111ll1l1_opy_)
        archive.addfile(tarinfo, io.BytesIO(bstack11l111ll1l1_opy_))
    bstack11lll1l1l1_opy_ = MultipartEncoder(
      fields= {
        bstack1l1ll11_opy_ (u"ࠧࡥࡣࡷࡥࠬᰎ"): (os.path.basename(output_file), open(os.path.abspath(output_file), bstack1l1ll11_opy_ (u"ࠨࡴࡥࠫᰏ")), bstack1l1ll11_opy_ (u"ࠩࡤࡴࡵࡲࡩࡤࡣࡷ࡭ࡴࡴ࠯ࡹ࠯ࡪࡾ࡮ࡶࠧᰐ")),
        bstack1l1ll11_opy_ (u"ࠪࡧࡱ࡯ࡥ࡯ࡶࡅࡹ࡮ࡲࡤࡖࡷ࡬ࡨࠬᰑ"): uuid
      }
    )
    response = requests.post(
      bstack1l1ll11_opy_ (u"ࠦ࡭ࡺࡴࡱࡵ࠽࠳࠴ࡻࡰ࡭ࡱࡤࡨ࠲ࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡥ࡯࡭ࡪࡴࡴ࠮࡮ࡲ࡫ࡸ࠵ࡵࡱ࡮ࡲࡥࡩࠨᰒ"),
      data=bstack11lll1l1l1_opy_,
      headers={bstack1l1ll11_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡔࡺࡲࡨࠫᰓ"): bstack11lll1l1l1_opy_.content_type},
      auth=(config[bstack1l1ll11_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨᰔ")], config[bstack1l1ll11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪᰕ")])
    )
    os.remove(output_file)
    if response.status_code != 200:
      get_logger().debug(bstack1l1ll11_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡶࡲ࡯ࡳࡦࡪࠠ࡭ࡱࡪࡷ࠿ࠦࠧᰖ") + response.status_code)
  except Exception as e:
    get_logger().debug(bstack1l1ll11_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡵࡨࡲࡩ࡯࡮ࡨࠢ࡯ࡳ࡬ࡹ࠺ࠨᰗ") + str(e))
  finally:
    try:
      bstack1ll111l111l_opy_()
      bstack11l111lllll_opy_()
    except:
      pass