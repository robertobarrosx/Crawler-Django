from multiprocessing import  Process, Queue
import multiprocessing
import time
import os


def funcao(q):
    # pegando o id do processo atual (filho)
    id = os.getpid()
    # pegando o id do processo pai
    ppid = os.getppid()
    nome = multiprocessing.current_process().name
    print("{} - Eu sou o processo id={} ppid={}".format(nome, id, ppid))
    time.sleep(120)


if __name__ == "__main__":
    processos = []
    # pegando o id do processo atual
    id = os.getpid()
    print("Eu sou o processo pai id={}".format(id))
    q = Queue()
    for i in range(5):
        processo = Process(name="Processinho {}".format(i),
                                           target=funcao, args=(i,q,))
        processo.start()

        processos.append(processo)

    time.sleep(10)

    # percorre os processos filhos verificando se estão executando
    # se sim, envia o sinal de finalização
    for processo in processos:
        if (processo.is_alive()):
            print("Terminando processo {}".format(processo.pid))
            processo.terminate()

    for processo in processos:
        processo.join()

    print("Pai finalizando...!!!")