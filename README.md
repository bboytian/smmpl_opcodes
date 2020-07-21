# smmpl_opcodes

Operational code for scanning mini micropulse lidar

## Usage

### Running measurements

Choice between quickscanpattern measurement and skyscan (normal oprations) is adjusted in params.

```
python -m smmpl_opcodes
```

### Generate scan patterns

Timings of scan patterns can adjusted in the main script.

```
python -m smmpl_opcodes.scanpat_calc
```

### Visualisation of scan pattern

Timing of visualisation is the package's main script. Toggle for real time animation and fast forward animation

```
python -m smmpl_opcodes.scan_vis
```

### Data organisation

Move data from SigmaMPL folder to data folders specified in params.

```
python -m smmpl_opcodes.sop.file_man
```

### Getting current sun position

```
python -m smmpl_opcodes.scanpat_calc.sunforecaster
```