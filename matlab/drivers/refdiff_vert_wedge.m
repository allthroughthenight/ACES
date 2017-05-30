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

[metric, g, rho, labelUnitDist, labelUnitWt] = USER_INPUT_METRIC_IMPERIAL();

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

% Single case input for metric measurments
if single_case
    [Hi] = USER_INPUT_DATA_VALUE(['Enter Hi: incident wave height (' labelUnitDist '): '], 0.1, 200);

    [T] = USER_INPUT_DATA_VALUE('Enter T: water period (sec): ', 1, 1000);

    [d] = USER_INPUT_DATA_VALUE(['Enter d: water depth (' labelUnitDist '): '], 0.01, 5000);
    
    [alpha] = USER_INPUT_DATA_VALUE('Enter alpha: wave angle (deg): ', 0, 180);
    
    [wedgang] = USER_INPUT_DATA_VALUE('Enter wedgang: wedge angle (deg): ', 0, 180);
    
    if mode == 0
        [xcor] = USER_INPUT_DATA_VALUE(['Enter xcor: x-coordinate (' labelUnitDist '): '], -5280, 5280);

        [ycor] = USER_INPUT_DATA_VALUE(['Enter ycor: y-coordinate (' labelUnitDist '): '], -5280, 5280);
    else
        [x0] = USER_INPUT_DATA_VALUE(['Enter x0: x start coordinate (' labelUnitDist '): '], -5280, 5280);

        [xend] = USER_INPUT_DATA_VALUE(['Enter xend: x end coordinate (' labelUnitDist '): '], -5280, 5280);

        [dx] = USER_INPUT_DATA_VALUE(['Enter dx: x spatial increment (' labelUnitDist '): '], 0.1, 5280);

        [y0] = USER_INPUT_DATA_VALUE(['Enter y0: y start coordinate (' labelUnitDist '): '], -5280, 5280);

        [yend] = USER_INPUT_DATA_VALUE(['Enter yend: y end coordinate (' labelUnitDist '): '], -5280, 5280);

        [dy] = USER_INPUT_DATA_VALUE(['Enter dy: y spatial increment (' labelUnitDist '): '], 0.1, 5280);
    end
    
    numCases = 1;
else
    multiCaseData = {...
        ['Hi: incident wave height (' labelUnitDist ')'], 0.1, 200;...
        'T: water period (sec)', 1, 1000;...
        ['d: water depth (' labelUnitDist ')'], 0.01, 5000;...
        'alpha: wave angle (deg)', 0, 180;...
        'wedgang: wedge angle (deg)', 0, 180};
    
    if mode == 0
        multiCaseData = [multiCaseData;...
            {['xcor: x-coordinate (' labelUnitDist ')'], -5280, 5280;...
            ['ycor: y-coordinate (' labelUnitDist ')'], -5280, 5280}];
    else
        multiCaseData = [multiCaseData;...
            {['x0: x start coordinate (' labelUnitDist '): '], -5280, 5280;...
            ['xend: x end coordinate (' labelUnitDist '): '], -5280, 5280;...
            ['dx: x spatial increment (' labelUnitDist '): '], 0.1, 5280;...
            ['y0: y start coordinate (' labelUnitDist '): '], -5280, 5280;...
            ['yend: y end coordinate (' labelUnitDist '): '], -5280, 5280;...
            ['dy: y spatial increment (' labelUnitDist '): '], 0.1, 5280}];
    end
    
    [varData, numCases] = USER_INPUT_MULTI_MODE(multiCaseData);
    
    HiList = varData(1, :);
    TList = varData(2, :);
    dList = varData(3, :);
    alphaList = varData(4, :);
    wedgangList = varData(5, :);
    
    if mode == 0
        xcorList = varData(6, :);
        ycorList = varData(7, :);
    else
        x0List = varData(6, :);
        xendList = varData(7, :);
        dxList = varData(8, :);
        y0List = varData(9, :);
        yendList = varData(10, :);
        dyList = varData(11, :);
    end
end

for loopIndex = 1:numCases
    if ~single_case
        Hi = HiList(loopIndex);
        T = TList(loopIndex);
        d = dList(loopIndex);
        alpha = alphaList(loopIndex);
        wedgang = wedgangList(loopIndex);
        
        if mode == 0
            xcor = xcorList(loopIndex);
            ycor = ycorList(loopIndex);
        else
            x0 = x0List(loopIndex);
            xend = xendList(loopIndex);
            dx = dxList(loopIndex);
            y0 = y0List(loopIndex);
            yend = yendList(loopIndex);
            dy = dyList(loopIndex);
        end
    end
    
    assert(wedgang>=0 && wedgang<=180,'Error: Range is 0.0 to 180.0')

    % Single Point Case
    if mode==0
        [L,k]=WAVELEN(d,T,50,g);

        [steep,maxstp]=ERRSTP(Hi,d,L);
        assert(steep<maxstp,'Error: Input wave unstable (Max: %0.4f, [H/L] = %0.4f)',maxstp,steep')

        [Hb]=ERRWAVBRK1(d,0.78);
        assert(Hi<Hb,'Error: Input wave broken (Hb = %6.2f m)',Hb)

        [phi,beta,H,error]=DRWEDG(xcor,ycor,Hi,alpha,wedgang,L);
        assert(error~=1,'Error: (x,y) location inside structure.')

        fprintf('%s \t\t\t %6.2f \t %s \n','Wavelength',L,labelUnitDist);
        fprintf('%s \t %6.2f \n','Mod factor (phi)',phi);
        fprintf('%s \t\t\t %6.2f \t %s \n','Wave phase',beta,'rad');
        fprintf('%s \t %6.2f \t %s \n','Mod wave height',H,labelUnitDist);

    %Uniform Grid Case
    elseif mode==1
        xcors = [];
        nxpt=floor((xend-x0+dx)/dx);

        for i=1:nxpt
            xcors(i)=(x0+(i-1)*dx);
        end

        ycors = [];
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

        phi = [];
        beta = [];
        H = [];
        for i=1:nypt
            for j=1:nxpt
                xx=xcors(1,j);
                yy=ycors(i,1);
                [phi(i,j),beta(i,j),H(i,j),error]=DRWEDG(xx,yy,Hi,alpha,wedgang,L);
                assert(error~=1,'Error: (x,y) location inside structure.')
            end
        end

        fprintf('%s \t\t\t %6.2f \t %s \n','Wavelength',L,labelUnitDist);
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
end