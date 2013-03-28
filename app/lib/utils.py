import random
import string


def random_string(size=6, chars=string.ascii_letters + string.digits):
    """ Generate random string """
    return ''.join(random.choice(chars) for _ in range(size))
