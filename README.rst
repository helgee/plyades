**DEPRECATED**

- For a spiritual successor in Python have a look at `poliastro <https://github.com/poliastro/poliastro>`_.
- If you are interested in Julia have a look at `Astrodynamics.jl <https://github.com/JuliaSpace/Astrodynamics.jl>`_.

Plyades
=======

.. image:: https://travis-ci.org/helgee/plyades.png
    :target: https://travis-ci.org/helgee/plyades

Plyades is an MIT-licensed astrodynamics library written in Python.
It aims to provide a comprehensive toolset for fast development of
high-performance mission analysis applications.
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
