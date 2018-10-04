# -*- coding: utf-8 -*-

"""enables to import modules through the web, by adding urls to the python path.
"""
#authors: Jure Vrscaj <jure@codeshift.net> (copyright (c) 2006-10),
#         송영진(MyEvan) <myevan_net@naver.com> (copyright (c) 2010), 
#         Alex Bodnaru <alexbodn@012.net.il> (copyright (c) 2010)

# This is free software; you may use, copy, modify and/or distribute this work
# under the terms of the MIT License.


import sys
from urlimport import UrlFinder, config, reset, DefaultErrorHandler

__all__ = ('config', 'reset', 'DefaultErrorHandler')

# register The Hook
sys.path_hooks = \
    [x for x in sys.path_hooks if x.__name__ != 'UrlFinder'] + [UrlFinder]


