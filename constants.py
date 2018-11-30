
import string

MANAGER_ID = 'manager_id'

CAPTCHA_SOURCE = list(string.ascii_letters)
CAPTCHA_SOURCE.extend(list(map(str, range(0, 10))))