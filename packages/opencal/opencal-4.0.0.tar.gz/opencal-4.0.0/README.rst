=======
OpenCAL
=======

Copyright (c) 2008-2024 Jérémie DECOCK <jd.jdhp@gmail.com> (www.jdhp.org)

* Web site: https://gitlab.com/opencal/opencal-lib-python
* Online documentation: https://opencal.gitlab.io/opencal-lib-python
* Source code: https://gitlab.com/opencal/opencal-lib-python
* Issue tracker: https://gitlab.com/opencal/opencal-lib-python/issues
* Pytest code coverage: https://opencal.gitlab.io/opencal-lib-python/htmlcov/index.html
* OpenCAL on PyPI: https://pypi.org/project/opencal


Table of Contents
=================

.. contents::
   :depth: 2


Description
===========

OpenCAL core library for Python

Note:

    This project is still in beta stage, so the API is not finalized yet.


Dependencies
============

OpenCAL requires Python 3.11 (or newer) and Python packages listed in the `requirements.txt` file.


.. _install:

Installation (development environment)
======================================

Posix (Linux, MacOSX, WSL, ...)
-------------------------------

From the OpenCAL source code::

    conda deactivate         # Only if you use Anaconda...
    python3 -m venv env
    source env/bin/activate
    python3 -m pip install --upgrade pip
    python3 -m pip install -r requirements-dev.txt


Windows
-------

From the OpenCAL source code::

    conda deactivate         # Only if you use Anaconda...
    python3 -m venv env
    env\Scripts\activate.bat
    python3 -m pip install --upgrade pip
    python3 -m pip install -r requirements-dev.txt


Installation (production environment)
=====================================

::

    pip install opencal


Documentation
=============

* Online documentation: https://opencal.gitlab.io/opencal-lib-python
* API documentation: https://opencal.gitlab.io/opencal-lib-python/api.html


Build and run the Python Docker image
=====================================

Build the docker image
----------------------

From the OpenCAL source code::

    docker build -t opencal:latest .

Run unit tests from the docker container
----------------------------------------

From the OpenCAL source code::

    docker run opencal pytest

Run an example from the docker container
----------------------------------------

From the OpenCAL source code::

    docker run opencal python3 /app/examples/hello.py


Bug reports
===========

To search for bugs or report them, please use the OpenCAL Bug Tracker at:

    https://gitlab.com/opencal/opencal-lib-python/issues


License
=======

This project is provided under the terms and conditions of the `MIT License`_.


.. _MIT License: http://opensource.org/licenses/MIT
.. _command prompt: https://en.wikipedia.org/wiki/Cmd.exe