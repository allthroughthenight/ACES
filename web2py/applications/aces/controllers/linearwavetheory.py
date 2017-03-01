from helper_functions import *
import json
import math

#def index():
#    return dict(message="hello world")

def index():
    form = SQLFORM.factory(
        Field('H', requires=IS_NOT_EMPTY()),
        Field('T', requires=IS_NOT_EMPTY()),
        Field('d', requires=IS_NOT_EMPTY()),
        Field('z', requires=IS_NOT_EMPTY()),
    )
    if form.process().accepted:
        redirect(URL('second', vars=dict(form.vars)))
    return dict(form=form)

def second():
    values = dict(request.vars) or redirect(URL('first'))
    return dict(lwt(values))

def lwt(input_dict):
#def lwt(H, T, d, z, xL, unitSystem):
    #internal = list(input_dict.values())
    H = int(input_dict.get('H'))
    T = int(input_dict.get('T'))
    d = int(input_dict.get('d'))
    z = int(input_dict.get('z'))
    xL = 4
    unitSystem = 'I'
    ## *********** Don't change anything here ******************
    twopi = 2 * math.pi
    nIteration = 50
    if unitSystem == 'I': # imperial
        g = 32.17 # gravitational acceleration (ft/sec^2)
        rho = 1.989 # rho/g = 63.99/32.17 lb sec^2/ft^4 (sea water)
    elif unitSystem == 'M': # metric
        rho = 1025.09
        g = 9.81

    L, k = wavelen(d, T, nIteration, g)

    theta =  xL * twopi # theta=(kx-wt) where arbitrarily t=0 and k=2*pi/L

    '''
    # Check for monochromatic wave breaking (depth limited - no slope)
    Hb = errwavbrk1(d, 0.78)
    if (H >= Hb):
        print("Error: Input wave broken (Hb = %6.2f m)" % Hb)
        return

    # Check to make sure vertical coordinate is within waveform
    eta = (H / 2) * math.cos(theta)
    if not (z < eta and (z + d) > 0):
        print("Error: Point outside waveform.")
        return
        '''

    # Main computations
    arg = (2 * k * d / (math.sinh(2 * k * d)))
    tot = d + z

    C = L / T
    Cg = 0.5 * (1 + arg) * C
    # come back to this - check math when multiplying (1 / 8) * ...
    E = rho * g * (H**2) / 8
    Ef = E * Cg
    Ur = L**2 * H / (d**3)
    px = (-H / 2) * (math.cosh(k * tot) / math.sinh( k * d)) * math.sin(theta)
    py = ( H / 2) * (math.sinh(k * tot) / math.sinh(k * d)) * math.cos(theta)
    u = (H * math.pi / T) * (math.cosh(k * tot) / math.sinh( k * d)) * math.cos(theta)
    w = (H * math.pi / T) * (math.sinh(k * tot) / math.sinh(k * d)) * math.sin(theta)
    dudt = (H * 2 * math.pi**2 / (T**2)) * (math.cosh(k * tot) / math.sinh(k * d)) * math.sin(theta)
    dwdt = (-H * 2 * math.pi**2 / (T**2)) * (math.sinh(k * tot) / math.sinh(k * d)) * math.cos(theta)
    pres = -rho * g * z + rho * g * (H / 2) * (math.cosh(k * tot) / math.cosh(k * d)) * math.cos(theta)
    # come back to this!!! supposed to be py rather than pz??
    pz = 0

    localVars = locals()
    return dict(localVars=localVars)
    #return H, T, d, z, xL, L, C, Cg, E, Ef, Ur, eta, px, py, pz, u, w, dudt, dwdt, pres

    ''' plotting waveform
    t = np.arange(-1, 1, 0.001)
    plottheta = t * np.pi * 2

    ploteta = (H / 2) * np.cos(plottheta)
    plotu = (H * np.pi / T) * (np.cosh(k * tot) / np.sinh(k * d)) * np.cos(plottheta)
    plotw = (H * np.pi / T) * (np.sinh(k * tot) / np.sinh(k * d)) * np.sin(plottheta)

    plt.subplot(3, 1, 1)
    plt.plot(t, ploteta, lw=2)
    plt.ylabel('Elevation [m]')
    plt.ylim(-4, 4)
    plt.axhline(color = 'r', linestyle = '--')

    # subplot
    plt.subplot(3, 1, 2)
    plt.plot(t, plotu, lw=2)
    plt.axhline(color = 'r', linestyle = '--')
    plt.ylabel('Velocity, u [m/s]')
    plt.ylim(-2, 2)

    # subplot
    plt.subplot(3, 1, 3)
    plt.plot(t, plotw, lw=2)
    plt.axhline(color = 'r', linestyle = '--')
    plt.ylabel('Velocity, w [m/s]')
    plt.ylim(-1, 1)

    plt.tight_layout(pad=0.4)

    plt.show() '''


class LinearWaveTheoryOutput:
    # Default INPUT
    H = 6.30
    T = 8
    d = 20.0
    z = -12.0
    xL = 0.75

    # OUTPUT
    L = 0
    C = 0
    Cg = 0
    E = 0
    Ef = 0
    Ur = 0
    eta = 0
    px = 0
    # missing py from matlab documentation
    py = 0
    pz = 0
    u = 0
    w = 0
    dudt = 0
    dwdt = 0
    pres = 0

    def __init__(self): pass

    def toString(self):
        print("\t\t\t\t\t %s \n" % ("Units"))
        print("%s \t\t %-6.2f \t %s \n" % ("Wavelength", self.L, "m"))
        print("%s \t\t %-6.2f \t %s \n" % ("Celerity", self.C, "m/s"))
        print("%s \t\t %-6.2f \t %s \n" % ("Group speed", self.Cg, "m/s"))
        print("%s \t\t %-8.2f \t %s \n" % ("Energy density", self.E, "N-m/m^2"))
        print("%s \t\t %-8.2f \t %s \n" % ("Energy flux", self.Ef, "N-m/m-s"))
        print("%s \t\t %-6.2f \n" % ("Ursell number", self.Ur))
        print("%s \t\t %-6.2f \t %s \n" % ("Elevation", self.eta, "m"))
        print("%s \t %-6.2f \t %s \n" % ("Horz. displacement", self.px, "m"))
        print("%s \t %-6.2f \t %s \n" % ("Vert. displacement", self.py, "m"))
        print("%s \t\t %-6.2f \t %s \n" % ("Horz. velocity", self.u, "m/s"))
        print("%s \t\t %-6.2f \t %s \n" % ("Vert. velocity", self.w,"m/s"))
        print("%s \t %-6.2f \t %s \n" % ("Horz. acceleration", self.dudt, "m/s^2"))
        print("%s \t %-6.2f \t %s \n" % ("Vert. acceleration", self.dwdt, "m/s^2"))
        print("%s \t\t %-8.2f \t %s \n" % ("Pressure", self.pres, "N/m^2"))
