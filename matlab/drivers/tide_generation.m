clear all
clc

%% ACES Update to MATLAB
%-------------------------------------------------------------
% Driver for Constituent Tide Record Generation (page 1-4 in ACES User's Guide)
% Provides a tide elevation record at a specific time and locale using
% known amplitudes and epochs for individual harmonic constiuents

% Updated by: Mary Anderson, USACE-CHL-Coastal Processes Branch
% Date Transferred: April 11, 2011
% Date Verified: May 30, 2012

% Requires the following functions:
% ANG360
% DAYOYR
% GAGINI
% GTERMS
% NFACS
% ORBIT
% TIDELV

% MAIN VARIABLE LIST:
%   INPUT
%   year: year simulation starts
%   mon: month simulation starts
%   day: day simulation starts
%   hr: hr simulation starts
%   tlhrs: length of record (hr)
%   nogauge: total number of gauges (default=1)
%   ng: gauge of interest (default=1)
%   glong: gauge longitude (deg)
%   delt: output time interval (min)
%   gauge0: mean water level height above datum
%   cst: constituents name (read-in from file called tides.txt)
%   amp: amplitdutes of constituents (m, read-in from file)
%   ep: epochs of constituents (read-in from file)
%   requires constituent data entry in tides.txt

%   OUTPUT
%   ytide: tidal surface elevations

%   OTHERS
%   dayj: Julian day of the year (1-365/366 if leap year)
%   alpha: angular arguments for constiuents (deg)
%   fndcst: node factors for constiuents (deg)
%   eqcst: Greenwhich equlibrium arguments for constituents (deg)
%   acst: orbital speeds of constituents (deg/hr)
%   pcst: number of tide cycles per day per constiuent
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

accepted = false;
metric = '';
while accepted == false
    metric=input('Input in feet or meters? (f or m): ', 's');
    
    if strcmp('f', metric);
        accepted = true;
        metric=false;
    elseif strcmp('m', metric);
        accepted = true;
        metric=true;
    else
        fprintf('f or m only\n');
    end
end

if single_case && strcmp('m', metric)
	prompt = 'Enter year simulation starts (YYYY): ';
	year=input(prompt);

	prompt = 'Enter month simulation starts (MM): ';
	month=input(prompt);

	prompt = 'Enter day simulation starts (DD): ';
	day=input(prompt);

	prompt = 'Enter hour simulation starts (HH.H): ';
	hr=input(prompt);

	prompt = 'Enter length of record (tlhrs) (HH.H): ';
	tlhrs=input(prompt);

	prompt = 'Enter total number of gauges: ';
	nogauge=input(prompt);

	prompt = 'Enter gauge longitude (deg): ';
	glong=input(prompt);

	prompt = 'Enter output time interval (min): ';
	delt=input(prompt);

	prompt = 'Enter mean water level height above datum [m]: ';
	gauge0=input(prompt);
elseif single_case && strcmp('f', metric)
	prompt = 'Enter year simulation starts (YYYY): ';
	year=input(prompt);

	prompt = 'Enter month simulation starts (MM): ';
	month=input(prompt);

	prompt = 'Enter day simulation starts (DD): ';
	day=input(prompt);

	prompt = 'Enter hour simulation starts (HH.H): ';
	hr=input(prompt);

	prompt = 'Enter length of record (tlhrs) (HH.H): ';
	tlhrs=input(prompt);

	prompt = 'Enter total number of gauges: ';
	nogauge=input(prompt);

	prompt = 'Enter gauge longitude (deg): ';
	glong=input(prompt);

	prompt = 'Enter output time interval (min): ';
	delt=input(prompt);

	prompt = 'Enter mean water level height above datum [ft]: ';
	gauge0=input(prompt);
else
    % TODO 
    % Default multi-case block. Eventually to be repalced with csv/tsv file
    % reader
	year=1990;
	mon=12;
	day=20;
	hr=10.0;
	tlhrs=24.0;
	nogauge=1;
	glong=40.00;
	delt=15.0;
	gauge0=0.0;
end

% Meters to feet constant for convertion
m2ft=3.28084;

% Convert feet input to meters based if input is in feet
if strcmp('m', metric);
    gauge0 = gauge0*m2ft;
end

delthr=delt/60;

fid = fopen('tides.txt');
C = textscan(fid, '%s %f %f');
fclose(fid);

cst=C{1};
amp=C{2};
ep=C{3};

acst=[28.9841042,30.0,28.4397295,15.0410686,57.9682084,...
     13.9430356,86.9523127,44.0251729,60.0,57.4238337,28.5125831,90.0,...
     27.9682084,27.8953548,16.1391017,29.4556253,15.0,14.4966939,...
     15.5854433,0.5443747,0.0821373,0.0410686,1.0158958,1.0980331,...
     13.4715145,13.3986609,29.9589333,30.0410667,12.8542862,14.9589314,...
     31.0158958,43.4761563,29.5284789,42.9271398,30.0821373,...
     115.9364169,58.9841042];

pcst=[2,2,2,1,4,1,6,3,4,4,2,6,2,2,1,2,1,1,1,0,0,0,0,0,1,1,2,2,1,1,2,3,2,3,2,8,4];

%% Intialize gage-specific info relevant to harmonic constituents
[alpha,fndcst]=GAGINI(nogauge,year,mon,day,hr,tlhrs,glong,ep,acst,pcst);

ntid=floor(tlhrs/delthr)+1;

for i=1:ntid
    xtim(i)=(i-1)*delthr;
    [tidelv(i)]=TIDELV(nogauge,xtim(i),amp,alpha,fndcst,acst);
end

ytide=gauge0+tidelv;

figure(1)
title('Tide Elevations [from constituents]')
plot(xtim,ytide)
xlabel('Time [hr]')
ylabel('Elevation [ft]') %output same units as amplitude, datum input


