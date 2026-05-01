import psutil, datetime

unix_boottime = psutil.boot_time()

boot_time = datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")

print(type(boot_time))