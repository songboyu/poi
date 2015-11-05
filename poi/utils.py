# -*- coding: utf-8 -*-

import datetime
import doctest


def timestamp2datetime(stamp):
    """Convert JS time stamp to time string.

    >>> timestamp2datetime('1186311531917')
    '2007-08-05 18:58:51'
    """
    return datetime.datetime.fromtimestamp(int(stamp) / 1000.0).strftime('%Y-%m-%d %H:%M:%S')


if __name__ == '__main__':
    doctest.testmod()
