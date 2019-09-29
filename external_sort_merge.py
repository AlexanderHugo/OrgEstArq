import os
import sys
import struct
from queue import Queue

if len(sys.argv) != 2:
	print("USO {} [source_filename]".format(sys.argv[0]))
	quit()

source = sys.argv[1]

def match(a,b):
    r1 = registroCEP.unpack(a)
    r2 = registroCEP.unpack(b)
    return r1[cep] < r2[cep]

def sort_by_func(a):
    r = registroCEP.unpack(a)
    return r[cep]

registroCEP = struct.Struct("72s72s72s72s2s8s2s")
cep = 5
num_partitions = 8

f = open(source,"rb")
f.seek(0,2)
pos = f.tell()
f.seek(0)
qtd = int(pos/registroCEP.size)

buffer = qtd//num_partitions*registroCEP.size
mod = qtd%num_partitions

os.mkdir('tmp_dir')
q = Queue() 

for i in range(num_partitions):
    if i == 7:
        buffer = buffer + mod * registroCEP.size

    lines = f.read(buffer)

    r_in_buffer = buffer // registroCEP.size
    start, end = 0, registroCEP.size
    reg_values = list()
    for _ in range(r_in_buffer):
        reg_values.append(lines[start:end])
        start += registroCEP.size
        end += registroCEP.size

    reg_values.sort(key=sort_by_func)
    out = b''.join(reg_values)

    path = 'tmp_dir/cep{}.dat'.format(i)
    g = open(path, "wb")
    g.write(out)
    g.close()
    q.put(path)  # add na queue a partição
    print('particao {} criada'.format(path))

f.close()
n = num_partitions

while q.qsize() > 1:
    path1 = q.get()
    path2 = q.get()
    print('intercalando {} e {}'.format(path1,path2))
    f1 = open(path1,"rb")
    f2 = open(path2, "rb")

    pathout = 'tmp_dir/cep{}.dat'.format(n)
    n += 1
    h = open(pathout,"wb")

    l1 = f1.read(registroCEP.size)
    l2 = f2.read(registroCEP.size)

    while(l1 and l2):
        if(match(l1,l2)):
            h.write(l1)
            l1 = f1.read(registroCEP.size)
        else:
            h.write(l2)
            l2 = f2.read(registroCEP.size)

    while(l1):
        h.write(l1)
        l1 = f1.read(registroCEP.size)

    while(l2):
        h.write(l2)
        l2 = f2.read(registroCEP.size)

    f1.close()
    f2.close()
    h.close()

    os.remove(path1)
    os.remove(path2)

    q.put(pathout)
    print('Left: ',list(q.queue))

final_file = 'cep_ordenado.dat'

# move e renomeia o arquivo final
os.rename(pathout,final_file)
os.removedirs('tmp_dir')

print('Arquivo finalizado!')