from mpi4py import MPI
import numpy as np

# Initialize MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

N = None
data = None

if rank == 0:
    # Get number of elements
    N = int(input("Enter the number of elements (N): "))
    
    if N % size != 0:
        print(f"Error: {N} elements cannot be divided equally among {size} processes.")
        comm.Abort()
    
    # Generate array
    data = np.random.randint(1, 101, size=N, dtype='i')
    print("Generated array:", data)

# Broadcast N to all
N = comm.bcast(N, root=0)

# Determine chunk size
chunk_size = N // size
local_data = np.empty(chunk_size, dtype='i')

# Scatter data to all processes
comm.Scatter([data, MPI.INT], [local_data, MPI.INT], root=0)

# Local sum calculation
local_sum = np.sum(local_data)

# Each process prints its own local sum
# Collect local sums to print in order after all processes have computed
local_sums = comm.gather(local_sum, root=0)

# Reduce to get total sum at root
total_sum = comm.reduce(local_sum, op=MPI.SUM, root=0)

# Root prints full array and total sum
if rank == 0:
    for i in range(size):
        print(f"Process {i} local sum: {local_sums[i]}")
    print("\nTotal sum of the array:", total_sum)