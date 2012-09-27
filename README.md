Matplotlib Print
================

Add print buttons to the toolbar on Matplotlib figures.

How to use
==========

Simply `import print_toolbar` before you `import matplotlib`.
Now when you show a figure, it should have Page Setup and Print buttons added to its toolbar.

Bugs and limitations
====================

There was an [issue](https://github.com/matplotlib/matplotlib/issues/670) opened on Matplotlib for this, but they closed it as *wontfix* because printing is almost impossible to do properly in a cross-platform and cross-backend way.
I agree with that and therefore, I'm not even going to try.
This tool will work on whatever backends I feel the need to implement it on, on whatever platforms.
Currently, it works on the

- Wx
- WxAgg
- TkAgg

backends, on

- Windows.

This list will probably grow at some point.
I am happy to accept contributions for other backends and other platforms.