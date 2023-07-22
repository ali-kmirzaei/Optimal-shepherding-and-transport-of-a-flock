parameters = {
    "timesteps" : 100000,
    "num_agents" :  50,
    "L" : 0, #periodic_boundary_conditions
    "sample_number" : 50,
    "v_sheep" : 0.05,
    "v_dog" : 0.5,
    "dt" : 0.05,
    "r" : 0.1, #r_vicsek_radius
    "ls" : 0.01, #ls_sheep_sheep_repulsion_lengthscale; main=0.01, another=0.05
    "ld" : 0.2, #1_ld_dog_sheep_repulsion_scale
    "eta" : 0.2, #eta_vicsek_noise

    "alpha" : 0.1, #alpha_vicsek_weight
    "beta" : 0.1, #beta_hard_shell_weight
    "gamma" : 0.005, #gamma_cm_attraction_weight
    "delta" : 0.9, #delta_dog_repulstion_weight

    "x_obstacle" : -2,
    "y_obstacle" : 3,
    "x_target" : -5,
    "y_target" : 5,
    "xd_start": 0.,
    "yd_start": -2.0,

    "dist_weight" : 3, #dist_weight_for_cost_function; main=2, best=3
    "spread_weight" : 5, #spread_weight_for_cost_function; main=10, best=5
    "coll_weight_factor" : 0.001, #collinear_weight_for_cost_function; main=0.001, best=0.001

    "dog_range": 6.28318530718,
    "bound": 1,  # boundary_for_sheep_initialization
    "grid_spacing": 0.01,  # grid_spacing_for_density_function_calculations
    "max_spread_X" : 0, #max_spread_X*ls
    "min_spread_X" : 0, #min_spread_X*ls
    "dist_weight_factor" : 0, #dist_weight_factor
    "speed_weight_factor" : 0, #speed_weight_factor
    "driving_on" : 0, #driving_on?
    "dog_dist_factor" : 10, #max_ld*X_distance_sheep_to_dogs_for_interaction
    "mod_dump_data" : 20, #how_often_to_dump_data
    "cm" : [0, 0]
}
