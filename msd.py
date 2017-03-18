#!/usr/bin/python

from dateutil import relativedelta as rdelta
from datetime import date


d1 = date(1955,1,1)
d2 = date(2012,3,1)
rd = rdelta.relativedelta(d2,d1)

nynm = "{0.years},{0.months}".format(rd)
ny = int(nynm.split(",")[0])
nm = int(nynm.split(",")[1])

nmonths = (ny*12) + nm



