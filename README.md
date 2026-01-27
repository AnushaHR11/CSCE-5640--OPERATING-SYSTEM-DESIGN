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
