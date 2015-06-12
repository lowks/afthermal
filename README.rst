afthermal
=========

``afthermal`` is a driver/library for the popular `Adafruit
<https://www.adafruit.com/products/597>`_ (originally Cashino
A2) thermal printer [1]_.

Partially, it is inspired by previous efforts:

* https://github.com/adafruit/Adafruit-Thermal-Printer-Library
* https://github.com/adafruit/Python-Thermal-Printer/
* https://github.com/luopio/py-thermal-printer/

It does try to be a little more pythonic and efficient than previous efforts,
which have mostly been 1:1 ports from other languages. Specifically, it boasts
additional features such as:

* Adapters to print images from PIL_ / Pillow_ as well as OpenCV_
* A fast Floyd-Steinberg_ implementation to dither OpenCV_ images.
* Command-line utilities for calibrating the printer for optimum speed and
  quality, as well as other capabilities
* Comfortable handling of text formatting
* Support for printing QR codes via PyQRCode_ without having to render them
  into images first

.. [1] Specification is available at http://www.adafruit.com/datasheets/CSN-A2%20User%20Manual.pdf

.. _PyQRCode: https://pypi.python.org/pypi/PyQRCode
.. _OpenCV: https://opencv-python-tutroals.readthedocs.org
.. _Pillow: http://pillow.readthedocs.org
.. _PIL: http://www.pythonware.com/products/pil/
.. _Floyd-Steinberg: https://en.wikipedia.org/wiki/Floyd%E2%80%93Steinberg_dithering


Installation
------------

``afthermal`` is installable from ``pip``. It supports an extra feature named
``tools``, installing it will include numerous tools for calibrating the
printer or other tasks:

.. code-block:: sh

   $ pip install 'afthermal[tools]'

It includes a C extension for Floyd-Steinberg_ dithering, since OpenCV_ does
not ship with a dithering function.


Full docs
---------

The complete documentation is housed at http://pythonhosted.org/afthermal.
