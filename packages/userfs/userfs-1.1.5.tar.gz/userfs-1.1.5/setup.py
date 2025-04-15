# =====================================
# generator=datazen
# version=3.2.1
# hash=856439de96bc85ee8796f6c4c686eda7
# =====================================

"""
userfs - Package definition for distribution.
"""

# third-party
try:
    from setuptools_wrapper.setup import setup
except (ImportError, ModuleNotFoundError):
    from userfs_bootstrap.setup import setup  # type: ignore

# internal
from userfs import DESCRIPTION, PKG_NAME, VERSION

author_info = {
    "name": "Libre Embedded",
    "email": "vaughn@libre-embedded.com",
    "username": "libre-embedded",
}
pkg_info = {
    "name": PKG_NAME,
    "slug": PKG_NAME.replace("-", "_"),
    "version": VERSION,
    "description": DESCRIPTION,
    "versions": [
        "3.12",
        "3.13",
    ],
}
setup(
    pkg_info,
    author_info,
)
