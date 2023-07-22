from parameters import parameters as pars
from random import random
import math
import numpy as np


def vicsek(x, y, theta, j):
    result = 0
    cnt = 0
    # noise = pars['eta'] * 2 * random()/0.5 #?#
    noise = np.random.uniform(-pars['eta']/2, pars['eta']/2)
    for i in range(pars['num_agents']):
        delta = math.sqrt((x[j]-x[i])**2 + (y[j]-y[i])**2)
        if delta < pars['r']:
            result += theta[i]
            cnt += 1
    theta_vsk = result/cnt + noise
    return [pars['v_sheep']*math.cos(theta_vsk), pars['v_sheep']*math.sin(theta_vsk)], theta_vsk

def sheep_repulsor(x, y, j):
    fx = 0
    fy = 0
    theta = 0
    for i in range(pars['num_agents']):
        if i == j: continue
        dx = x[j] - x[i]
        dy = y[j] - y[i]
        delta = math.sqrt(dx**2 + dy**2)
        ls = 5*pars['ls']
        # if delta < 10*pars['ls']:
        if delta < ls:
            theta_dr = math.atan2(dy, dx)
            theta += theta_dr
            fx += math.exp(-delta/ls) * math.cos(theta_dr)
            fy += math.exp(-delta/ls) * math.sin(theta_dr)
    return [fx, fy], theta

def sheep_attractor(x, y, j):
    dx = pars['cm'][0] - x[j]
    dy = pars['cm'][1] - y[j]
    theta_lr = math.atan2(dy, dx)
    return [pars['v_sheep']*math.cos(theta_lr), pars['v_sheep']*math.sin(theta_lr)], theta_lr

def dog_repulsor(j, x, y, xd2, yd2, angle):
    fx = 0
    fy = 0
    dx = x[j] - xd2
    dy = y[j] - yd2
    delta = math.sqrt(dx**2 + dy**2)
    theta_dr = math.atan2(dy, dx)
    # lambda1 = 0
    # f = math.exp(-delta/pars['ld']) * math.exp(math.cos(theta_dr-angle)*lambda1) #?#
    # return [f*math.cos(theta_dr), f*math.sin(theta_dr)], theta_dr
    ## if delta < pars['ld']:
    fx = math.exp(-delta/pars['ld']) * math.cos(theta_dr)
    fy = math.exp(-delta/pars['ld']) * math.sin(theta_dr)
    return [fx, fy], theta_dr

def cost_function(x_test, y_test, xd2, yd2):

    x_cm = 0
    y_cm = 0
    for i in range(pars['num_agents']):
        x_cm += x_test[i]
        y_cm += y_test[i]
    x_cm /= pars['num_agents']
    y_cm /= pars['num_agents']

    cost_function_val = [0, 0, x_cm, y_cm]

    dx = pars['x_target']-x_cm
    dy = pars['y_target']-y_cm
    dr = math.sqrt(dx**2 + dy**2)
    sheep_spread = 0
    for k in range(pars['num_agents']):
        dx = x_test[k] - x_cm
        dy = y_test[k] - y_cm
        dist = dx**4 + dy**4
        sheep_spread += dist
    # sheep_spread = math.sqrt(math.sqrt( sheep_spread/pars['num_agents'] ))
    sheep_spread = (sheep_spread/pars['num_agents']) ** 0.25
    cost_function_val[1] = sheep_spread

    tmp_angle_herd_target = math.atan2(pars['y_target']-y_cm, pars['x_target']-x_cm)
    tmp_x_dog_target = x_cm + pars['ld'] * math.cos(tmp_angle_herd_target)
    tmp_y_dog_target = y_cm + pars['ld'] * math.sin(tmp_angle_herd_target)
    tmp_driving_cost = (xd2-tmp_x_dog_target)**2 + (yd2-tmp_y_dog_target)**2
    cost_function_val[0] = pars['dist_weight']*dr +\
                           pars['spread_weight']*sheep_spread +\
                           pars['coll_weight_factor']*tmp_driving_cost

    return cost_function_val

