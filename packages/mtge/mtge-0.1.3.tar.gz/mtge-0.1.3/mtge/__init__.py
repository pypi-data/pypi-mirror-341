__doc__= """mtge
=====
Mortgage Cashflow Calculator"""
__author__ = 'Ted Hong'
__credits__ = 'Beyondbond Risk Lab'
__name__ = 'mtge'
from .xux64 import *
from .mtge_calc import *
all_vars = {k:v for (k,v) in globals().items() if callable(v)}
__all__ = list(all_vars.keys())
