import psutil



def test1():
    pids = psutil.get_pid_list()
    pids.sort()
    for pid in pids:
        p = psutil.Process(pid)
        print("%4d %s %s"%(pid, p.name, " ".join(p.cmdline)))

test1()