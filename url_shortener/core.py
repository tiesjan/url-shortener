import random
import string


def generate_slug(length=6):
    slug = ''
    while True:
        char = random.SystemRandom().choice(string.ascii_letters + string.digits)
        if slug and slug[-1] == char:
            continue

        slug += char

        if len(slug) == length:
            return slug
