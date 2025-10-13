from typing import Awaitable, Callable
from slugify import slugify
import random
import string

def random_suffix(n=5):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=n))

async def make_unique_slug(title: str, exists_check_fn: Callable[[str], Awaitable[bool]], max_attempts: int = 10) -> str:
    base = slugify(title, lowercase=True, separator='-')
    slug = base
    attempt = 0
    while await exists_check_fn(slug):
        attempt += 1
        slug = f"{base}-{random_suffix()}"
        if attempt > max_attempts:
            slug = f"{base}-{random_suffix(max_attempts)}"
            break
    return slug
