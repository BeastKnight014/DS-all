from mpi4py import MPI
import numpy as np
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
N = None
data = None
if rank == 0:
    N = int(input("Enter the number of elements (N): "))
    if N % size != 0:
        print(f"Error: {N} elements cannot be divided equally among {size} processes.")
        comm.Abort()
    data = np.random.randint(1, 101, size=N, dtype='i')
    print("Generated array:", data)
N = comm.bcast(N, root=0)
chunk_size = N // size
local_data = np.empty(chunk_size, dtype='i')
comm.Scatter([data, MPI.INT], [local_data, MPI.INT], root=0)
local_sum = np.sum(local_data)
local_sums = comm.gather(local_sum, root=0)
total_sum = comm.reduce(local_sum, op=MPI.SUM, root=0)
if rank == 0:
    for i in range(size):
        print(f"Process {i} local sum: {local_sums[i]}")
    print("\nTotal sum of the array:", total_sum)