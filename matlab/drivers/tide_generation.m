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


SET_PATHS();

[metric, g, labelUnitDist, labelUnitWt] = USER_INPUT_METRIC_IMPERIAL();

inputDataList = {...
    'year simulation starts (YYYY)', 1900, 2050;...
    'month simulation starts (MM)', 1, 12;...
    'day simulation starts (DD)', 1, 31;...
    'hour simulation starts (HH.H)', 0, 24;...
    'length of record (tlhrs) (HH.H)', 0, 744;...
    'output time interval (min)', 1, 60;...
    ['mean water level height above datum [' labelUnitDist ']'], -100, 100;...
    'gauge longitude (deg)', -180, 180};
[outputDataList] = USER_INPUT_FILE_INPUT_SINGLE(inputDataList);

year = outputDataList(1);
mon = outputDataList(2);
day = outputDataList(3);
hr = outputDataList(4);
tlhrs = outputDataList(5);
delt = outputDataList(6);
gauge0 = outputDataList(7);
glong = outputDataList(8);


accepted = false;
while ~accepted
    fprintf('\nConstituent Data Loading from file\n');
    [constituentFilename] = USER_INPUT_FILE_NAME();

    fid = fopen(constituentFilename);
    C = textscan(fid, '%s %f %f');
    fclose(fid);

    if length(C{2}) == 0 || length(C{3}) == 0
        fprintf('ERROR: Constituent Data Incomplete.\n');
        fprintf('Please correct the input file and try again.\n');
    else
        accepted = true;
    end
end

cst=C{1};
amp=C{2};
ep=C{3};


delthr=delt/60;

%prompt = 'Enter total number of gauges: ';
% nogauge=input(prompt);
nogauge = 1; % one gauge is examined.

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
ylabel(['Elevation [' labelUnitDist ']']) %output same units as amplitude, datum input

% File Output
fileOutputArgs = {'Enter the description for this file: '};
[fileOutputData] = USER_INPUT_FILE_OUTPUT(fileOutputArgs);

if fileOutputData{1}
    fId = fopen('output/tide_generation.txt', 'wt');

    fprintf(fId, 'CONSTITUENT TIDE ELEVATION RECORD\n');
    fprintf(fId, '%s\n', fileOutputData{2});
    fprintf(fId, 'TIME\tELEVATION\n');

    for loopIndex = 1:length(xtim)
        fprintf(fId, '%-6.2f\t%-6.2f\n',...
            xtim(loopIndex),...
            ytide(loopIndex));
    end

    fclose(fId);
end
