from astropy.time import TimeDelta
import numpy as np
from scipy.integrate import ode
import warnings

class Propagator:
    def __init__(self, s0, dt, **kwargs):
        self.s0 = s0
        self.dt = dt
        self.forces = []
        self.solver = ode(self._rhs).set_integrator('dop853', nsteps=1, **kwargs)
        self.solver.set_initial_value(np.array(s0), 0.0)
        self.solver._integrator.iwork[2] = -1

    def _rhs(self, t, y):
        f = np.zeros_like(y)
        s = type(self.s0)(
            y[:3], y[3:], self.s0.t + TimeDelta(t, format='sec'),
            frame=self.s0.frame,
            body=self.s0.body,
            vars=y[6:],
        )
        for fn in self.forces:
            f += fn(s)
        return f

    def step(self):
        warnings.filterwarnings("ignore", category=UserWarning)
        self.solver.integrate(self.dt, step=True)
        warnings.resetwarnings()
        return self.solver.t, self.solver.y

    def __iter__(self):
        while not np.isclose(self.solver.t, self.dt):
            yield self.step()
