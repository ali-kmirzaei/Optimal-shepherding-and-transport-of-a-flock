import math
from parameters import parameters as pars
from random import random
import forces_cost as fc


def get_cm(x, y):
    xt = 0
    yt = 0
    for i in range(pars['num_agents']):
        xt += x[i]
        yt += y[i]
    pars['cm'] = [xt/pars['num_agents'], yt/pars['num_agents']]

def sheep_step_no_dog(x, y, theta, x2, y2, theta2):
    get_cm(x, y)
    for i in range(pars['num_agents']):
        # Viscek interaction
        v_vsk, theta_vsk = fc.vicsek(x, y, theta, i)
        x_next = pars['alpha']*v_vsk[0]*pars['dt']
        y_next = pars['alpha']*v_vsk[1]*pars['dt']
        # Hard sphere repulsion
        v_sr, theta_sr = fc.sheep_repulsor(x, y, i)
        x_next += pars['beta']*v_sr[0]*pars['dt']
        y_next += pars['beta']*v_sr[1]*pars['dt']
        # CM attraction
        v_cm, theta_cm = fc.sheep_attractor(x, y, i)
        x_next += pars['gamma']*v_cm[0]*pars['dt']
        y_next += pars['gamma']*v_cm[1]*pars['dt']
        # Update x2, y2
        x2[i] = x[i] + x_next
        y2[i] = y[i] + y_next
        theta2[i] = math.atan2(y_next, x_next)
    return x2, y2, theta2

def test_propagate_sheep(x, y, x2, y2, xd2, yd2, angle):
    x_test = list()
    y_test = list()
    theta_test = list()
    for i in range(pars['num_agents']):
        v_dr, theta_dr = fc.dog_repulsor(i, x, y, xd2, yd2, angle)
        x_next_test = pars['delta'] * v_dr[0] * pars['dt']
        y_next_test = pars['delta'] * v_dr[1] * pars['dt']
        x_test.append(x_next_test + x2[i])
        y_test.append(y_next_test + y2[i])
        theta_test.append(theta_dr)
    return x_test, y_test, theta_test

def first_round(x, y, x2, y2, xd, yd, xcm_final, ycm_final, sheep_spread_final):
    cost_min = math.exp(100)
    cost_max = 0
    cost_tmp = 0
    theta_dog = 0
    xd_f = xd
    yd_f = yd
    for i in range(pars['sample_number']):
        get_cm(x, y)
        dog_sample_angle = pars["dog_range"] * (random()-0.5)
        xd2 = xd + pars['v_dog'] * math.cos(dog_sample_angle) * pars['dt']
        yd2 = yd + pars['v_dog'] * math.sin(dog_sample_angle) * pars['dt']
        delta = math.sqrt((xd2-pars['cm'][0])**2 + (yd2-pars['cm'][1])**2)
        if delta < 5 * pars['dog_dist_factor'] * pars['ld']: #?#
        # if delta < pars['ld']:
            x_test, y_test, theta_test = test_propagate_sheep(x, y, x2, y2, xd2, yd2, dog_sample_angle)
            # get_cm(x_test, y_test)
            cost_function_val = fc.cost_function(x_test, y_test, xd2, yd2)
            cost_tmp = cost_function_val[0]
            if cost_tmp <= cost_min:
                xd_f = xd2
                yd_f = yd2
                cost_min = cost_tmp
                sheep_spread_final = cost_function_val[1]
                xcm_final = cost_function_val[2]
                ycm_final = cost_function_val[3]
                theta_dog = dog_sample_angle
            elif cost_tmp >= cost_max:
                cost_max = cost_tmp
        else:
            tmp_angle_dog_herd = math.atan2(pars['cm'][1]-yd, pars['cm'][0]-xd)
            xd_f = xd + pars['v_dog'] * math.cos(tmp_angle_dog_herd) * pars['dt']
            yd_f = yd + pars['v_dog'] * math.sin(tmp_angle_dog_herd) * pars['dt']
    return xd_f, yd_f, theta_dog, xcm_final, ycm_final, sheep_spread_final

def final_round(x, x2, y, y2, xdog, ydog, xdogf, ydogf, theta2):
    xd = xdog
    yd = ydog
    xd2 = xdogf
    yd2 = ydogf
    dog_vel_angle = math.atan2(yd2-yd, xd2-xd)
    # delta = math.sqrt((xd2-xd)**2 + (yd2-yd)**2)
    # if delta > v_dog_tmp*pars['dt']: pass
    for i in range(pars['num_agents']):
        x_next = x2[i]-x[i]
        y_next = y2[i]-y[i]
        v_dr, theta = fc.dog_repulsor(i, x, y, xd2, yd2, dog_vel_angle)
        x_next += pars['delta']*v_dr[0]*pars['dt']
        y_next += pars['delta']*v_dr[1]*pars['dt']
        x2[i] = x_next + x[i]
        y2[i] = y_next + y[i]
        theta2[i] = math.atan2(y_next, x_next)
    #?#
    return x2, y2, theta2

def is_close(xcm_final, ycm_final):
    dx = xcm_final-pars['x_target']
    dy = ycm_final-pars['y_target']
    if dx**2 + dy**2 < pars['num_agents']*pars['ls']:
        return 1
    return 0

