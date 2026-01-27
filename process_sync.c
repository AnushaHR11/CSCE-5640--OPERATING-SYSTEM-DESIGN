#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/wait.h>
#include <unistd.h>

int main(void) {
    int pipefd[2];

    /* Pipe used only to synchronize output order */
    if (pipe(pipefd) == -1) {
        perror("pipe");
        return EXIT_FAILURE;
    }

    pid_t pid = fork();
    if (pid < 0) {
        perror("fork");
        close(pipefd[0]);
        close(pipefd[1]);
        return EXIT_FAILURE;
    }

    if (pid == 0) {
        /* ---------------- Child process ---------------- */
        close(pipefd[1]); /* close write end */

        /* Wait until parent prints its PID */
        char token;
        ssize_t n = read(pipefd[0], &token, 1);
        if (n < 0) {
            perror("child read (sync)");
            close(pipefd[0]);
            _exit(EXIT_FAILURE);
        } else if (n == 0) {
            fprintf(stderr, "child: sync pipe closed unexpectedly\n");
            close(pipefd[0]);
            _exit(EXIT_FAILURE);
        }
        close(pipefd[0]);

        printf("Child Process ID: %d\n", (int)getpid());
        fflush(stdout);

        /* Replace child process image with "ls -l" */
        execlp("ls", "ls", "-l", (char *)NULL);

        /* If execlp returns, it failed */
        perror("execlp");
        _exit(127);
    } else {
        /* ---------------- Parent process ---------------- */
        close(pipefd[0]); /* close read end */

        printf("Parent Process ID: %d\n", (int)getpid());
        fflush(stdout);

        /* Signal child to continue */
        char token = 'X';
        if (write(pipefd[1], &token, 1) != 1) {
            perror("parent write (sync)");
            close(pipefd[1]);
            /* Still attempt to wait for child to avoid zombie */
        }
        close(pipefd[1]);

        int status;
        pid_t w = waitpid(pid, &status, 0);
        if (w < 0) {
            perror("waitpid");
            return EXIT_FAILURE;
        }

        if (WIFEXITED(status)) {
            int code = WEXITSTATUS(status);
            if (code != 0) {
                fprintf(stderr, "Child exited with status %d\n", code);
            }
        } else if (WIFSIGNALED(status)) {
            fprintf(stderr, "Child terminated by signal %d\n", WTERMSIG(status));
        }

        printf("Child process has completed.\n");
        return EXIT_SUCCESS;
    }
}