**Note:** This software is currently a work in progress and far from feature completeness.

Plyades
=======

.. image:: https://travis-ci.org/helgee/plyades.png
    :target: https://travis-ci.org/helgee/plyades

Plyades is an astrodynamics library, written in Python and based on Numpy and Scipy.	

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
