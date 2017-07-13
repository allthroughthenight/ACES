# Fully developed wave growth estimates

#   INPUT
#   u: wind velocity
#   g: gravitational acceleration

#   OUTPUT
#   Hfd: duration-limited wave height
#   Tfd: duration-limited wave period

def WGFD(u, g):
    Hfd = 0.2433*(u**2/g)
    Tfd = 8.134*(u/g)

    return Hfd, Tfd