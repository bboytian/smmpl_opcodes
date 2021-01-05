# smmpl_opcodes

Operational code for scanning mini micropulse lidar

## Usage

### Running measurements

Before running scan protocol, set the scan protocol in `smmpl_opcodes.global_imports.params.smmpl_opcodes`.
At this stage there are 3 `MEASUREMENTPROTOCOL`s to select from:
1. `'skyscan'`; operational sky scanning protocol
2. `'caliskyscan'`; operation sky scanning protocol with weekly horizontal sweep calibration
3. `'quickscan'`; quickscan protocols, have to specify the QUICKSCANTYPE, types are listed below
    1. `'horisweep'`; horizontal azimuthal calibration
    2. `'suncone'`; protocol to characterise sensitivity to suncone

```
python -m smmpl_opcodes
```
All protocols run the following services
1. Live status monitoring and notification (via Telegram)
2. Regular data moving and sync to solaris server (if specified)
3. Measurement protocol

### Running independent services

To perform background data organisation and transfer to server

```
python -m smmpl_opcodes.sop.file_man
```

To perform real time status monitoring and daily notification

```
python -m smmpl_opcodes.scan_event
```

To save webswitch log file and clear it on a regular basis
```
python -m smmpl_opcodes.sop.webswitch_logger
```


### Post measurement clean up

Can also be used to perform data organisation and sync; i.e. move data from SigmaMPL folder to data folders specified in params, and sync to solaris server (if specified)

```
python -m smmpl_opcodes.sop
```

### Generate sky scan protocol scan patterns

Timings of scan patterns can adjusted in the main script.

```
python -m smmpl_opcodes.scanpat_calc
```

### Getting current sun position and lidar direction to sun

```
python -m smmpl_opcodes.scanpat_calc.sunforecaster
```