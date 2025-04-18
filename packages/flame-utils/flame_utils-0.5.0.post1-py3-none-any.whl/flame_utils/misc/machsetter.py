#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from flame import Machine

import numpy as np

_LOGGER = logging.getLogger(__name__)


def machine_setter(_latfile=None, _machine=None, _handle_name=None):
    """ set flame machine, prefer *_latfile*

    :return: FLAME machine object
    """
    if _latfile is not None:
        try:
            with open(_latfile, 'rb') as f:
                m = Machine(f)
        except:
            if _machine is None:
                _LOGGER.error("{}: Failed to initialize flame machine".format(
                    _handle_name))
                return None
            else:
                _LOGGER.warning("{}: Failed to initialize flame machine, "
                                "use _machine instead".format(_handle_name))
                m = _machine
    else:
        if _machine is None:
            return None
        else:
            m = _machine
    return m


def is_zeros_states(s):
    """ test if flame machine states is all zeros

    Returns
    -------
    True or False
        True if is all zeros, else False
    """
    return getattr(s, 'ref_IonEk') == 0.0


def get_share_keys(machine):
    """Get share keys of lattice file.

    Returns
    -------
    List of share keys
    """
    if not isinstance(machine, Machine):
        return None
    mks = machine.conf().keys()
    share_keys = [k for k in mks if k not in ("elements", "name")]
    return  share_keys