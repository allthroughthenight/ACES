clear all
clc

%% ACES Update to MATLAB
%-------------------------------------------------------------
% Driver for Fourier Series Wave Theory (page 2-3 of ACES User's
% Guide). Yields various parameters for progressive waves of permanent
% form as predicted by Fourier series approximation. Provies estimates
% for common engineering parameters such as water surface elevation,
% integral wave properties, and kinematics as functions of wave height,
% period, water depth, and position in the wave form which is assumed to
% exist on a uniform co-flowing current.

% Updated by: Mary Anderson, USACE-CHL-Coastal Processes Branch
% Date Created: July 1, 2011
% Date Modified:

% Requires the following functions:
% ERRWAVBRK
% FWTPRE

% MAIN VARIABLE LIST:
%   INPUT
%   H: wave height
%   d: water depth
%   T: wave period
%   celdef: celerity defintion
%   u: mean velocity
%   nofour: number of terms in Fourier series
%   nosteps: number of steps in wave height ramping

%   OUTPUT
%   c: celerity
%   L: wavelength
%   eul: mean Eulerian fluid velocity
%   mass: mean mass transport velocity
%   rel2wave: mean velocity relative to wave
%   flux: volume flux
%   B: Bernoulli constant
%   I: impulse
%   Ek: kinetic energy
%   Ep: potential energy
%   Etot: energy density
%   ub: mean square of bed velocity
%   Sxx: radiation stress
%   F: wave power (energy flux)
%   Q: volume flux

%   OTHERS
%-------------------------------------------------------------

addpath('~/aces/matlab/functions'); % Path to functions folder

%must be entered in English units
H=4;
d=22;
celdef=1; %1 for Eulerian, 2 for Stokes
T=9.0;
u=0.0;
nofour=16;
nosteps=5;

g=32.2;
[Hbs]=ERRWAVBRK(H,T,0,d,0.78);l
if false
	if error==1
	    str = ['Error: Input wave broken (Hb = ',num2str(Hbs),' m)'];
	    disp(str)
	    break
	end
end
[Hnon,L,Hod,unon]=FWTPRE(g,T,H,d,u);
