% Transmitted wave height by overtopping of an impermebale structure

%   INPUT
%   bb: structure crest width
%   H: total structure height above sea floor
%   R: wave runup
%   H: incident wave height
%   free: freeboard (difference between height of structure and still water
%   depth at structure)

%   OUTPUT
%   Ht: transmitted wave height

function [Ht]=HTP(bb,hs,R,H,free)

c=0.51-0.11*(bb/hs);

Kt=c*(1-(free/R));

if Kt<0
    Kt=0.0;
end

Ht=Kt*H;
end