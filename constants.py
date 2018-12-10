
import string

MANAGER_ID = 'manager_id'
USER_ID = 'USER_ID_XXX'

CAPTCHA_SOURCE = list(string.ascii_letters)
CAPTCHA_SOURCE.extend(list(map(str, range(0, 10))))