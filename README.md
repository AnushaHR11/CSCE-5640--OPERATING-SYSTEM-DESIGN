# CSCE-5640--OPERATING-SYSTEM-DESIGN
1. Process Creation and Termination
    Assignment 3: Process Creation and Termination
    Files: process_sync.c

   What the program does:
   1) Creates a pipe to synchronize output order.
   2) Calls fork() to create a child process.
   3) Parent process:
      - Prints the parent PID
      - Signals the child through the pipe
      - Waits for the child to finish using waitpid()
      - Prints "Child process has completed."
  4) Child process:
   - Waits until parent signals through the pipe
   - Prints the child PID
   - Executes "ls -l" using execlp()
5) Errors are handled with perror() and proper exit codes.

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
