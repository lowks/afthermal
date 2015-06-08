afthermal
=========

``afthermal`` is a driver/library for the https://www.adafruit.com/products/597
thermal printer [1]_.

Partially, it is inspired by previous efforts:

* https://github.com/adafruit/Adafruit-Thermal-Printer-Library
* https://github.com/adafruit/Python-Thermal-Printer/
* https://github.com/luopio/py-thermal-printer/

It does try to be a little more pythonic and efficient than previous efforts,
which have mostly been 1:1 ports from other languages.

.. [1] Specification is available at http://www.adafruit.com/datasheets/CSN-A2%20User%20Manual.pdf


Installation
------------

``afthermal`` is installable from ``pip``. It supports an extra feature named
``tools``, installing it will include numerous tools for calibrating the
printer or other tasks:

.. code-block:: sh

   $ pip install 'afthermal[tools]'
