from MedoSigner import Argus,Gorgon,md5,Ladon
from urllib.parse import urlencode
import time
def Sign(params, payload: str = None, sec_device_id: str = "", cookie: str or None = None, aid: int = 1233, license_id: int = 1611921764, sdk_version_str: str = "2.3.1.i18n", sdk_version: int =2, platform: int = 19, unix: int = None):
	       x_ss_stub = md5(payload.encode('utf-8')).hexdigest() if payload != None else None
	       data=payload
	       if not unix: unix = int(time.time())
	       return Gorgon(params, unix, payload, cookie).get_value() | { "x-ladon"   : Ladon.encrypt(unix, license_id, aid),"x-argus"   : Argus.get_sign(params, x_ss_stub, unix,platform        = platform,aid             = aid,license_id      = license_id,sec_device_id   = sec_device_id,sdk_version     = sdk_version_str, sdk_version_int = sdk_version)}
def Params(params):
	m = Sign(params=urlencode(params),payload="",cookie="")
	return m