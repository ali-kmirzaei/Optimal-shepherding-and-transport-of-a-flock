from parameters import parameters as pars
import numpy as np
import herding as h

def store_data(file, data, timestep):
    for i in range(pars['num_agents']):
        line = str(timestep)+' '+str(i)+' '+str(data[0][i])+' '+str(data[1][i])+' '+str(data[2][i])+' '+str(data[3])+' '+str(data[4])+' '+str(data[5])+'\n'
        file.write(line)

def store_cost(file, data, timestep):
    line = str(timestep)+' '+str(data[0])+' '+str(data[1])+' '+str(data[2])+' '+str(data[3])+' '+str(data[4])+'\n'
    file.write(line)

def load_data(dat_field):
    xpart = dat_field[:, 2]
    ypart = dat_field[:, 3]
    thetapart = dat_field[:, 4]
    xdog = dat_field[:, 5]
    ydog = dat_field[:, 6]
    thetadog = dat_field[:, 7]
    dat_times = dat_field[:, 0]
    timesteps = int(len(dat_times)/pars['num_agents'])
    times = np.arange(0,timesteps,1)
    return xpart, ypart, thetapart, xdog, ydog, thetadog, dat_times, timesteps, times

def get_targets(x, y):
    dx = pars['x_target'] - pars['x_obstacle']
    dy = pars['y_target'] - pars['y_obstacle']
    theta_ot = np.arctan2(dy, dx)

    h.get_cm(x, y)
    dx = pars['x_target'] - pars['cm'][0]
    dy = pars['y_target'] - pars['cm'][1]
    theta_cmt = np.arctan2(dy, dx)

    delta = abs(theta_ot-theta_cmt)

    print(delta)
    targets = list()
    if delta < 0.1:
        x_target_half = pars['x_obstacle'] + 1
        y_target_half = pars['y_obstacle'] + 1
        targets.append((x_target_half, y_target_half))
    targets.append((pars["x_target"], pars["y_target"]))
    print(targets)
    return targets
