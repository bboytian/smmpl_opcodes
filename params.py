# data
'''
directories seen by python C:/Program Files (x86)/...;  '/' or '\\' is allowed
directories seen by gitbash, i.e. os.system C:/Program\ Files\ \(x86\)/...
                                         or 'C:/Program Files (x86)/...'
directories seen by rsync in os.system /c/Program\ Files\ \(x86\)/...
'''

## on smmpl laptop
MPLSIGMADIR = 'C:/Program Files (x86)/SigmaMPL'
MPLSIGMADATADIR = MPLSIGMADIR + '/DATA'
MPLSIGMALOGDIR = MPLSIGMADIR + '/Log'
MPLCONFIGFILE = MPLSIGMADIR + '/mpl.ini'
MPLSIGMAPROG = 'SigmaMPL2015R2.3.exe'
MPLSIGMAPROGDIR = MPLSIGMADIR + '/' + MPLSIGMAPROG
MPLDESKDIR = 'C:/Users/mpluser/Desktop'

MPLDESKDIR = '/home/tianli/SOLAR_EMA_project/data' # for testing purposes

MPLDATADIR = MPLDESKDIR + '/smmpl_E2'
MPLOPCODESDIR = MPLDESKDIR + '/smmpl_opcodes'

## on solaris server
# SOLARISIP = '137.132.39.187'
SOLARISUSER = 'tianli'
SOLARISIP = '192.168.1.75'      # for testing purposes

SOLARISDATADIR = '/home/tianli/SOLAR_EMA_project/data'
SOLARISMPLDATADIR = SOLARISDATADIR + '/smmpl_E2'
SOLARISRAZONDATADIR = SOLARISDATADIR + '/razon_E2'

## data nomenclature; indices to change manually when fmts are adjusted
DATEFMT, TIMEFMT = '{:%Y%m%d}', '{:%Y%m%d%H%M}' # has to be compatible for pandas
DATELEN, TIMELEN = 8, 12
SCANPATSDATEIND, SCANPATEDATEIND, SCANPATDATEIND = -36, -23, -11
SCANPATFILE = TIMEFMT + '_' + TIMEFMT + 'scanpat.txt'
MPLDATEIND, MPLTIMEIND = -8, -4
MPLFILE = TIMEFMT + '.mpl'
MPLEOMTIMEIND = -8
MPLEOMFILE = TIMEFMT + 'eom.flag' # indicates end of measurement
MPLLOGDATEIND, MPLLOGTIMEIND = -14, -10
MPLLOGFILE = TIMEFMT + 'MPLLog.txt'
MPLLOGCURFILE = 'mplLog.txt'
PSLOGFILE = DATEFMT + '{}.log' # names are controlled in __main__
JSONFILE = DATEFMT + '.json'          # name of processed data file


# scripting; __main__
DAYSINADV = 1                  # [day] in adv to calculate scanpat in coldstart
FILEMANWAIT = 10               # [min]
WAITCHECK = 60                 # [s]


# computations

## scanpat_calc.__main__
CALCDURATION = 1                # [day] # also in __main__
UTC = 0                         # [hr] # '0' if run on computer with gmt time
FINEDELTATIME = 2               # [min]
SEGDELTA = 30                   # [min]

ELEVATION = 0                              # [m]
LATITUDE, LONGITUDE = 1.299119, 103.771232 # [deg]

ANGOFFSET = 141                 # [deg]
PRIMARYAXIS = 'elevation'       # 'azimuth' or 'elevation'

## scanpat_calc.pathplanner.calc_dirpointsara
RAVELSTR = 's'                  # only 's' for now
RAVELARGS = 0                   # 0 to 3

## scanpat_calc.sunforcaster.__init__
SFAPI = 'pysolar_API'           # 'pysolar_API' or 'pysolarfast_API' recommended

## scanpat_calc.targetgenerator.plotshapes.__init__
R = 15                  # lidar SNR range limit
L0 = 6                  # size of grid
LP = 5                  # size of pixel
THETAS = 0.05           # solid angle of sun cone
CLOSEPROXTHRES = LP/3   # for targ_aimlines
## scanpat_calc.targetgenerator.plotshapes.cone
PHINUMINTS = 4        # discretisation
RHONUMINTS = 1
LNUMSWATH = 10
ALPHASHAPE = 0.1      # alphashape parameter for cone swath optimising
SWATHPLOTANG = 85     # [deg], angle range where sun swath is well defined
## scanpat_calc.targetgenerator.plotshapes.cone
FILLERNUM = 1e4                 # [km] for resample_func, !> grid size

                                
# visualisation; params specific to plotting are left in the scripts

## scan_vis.__main__
REALTIMEBOO = True
REALTIMEFPS = 2

FAKETIMESTARTTIME = '2020-05-21 12:00:00'
FAKETIMEFPS = 1000
FAKETIMEEQUIVTIME = 20          # [s]
FAKETIMEINTERVAL = 0

VISDURATION = 2                 # [hr]

## scanpat_calc.pathplanner.calc_pathara
ANGLERES = 0.1                  # [deg] for visualisation
