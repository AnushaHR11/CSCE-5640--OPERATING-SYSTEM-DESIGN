#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <semaphore.h>
#include <unistd.h>

#define DEFAULT_BUFFER_SIZE 5

typedef struct {
    int *buffer;
    int buffer_size;

    int in;   // next write index
    int out;  // next read index

    int total_items;              // total items to be produced overall
    int produced_count;           // protected by count_mutex
    int consumed_count;           // protected by count_mutex

    sem_t empty;                  // counts empty slots
    sem_t full;                   // counts filled slots
    sem_t mutex;                  // protects buffer access

    pthread_mutex_t count_mutex;  // protects produced_count/consumed_count
} Shared;

typedef struct {
    int id;
    Shared *shared;
} ThreadArg;

static void *producer(void *arg) {
    ThreadArg *a = (ThreadArg *)arg;
    Shared *s = a->shared;

    while (1) {
        // Decide next item number safely (global total production)
        pthread_mutex_lock(&s->count_mutex);
        if (s->produced_count >= s->total_items) {
            pthread_mutex_unlock(&s->count_mutex);
            break;
        }
        int item = ++s->produced_count;
        pthread_mutex_unlock(&s->count_mutex);

        // Wait for empty slot, then lock buffer
        sem_wait(&s->empty);
        sem_wait(&s->mutex);

        // Critical section: write to buffer
        s->buffer[s->in] = item;
        s->in = (s->in + 1) % s->buffer_size;

        printf("Producer %d produced item %d\n", a->id, item);

        // Unlock buffer, signal full slot
        sem_post(&s->mutex);
        sem_post(&s->full);

        // Slow it a bit so output is readable (optional)
        usleep(80000);
    }

    return NULL;
}

static void *consumer(void *arg) {
    ThreadArg *a = (ThreadArg *)arg;
    Shared *s = a->shared;

    while (1) {
        // Check if all items are already consumed (avoid hanging)
        pthread_mutex_lock(&s->count_mutex);
        if (s->consumed_count >= s->total_items) {
            pthread_mutex_unlock(&s->count_mutex);
            break;
        }
        pthread_mutex_unlock(&s->count_mutex);

        // Wait for full slot, then lock buffer
        sem_wait(&s->full);
        sem_wait(&s->mutex);

        // Critical section: read from buffer
        int item = s->buffer[s->out];
        s->out = (s->out + 1) % s->buffer_size;

        sem_post(&s->mutex);
        sem_post(&s->empty);

        // Count consumption safely
        pthread_mutex_lock(&s->count_mutex);
        if (s->consumed_count < s->total_items) {
            s->consumed_count++;
            printf("Consumer %d consumed item %d\n", a->id, item);
        }
        pthread_mutex_unlock(&s->count_mutex);

        usleep(120000);
    }

    return NULL;
}

int main(int argc, char *argv[]) {
    int producers = 1;
    int consumers = 1;
    int total_items = 10;
    int buffer_size = DEFAULT_BUFFER_SIZE;

    // Optional CLI: ./pc <producers> <consumers> <total_items> [buffer_size]
    if (argc >= 4) {
        producers = atoi(argv[1]);
        consumers = atoi(argv[2]);
        total_items = atoi(argv[3]);
    }
    if (argc >= 5) {
        buffer_size = atoi(argv[4]);
    }

    if (producers <= 0 || consumers <= 0 || total_items <= 0 || buffer_size <= 0) {
        fprintf(stderr, "Usage: %s <producers> <consumers> <total_items> [buffer_size]\n", argv[0]);
        return 1;
    }

    Shared s;
    s.buffer_size = buffer_size;
    s.buffer = (int *)malloc(sizeof(int) * s.buffer_size);
    if (!s.buffer) {
        perror("malloc");
        return 1;
    }

    s.in = 0;
    s.out = 0;
    s.total_items = total_items;
    s.produced_count = 0;
    s.consumed_count = 0;

    sem_init(&s.empty, 0, s.buffer_size); // initially all slots empty
    sem_init(&s.full, 0, 0);              // initially no items
    sem_init(&s.mutex, 0, 1);             // binary semaphore (mutex)

    pthread_mutex_init(&s.count_mutex, NULL);

    pthread_t *pt = (pthread_t *)malloc(sizeof(pthread_t) * producers);
    pthread_t *ct = (pthread_t *)malloc(sizeof(pthread_t) * consumers);
    ThreadArg *pargs = (ThreadArg *)malloc(sizeof(ThreadArg) * producers);
    ThreadArg *cargs = (ThreadArg *)malloc(sizeof(ThreadArg) * consumers);

    if (!pt || !ct || !pargs || !cargs) {
        perror("malloc");
        free(s.buffer);
        return 1;
    }

    for (int i = 0; i < producers; i++) {
        pargs[i].id = i + 1;
        pargs[i].shared = &s;
        pthread_create(&pt[i], NULL, producer, &pargs[i]);
    }

    for (int i = 0; i < consumers; i++) {
        cargs[i].id = i + 1;
        cargs[i].shared = &s;
        pthread_create(&ct[i], NULL, consumer, &cargs[i]);
    }

    for (int i = 0; i < producers; i++) pthread_join(pt[i], NULL);
    for (int i = 0; i < consumers; i++) pthread_join(ct[i], NULL);

    printf("Done. Produced=%d, Consumed=%d\n", s.produced_count, s.consumed_count);

    sem_destroy(&s.empty);
    sem_destroy(&s.full);
    sem_destroy(&s.mutex);
    pthread_mutex_destroy(&s.count_mutex);

    free(pt);
    free(ct);
    free(pargs);
    free(cargs);
    free(s.buffer);

    return 0;
}
