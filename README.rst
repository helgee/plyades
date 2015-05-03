**Note:** This software is currently work in progress and far from feature completeness.

Plyades
=======

.. image:: https://travis-ci.org/helgee/plyades.png
    :target: https://travis-ci.org/helgee/plyades

Plyades is an MIT-licensed astrodynamics library written in Python.
It aims to provide a comprehensive toolset for fast development of performant
mission analysis applications.
The API provides powerful high-level objects for pythonic ease-of-use while the
low-level functional building blocks can also be used independently.

.. code-block:: python

    import plyades as pl

    state = pl.examples.iss

    p = pl.Orbit(state)
    p.propagate(revolutions=1)
    p.plot()


Documentation
-------------
Read the documentation at `http://plyades.readthedocs.org <http://plyades.readthedocs.org>`_.

Installation
------------
Clone the repository.

Dependencies
^^^^^^^^^^^^

* Numpy
* Scipy

Getting Started
---------------

State Representation
^^^^^^^^^^^^^^^^^^^^

Orbit Propagation
^^^^^^^^^^^^^^^^^

Visualization
^^^^^^^^^^^^^
