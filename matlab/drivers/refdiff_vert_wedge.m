clear all
clc

%% ACES Update to MATLAB
%-------------------------------------------------------------
% Driver for Combined Diffraction and Reflection by a Vertical Wedge
% (page 3-3 in ACES User's Guide). Estimates wave height modification due
% to combined diffraction and reflection near jetted harbor entrances,
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

SET_PATHS();

[single_case] = USER_INPUT_SINGLE_MULTI_CASE();

[metric, g] = USER_INPUT_METRIC_IMPERIAL();

% Single case input for metric measurments
if single_case
    if metric
        [Hi] = USER_INPUT_DATA_VALUE('Enter Hi: incident wave height (m): ', 0.1, 200);
    else
        [Hi] = USER_INPUT_DATA_VALUE('Enter Hi: incident wave height (ft): ', 0.1, 200);
    end

    [T] = USER_INPUT_DATA_VALUE('Enter T: water period (sec): ', 1, 1000);

    if metric
        [d] = USER_INPUT_DATA_VALUE('Enter d: water depth (m): ', 0.01, 5000);
    else
        [d] = USER_INPUT_DATA_VALUE('Enter d: water depth (ft): ', 0.01, 5000);
    end
    
    [alpha] = USER_INPUT_DATA_VALUE('Enter alpha: wave angle (deg): ', 0, 180);
    
    [wedgang] = USER_INPUT_DATA_VALUE('Enter wedgang: wedge angle (deg): ', 0, 180);
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
        if metric
            [xcor] = USER_INPUT_DATA_VALUE('Enter xcor: x-coordinate (m): ', -5280, 5280);
        else
            [xcor] = USER_INPUT_DATA_VALUE('Enter xcor: x-coordinate (ft): ', -5280, 5280);
        end

        if metric
            [ycor] = USER_INPUT_DATA_VALUE('Enter ycor: y-coordinate (m): ', -5280, 5280);
        else
            [ycor] = USER_INPUT_DATA_VALUE('Enter ycor: y-coordinate (ft): ', -5280, 5280);
        end
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
        if metric
            [x0] = USER_INPUT_DATA_VALUE('Enter x0: x start coordinate (m): ', -5280, 5280);
        else
            [x0] = USER_INPUT_DATA_VALUE('Enter x0: x start coordinate (ft): ', -5280, 5280);
        end

        if metric
            [xend] = USER_INPUT_DATA_VALUE('Enter xend: x end coordinate (m): ', -5280, 5280);
        else
            [xend] = USER_INPUT_DATA_VALUE('Enter xend: x end coordinate (ft): ', -5280, 5280);
        end
        
        if metric
            [dx] = USER_INPUT_DATA_VALUE('Enter dx: x spatial increment (m): ', 0.1, 5280);
        else
            [dx] = USER_INPUT_DATA_VALUE('Enter dx: x spatial increment (ft): ', 0.1, 5280);
        end
        
        if metric
            [y0] = USER_INPUT_DATA_VALUE('Enter y0: y start coordinate (m): ', -5280, 5280);
        else
            [y0] = USER_INPUT_DATA_VALUE('Enter y0: y start coordinate (ft): ', -5280, 5280);
        end
        
        if metric
            [yend] = USER_INPUT_DATA_VALUE('Enter yend: y end coordinate (m): ', -5280, 5280);
        else
            [yend] = USER_INPUT_DATA_VALUE('Enter yend: y end coordinate (ft): ', -5280, 5280);
        end
        
        if metric
            [dy] = USER_INPUT_DATA_VALUE('Enter dy: y spatial increment (m): ', 0.1, 5280);
        else
            [dy] = USER_INPUT_DATA_VALUE('Enter dy: y spatial increment (ft): ', 0.1, 5280);
        end
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





