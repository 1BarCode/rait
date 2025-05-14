# p = [0, 1, 0, 0, 0]
p = [] # each position is Xi
n = 5
for i in range(n):
    p.append(0.2)

world = ['green', 'red', 'red', 'green', 'green']
measurements = ['red', 'red']
pHit = 0.6      # P(Z = sensed_color | Xi = correct_color)
pMiss = 0.2     # P(Z = sensed_color | Xi != correct_color)
# Therefore: 
# func sense = P(Xi | Z) = [ P(Z | Xi) * P(Xi) ] / P(Z)
# P(Z) = sum( P(Z | Xi) * P(Xi) )
# P(Z | Xi) * P(Xi) = (hit * pHit + (1 - hit) * pMiss)) * p[i]
# P(Z | Xi) = (hit * pHit + (1 - hit) * pMiss))
# P(Xi) = p[i]

# Note: P(Xi): prior prob. that robot is at position i
# P(Z | Xi): probab of observing measurement Z if robot were at position i
# P(Z): normalized constant to make posterior a proper prob. distr.

# Returns the posterior distribution q
# Given prior distribution p and Z is a measurement the robot senses at a given point in time
def sense(p, Z):
    q = []
    for i in range(len(p)):
        hit = (Z == world[i])
        q.append(p[i] * (hit * pHit + (1 - hit) * pMiss))
    s = sum(q)
    for i in range(len(q)):
        q[i] = q[i] / s
    return q

# Robots movement are not accurate, so we model probability of robot landing exactly, undershoot and overshoot
pExact = 0.8 # P(Xi | Xj)
pOvershoot = 0.1
pUndershoot = 0.1
# Returns the post distribution q, 
# Given prior dist p and U units to the right
def move2(p, U):
    l = len(p)
    # fill list with 0
    q = [0.0] * l 
    for i in range(l):
        newPos = (i + U) % l
        q[newPos] = q[newPos] + (p[i] * pExact) # need to add prev prob if exist
        overshootPos = (i + U + 1) % l
        q[overshootPos] = q[overshootPos] + (p[i] * pOvershoot)
        undershootPos = (i + U - 1) % l
        q[undershootPos] = q[undershootPos] + (p[i] * pUndershoot)
    return q

# print(move(p, 2))

# Lecture version of move
# Move is a convolution (addition of all possibilities when shifting)
# prior: [0, 1, 2, 3, 4] 
# post: [_, _, _, X3, _]
# TOTAL PROBABILITY of X3 is prob of 2 going to X3 (exact) + prob of 2 to X3 (overshoot) + prob of 3 to X3 (undershoot)
def move(p, U):
    q = []
    for i in range(len(p)):
        # instead of finding new position to right, find the value to left
        # GET TOTAL PROB ^
        s = pExact * p[(i-U) % len(p)]
        s = s + pOvershoot * p[(i-1-U) % len(p)] # i-1 overshoot probability
        s = s + pUndershoot * p[(i+1-U) % len(p)] # i+1 undershoot probability
        q.append(s)
    return q

motion = [1, 1]
for i in range(len(motion)):
    p = sense(p, measurements[i])
    p = move(p, motion[i])

print(p)

# Perform multiple consecutive measurements
# for m in measurements:
#     p = sense(p, m)
#     print(p)