#!/usr/bin/env python
from opentidalfarm import *

# Create a rectangular domain.
domain = FileDomain("mesh/mesh.xml")

# Specify boundary conditions.
bcs = BoundaryConditionSet()
bcs.add_bc("u", Constant((2, 0)), facet_id=1)
bcs.add_bc("eta", Constant(0), facet_id=2)
bcs.add_bc("u", facet_id=3, bctype="free_slip")
bcs.add_bc("u", facet_id=4, bctype="free_slip")

# Set the shallow water parameters
prob_params = SteadySWProblem.default_parameters()
prob_params.domain = domain
prob_params.bcs = bcs
prob_params.viscosity = Constant(2)
prob_params.depth = Constant(50)
prob_params.friction = Constant(0.0025)

# The next step is to create the turbine farm. In this case, the
# farm consists of 32 turbines, initially deployed in a regular grid layout.
# This layout will be the starting guess for the optimization.

# Before adding turbines we must specify the type of turbines used in the array.
# Here we used the default BumpTurbine which defaults to being controlled by
# just position. The diameter and friction are set. The minimum distance between
# turbines if not specified is set to 1.5*diameter.
turbine = BumpTurbine(diameter=20.0, friction=100.0, 
                      controls=Controls(friction=True))

# A rectangular farm is defined using the domain and the site dimensions.
n_turbines_x = 6
n_turbines_y = 4
basin_x = 640
basin_y = 320
site_x = 320
site_y = 160
if (n_turbines_x == 1):
    site_x = 40
if (n_turbines_y == 1):
    site_y = 40
farm = RectangularFarm(domain, 
                       site_x_start=basin_x/2 - site_x/2, 
                       site_x_end=basin_x/2 + site_x/2,
                       site_y_start=basin_y/2 - site_y/2,
                       site_y_end=basin_y/2 + site_y/2,
                       turbine=turbine)

# Turbines are then added to the site in a regular grid layout.
farm.add_regular_turbine_layout(num_x=n_turbines_x, num_y=n_turbines_y)

prob_params.tidal_farm = farm

# Now we can create the shallow water problem

problem = SteadySWProblem(prob_params)

# Next we create a shallow water solver. Here we choose to solve the shallow
# water equations in its fully coupled form. We also set the dump period to 1 in
# order to save the results of each optimisation iteration to disk.

sol_params = CoupledSWSolver.default_parameters()
sol_params.dump_period = 1
solver = CoupledSWSolver(problem, sol_params)

# Next we create a reduced functional, that is the functional considered as a
# pure function of the control by implicitly solving the shallow water equations. For
# that we need to specify the objective functional (the value that we want to
# optimize), the control (the variables that we want to change), and our shallow
# water solver.import ipdb
functional = PowerFunctional(problem)
control = TurbineFarmControl(farm)
rf_params = ReducedFunctional.default_parameters()
rf_params.scale = 10**-6
rf_params.automatic_scaling = False
rf = ReducedFunctional(functional, control, solver, rf_params)

# Now we can define the constraints for the controls and start the
# optimisation.
lb, ub = farm.friction_constraints(lower_bounds=0, upper_bounds=1000)
f_opt = maximize(rf, bounds=[lb, ub], method="L-BFGS-B", options={'maxiter':
    10, 'ftol': 1.0e-04})
print f_opt

# Store the optimized values so it can be plotted with 'plot_pitch_opt.py' 
import numpy as np 
np.save("pitch_opt_steady_channel.npy", f_opt)
