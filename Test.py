from Process import *

test_list = [
    {
        "k": 2,
        "r": 10,
        "n": [2, 4, 8, 16, 32]
    },
    {
        "k": 1,
        "r": 5,
        "n": [2, 4, 8, 16, 32, 64]
    },
    {
        "k": 0,
        "r": 3,
        "n": [2, 4, 8, 16, 32, 128]
    },
]

def createProcess(time_sleep, repetion):
    for i in range(repetion):

        Process(f"PROCESS-02_{i}", time_sleep).send(Protocol.REQUEST)

if __name__ == "__main__":
    for details in test_list:
        k = details['k']
        r = details['r']
        n_list = details['n']

        for n in n_list:
            print(f"Test 01 - n={n} sum(k)={n * r * k}")
            sleep(3)
            
            for i in range(n):
                t = Thread(target=createProcess, args=(k, r))
                input()
                t.start()
