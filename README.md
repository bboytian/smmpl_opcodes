# smmpl_opcodes

Operational code for scanning mini micropulse lidar

## Usage

### Running measurements

Choice between quickscanpattern measurement and skyscan (normal oprations) is adjusted in params.

```
python -m smmpl_opcodes
```
The skyscan measurement has the following services, each with their own logs,
on top of the main log
1. Live status monitoring and notification (via Telegram)
2. Regular data moving and sync to solaris server
3. Booting and init configuration of SigmaMPL program for measurement


### Generate scan patterns

Timings of scan patterns can adjusted in the main script.

```
python -m smmpl_opcodes.scanpat_calc
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