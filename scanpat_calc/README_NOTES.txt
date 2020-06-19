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

To do
-----

- customization of aimpoints
  - point calculator using information from sun; takes in position of
  from input time params and have other params such as inter point
  angular distance (should be able to jump from here to measurement if
  needed)
  - hemgrid object which projects defined grid points onto a 2D grid
  system reminscent of og grid for ravelling, the height of the grid
  is to be 0 to be able to create hemisphere mask. grid.coordmag_mat
  has to be tweaked to not include the z direction
  - new math is requried for hem cone object
  - think about whether to incoporate these features into the current
  package or to copy and create a new package

- if needed, incorporate time averaging and bin size in file nomenclature

- remove redundancies in generation


Version updates
---------------

v0.0.0
	- working code for regular measurements; multiple grid system
          with grid heirachy
	- only 's' method of ravelling points available in path planner
