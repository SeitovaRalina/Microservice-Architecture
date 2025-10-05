import re
import random
import string

def slugify(value: str) -> str:
    value = value.lower()
    value = re.sub(r"[^a-z0-9\s-]", "", value)
    value = re.sub(r"[\s-]+", "-", value).strip("-")
    return value

def random_suffix(n=6):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=n))

def make_unique_slug(title: str, exists_check_fn):
    """
    exists_check_fn(slug: str) -> bool  ; returns True if slug already exists
    """
    base = slugify(title)
    slug = base
    attempt = 0
    while exists_check_fn(slug):
        attempt += 1
        slug = f"{base}-{random_suffix()}"
        if attempt > 10:
            slug = f"{base}-{random_suffix(12)}"
            break
    return slug
