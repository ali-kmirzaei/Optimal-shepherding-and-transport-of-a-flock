from parameters import parameters as pars
import herding as h
import ofunc as of
import forces_cost
from random import random
from tqdm import tqdm



# Initialize
xdog = pars['xd_start']
ydog = pars['yd_start']
thetadog = 0
xdogf = 0
ydogf = 0
thetadogf = 0

x = [pars['bound']*random() for i in range(pars['num_agents'])]
y = [pars['bound']*random() for i in range(pars['num_agents'])]
theta = [2*3.14*random() for i in range(pars['num_agents'])]
x2 = [0 for i in range(pars['num_agents'])]
y2 = [0 for i in range(pars['num_agents'])]
theta2 = [0 for i in range(pars['num_agents'])]

sheep_spread2 = 0
sheep_spread_final = 0
dist_weight_2 = pars['dist_weight'] #alpha value to play with!
# v_dog_tmp = pars['v_dog']
max_spread = pars['max_spread_X']*pars['ls']
min_spread = pars['min_spread_X']*pars['ls']
xcm_final = 0
ycm_final = 0

cost_file = open('cost.txt', 'w')
data_file = open('data.txt', 'w')
of.store_data(file=data_file, data=[x, y, theta, xdog, ydog, thetadogf], timestep=0)


targets = of.get_targets(x, y)
cnt = 0
for target in targets:
    cnt += 1
    pars["x_target"] = target[0]
    pars["y_target"] = target[1]
    for jj in tqdm(range(pars['timesteps'])):
        x2, y2, PASHM = h.sheep_step_no_dog(x, y, theta, x2, y2, theta2)
        if jj > 1*cnt:
            xdogf, ydogf, thetadog, xcm_final, ycm_final, sheep_spread_final = h.first_round(x, y, x2, y2, xdog, ydog, xcm_final, ycm_final, sheep_spread_final)
            x, y, theta = h.final_round(x, x2, y, y2, xdog, ydog, xdogf, ydogf, theta2)
            xdog = xdogf
            ydog = ydogf
        if h.is_close(xcm_final, ycm_final) == 1: break
        if jj%pars['mod_dump_data'] == 0:
            of.store_data(file=data_file, data=[x, y, theta, xdog, ydog, thetadog], timestep=jj+1)
            of.store_cost(file=cost_file, data=[dist_weight_2, pars['v_dog'], sheep_spread_final, xcm_final, ycm_final], timestep=jj+1)

