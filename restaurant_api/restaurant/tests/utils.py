import shutil
from functools import wraps

from config.settings import BASE_DIR


def rewrite_media_dir(func):
    """
    Sets a fake media directory for testing which will be deleted in the end.
    """

    @wraps(func)
    def inner(*args, **kwargs):
        new_media_root = BASE_DIR / 'test_media'
        try:
            with args[0].settings(MEDIA_ROOT=new_media_root):
                func(*args, **kwargs)
        finally:
            shutil.rmtree(new_media_root)

    return inner
