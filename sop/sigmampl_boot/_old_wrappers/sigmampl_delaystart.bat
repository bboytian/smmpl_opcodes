@ECHO OFF

ECHO waiting for other scripts to run
TIMEOUT /T 10 /NOBREAK

CD "C:\Program Files (x86)\SigmaMPL"

ECHO running main program
"C:\Program Files (x86)\SigmaMPL\SigmaMPL2015R2.3.exe" auto

