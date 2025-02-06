import math
import random
def grams(ounces):
    gram=float(ounces/28.3495231)
    return gram

def celcius(fare):
    c = float((5 / 9) * (fare - 32))
    return c

def solve(numheads, numlegs):
  for num_chickens in range(numheads + 1):
    num_rabbits = numheads - num_chickens
    total_legs = 2 * num_chickens + 4 * num_rabbits
    if total_legs == numlegs:
      return num_chickens, num_rabbits
  return None

def filter_prime(numbers):
    new_list = []
    for num in numbers:
        if num <= 1:
            continue
        is_prime = True
        for i in range(2, num):
            if num % i == 0:
                is_prime = False
                break
        if is_prime:
            new_list.append(num)
    return new_list

def reverse_words(sentence):
    x=sentence.split()
    return (' '.join(x[::-1]))

def has_33(nums,size):
    checker=False
    for i in range(1,size):
        if (nums[i-1]==3 and nums[i]==3):
            checker=True
    return checker

def spy_game(list_example,size):
    new_list=list()
    for i in range(0,size):
        if (list_example[i]==0 or list_example[i]==7):
            new_list.append(list_example[i])
    if (len(new_list)>=3):
        if (new_list[0]==0 and new_list[1]==0 and new_list[2]==7):
            return True
        else:
            return False
    else:
        return False
    
def volume(user_input):
    return (4*math.pi*pow(r,3))/3

def unique(numbers):
    new_list = []
    for num in numbers:
        if num not in new_list:  
            new_list.append(num)
        else:
            pass
    return new_list

def palindrome(sentence):
    new_sentence="".join(char.lower() for char in sentence if char.isalnum())
    return new_sentence == new_sentence[::-1]

def histogram(user_list):
    for num in user_list:
        print(int(num) * "*") #return imediately exits the loop

def randomizer():
    my_number = random.randrange(1, 21)  
    count = 0
    n = int(input())

    while n != my_number:  
        count += 1  
        if n > my_number:
            print("Your guess is too big")
        elif n < my_number:
            print("Your guess is too low")
        n = int(input()) 
    
    print(f"Good job, you have guessed in {count+1} guesses") 

def hello():
    print("Hello")