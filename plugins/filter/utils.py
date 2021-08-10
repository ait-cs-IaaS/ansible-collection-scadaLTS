# Make coding more python3-ish
from __future__ import absolute_import, division, print_function

import base64
import hashlib

from ansible.errors import AnsibleFilterError
from ansible.module_utils._text import to_bytes, to_text

__metaclass__ = type


def get_hash_bytes(data, hashtype='sha1'):
    """Generate a hash bytes from the given data string

    Args:
        data: The data string to hash
        hashtype (str, optional): The hash algorithm to use. Defaults to 'sha1'.

    Raises:
        AnsibleFilterError: If the given hash algorithm is not supported

    Returns:
        bytes: The hash in bytes format
    """
    try:
        h = hashlib.new(hashtype)
    except Exception as e:
        # hash is not supported?
        raise AnsibleFilterError(e)

    h.update(to_bytes(data, errors='surrogate_or_strict'))
    return h.digest()


def get_scadalts_password_hash(data, hashtype='sha1'):
    """Generate a base64 encoded hash digest as used by ScadaLTS to store passwords.

    Args:
        data: The password string
        hashtype (str, optional): The hash algorithm to use. Defaults to 'sha1'.

    Raises:
        AnsibleFilterError: If the given hash algorithm is not supported

    Returns:
        str: The b64 encoded password hash
    """
    return to_text(base64.b64encode(get_hash_bytes(data, hashtype=hashtype)))


class FilterModule(object):
    ''' ScadaLTS utility ansible filters '''

    def filters(self):
        return {
            "hash_bytes": get_hash_bytes,
            "password_hash": get_scadalts_password_hash
        }
