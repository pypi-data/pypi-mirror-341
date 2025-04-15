import logging

import odoo

from ..adapter import StorageAdapter
from . import patcher14
from .method_patcher import MethodPatcher

_logger = logging.getLogger("odoo_filestore_s3")

OdooStream = odoo.http.Stream


def _from_attachment(cls: type[OdooStream], attachment):
    return StorageAdapter.stream_from_attachment(cls, attachment)


PATCHED_METHOD = patcher14.PATCHED_METHOD + [
    MethodPatcher(OdooStream, "from_attachment", classmethod(_from_attachment)),
]
