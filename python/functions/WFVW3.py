import math

def WFVW3(N, x, y):

    eps = 1 * 10**(-6)
    nn = N - 1
    s[1] = 0
    s[N] = 0

    for i in range(2, nn):
        xi = x(i)
        xim1 = x(i - 1)
        xip1 = x(i + 1)
        yi = y(i)
        yim1 = y(i - 1)
        yip1 = y(i + 1)
        xx = xi - xim1
        h = xip1 - xim1
        work[i] = 0.5 * xx / h
        T = ((yip1 - yi) / (xip1 - xi) - (yi - yim1) / xx) / h
        s[i] = 2 * T
        g[i] = 3 * T

    w = 8 - 4 * math.sqrt(3)

    u = 100
    while u > eps:
        u = 0
        for i in range(2, nn):
            T = w * (-s[i] - work[i] * s[i - 1] - (0.5 - work[i]) * s[i + 1] + g[i])
            h = math.fabs(T)
            if h > u:
                u = h
            s[i] = s[i] + T

    inte = 0
    for i in range (1, nn):
        h = x[i + 1] - x[i]
        inte = (inte + 0.5 * h * (y[i] + y[i + 1])) - (1 / 24 * h**3 * (s[i] + s[i + 1]))

    return inte
