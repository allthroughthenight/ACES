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

SET_PATHS();

[metric, g, rho, labelUnitDist, labelUnitWt] = USER_INPUT_METRIC_IMPERIAL();

[H] = USER_INPUT_DATA_VALUE(['Enter H: wave height (' labelUnitDist '): '], 0.1, 200.0);

[T] = USER_INPUT_DATA_VALUE('Enter T: wave period (s): ', 1.0, 1000.0);

[d] = USER_INPUT_DATA_VALUE(['Enter d: water depth (' labelUnitDist '): '], 0.1, 5000.0);

[celdef] = USER_INPUT_FINITE_CHOICE('Enter celdef: celerity definition (1 for Euler, 2 for Stokes): ', {'1', '2'});

[u] = USER_INPUT_DATA_VALUE(['Enter u: mean velocity (' labelUnitDist 'ps): '], 1.0, 10.0);

[nofour] = USER_INPUT_DATA_VALUE('Enter nofour: the number of terms in Fourier Series: ', 1, 25);

[nosteps] = USER_INPUT_DATA_VALUE('Enter nosteps: the number of steps in Wave Height ramping: ', 1, 10);


[Hbs]=ERRWAVBRK(H,T,0,d,0.78);
if false
	if error==1
	    str = ['Error: Input wave broken (Hb = ',num2str(Hbs),' m)'];
	    disp(str)
	end
end
[Hnon,L,Hod,unon]=FWTPRE(g,T,H,d,u);



% File Output
fileOutputArgs = {};
[fileOutputData] = USER_INPUT_FILE_OUTPUT(fileOutputArgs);

if fileOutputData{1}
    fId = fopen('output/fourier.txt', 'wt');

    fprintf(fId, 'Partial Listing of Plot Output File 1\n\n');
    
    fprintf(fId, 'Section 1 of the plot output file 1\n\n');
    
    fprintf(fId, 'Section 2 of the plot output file 2\n\n');

    fclose(fId);
end