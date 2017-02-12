#!/usr/bin/env python
# --------------------------------------------------------
#       Script to parse credit card information into statistics
# created on February 2nd 2017 by M. Reichmann (remichae@phys.ethz.ch)
# --------------------------------------------------------

from datetime import datetime
from collections import OrderedDict

categories = ['Mensa', 'Groc.', 'Events', 'SBB', 'Flights', 'Mfg']

lines = []
info = []
month_info = OrderedDict()


def parse_info(file_name):
    f = open(file_name)
    ls = [line_.split('\t') for line_ in f.readlines()]
    f.close()
    return ls


lines += parse_info('swiss_master.inf')
lines += parse_info('cash.inf')

for i, line in enumerate(lines):
    info.append(OrderedDict())
    info[i]['order_date'] = datetime.strptime(line[0], '%d.%m.%Y')
    info[i]['execution_date'] = datetime.strptime(line[1], '%d.%m.%Y')
    info[i]['info_str'] = ' '.join(line[2:-1])
    info[i]['value'] = float(line[-1])


def get_month(d):
    return d.strftime('%b')


for i in xrange(1, 13):
    month_info[get_month(datetime.strptime(str(i), '%m'))] = {cat: 0 for cat in categories}

for dic in info:
    if any((word in dic['info_str']) for word in ['SV (Schweiz)', 'Scolarest', 'WOKA']):
        month_info[get_month(dic['order_date'])]['Mensa'] += dic['value']
    if any(word in dic['info_str'] for word in ['SBB']):
        month_info[get_month(dic['order_date'])]['SBB'] += dic['value']


def print_info():
    print '\norder data\texec date\tinfo\t\t' + 'value'.rjust(7)
    for dic_ in info:
        print '{0}\t{1}\t{2}\t{3:7.2f}'.format(dic_['order_date'].strftime('%Y-%m-%d'), dic_['execution_date'].strftime('%Y-%m-%d'), dic_['info_str'][:10].ljust(10), dic_['value'])


def print_month_info():
    print '\nMonth\t' + '\t'.join(cat.rjust(7) for cat in categories)
    for month, dic_ in month_info.iteritems():
        print '{0}\t{1:7.2f}\t{2:7.2f}\t{3:7.2f}\t{4:7.2f}'.format(month, *[dic_[cat] for cat in categories])
    print '*' * 40
    print 'Total\t{0:7.2f}\t{1:7.2f}\t{2:7.2f}\t{3:7.2f}'.format(*[sum(dic_[cat] for dic_ in month_info.itervalues()) for cat in categories])


def get_food():
    pass


print_info()
print_month_info()
