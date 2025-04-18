# -*- coding: utf-8 -*-
# Copyright 2020 by Forschungszentrum Juelich GmbH
# Author: J. Caron
#
"""Subpackage containing functionality for visualisation of multidimensional fields."""


from . import fields
from . import io
from . import models
from . import reconstruct
from . import vis
from . import utils

__version__ = "0.3.5"
__git_revision__ = "undefined"

import logging
_log = logging.getLogger(__name__)
_log.info(f'Imported EMPyRe V-{__version__}')
del logging

__all__ = ['fields', 'io', 'models', 'reconstruct', 'vis', 'utils']
