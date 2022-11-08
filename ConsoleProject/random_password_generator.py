import string
from random import randint,shuffle,choice
import time



def generate_password1(password_length:int=15):
    characters = list(string.ascii_letters + string.digits + " !@#$%^&*()")
    l=len(characters)-1
    password=''
    for x in range(password_length):
        password+=characters[randint(0,l)]
    
    return password
    

def generate_password2(password_length:int =15):
    characters = list(string.ascii_letters + string.digits + " !@#$%^&*()")

    
    shuffle(characters)
    
    password = []
    
    for x in range(password_length):
        password.append(choice(characters))
    
    shuffle(password)
    
    password = "" .join(password)
    return password



if __name__=="__main__":
    start=time.time()
    print(generate_password1(20))
    print(f"gen1 {time.time()-start}")
    start=time.time()
    print(generate_password2(20))
    print(f"gen2 {time.time()-start}")
    

