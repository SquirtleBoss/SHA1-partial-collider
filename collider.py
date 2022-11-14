import multiprocessing
import hashlib
from multiprocessing import Process, Value

# Given an integer, turn it into binary then return hex representation
def IntToBytes(inputInt):
    ret = ''
    inputInt += 1
    while(inputInt > 0):
        n = inputInt % 96
        ret = chr(n+31) + ret
        inputInt = inputInt // 96
    return ret.encode()

def FindCollision(procnum, proccount, prefix, v, interval):
    begin = 1350000000      #begin here
    i = procnum * interval
    i += begin
    while(1):
        string = IntToBytes(i)
        hash = hashlib.sha1(string).hexdigest()
        if hash[:len(prefix)] == prefix:
            v.value = i
            break
        i += 1
        # leapfrogs over batches belonging to other processes when current batch finished
        if i % interval == 0:
            print('batch ' + str(i - interval) + '-' + str(i) + ' checked')
            i += interval*(proccount-1) + 1
        # stop if another process has found a solution
        if v.value != 0:
            break

if __name__ == "__main__":
    manager = multiprocessing.Manager()
    numcpu = multiprocessing.cpu_count()
    # determines how much a process should work on at a time (batch)
    intrvl = 5000000
    # edit for chosen prefix to collide with *****
    prefix = 'e1aaf6de4fe0c4bbf5b8ca38ab89a741db53ec' 
    # prints number of CPUs available
    print (numcpu)
    v = manager.Value('i', 0)
    procs = []
    for i in range(numcpu):
        proc = Process(target=FindCollision, args=(i, numcpu, prefix, v, intrvl))
        procs.append(proc)
        proc.start()
    for proc in procs:
        proc.join()
    print(IntToBytes(v.value))