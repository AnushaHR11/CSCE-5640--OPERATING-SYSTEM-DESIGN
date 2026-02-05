# CSCE-5640 : OPERATING-SYSTEM-DESIGN
<H2> 1. Process Creation and Termination <br> </H2>
    Assignment 3: Process Creation and Termination <br>
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
    Assignment 5: Producer-Consumer using Semaphores <br>
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
