from .globalimports import *
import subprocess as sub

# '''"'{}' -o 'StrictHostKeyChecking=no' -i '{}'"'''.format(
#     dc_gfunc(WINDOWFILESDIR, SSHFILE), IDRSADIR
# ),

_gitbash_mpldatadir = MPLDATADIR.replace('C:', '/cygdrive/c') # required for rsync
today = dt.datetime.now()
syncday_lst = [
    DATEFMT.format(today),
    DATEFMT.format(today - dt.timedelta(1))
]

cmd_l = [
    f'{dc_gfunc(WINDOWFILESDIR, RSYNCFILE)}',
    '-azzvi',
    '-e',
    f"'{dc_gfunc(WINDOWFILESDIR, SSHFILE)}'",
    '-o',
    'StrictHostKeyChecking=no',
    '-i',
    f"'{IDRSADIR}",
    '-R',
    '{}/./{{{}}}'.format(_gitbash_mpldatadir, ','.join(syncday_lst)),
    '{}@{}:{}'.format(SOLARISUSER, SOLARISIP, SOLARISMPLDATADIR)
]

for cmd in cmd_l:
    print(cmd)

cmd_subrun = sub.run(cmd_l, stdout=sub.PIPE, stderr=sub.STDOUT)
print(cmd_subrun.stdout.decode('utf-8'))
