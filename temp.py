from operator import truediv
from turtle import Screen
import numpy as np
import pygame
from time import time, sleep
from random import randint as r
import random

n = 10 
scrax = n*20
scray = n*20
background =(255, 255, 255)
screen = pygame.display.set_mode((scrax, scray))
colors = [(51, 51, 51) for i in range(n**2)]
reward = np.zeros((n, n))

states = {}
actions = {"up":0, "down":1, "left":2, "right":3}
terminals =[]
penalities = 10
Q = np.zeros((n**2, 4))
while penalities != 0:
    i = r(0, n-1)
    j = r(0, n-1)
    if reward[i, j] ==0 and [i, j] != [0, 0] and [i, j] !=[n-1, n-1]:
        reward[i, j] = -1
        penalities -= 1
        colors[i*n +j] = (0, 255, 0)
        terminals.append(i*n + j)
# colors [n*3 + 4] =(0, 255, 0)
# reward[3, 4] = -1
# terminals.append(n*3 +4)
# colors [n*4 + 4] =(0, 255, 0)
# reward[4, 4] = -1
# terminals.append(n*5 +4)
# colors [n*5 + 4] =(0, 255, 0)
# reward[5, 4] = -1
# terminals.append(n*5 +4)


# colors [n*5 + 5] =(0, 255, 0)
# reward[5, 5] = -1
# terminals.append(n*5 +5)


# colors [n*3 + 6] =(0, 255, 0)
# reward[3, 6] = -1
# terminals.append(n*3 +6)
# colors [n*4 + 6] =(0, 255, 0)
# reward[4, 6] = -1
# terminals.append(n*4 +6)
# colors [n*5 + 6] =(0, 255, 0)
# reward[5, 6] = -1
# terminals.append(n*5 +6)

reward[n-1, n-1] = 1
colors[n**2 - 1] =(0, 0, 255)
terminals.append(n**2 - 1)



k = 0
for i in range(n):
    for j in range(n):
        states[(i,j)] = k
        k+=1
istrain = True
current_pos = [0, 0]
alpha = 0.9
gamma = 0.8
epsilon = 1.0
decay_rate = 0.005

sheep_x = n-1
sheep_y = n-1
sheep_pos = []

def select_action(current_state):
    global current_pos,epsilon
    possible_action =[]
    if np.random.uniform() <= epsilon:
        if current_pos[0] != 0:
            possible_action.append("up")
        if current_pos[0] != n-1:
            possible_action.append("down")
        if current_pos[1] != 0:
            possible_action.append("left")
        if current_pos[1] != n-1:
            possible_action.append("right")
        action = actions[possible_action[r(0, len(possible_action)-1)]]    
    else:
        m = np.min(Q[current_state])
        if current_pos[0] != 0: #up
            possible_action.append(Q[current_state,0])
        else:
            possible_action.append(m - 100)
        if current_pos[0] != n-1: #down
            possible_action.append(Q[current_state,1])
        else:
            possible_action.append(m - 100)
        if current_pos[1] != 0: #left
            possible_action.append(Q[current_state,2])
        else:
            possible_action.append(m - 100)
        if current_pos[1] != n-1: #right
            possible_action.append(Q[current_state,3])
        else:
            possible_action.append(m - 100)
        action = random.choice([i for i, a in enumerate(possible_action) if a == max(possible_action)])
    
    return action

def episode():
    global current_pos,epsilon, isdog
    current_state = states[(current_pos[0], current_pos[1])]
    action = select_action(current_state)
    if action == 0:
        current_pos[0] -= 1
    elif action == 1:
        current_pos[0] += 1
    elif action == 2:
        current_pos[1] -= 1
    elif action == 3:
        current_pos[1] += 1

    new_state = states[(current_pos[0],current_pos[1])]
    if new_state not in terminals:
        Q[current_state, action] += alpha*(reward[current_pos[0], current_pos[1]] + gamma*(np.max(Q[new_state]))- Q[current_state, action])
    else:
        Q[current_state, action] += alpha*(reward[current_pos[0], current_pos[1]] - Q[current_state, action])   
        if istrain == True:
            current_pos = [0,0]
        else:
            isdog = True
            while isdog:
                dog_x = r(0, n-1)
                dog_y = r(0, n-1)
                if reward[dog_x, dog_y] == 0:
                    isdog = False
            current_pos = [dog_x, dog_y]
        epsilon = np.exp(-decay_rate*i)

def layout():
    c =0
    for i in range(0, scrax , 20):
        for j in range(0, scray, 20):
            pygame.draw.rect(screen, (255, 255, 255), (j, i, j+20, i+20),0)
            pygame.draw.rect(screen, colors[c], (j+3, i+3, j+17, i+17))
            c += 1

run = True
delay =0.5 
for i in range(10000):
    episode()
# current_pos = [0,0]
dog_x = 0
dog_y = 0
istrain = False

isdog = True
while isdog:
    dog_x = r(0, n-1)
    dog_y = r(0, n-1)
    if reward[dog_x, dog_y] == 0:
        isdog = False

while run:
    screen.fill(background)
    layout()
    episode()
    sleep(delay)
    pygame.draw.circle(screen, (25,129,230), (current_pos[1]*20+11, current_pos[0]*20+11), 8, 0)
    pygame.display.flip()
    # if current_pos == [n-1, n-1]:
    #     pygame.quit()
pygame.quit()






