# smmpl_opcodes

Operational code for scanning mini micropulse lidar

## Usage

### Running measurements

Running of measurement protocol; scripts titled as `<protocol name>_main.py`

```
python -m smmpl_opcodes
```
All protocols run the following services
1. Live status monitoring and notification (via Telegram)
2. Regular data moving and sync to solaris server
3. Measurement protocol

Be sure to check these parameters which are crucial for running the right measurement:
1. MEASUREMENTPROTOCOL
2. QUICKSCANTYPE ;if MEASUREMENTPROTOCOL == 'quickscan'
3. DOUBLEINITBOO

### Running independent services

To perform background data organisation and transfer to server

```
python -m smmpl_opcodes.sop.file_man
```

To perform real time status monitoring and daily notification

```
python -m smmpl_opcodes.scan_event
```


### Post measurement clean up

Can also be used to perform data organisation and sync; i.e. move data from SigmaMPL folder to data folders specified in params, and sync to solaris server

```
python -m smmpl_opcodes.sop
```

### Generate scan patterns

Timings of scan patterns can adjusted in the main script.

```
python -m smmpl_opcodes.scanpat_calc
```

### Getting current sun position

```
python -m smmpl_opcodes.scanpat_calc.sunforecaster
```