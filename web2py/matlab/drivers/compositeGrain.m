clear all
clc

%% ACES Update to MATLAB COMPOSITE GRAIN SIZE DISTRIBUTION
%-------------------------------------------------------------
% Evaluates the suitable of borrow material as beach fill and give overfill
% nourishment ratios. (Aces Tech Manual Chapter 6-3-1)

% Updated by: Yaprak Onat
% Date Created: June 21, 2016
% Date Modified: 

% Requires the following functions:


% MAIN VARIABLE LIST:
%   INPUT
%  Vol_i = initial volume (yd^3 or m^3) Range 1 to 10^8
%   M_R = Native mean (phi, mm) Range -5 to 5
%   ro_n = native standard deviation (phi) Range 0.01 to 5
%   M_b = borrow mean (phi, mm) Range -5 to 5
%   ro_b = borrow standard deviation (phi) Range 0.01 to 5
%
%   OUTPUT
%   R_A = Overfill Ratio
%   Rj = Renourishment factor
%   Vol_D = Design Volume (yd^3 or m^3)

%   OTHERS
%   g: gravity [32.17 ft/s^2]
%   rho: density of water [1.989 (salt water) or 1.94 (fresh water) slugs/ft^3]
%   rhos: density of sediment [5.14 slugs/ft^3 in FORTRAN source code]
%-------------------------------------------------------------

addpath('../functions'); % Path to functions folder

% Chose the unit of measurement 
unit = {};
 disp ('chose unit of measurement, phi, mm, ASTM')
 % write if clause for selection of the character
% Enter the data set
% edit the sample data set