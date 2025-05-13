p = [0, 1, 0, 0, 0]
n = 5
# for i in range(n):
#     p.append(0.2)

world = ['green', 'red', 'red', 'green', 'green']
measurements = ['red', 'green']
pHit = 0.6
pMiss = 0.2

# Returns the posterior distribution q
# Given prior distribution p, Z is a measurement
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
pExact = 0.8
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
def move(p, U):
    q = []
    for i in range(len(p)):
        # instead of finding new position to right, find the value to left
        s = pExact * p[(i-U) % len(p)]
        s = s + pOvershoot * p[(i-U-1) % len(p)]
        s = s + pUndershoot * p[(i-U+1) % len(p)]
        q.append(s)
    return q

for k in range(1000):
    p = move(p, 1)

print(p)

# Perform multiple consecutive measurements
# for m in measurements:
#     p = sense(p, m)
#     print(p)