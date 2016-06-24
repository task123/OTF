from opentidalfarm import *
import os
parameters["adjoint"]["allow_zero_derivatives"] = True
# Create a rectangular domain.
domain = FileDomain("mesh/mesh.xml")

# Boundary conditions
bcs = BoundaryConditionSet()
bcs.add_bc("u", Constant((2, 0)), facet_id=1)
bcs.add_bc("eta", Constant(0), facet_id=2)
bcs.add_bc("u", facet_id=3, bctype="free_slip")
bcs.add_bc("u", facet_id=4, bctype="free_slip")

# Set the problem_params for the Shallow water problem
problem_params = SWProblem.default_parameters()
problem_params.bcs = bcs
problem_params.domain = domain

# Activate the relevant terms
problem_params.include_advection = True
problem_params.include_viscosity = True
problem_params.linear_divergence = False

# Physical settings
problem_params.friction = Constant(0.0025)
problem_params.viscosity = Constant(3.0)
problem_params.depth = Constant(50)
problem_params.g = Constant(9.81)

# Set time parameters
period = 12. * 60 * 60
problem_params.start_time = Constant(1. / 4 * period)
problem_params.dt = Constant(period / 50)
n_time_steps = 3
problem_params.finish_time = problem_params.start_time + \
                             (n_time_steps-1) * problem_params.dt

problem_params.functional_final_time_only = False

# Use Crank-Nicolson to get a second-order time-scheme
problem_params.theta = 0.5

# Create a turbine
turbine = BumpTurbine(diameter=20., friction=400.0,
					  controls=Controls(dynamic_friction=True))

# Adjust some global options
options["output_turbine_power"] = True

# Create Tidalfarm
n_turbines_x = 1
n_turbines_y = 1
basin_x = 640
basin_y = 320
site_x = 320
site_y = 160
if (n_turbines_x == 1):
    site_x = 40
if (n_turbines_y == 1):
    site_y = 40
turbine_pos = []
farm = RectangularFarm(domain,
					   site_x_start = basin_x/2 - site_x/2,
					   site_x_end = basin_x/2 + site_x/2,
					   site_y_start = basin_y/2 - site_y/2,
					   site_y_end = basin_y/2 + site_y/2,
					   turbine = turbine)

farm.add_regular_turbine_layout(num_x=n_turbines_x, num_y=n_turbines_y)

# Extend the friction array to hold all the time steps
friction = farm._parameters["friction"]
farm._parameters["friction"] = [friction]*(n_time_steps)

problem_params.tidal_farm = farm


# Create problem
problem = SWProblem(problem_params)
solver_params = CoupledSWSolver.default_parameters()
solver_params.dump_period = 1
solver_params.cache_forward_state = False
solver = CoupledSWSolver(problem, solver_params)

functional = PowerFunctional(problem)
control = TurbineFarmControl(farm)
rf_params = ReducedFunctionalParameters()
rf_params.scale = 10**-6
rf_params.automatic_scaling = False
rf = ReducedFunctional(functional, control, solver, rf_params)
j1= rf([0, 500, 500])
j2= rf([500, 500, 500])
print j1
print j2
exit()
# Now we can define the constraints for the controls and start the
# optimization.
lb, ub = farm.friction_constraints(n_time_steps=n_time_steps,
                                   lower_bounds=0., upper_bounds=500.)
f_opt = maximize(rf, bounds=[lb,ub],  method="L-BFGS-B", 
                 options={'maxiter': 20,'ftol': 1.0e-04})
f_opt = f_opt.reshape((n_time_steps, n_turbines_x, n_turbines_y))
print f_opt

# Store the optimized values so it can be plotted with 'plot_pitch_opt.py' 
#import numpy as np
import ipdb
ipdb.set_trace()
#np.save("pitch_opt.npy", f_opt)
