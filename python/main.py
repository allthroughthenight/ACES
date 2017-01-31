# from snells_law import *
from linear_wave_theory import *

def main():
    # temp = SnellOutput()
    # temp = snellsLaw(6, 10, 18, 6, 100, 13)
    # temp.toString()
    temp = LinearWaveTheoryOutput()
    temp = linearWaveTheory(6.30, 8, 20.0, -12.0, 0.75)
    temp.toString()

main()
