"""
Implements useful new maps that make development that slightly easier.
"""

from .version import __version__
from .attribute_dict import AttributeDict
from .group_dict import GroupDict
from .super_dict import SuperDict
from .virtual_iterable import VirtualIterable

__all__ = [
    "__version__",
    "AttributeDict",
    "GroupDict",
    "SuperDict",
    "VirtualIterable",
]
