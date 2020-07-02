import subprocess as sub

cmd_l = [
    '''{} -azzvi -e "'{}' -o 'StrictHostKeyChecking=no' -i '{}'"'''.format(
        dc_gfunc(WINDOWFILESDIR, RSYNCFILE),
        dc_gfunc(WINDOWFILESDIR, SSHFILE), IDRSADIR
    )
    + ''' C:/Users/mpluser/Desktop/2020002test.txt {}@{}:{}'''.format(
        SOLARISUSER, SOLARISIP, '/home/tianli/Desktop/'
    )
]
print(cmd_l[0])
cmd_subrun = sub.run(cmd_l, stdout=sub.PIPE, stderr=sub.STDOUT)
print(cmd_subrun.stdout.decode('utf-8'))
