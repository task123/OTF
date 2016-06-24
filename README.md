# OTF
Testing out optimizing the pitch of the blades in a tidal turbine array using OpenTidalFarm.

The example pitch-opt-dynamic-channel.py seem to be working. 

The changes in OpenTidalFarm made to get the dynamic optimization to  work does NOT pass all the tests in OpenTidalFarm: "    "True value of Condtional should only be one function: " + repr(true))
../../../build/lib/python2.7/site-packages/ffc/log.py:44: in ffc_assert
    condition or error(*message)
<string>:1: in <lambda>
    ???
_ _ _ _ _ _" 
"../../../build/lib/python2.7/site-packages/ufl/log.py:158: Exception"
1 failed, 28 passed in 1239.84 seconds

The result changing depending if the F in couple_sw_solve.py is updated
explisitly each time as it is now or if it leaft untouched. 

The result does often oscillate a bit. 

The optimization should be check to see if the results make physical sense.
It should be tested for different timesteps.
It should be tested for more turbines.
It should be tested with more realistical boundary conditions.
It should be compared to individual optimization and static optimization.
It should be tested with position optimiztion and compered with just position
optimization.
