from random import randint
from Process import Process
from threading import Thread

pix_keys = [
    "igor_abc",
    "juares_egf",
    "veto_2asd",
    "gabras_8s4d",
    "matas_abc",
    "kaique_abc",
    "hitalo_valvo_asdasjh",
]

for pos, key in enumerate(pix_keys):
    value = randint(-10, 50)

    print(f"POS={pos}   KEY={key}   VALUE={value}")
    process = Process(pos, 2, key, value)
    thread = Thread(target=process.requestOperation, args=()).start()

    input()
    