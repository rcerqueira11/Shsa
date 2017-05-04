# -*- enconding: utf-8 -*-

from Crypto.Cipher import AES
import base64
import random
import time

SECRET_TAB_KEY = u"tVW7I-@_jWloKPlA@\59TtqT%$UeQF1LM"

BLOCK_SIZE = 32
PADDING = '@'
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING
cipher = AES.new(SECRET_TAB_KEY)

encode = lambda s: base64.b64encode(cipher.encrypt(pad(s)),'!-')
decode = lambda e: cipher.decrypt(base64.b64decode(e.encode("ascii"),'!-')).rstrip(PADDING)
