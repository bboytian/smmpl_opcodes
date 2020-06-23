sop
===

A toolbox containing two main packages, file_man and sigmampl_boot.

file_man is used to manage the files within the smmpl laptop as well
as the file transfer from lidar laptop to server

sigmampl_boot takes care of the killing and starting of measurement of
the SigmaMPL program. It takes care of clearing up redundant log files
as well.

Deprecated
----------
- _old_wrappers
	- wrappers for scan_init are placed
		1. scan_init.sh is a bash wrapper for scan_init.py using the conda env
		2. scan_init.bat is a batch file wrapper for scan_init.sh

	- wrappers for sigma boot and kill