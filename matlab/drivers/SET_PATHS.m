function [] = SET_PATHS()
%SET_PATHS
%   Set additional paths needed by the drivers.

driversDir = pwd();
parentDir = fileparts(driversDir);

% Set path to functions for windows or linux base on previous answer
if isunix
  % Path to functions folder for linux
  functionsPath = '~/aces/matlab/functions';
else
  % Path to fucntions folder for windows
  functionsPath = [parentDir '\\functions'];
end

% Add correct function path
addpath(functionsPath);

end

