from matrix import matrix

# example
# a = matrix([[10.], [10.]])
# F = matrix([[12., 8.], [6., 2.]])
# b = F * a
# b.show()

def kalman_filter(x, P):
    for n in range(len(measurements)):
        # measurement update
        # vectorize meas for compatib. -> Z is real-world ground truth from sensors w/ noise, here, it's just given
        Z = matrix([[measurements[n]]]) 
        # error/residual btw meas and predict (H * x) 
        y = Z - (H * x) 
        # covariance, measure uncertainty in residual y
        # H * P * H^T projects state uncertainty into measurement space
        # R is sensor noise - added, cos measurements are noisy
        S = H * P * H.transpose() + R 
        # K = Kalman Gain, tells how much to trust the measurement vs current prediction
        # higher K -> trust measurement more, lower K -> trust prediction more
        K = P * H.transpose() * S.inverse()
        # update state
        x = x + (K * y)
        P = (I - (K * H)) * P
        print('mx = ')
        x.show()
        print('mP = ')
        P.show()

        # prediction
        x = (F * x) + u
        P = F * P * F.transpose()
        print('px = ')
        x.show()
        print('pP = ')
        P.show()
    return x, P

measurements = [1, 2, 3]

x = matrix([[0.], [0.]]) # initial state (position and velocity)
P = matrix([[1000., 0.], [0., 1000.]]) # initial variance matrix / uncertainty, high uncertainty in position & velocity
# P[0][0] = variance position, P[1][1] = variance velocity
# covariance != correlation, correlation is normalized
# P[0][1] = Cov(pos, vel), P[1][0] = Cov(pos, vel)
u = matrix([[0.], [0.]]) # external motion, 0, 0 so no effect
F = matrix([[1., 1.], [0., 1.]]) # next state function
H = matrix([[1., 0.]]) # measurement function
R = matrix([[1.]]) # measurement uncertainty
I = matrix([[1., 0.], [0., 1.]]) # identity matrix

print(kalman_filter(x, P))