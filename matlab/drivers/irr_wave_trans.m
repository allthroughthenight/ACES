clear all
clc

%% ACES Update to MATLAB
%-------------------------------------------------------------
% Driver for Irregular Wave Transformation (page 3-2 of ACES User's 
% Guide). Yields cumulative probability distributions of wave heights as
% a field of irregular waves propagate from deep water through the surf
% zone.

% Updated by: Mary Anderson, USACE-CHL-Coastal Processes Branch
% Date Created: July 1, 2011
% Date Verified: June 8, 2012 

% Requires the following functions:
% ERRWAVBRK1
% GODA
% GODA2
% GODA3
% GODA4
% GODA5

% MAIN VARIABLE LIST:
%   INPUT
%   Ho: significant deepwater wave height
%   d: water depth
%   Ts: significant wave period
%   cotnsl: cotangent of nearshore slope
%   direc: principle direction of incident wave spectrum

%   OUTPUT
%   Hs: significant wave height
%   Hbar: mean wave height
%   Hrms: root-mean-square wave height
%   H10: average of highest 10 percent of all waves
%   H2: average of highest 2 percent of all waves
%   Hmax: maximum wave height
%   Ks: shoaling coefficient
%   psi: root-mean-square surf beat
%   Sw: wave setup
%   HoLo: deepwater wave steepness
%   Kr: effective refraction coefficient
%   doH: ratio of water depth to deepwater wave height
%   doL: relative water depth

%   OTHERS
%-------------------------------------------------------------

% Ask user if running windows or linux to set functions path
accepted = false;
while accepted == false
    linux=input('Linux or Windows? (l or w): ', 's');
    
    if strcmp('l', linux);
        accepted = true;
        linux=true;
    elseif strcmp('w', linux);
        accepted = true;
        linux=false;
    else
        fprintf('l or w only\n');
    end
end

% Set path to functions for windows or linux base on previous answer
if linux
  % Path to functions folder for linux
  functionsPath = '~/aces/matlab/functions';
else
  % Path to fucntions folder for windows
  functionsPath = strcat (getenv('USERPROFILE'), '\\Documents\\aces\\matlab\\functions');
end

% Add correct function path
addpath(functionsPath);

% Ask user for single or multi-input (from a file)
accepted = false;
single_case = '';
while accepted == false
    single_case=input('Single or Multi-case? (s or m): ', 's');
    
    if strcmp('s',single_case);
        accepted = true;
        single_case=true;
    elseif strcmp('m', single_case);
        accepted = true;
        single_case=false;
    else
        fprintf('s or m only\n');
    end
end

% Single case input
if single_case
	prompt = 'Enter Ho: significant deepwater wave height]: ';
	Ho = input(prompt);

	prompt = 'Enter d: water depth: ';
	d = input(prompt);

	prompt = 'Enter Ts: significant wave period: ';
	Ts = input(prompt);
    
    prompt = 'Enter cotnsl: cotangent of nearshore slope: ';
	cotnsl = input(prompt);
    
    prompt = 'Enter direc: principle direction of incident wave spectrum: ';
	direc = input(prompt);

else
    % TODO 
    % Default multi-case block. Eventually to be repalced with csv/tsv file
    % reader
	Ho=6.096;
    d=15.24;
    Ts=8.0;
    cotnsl=100.0;
    direc=10.0;
end

% Meter to centimeter constant
m2cm=100;

% Convert meter input to centimeters
g=9.81*m2cm;
Ho=Ho*m2cm;
d=d*m2cm;

[Hb]=ERRWAVBRK1(d,0.78);
assert(Ho<Hb,'Error: Input wave broken (Hb = %6.2f m)',Hb)

[Ks,Kr,Hmax,Hrms,Hbar,Hs,H10,H02,SBrms,HoLo,dLo,dHo,deepd,theta,Sw,Hxo,cdfo,Hx,cdfx]=GODA(Ho,d,Ts,cotnsl,direc,g);

figure(1)
plot(Hxo/m2cm,cdfo)
title('Deep Water')
xlabel('H [m]')
ylabel('CDF')

figure(2)
plot(Hx/m2cm,cdfx)
title('Subject Depth')
xlabel('H [m]')
ylabel('CDF2')

fprintf('\t\t %s \t\t %s \n','Subject','Deep')
fprintf('%s \t\t %-6.2f \t %-6.2f \n','Hs',Hs(2)/m2cm,Hs(1)/m2cm)
fprintf('%s \t %-6.2f \t %-6.2f \n','Hmean',Hbar(2)/m2cm,Hbar(1)/m2cm)
fprintf('%s \t %-6.2f \t %-6.2f \n','Hrms',Hrms(2)/m2cm,Hrms(1)/m2cm)
fprintf('%s \t %-6.2f \t %-6.2f \n','H10%',H10(2)/m2cm,H10(1)/m2cm)
fprintf('%s \t %-6.2f \t %-6.2f \n','H02%',H02(2)/m2cm,H02(1)/m2cm)
fprintf('%s \t %-6.2f \t %-6.2f \n','Hmax%',Hmax(2)/m2cm,Hmax(1)/m2cm)
disp(' ')
fprintf('%s \t\t %-6.4f \t %-6.4f \n','Ks',Ks(2),Ks(1))
fprintf('%s \t %-6.4f \t %-6.4f \n','SBrms',SBrms(2)/m2cm,SBrms(1)/m2cm)
fprintf('%s \t\t %-6.4f \t %-6.4f \n','Sw',Sw(2)/m2cm,Sw(1)/m2cm)
fprintf('%s \t %-6.4f \t %-6.4f \n','Ho/Lo',HoLo(1),HoLo(1))
fprintf('%s \t\t %-6.4f \n','Kr',Kr(1))
fprintf('%s \t %-6.4f \t %-6.4f \n','d/Ho',dHo(2),dHo(1))
fprintf('%s \t %-6.4f \t %-6.4f \n','d/Lo',dLo(2),dLo(1))




