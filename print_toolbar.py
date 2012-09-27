"""
Importing this module adds "Print" and "Page Setup" buttons to the
Matplotlib toolbar (in Windows only).

Import it _before_ you import matplotlib!

Incorporates code from:
http://timgolden.me.uk/python/win32_how_do_i/print.html
http://dalelane.co.uk/blog/?p=778
"""

import matplotlib

backend = matplotlib.rcParams['backend']

if backend.lower() in ('wx', 'wxagg'):
    import print_toolbar_wx
elif backend.lower() == 'tkagg':
    import print_toolbar_tk
else:
    raise ImportError('Print toolbar unsupported for backend {}'.format(backend))

if __name__ == '__main__':
    from matplotlib import pyplot as P
    import numpy as N
    x = N.linspace(0, 10)
    y = x ** 2
    P.plot(x, y)
    P.show()
