import random
import string

requirements = string.ascii_letters + string.digits + string.punctuation

def generatePassword(length):
    password = "".join(random.sample(requirements, length))
    return password

generated = generatePassword(10)
print(generated)
