R0 = 100.0
A = 3.9083e-3
B = -5.775e-7
C = -4.183e-12

def R2C(R):
    if R >= 100.0:
        return (-R0*A
                +(R0**2 * A**2
                  - 4 * R0 * B * (R0 - R))**0.5)\
               /(2*R0*B)

def C2R(C):
    if C >= 0.0:
        return R0 * (1 + A * C + B * C**2)


