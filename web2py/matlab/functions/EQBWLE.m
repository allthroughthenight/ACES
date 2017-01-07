% Transforms trapezoidal breakwater into a hydraulically equivalent
% rectangular breakwater

%   INPUT
%   rechd: head difference across equivalent rectangular breakwater
%   traphd: head difference across trapezoidal breakwater
%   d: water depth
%   nummat: number of materials in the breakwater
%   numlay: number of layers in the breakwater
%   diam: mean diameter of material in the breakwater
%   por: porosity of the various materials
%   thk: thickness of each layer
%   len: length of each material in the breakwater
%   pref: porosity of reference material (0.435)
%   dref: one half mean diameter of reference material

%   OUTPUT
%   lequiv: equivalent length of rectangular breakwater

%   OTHER:
%   betar and beta: turbulent resistance coefficients for the equivalent
%                   and trapezoidal breakwater

function [lequiv]=EQBWLE(rechd,traphd,d,nummat,numlay,diam,por,thk,len,pref,dref)

    % find betar and beta
    beta0=2.7;
    betar=beta0*((1-pref)/(pref^3*dref));

    for i=1:nummat
        beta(i)=beta0*((1-por(i))/(por(i)^3*diam(i)));
    end

    % find equivalent rectangular breakwater length
    for j=1:numlay %layer is columns
        for k=1:nummat % material number is rows
            ind(k)=(beta(k)/betar)*len(k,j);
        end
        sum1=sum(ind);
        ind2(j)=(thk(j)/d)/sqrt(sum1);
    end
        sum2=sum(ind2);
        lequiv=1/sum2^2*(rechd/traphd);
end
    


        