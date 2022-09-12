import hashlib

# import random
# import time
# from threading import Thread
#
# def generate_transactions():
#     while True:
#         print(random.randrange(1,20))
#         time.sleep(1)
#
#
# def generate_transactions_2():
#     while True:
#         print(random.randrange(20,40))
#         time.sleep(1)
#
# thread_1 = Thread(target = generate_transactions)
# thread_2 = Thread(target = generate_transactions_2)
#
# thread_1.start()
# thread_2.start()

def proof_of_work(last_proof):
    """
    Simple Proof of Work Algorithm:
     - Find a number p' such that hash(pp') contains leading 4 zeroes, where p is the previous p'
     - p is the previous proof, and p' is the new proof
    :param last_proof: <int>
    :return: <int>
    """

    proof = 0
    while valid_proof(last_proof, proof) is False:
        proof += 1

    return proof



def valid_proof(last_proof, proof):
    """
    Validates the Proof: Does hash(last_proof, proof) contain 4 leading zeroes?
    :param last_proof: <int> Previous Proof
    :param proof: <int> Current Proof
    :return: <bool> True if correct, False if not.
    """

    guess = f'{last_proof}{proof}'.encode()
    print(guess)
    guess_hash = hashlib.sha256(guess).hexdigest()
    print(guess_hash)
    if guess_hash[:2]=="00":
        print(guess, guess_hash)
    return guess_hash[:2] == "00"


proof_of_work(27819)