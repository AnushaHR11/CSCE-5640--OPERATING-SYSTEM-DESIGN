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


<H2> 4. Implementing Multilevel Feedback Queue (MLFQ) Scheduling <br>
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

