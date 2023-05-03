from random import randint
from Process import Process
from Transfer import *
from threading import Thread
from time import sleep
from User import User

test_list = [
    {
        "k": 2,
        "r": 10,
        "n": [2]
    },
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

users = [
    User("a", "b", "igor_abc"),
    User("a", "b", "juares_egf"),
    User("a", "b", "veto_2asd"),
    User("a", "b", "gabras_8s4d"),
    User("a", "b", "matas_abc"),
    User("a", "b", "kaique_abc"),
    User("a", "b", "hitalo_calvo_asdasjh"),
]

transfers = []
def makeTransfers():
    for user in users:
        for user_receive in users:
            if user != user_receive:
                transfers.append(
                    Transfer(
                        user,
                        user_receive.pix_key,
                        randint(1, 500)
                    )
                )
makeTransfers()

def getRandomUser() -> User:
    return users[randint(0, len(users) - 1)]

def getRandomTransfers(repetitions) -> list:
    return [
        transfers[randint(0, len(transfers) - 1)] for i in range(repetitions)
    ]

def build(repetitions):
    Process(
        getRandomTransfers(repetitions),
        time_sleep=2
    )

# Executar testes
for test in test_list:
    process = []

    for n in test["n"]:
        for k in range(0, n):
            process.append(
                Thread(target=build, args=([test["r"]]))
            )

    print(f"\n\nTEST[{test}] -> Press [Enter] to run Test")
    input()

    for p in process:
        p.start()

    sleep(20)
    print("Sleep test finished ...")
    