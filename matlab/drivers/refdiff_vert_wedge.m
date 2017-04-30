clear all
clc

%% ACES Update to MATLAB
%-------------------------------------------------------------
% Driver for Combined Diffraction and Reflection by a Vertical Wedge
% (page 3-3 in ACES User's Guide). Estimates wave height modifcation due
% to combined diffraction and reflection near jettted harbor entrances,
% quay walls, and other such structures.

% Updated by: Mary Anderson, USACE-CHL-Coastal Processes Branch
% Date Created: April 12, 2011
% Date Verified: June 18, 2012

% Requires the following functions:
% DRWEDG
% ERRSTP
% ERRWAVBRK1
% WAVELEN

% MAIN VARIABLE LIST:
%   INPUT
%   Hi: incident wave height (m)
%   T: water period (sec)
%   d: water depth (m)
%   alpha: wave angle (deg)
%   wedgang: wedge angle (deg)
%   mode: change for single (0) or uniform grid case (1)
%   xcor: x-coordinate (m) (single case only)
%   ycor: y-coordinate (m) (single case only)
%   x0: x start coordinate (m) (grid case only)
%   xend: x end coordinate (m) (grid case only)
%   dx: x spatial increment (m) (grid case only)
%   y0: y start coordinate (m) (grid case only)
%   yend: y end coordinate (m) (grid case only)
%   dy: y spatial increment (m) (grid case only)

%   OUTPUT
%   L: wave length (m)
%   phi: modification factor (H/Hi)
%   beta: wave phase (rad)
%   H: modified wave height (m)

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

% Single case input for metric measurments
if single_case
	prompt = 'Enter Hi: incident wave height (m): ';
	Hi = input(prompt);

	prompt = 'Enter T: water period (sec): ';
	T = input(prompt);

	prompt = 'Enter d: water depth (m): ';
	d = input(prompt);
    
    prompt = 'Enter alpha: wave angle (deg): ';
	alpha = input(prompt);
    
    prompt = 'Enter wedgang: wedge angle (deg): ';
	wedgang = input(prompt); 
else
    % TODO 
    % Default multi-case block. Eventually to be repalced with csv/tsv file
    % reader
    Hi=2;
    T=8;
    d=20;
    alpha=135;
    wedgang=15;
    g=32.17;
end

assert(wedgang>=0 && wedgang<=180,'Error: Range is 0.0 to 180.0')
mode=0;
% Ask user if mode 0 single, or 1 grid
accepted = false;
while accepted == false
    mode=input('Mode 1 Single Case or Mode 2 Grid Case (1 or 2): ', 's');
    
    if strcmp('1', mode);
        accepted = true;
        mode=0;
    elseif strcmp('2', mode);
        accepted = true;
        mode=1;
    else
        fprintf('1 or 2 only\n');
    end
end

if mode==0
    % Single Point Case
    if single_case
        prompt = 'Enter xcor: x-coordinate (m): ';
        xcor = input(prompt);

        prompt = 'Enter ycor: y-coordinate (m): ';
        ycor = input(prompt);
    else
        xcor=-33;
        ycor=10;
    end

    [L,k]=WAVELEN(d,T,50,g);
    
    [steep,maxstp]=ERRSTP(Hi,d,L);
    assert(steep<maxstp,'Error: Input wave unstable (Max: %0.4f, [H/L] = %0.4f)',maxstp,steep')
    
    [Hb]=ERRWAVBRK1(d,0.78);
    assert(Hi<Hb,'Error: Input wave broken (Hb = %6.2f m)',Hb)
    
    [phi,beta,H,error]=DRWEDG(xcor,ycor,Hi,alpha,wedgang,L);
    assert(error~=1,'Error: (x,y) location inside structure.')
    
    fprintf('%s \t\t\t %6.2f \t \n','Wavelength',L);
    fprintf('%s \t %6.2f \n','Mod factor (phi)',phi);
    fprintf('%s \t\t\t %6.2f \t %s \n','Wave phase',beta,'rad');
    fprintf('%s \t %6.2f \t \n','Mod wave height',H);
    
elseif mode==1
    %Uniform Grid Case
    
    if single_case
        prompt = 'Enter x0: x start coordinate (m): ';
        x0 = input(prompt);

        prompt = 'Enter xend: x end coordinate (m): ';
        xend = input(prompt);
        
        prompt = 'Enter dx: x spatial increment (m): ';
        dx = input(prompt);
        
        prompt = 'Enter y0: y start coordinate (m): ';
        y0 = input(prompt);
        
        prompt = 'Enter yend: y end coordinate (m): ';
        yend = input(prompt);
        
        prompt = 'Enter dy: y spatial increment (m): ';
        dy = input(prompt);
    else
        x0=-800;
        xend=100;
        dx=100;
        y0=-450;
        yend=150;
        dy=50;
    end
        
    nxpt=floor((xend-x0+dx)/dx);
    
    for i=1:nxpt
        xcors(i)=(x0+(i-1)*dx);
    end
    
    nypt=floor((yend-y0+dy)/dy);
    
    for i=1:nypt
        ycors(i,1)=(y0+(i-1)*dy);
    end
    
    ycors=ycors(end:-1:1);
    
    [L,k]=WAVELEN(d,T,50,g);
    
    [steep,maxstp]=ERRSTP(Hi,d,L);
    assert(steep<maxstp,'Error: Input wave unstable (Max: %0.4f, [H/L] = %0.4f)',maxstp,steep')
    
    [Hb]=ERRWAVBRK(T,d,0,0.78,0);
    assert(Hi<Hb,'Error: Input wave broken (Hb = %6.2f m)',Hb)
    
    for i=1:nypt
        for j=1:nxpt
            xx=xcors(1,j);
            yy=ycors(i,1);
            [phi(i,j),beta(i,j),H(i,j),error]=DRWEDG(xx,yy,Hi,alpha,wedgang,L);
            assert(error~=1,'Error: (x,y) location inside structure.')
        end
    end
    
    fprintf('%s \t\t\t %6.2f \t \n','Wavelength',L);
    fprintf('%s \n','Modification Factors:')
    phi=cat(2,ycors,phi);
    xcors=[999,xcors];
    phi=cat(1,xcors,phi);
    disp(phi)
    
    fprintf('%s \n','Modified Wave Heights:');
    H=cat(2,ycors,H);
    H=cat(1,xcors,H);
    disp(H)
    
    fprintf('%s \n','Phase Angles (rad):');
    beta=cat(2,ycors,beta);
    beta=cat(1,xcors,beta);
    disp(beta)
end





