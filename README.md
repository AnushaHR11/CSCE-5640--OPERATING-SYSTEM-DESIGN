# CSCE-5640--OPERATING-SYSTEM-DESIGN
1. Process Creation and Termination
    Assignment 3: Process Creation and Termination
    Files: process_sync.c

   What the program does:
   i. Creates a pipe to synchronize output order.
   ii. Calls fork() to create a child process.
   iii. Parent process:
      - Prints the parent PID
      - Signals the child through the pipe
      - Waits for the child to finish using waitpid()
      - Prints "Child process has completed."
    iv. Child process:
        - Waits until parent signals through the pipe
        - Prints the child PID
        - Executes "ls -l" using execlp()
    v. Errors are handled with perror() and proper exit codes.

How to compile:
gcc -Wall -Wextra -O2 -o process_sync.c

How to run:
./process_sync

Expected output (example):
Parent Process ID: 5797
Child Process ID: 5798
total 28
-rw-rw-rw- 1 codespace root         64 Jan 27 03:22 README.md
-rwxrwxrwx 1 codespace codespace 16664 Jan 27 03:25 process_sync
-rw-rw-rw- 1 codespace codespace  2371 Jan 27 03:24 process_sync.c
Child process has completed.

2. Implementing the Producer-Consumer Problem with Semaphores
    Assignment 5: Producer-Consumer using Semaphores
    How it works:
   - We use a fixed-size shared buffer (circular queue).
   - Semaphores:
  1) empty: counts available empty slots in the buffer
  2) full : counts filled slots in the buffer
  3) mutex: ensures mutual exclusion while accessing the buffer (critical section)

Flow:
Producer:
  - choose next item number (protected by count_mutex)
  - wait(empty)
  - wait(mutex)
  - insert item into buffer
  - post(mutex)
  - post(full)

Consumer:
  - wait(full)
  - wait(mutex)
  - remove item from buffer
  - post(mutex)
  - post(empty)
  - update consumed_count (protected by count_mutex)

Parameter passing method:
- Each thread receives a pointer to a ThreadArg struct:
    typedef struct { int id; Shared *shared; } ThreadArg;
- This avoids global per-thread variables and safely passes:
  - the thread’s id
  - the pointer to the shared data structure (buffer + semaphores)

Compile:
  gcc -o producer_consumer producer_consumer.c -pthread
  
How to run:
./producer_consumer

Expected output:
Producer 1 produced item 1
Consumer 1 consumed item 1
Producer 1 produced item 2
Consumer 1 consumed item 2
Producer 1 produced item 3
Consumer 1 consumed item 3
Producer 1 produced item 4
Producer 1 produced item 5
Consumer 1 consumed item 4
Producer 1 produced item 6
Consumer 1 consumed item 5
Producer 1 produced item 7
Producer 1 produced item 8
Consumer 1 consumed item 6
Producer 1 produced item 9
Consumer 1 consumed item 7
Producer 1 produced item 10
Consumer 1 consumed item 8
Consumer 1 consumed item 9
Consumer 1 consumed item 10
Done. Produced=10, Consumed=10
