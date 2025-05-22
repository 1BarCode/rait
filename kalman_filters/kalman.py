from math import *

# function to get the probability given: average, covariance, x
def prob(mu, sigma2, x):
    return 1 / sqrt(2.0 * pi * sigma2) * exp(-.5 * (x-mu)**2 / sigma2)

# update mean and variance when given mean and variance of prior belief and mean and variance of measurement
def update(mean1, var1, mean2, var2):
    new_mean = ((var2 * mean1) + (var1 * mean2)) / (var1 + var2)
    new_var = 1 / ((1 / var1) + (1 / var2))
    return [new_mean, new_var]

# print(update(10., 8., 13, 2.))

# predict new mean and var of motion
def predict(mean1, var1, mean2, var2):
    new_mean = mean1 + mean2
    new_var = var1 + var2
    return [new_mean, new_var]


def kf(measurements, motion, measurement_var, motion_var, mu, var):
    for i, measurement in enumerate(measurements):
        [mu, var] = update(mu, var, measurement, measurement_var)
        print("update:", [mu, var])
        [mu, var] = predict(mu, var, motion[i], motion_var)
        print("predict:", [mu, var])

measurements = [5., 6., 7., 9., 10.]
measurement_var = 4. # measured sigma / uncertainty
motion = [1., 1., 2., 1., 1.] # motion mean
motion_var = 2. # motion variance / uncertainty
mu = 0. # original mean
var = 1000. # original sigma / uncertainty
kf(measurements, motion, measurement_var, motion_var, mu, var)