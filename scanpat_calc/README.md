scanpat_calc
============

A program to compute the scan pattern for the objects configured in
scanpat_calc.targetgenerator.plotshapes.__init__

Input parameters of the code are mainly in __scanpat_calc.__main__
Output of the code is specified in scanpat_calc.__main__

amongst the objects specified in plotshapes, there is a hierachy.
	- points are initialised by grid
	- hemisphere creates a circular mask at grid height
	- cone creates a cone slice mask at grid height
	- aimlines applies the mask
	- aimpath ravels the points using the info from the mask and
	logic from pathplanner
