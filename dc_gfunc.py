lst1 =[
    "functions.py",
    "functions.py",
    "functions.py",
    "functions.py",
    "scan_event/scanpat_reader.py",
    "scan_event/mpllog_retroreader.py",
    "scanpat_calc/__main__.py",
    "scanpat_calc/__main__.py",
    "skyscan_main.py",
    "skyscan_main.py",
    "skyscan_main.py",
    "skyscan_main.py",
    "sop/sigmampl_boot/sigmampl_startkill.py",
    "sop/sigmampl_boot/scan_init.py",
    "sop/sigmampl_boot/scan_init.py",
    "sop/sigmampl_boot/scan_init.py",
    "sop/sigmampl_boot/prepostmea_fileman.py",
    "sop/sigmampl_boot/prepostmea_fileman.py",
    "sop/file_man/mpl_organiser.py",
    "sop/file_man/mpl_organiser.py",
    "sop/file_man/mpl_organiser.py",
    "sop/file_man/mpl_organiser.py",
    "sop/file_man/mpl_organiser.py",
    "sop/file_man/mpl_organiser.py"
]

lst2 = [
    "scan_event/scanpat_reader.py",
    "scan_event/mpllog_retroreader.py",
    "scanpat_calc/__main__.py",
    "scanpat_calc/__main__.py",
    "skyscan_main.py",
    "skyscan_main.py",
    "skyscan_main.py",
    "skyscan_main.py",
    "skyscan_main.py",
    "skyscan_main.py",
    "skyscan_main.py",
    "skyscan_main.py",
    "sop/file_man/mpl_organiser.py",
    "sop/file_man/mpl_organiser.py",
    "sop/file_man/mpl_organiser.py",
    "sop/file_man/mpl_organiser.py",
    "sop/file_man/mpl_organiser.py",
    "sop/file_man/mpl_organiser.py"  
]


if __name__ == '__main__':
    lst = []
    for l in lst1:
        if l not in lst2:
            lst.append(l)
    lst = list(set(lst))
    print(lst)
