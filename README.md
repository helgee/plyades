**Note:** This software is currently a work in progress and most features mentioned below are not implemented, yet. 

Plyades
=======
[![Build Status](https://travis-ci.org/helgee/plyades.png)](https://travis-ci.org/helgee/plyades)

Plyades is an astrodynamics library, written in Python and based on Numpy and Scipy.	

```python
import plyades as pl

tle = '''ISS (ZARYA)             
1 25544U 98067A   13008.88529319  .00008403  00000-0  14424-3 0  9866
2 25544  51.6459 179.6935 0016178 136.4951 358.8863 15.51957773809967'''

initial_state = pl.state.from_tle(tle)

p = pl.Propagator(initial_state)
p.propagate(days=5)
p.plot()

elements = p.results[-1].elements
```

# Documentation

# Installation
Clone the repository.

# Dependencies

* Numpy
* Scipy

# Getting Started
## State Representation
Plyades' basic data type is the state


## Orbit Propagation


## Orbit Determination


## Visualization
