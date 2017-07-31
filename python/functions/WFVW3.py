import math

def WFVW3(N, x, y):
    eps = 1.0 * 10**(-6)
    nn = N - 1
    s = [0.0 for i in range(N)]
    g = [0.0 for i in range(nn)]
    work = [0.0 for i in range(nn)]

    for i in range(1, nn):
        xi = x[i]
        xim1 = x[i - 1]
        xip1 = x[i + 1]
        yi = y[i]
        yim1 = y[i - 1]
        yip1 = y[i + 1]
        xx = xi - xim1
        h = xip1 - xim1
        work[i] = 0.5 * xx / h
        T = ((yip1 - yi) / (xip1 - xi) - (yi - yim1) / xx) / h
        s[i] = 2.0 * T
        g[i] = 3.0 * T

    w = 8.0 - 4.0 * math.sqrt(3)

    u = 100.0
    while u > eps:
        u = 0.0
        for i in range(1, nn):
            T = w * (-s[i] - work[i] * s[i - 1] - (0.5 - work[i]) * s[i + 1] + g[i])
            h = abs(T)
            if h > u:
                u = h
            s[i] = s[i] + T

    inte = 0.0
    for i in range(nn):
        h = x[i + 1] - x[i]
        inte = (inte + 0.5 * h * (y[i] + y[i + 1])) - (1.0 / 24.0 * h**3 * (s[i] + s[i + 1]))

    return inte