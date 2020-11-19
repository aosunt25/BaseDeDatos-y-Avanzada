#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <sys/wait.h>
#include <stdlib.h>
#include <pthread.h>
#include <semaphore.h>
#include <sys/sem.h>
#include <sys/ipc.h>

#define THREADS 5
#define SEM_NOMBRE1 "mi_sem1"
#define SEM_NOMBRE2 "mi_sem2"
#define SEM_NOMBRE3 "mi_sem3"
#define SEM_NOMBRE4 "mi_sem4"
#define SEM_NOMBRE5 "mi_sem5"

typedef struct filosofo
{
    char *nombre;
    sem_t *ten1;
    sem_t *ten2;
    int derecho;
    int pos;
} filosofo;



sem_t *tenedor1;
sem_t *tenedor2;
sem_t *tenedor3;
sem_t *tenedor4;
sem_t *tenedor5;


filosofo th1, th2, th3, th4, th5;

void comiendo(filosofo filos){
    if(filos.derecho){
        printf("Va a tomar el primer tenedor %d%s\n",filos.pos, filos.nombre);
        //pthread_mutex_lock(filos.ten1);
        sem_wait(filos.ten1);
        printf("Tiene el primer tenedor %d%s\n", (filos.pos+1)%5,filos.nombre);
        printf("Con hambre %s\n", filos.nombre);
        sleep(2);
        printf("Va a tomar el segundo tenedor %s\n", filos.nombre);
        //pthread_mutex_lock(filos.ten2);
        sem_wait(filos.ten2);
        printf("Agarra el segundo tenedor %s\n", filos.nombre);
        printf("Comiendo %s\n", filos.nombre);
        sleep(2);
        //pthread_mutex_unlock(filos.ten1);
        //pthread_mutex_unlock(filos.ten2);
        sem_post(filos.ten1);
        sem_post(filos.ten2);
    }
    else{
        printf("Va a tomar el primer tenedor %d%s\n", (filos.pos+1)%5, filos.nombre);
        //pthread_mutex_lock(filos.ten2);
        sem_wait(filos.ten2);
        printf("Tiene el primer tenedor %s\n", filos.nombre);
        printf("Con hambre %s\n", filos.nombre);
        sleep(2);
        printf("Va a tomar el segundo tenedor %d%s\n",filos.pos, filos.nombre);
        sem_wait(filos.ten1);
        printf("Agarra el segundo tenedor %s\n", filos.nombre);
        printf("Comiendo %s\n", filos.nombre);
        sleep(2);
        //pthrad_mutex_unlock(filos.ten1);
        //pthread_mutex_unlock(filos.ten2);
        sem_post(filos.ten1);
        sem_post(filos.ten2);
    }
    
    
}

void * proc1(void * arg) {
  filosofo *args = (filosofo*) arg;
  //printf("Filos %s\n", args->nombre);
  comiendo(*args);
  return arg;
}

int main()
{
    tenedor1 = sem_open(SEM_NOMBRE1, O_CREAT,S_IRWXU, 1);
    tenedor2 = sem_open(SEM_NOMBRE2, O_CREAT,S_IRWXU, 1);
    tenedor3 = sem_open(SEM_NOMBRE3, O_CREAT,S_IRWXU, 1);
    tenedor4 = sem_open(SEM_NOMBRE4, O_CREAT,S_IRWXU, 1);
    tenedor5 = sem_open(SEM_NOMBRE5, O_CREAT,S_IRWXU, 1);
    
    

    filosofo args[5];
    args[0].nombre = "Aristoteles";
    args[0].ten1 = tenedor1;
    args[0].ten2 = tenedor2;
    args[0].derecho = 0;
    args[0].pos = 0;

    args[1].nombre = "Sofocles";
    args[1].ten1 = tenedor2;
    args[1].ten2 = tenedor3;
    args[1].derecho = 0;
    args[1].pos = 1;

    args[2].nombre = "Demostenes";
    args[2].ten1 = tenedor3;
    args[2].ten2 = tenedor4;
    args[2].derecho = 0;
    args[2].pos = 2;

    args[3].nombre = "Platon";
    args[3].ten1 = tenedor4;
    args[3].ten2 = tenedor5;
    args[3].derecho = 0;
    args[3].pos = 3;

    args[4].nombre = "Tales";
    args[4].ten1 = tenedor5;
    args[4].ten2 = tenedor1;
    args[4].derecho = 0;
    args[4].pos = 4;
       
    pthread_t threads[THREADS];
    
    pthread_attr_t attr;

    pthread_attr_init(&attr);
    pthread_attr_setdetachstate( &attr, PTHREAD_CREATE_JOINABLE );
    pthread_attr_setscope( &attr, PTHREAD_SCOPE_SYSTEM );

    int i;
    for (i = 0; i < THREADS; i++) {
        int tmp = pthread_create(&threads[i], &attr, proc1, (void *) (args + i));
        if (tmp != 0) {
        printf("Problemas al crear el thread %d\n", i);
        exit(EXIT_FAILURE);
        }
    }
        
    /* esperando la terminación de los threads hijos */
    for (i = 0; i < THREADS; i++) {
        int tmp = pthread_join(threads[i], NULL);
        if (tmp != 0) {
        printf("Problemas esperando al thread %d\n", i);
        exit(EXIT_FAILURE);
        }
    }
    sem_post(tenedor1);
    sem_post(tenedor2);
    sem_post(tenedor3);
    sem_post(tenedor4);
    sem_post(tenedor5);
    sem_close(tenedor1); 
    sem_close(tenedor2); 
    sem_close(tenedor3); 
    sem_close(tenedor4); 
    sem_close(tenedor5); 
    sem_unlink(SEM_NOMBRE1);
    sem_unlink(SEM_NOMBRE2);
    sem_unlink(SEM_NOMBRE3);
    sem_unlink(SEM_NOMBRE4);
    sem_unlink(SEM_NOMBRE5);

    return 0;
}