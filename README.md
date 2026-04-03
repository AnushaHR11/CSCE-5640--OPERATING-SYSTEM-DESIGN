# CSCE-5640 : OPERATING-SYSTEM-DESIGN
<H2> 1. Process Creation and Termination <br> </H2>
    Assignment 1: Process Creation and Termination <br>
    Files: process_sync.c <br>

   What the program does: <br>
   i. Creates a pipe to synchronize output order. <br>
   ii. Calls fork() to create a child process. <br>
   iii. Parent process: <br>
      - Prints the parent PID <br>
      - Signals the child through the pipe <br>
      - Waits for the child to finish using waitpid() <br>
      - Prints "Child process has completed." <br>
    iv. Child process: <br>
        - Waits until parent signals through the pipe <br>
        - Prints the child PID <br>
        - Executes "ls -l" using execlp() <br>
    v. Errors are handled with perror() and proper exit codes. <br>

How to compile: <br>
gcc -Wall -Wextra -O2 -o process_sync.c

How to run: <br>
./process_sync

Expected output (example): <br>
Parent Process ID: 5797 <br>
Child Process ID: 5798 <br>
total 28 <br>
-rw-rw-rw- 1 codespace root         64 Jan 27 03:22 README.md <br>
-rwxrwxrwx 1 codespace codespace 16664 Jan 27 03:25 process_sync <br>
-rw-rw-rw- 1 codespace codespace  2371 Jan 27 03:24 process_sync.c <br>
Child process has completed.

<h2>2. Implementing the Producer-Consumer Problem with Semaphores <br></h2>
    Assignment 2: Producer-Consumer using Semaphores <br>
    How it works: <br>
   - We use a fixed-size shared buffer (circular queue). <br>
   - Semaphores: <br>
      1) empty: counts available empty slots in the buffer <br>
      2) full : counts filled slots in the buffer <br>
      3) mutex: ensures mutual exclusion while accessing the buffer (critical section) <br>

Flow: <br>
Producer: <br>
  - choose next item number (protected by count_mutex)
  - wait(empty)
  - wait(mutex)
  - insert item into buffer
  - post(mutex)
  - post(full)

Consumer: <br>
  - wait(full)
  - wait(mutex)
  - remove item from buffer
  - post(mutex)
  - post(empty)
  - update consumed_count (protected by count_mutex)

Parameter passing method: <br>
- Each thread receives a pointer to a ThreadArg struct:<br>
    typedef struct { int id; Shared *shared; } ThreadArg; <br>
- This avoids global per-thread variables and safely passes: <br>
  - the thread’s id <br>
  - the pointer to the shared data structure (buffer + semaphores) <br>

Compile: <br>
  gcc -o producer_consumer producer_consumer.c -pthread
  
How to run: <br>
./producer_consumer

Expected output: <br>
Producer 1 produced item 1 <br>
Consumer 1 consumed item 1 <br>
Producer 1 produced item 2 <br>
Consumer 1 consumed item 2 <br>
Producer 1 produced item 3 <br>
Consumer 1 consumed item 3 <br>
Producer 1 produced item 4 <br>
Producer 1 produced item 5 <br>
Consumer 1 consumed item 4 <br>
Producer 1 produced item 6 <br>
Consumer 1 consumed item 5 <br>
Producer 1 produced item 7 <br>
Producer 1 produced item 8 <br>
Consumer 1 consumed item 6 <br>
Producer 1 produced item 9 <br>
Consumer 1 consumed item 7 <br>
Producer 1 produced item 10 <br>
Consumer 1 consumed item 8 <br>
Consumer 1 consumed item 9 <br>
Consumer 1 consumed item 10 <br>
Done. Produced=10, Consumed=10 <br>

<H2> 3.Implementing Round Robin Scheduling<br> </H2>
Banker’s Algorithm Implementation <br>
Files: bankers_algorithm.py <br>

What the program does: <br>
i. Accepts the number of processes and resource types from the user. <br>
ii. Takes Allocation, Max, and Available matrices as input. <br>
iii. Computes the Need matrix using (Need = Max − Allocation). <br>
iv. Performs the Safety Algorithm: <br>
    - Checks if the system is in a safe state. <br>
    - Displays the safe sequence of processes if safe. <br>
v. Allows the user to make a resource request: <br>
    - Verifies Request ≤ Need. <br>
    - Verifies Request ≤ Available. <br>
    - Temporarily allocates resources and rechecks safety. <br>
    - Grants or denies the request accordingly. <br>
vi. Input validation and error handling are included. <br>

How to run: <br>
python bankers_algorithm.py <br>

Expected output (example): <br>
Enter the number of processes: 3 <br>
Enter the number of resource types: 2 <br>
Enter the Allocation matrix (3 rows, each with 2 integers): <br>
1 0 <br>
2 1 <br>
0 3 <br>
Enter the Max matrix (3 rows, each with 2 integers): <br>
3 2 <br>
3 3 <br>
2 3 <br>
Enter the Available resources: 2 1 <br>
System is in a SAFE state. <br>
Safe sequence: P2 -> P0 -> P1 <br>


<H2> 4. Implementing Multilevel Feedback Queue (MLFQ) Scheduling <br></H2>
    To understand adaptive CPU scheduling by simulating a Multilevel Feedback Queue (MLFQ) with three levels. <br>
    Files: deadlock_wfg.cpp <br>

What the program does: <br>
i. Accepts number of processes and edges as input. <br>
ii. Constructs a wait-for graph where an edge (u → v) means process u is waiting for process v. <br>
iii. Uses Depth First Search (DFS) to traverse the graph. <br>
iv. Detects a cycle by identifying a back edge during DFS. <br>
v. If a cycle is found, reports that a deadlock exists and prints the processes involved. <br>
vi. If no cycle is found, reports that no deadlock exists. <br>

How to compile: <br>
g++ -std=c++17 -Wall -Wextra -O2 deadlock_wfg.cpp -o deadlock_wfg <br>

How to run (interactive mode): <br>
./deadlock_wfg <br>

Expected output: <br>
Enter number of processes: 4 <br>
Enter number of edges: 4 <br>
Deadlock: YES <br>
Processes in cycle: P1 -> P2 -> P3 -> P1 <br>

Expected output (example – no deadlock case): <br>
Enter number of processes: 3 <br>
Enter number of edges: 2 <br>
Deadlock: NO <br>
No cycle found in the wait-for graph. <br>



<H2> 5. Simulate Page Replacement Algorithms <br></H2>
    Objective: To evaluate FIFO, LRU, and Optimal page replacement algorithms. <br>
    Files: page_replacement.py <br>

Algorithms: <br>
FIFO (First-In First-Out):<br>
Replaces the page that has been in memory the longest. It is simple and fast but does not consider how frequently or recently a page is used.<br>

LRU (Least Recently Used):<br>
Replaces the page that has not been used for the longest time in the past. This typically performs better than FIFO because it uses recent history as a predictor of near-future use, but it needs tracking of “last used time” (overhead).<br>

Optimal:<br>
Replaces the page whose next use is farthest in the future (or never used again). This gives the minimum possible faults for a given reference string and frames, but it is not implementable in real OSs because it requires knowing future references. It is used as a benchmark.<br>

What the program does: <br>
i. Accepts number of frames and a reference string as input. <br>
ii. Simulates FIFO (First-In First-Out) page replacement algorithm. <br>
iii. Simulates LRU (Least Recently Used) page replacement algorithm. <br>
iv. Simulates Optimal page replacement algorithm. <br>
v. Displays frame contents at each step for all algorithms. <br>
vi. Counts and displays the total number of page faults for each algorithm. <br>
vii. Compares the performance of FIFO, LRU, and Optimal algorithms. <br>

How to compile (C++ version, if applicable): <br>
g++ -std=c++17 -Wall -Wextra -O2 page_replacement.cpp -o page_replacement <br>

How to run (interactive mode – C++ version): <br>
./page_replacement <br>

Expected output: <br>
Test1:<br>
$ python3 page_replacement.py --frames 3 --ref "7 0 1 2 0 3 0 4 2 3 0 3 2" <br>
Reference string: ['7', '0', '1', '2', '0', '3', '0', '4', '2', '3', '0', '3', '2'] <br>
Frames: 3 <br>

=== FIFO === <br>
Step  Page  Fault  Frames <br>
   1     7      Y  [7, -, -] <br>
   2     0      Y  [7, 0, -] <br>
   3     1      Y  [7, 0, 1] <br>
   4     2      Y  [2, 0, 1] <br>
   5     0      N  [2, 0, 1] <br>
   6     3      Y  [2, 3, 1] <br>
   7     0      Y  [2, 3, 0] <br>
   8     4      Y  [4, 3, 0] <br>
   9     2      Y  [4, 2, 0] <br>
  10     3      Y  [4, 2, 3] <br>
  11     0      Y  [0, 2, 3] <br>
  12     3      N  [0, 2, 3] <br>
  13     2      N  [0, 2, 3] <br>
FIFO Page Faults: 10 <br>

=== LRU === <br>
Step  Page  Fault  Frames <br>
   1     7      Y  [7, -, -] <br>
   2     0      Y  [7, 0, -] <br>
   3     1      Y  [7, 0, 1] <br>
   4     2      Y  [2, 0, 1] <br>
   5     0      N  [2, 0, 1] <br>
   6     3      Y  [2, 0, 3] <br>
   7     0      N  [2, 0, 3] <br>
   8     4      Y  [4, 0, 3] <br>
   9     2      Y  [4, 0, 2] <br>
  10     3      Y  [4, 3, 2] <br>
  11     0      Y  [0, 3, 2] <br>
  12     3      N  [0, 3, 2] <br>
  13     2      N  [0, 3, 2] <br>
LRU Page Faults: 9 <br>

=== Optimal === <br>
Step  Page  Fault  Frames <br>
   1     7      Y  [7, -, -] <br>
   2     0      Y  [7, 0, -] <br>
   3     1      Y  [7, 0, 1] <br>
   4     2      Y  [2, 0, 1] <br>
   5     0      N  [2, 0, 1] <br>
   6     3      Y  [2, 0, 3] <br>
   7     0      N  [2, 0, 3] <br>
   8     4      Y  [2, 4, 3] <br>
   9     2      N  [2, 4, 3] <br>
  10     3      N  [2, 4, 3] <br>
  11     0      Y  [2, 0, 3] <br>
  12     3      N  [2, 0, 3] <br>
  13     2      N  [2, 0, 3] <br>
Optimal Page Faults: 7 <br>

Summary (faults): <br>
  FIFO   : 10 <br>
  LRU    : 9 <br>
  Optimal: 7 <br>

Test 2: <br>
$ python3 page_replacement.py --frames 3 --ref "1 2 3 4 1 2 5 1 2 3 4 5" <br>
Reference string: ['1', '2', '3', '4', '1', '2', '5', '1', '2', '3', '4', '5'] <br>
Frames: 3 <br>

=== FIFO === <br>
Step  Page  Fault  Frames <br>
   1     1      Y  [1, -, -] <br>
   2     2      Y  [1, 2, -] <br>
   3     3      Y  [1, 2, 3] <br>
   4     4      Y  [4, 2, 3] <br>
   5     1      Y  [4, 1, 3] <br>
   6     2      Y  [4, 1, 2] <br>
   7     5      Y  [5, 1, 2] <br>
   8     1      N  [5, 1, 2] <br>
   9     2      N  [5, 1, 2] <br>
  10     3      Y  [5, 3, 2] <br>
  11     4      Y  [5, 3, 4] <br>
  12     5      N  [5, 3, 4] <br>
FIFO Page Faults: 9 <br>

=== LRU === <br>
Step  Page  Fault  Frames <br>
   1     1      Y  [1, -, -] <br>
   2     2      Y  [1, 2, -] <br>
   3     3      Y  [1, 2, 3] <br>
   4     4      Y  [4, 2, 3] <br>
   5     1      Y  [4, 1, 3] <br>
   6     2      Y  [4, 1, 2] <br>
   7     5      Y  [5, 1, 2] <br>
   8     1      N  [5, 1, 2] <br>
   9     2      N  [5, 1, 2] <br>
  10     3      Y  [3, 1, 2] <br>
  11     4      Y  [3, 4, 2] <br>
  12     5      Y  [3, 4, 5] <br>
LRU Page Faults: 10 <br>

=== Optimal === <br>
Step  Page  Fault  Frames <br>
   1     1      Y  [1, -, -] <br>
   2     2      Y  [1, 2, -] <br>
   3     3      Y  [1, 2, 3] <br>
   4     4      Y  [1, 2, 4] <br>
   5     1      N  [1, 2, 4] <br>
   6     2      N  [1, 2, 4] <br>
   7     5      Y  [1, 2, 5] <br>
   8     1      N  [1, 2, 5]<br>
   9     2      N  [1, 2, 5] <br>
  10     3      Y  [3, 2, 5] <br>
  11     4      Y  [4, 2, 5] <br>
  12     5      N  [4, 2, 5] <br>
Optimal Page Faults: 7 <br>

Summary (faults): <br>
  FIFO   : 9 <br>
  LRU    : 10 <br>
  Optimal: 7<br>

  Test 3: <br>
$ python3 page_replacement.py <br>
Reference string: ['2', '3', '2', '1', '5', '2', '4', '5', '3', '2', '5', '2'] <br>
Frames: 4 <br>

=== FIFO === <br>
Step  Page  Fault  Frames <br>
   1     2      Y  [2, -, -, -]<br>
   2     3      Y  [2, 3, -, -]<br>
   3     2      N  [2, 3, -, -]<br>
   4     1      Y  [2, 3, 1, -]<br>
   5     5      Y  [2, 3, 1, 5]<br>
   6     2      N  [2, 3, 1, 5]<br>
   7     4      Y  [4, 3, 1, 5]<br>
   8     5      N  [4, 3, 1, 5]<br>
   9     3      N  [4, 3, 1, 5]<br>
  10     2      Y  [4, 2, 1, 5]<br>
  11     5      N  [4, 2, 1, 5]<br>
  12     2      N  [4, 2, 1, 5]<br>
FIFO Page Faults: 6<br>

=== LRU ===<br>
Step  Page  Fault  Frames<br>
   1     2      Y  [2, -, -, -]<br>
   2     3      Y  [2, 3, -, -]<br>
   3     2      N  [2, 3, -, -]<br>
   4     1      Y  [2, 3, 1, -]<br>
   5     5      Y  [2, 3, 1, 5]<br>
   6     2      N  [2, 3, 1, 5]<br>
   7     4      Y  [2, 4, 1, 5]<br>
   8     5      N  [2, 4, 1, 5]<br>
   9     3      Y  [2, 4, 3, 5]<br>
  10     2      N  [2, 4, 3, 5]<br>
  11     5      N  [2, 4, 3, 5]<br>
  12     2      N  [2, 4, 3, 5]<br>
LRU Page Faults: 6<br>

=== Optimal ===<br>
Step  Page  Fault  Frames<br>
   1     2      Y  [2, -, -, -]<br>
   2     3      Y  [2, 3, -, -]<br>
   3     2      N  [2, 3, -, -]<br>
   4     1      Y  [2, 3, 1, -]<br>
   5     5      Y  [2, 3, 1, 5]<br>
   6     2      N  [2, 3, 1, 5] <br>
   7     4      Y  [2, 3, 4, 5]<br>
   8     5      N  [2, 3, 4, 5]<br>
   9     3      N  [2, 3, 4, 5]<br>
  10     2      N  [2, 3, 4, 5]<br>
  11     5      N  [2, 3, 4, 5]<br>
  12     2      N  [2, 3, 4, 5]<br>
Optimal Page Faults: 5<br>
Summary (faults):<br>
  FIFO   : 6<br>
  LRU    : 6<br>
  Optimal: 5<br>



<H2> 6. Thrashing Detector <br></H2>
    Objective: To simulate thrashing and calculate the working set of a process. <br>
    Files: thrashing_detector.py<br>

What the program does: <br>
i. Accepts logical address space size, page size, and logical addresses as input. <br>
ii. Converts logical addresses into page numbers to generate the reference string. <br>
iii. Accepts number of frames and working set window size (Δ). <br>
iv. Calculates the Working Set WS(t, Δ) at each time step. <br>
v. Simulates page replacement using the LRU algorithm. <br>
vi. Counts total page faults and calculates page fault rate. <br>
vii. Identifies thrashing when the working set size exceeds available frames. <br>
viii. Reports whether thrashing occurs and displays detailed step analysis. <br>

How to compile (if C++ version): <br>
g++ -std=c++17 -Wall -Wextra -O2 thrashing_detector.cpp -o thrashing_detector <br>

How to run (Python version): <br>
$ python3 thrashing_detector.py --frames 3 --window 4 --ref "1 2 3 4 1 2 5 1 2 3 4 5" --show_steps <br>

=== Thrashing Detector Report === <br>
References (pages): [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5] <br>
Frames: 3 <br>
Working set window Δ: 4 <br>
Total references: 12 <br>
LRU page faults: 10 (fault rate = 0.833) <br>
WS violations (|WS|>frames): 7 (0.583 of steps) <br>
Thrashing: YES <br>

--- Step Details (frames=3, window=4) --- <br>
Step  Page  WS_size  WS>F  Fault(LRU) <br>
   1     1        1     N          Y <br>
   2     2        2     N          Y <br>
   3     3        3     N          Y <br>
   4     4        4     Y          Y <br>
   5     1        4     Y          Y <br>
   6     2        4     Y          Y <br>
   7     5        4     Y          Y <br>
   8     1        3     N          N <br>
   9     2        3     N          N <br>
  10     3        4     Y          Y <br>
  11     4        4     Y          Y <br>
  12     5        4     Y          Y <br>

How to run (using logical addresses): <br>
$ python3 thrashing_detector.py --frames 3 --window 4 --las 8192 --page_size 1024 --addrs "0 20 1050 2048 2050 4096 5000" --show_steps <br>

=== Thrashing Detector Report === <br>
References (pages): [0, 0, 1, 2, 2, 4, 4] <br>
Frames: 3 <br>
Working set window Δ: 4 <br>
Total references: 7 <br>
LRU page faults: 4 (fault rate = 0.571) <br>
WS violations (|WS|>frames): 0 (0.000 of steps) <br>
Thrashing: NO <br>

--- Step Details (frames=3, window=4) --- <br>
Step  Page  WS_size  WS>F  Fault(LRU) <br>
   1     0        1     N          Y <br>
   2     0        1     N          N <br>
   3     1        2     N          Y <br>
   4     2        3     N          Y <br>
   5     2        3     N          N <br>
   6     4        3     N          Y <br>
   7     4        2     N          N <br>

Expected output: <br>
Test1:<br>
$ python3 thrashing_detector.py --frames 3 --window 3 --ref "1 2 3 4 1 2 5 1 2 3 4 5" <br>
python3 thrashing_detector.py --frames 3 --window 4 --ref "1 2 3 4 1 2 5 1 2 3 4 5" <br>
python3 thrashing_detector.py --frames 3 --window 6 --ref "1 2 3 4 1 2 5 1 2 3 4 5" <br>

=== Thrashing Detector Report === <br>
References (pages): [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5] <br>
Frames: 3 <br>
Working set window Δ: 3 <br>
Total references: 12 <br>
LRU page faults: 10 (fault rate = 0.833) <br>
WS violations (|WS|>frames): 0 (0.000 of steps) <br>
Thrashing: NO <br>

=== Thrashing Detector Report === <br>
References (pages): [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5] <br>
Frames: 3 <br>
Working set window Δ: 4 <br>
Total references: 12 <br>
LRU page faults: 10 (fault rate = 0.833) <br>
WS violations (|WS|>frames): 7 (0.583 of steps) <br>
Thrashing: YES <br>

=== Thrashing Detector Report === <br>
References (pages): [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5] <br>
Frames: 3 <br>
Working set window Δ: 6 <br>
Total references: 12 <br>
LRU page faults: 10 (fault rate = 0.833) <br>
WS violations (|WS|>frames): 9 (0.750 of steps) <br>
Thrashing: YES <br>

Test2:<br>
$ python3 thrashing_detector.py --frames 3 --window 3 --ref "7 0 1 2 0 3 0 4 2 3 0 3 2" <br>
python3 thrashing_detector.py --frames 3 --window 4 --ref "7 0 1 2 0 3 0 4 2 3 0 3 2" <br>
python3 thrashing_detector.py --frames 3 --window 6 --ref "7 0 1 2 0 3 0 4 2 3 0 3 2" <br>

=== Thrashing Detector Report === <br>
References (pages): [7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2] <br>
Frames: 3 <br>
Working set window Δ: 3 <br>
Total references: 13 <br>
LRU page faults: 9 (fault rate = 0.692) <br>
WS violations (|WS|>frames): 0 (0.000 of steps) <br>
Thrashing: NO <br>

=== Thrashing Detector Report === <br>
References (pages): [7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2] <br>
Frames: 3<br>
Working set window Δ: 4<br>
Total references: 13<br>
LRU page faults: 9 (fault rate = 0.692) <br>
WS violations (|WS|>frames): 5 (0.385 of steps) <br>
Thrashing: YES <br>

=== Thrashing Detector Report === <br>
References (pages): [7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2] <br>
Frames: 3 <br>
Working set window Δ: 6 <br>
Total references: 13 <br>
LRU page faults: 9 (fault rate = 0.692) <br>
WS violations (|WS|>frames): 10 (0.769 of steps) <br>
Thrashing: YES <br>



  <H2> 7. Simulate Dynamic Storage Allocation <br></H2>
Objective: To simulate and compare First-Fit, Best-Fit, and Worst-Fit memory allocation strategies for dynamic memory management. <br>
Files: dynamic_storage_allocation.py <br>

Algorithms: <br>
First-Fit:<br>
Allocates each process to the first memory block that is large enough to hold it. It is simple and fast because it scans memory from the beginning and stops at the first suitable block.<br>

Best-Fit:<br>
Allocates each process to the smallest available memory block that is large enough. It tries to reduce wasted space, but it may take more time because all blocks must be checked to find the best one.<br>

Worst-Fit:<br>
Allocates each process to the largest available memory block. The idea is to leave larger remaining spaces after allocation, but this may waste big blocks quickly.<br>

What the program does: <br>
i. Accepts the number of memory blocks and their sizes as input. <br>
ii. Accepts the number of processes and their sizes as input. <br>
iii. Simulates First-Fit memory allocation strategy. <br>
iv. Simulates Best-Fit memory allocation strategy. <br>
v. Simulates Worst-Fit memory allocation strategy. <br>
vi. Displays the allocation of each process to a memory block for all strategies. <br>
vii. Displays the leftover memory in each block after allocation. <br>
viii. Counts and displays the total internal fragmentation for each strategy. <br>
ix. Compares the performance of First-Fit, Best-Fit, and Worst-Fit. <br>

How to run (Python version): <br>
python3 dynamic_storage_allocation.py <br>

Expected output: <br>
Sample Test:<br>
$ python3 dynamic_storage_allocation.py <br>
Enter number of memory blocks: 5 <br>
Enter block sizes: 100 500 200 300 600 <br>
Enter number of processes: 4 <br>
Enter process sizes: 212 417 112 426 <br>

First Fit:<br>
Process   Size      Block Allocated   Leftover in Block<br>
1         212       2                 176<br>
2         417       5                 183<br>
3         112       2                 176<br>
4         426       Not Allocated     -<br>
Remaining memory in all blocks:<br>
Block 1: 100<br>
Block 2: 176<br>
Block 3: 200<br>
Block 4: 300<br>
Block 5: 183<br>
Internal Fragmentation (First Fit): 959<br>

Best Fit:<br>
Process   Size      Block Allocated   Leftover in Block<br>
1         212       4                 88<br>
2         417       2                 83<br>
3         112       3                 88<br>
4         426       5                 174<br>
Remaining memory in all blocks:<br>
Block 1: 100<br>
Block 2: 83<br>
Block 3: 88<br>
Block 4: 88<br>
Block 5: 174<br>
Internal Fragmentation (Best Fit): 533<br>

Worst Fit:<br>
Process   Size      Block Allocated   Leftover in Block<br>
1         212       5                 276<br>
2         417       2                 83<br>
3         112       5                 276<br>
4         426       Not Allocated     -<br>
Remaining memory in all blocks:<br>
Block 1: 100<br>
Block 2: 83<br>
Block 3: 200<br>
Block 4: 300<br>
Block 5: 276<br>
Internal Fragmentation (Worst Fit): 959<br>



<H2> 8. Paging Simulator <br></H2>
Objective: To simulate logical to physical address translation using paging technique. <br>
Files: paging_simulator.py <br>

Concept: <br>
Paging:<br>
Paging is a memory management technique where the logical memory is divided into fixed-size pages and physical memory is divided into frames of the same size. A page table is used to map logical pages to physical frames.<br>

Logical Address:<br>
A logical address consists of two parts: page number and offset. The page number identifies the page, and the offset identifies the exact location within that page.<br>

Physical Address:<br>
The physical address is obtained using the page table, where the page number is mapped to a frame number, and the offset remains unchanged.<br>

What the program does: <br>
i. Accepts logical address space size as input. <br>
ii. Accepts page size as input. <br>
iii. Calculates number of pages in logical address space. <br>
iv. Accepts logical address for translation. <br>
v. Converts logical address into page number and offset. <br>
vi. Maps page number to frame number using page table. <br>
vii. Displays the corresponding physical address. <br>
viii. Handles invalid addresses (out of range). <br>

How to run (Python version): <br>
python3 paging_simulator.py <br>

Expected output: <br>
Sample Test:<br>
$ python3 paging_simulator.py<br>
Enter logical address space size: 1024<br>
Enter page size: 128<br>
Enter logical address: 40<br>

Logical address 40 maps to page 0, offset 40.<br>
Physical address: Frame 0, offset 40.<br>
Physical address value: 40<br>

samole test 2: <br>
$  python3 paging_simulator.py<br>
Enter logical address space size: 1024<br>
Enter page size: 128<br>
Enter logical address: 140<br>

Logical address 140 maps to page 1, offset 12.<br>
Physical address: Frame 1, offset 12.<br>
Physical address value: 140<br>
