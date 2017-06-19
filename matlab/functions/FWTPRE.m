function [Hnon,L,Hoverd,unon, deptyp]=FWTPRE(g,T,H,d,u)
 %   Convert the dimensional input data into the required nondimensional forms
    % H is wave height
    % T is wave period
    % d is water depth
    % u is mean velocity 
    % finite deep water type
Hnon=H/(g*T^2); % Dimensionless wave height
L=((g*T^2)/(2*pi))*sqrt(tanh(1.22718*d/T^2)); %determine an approximate wavelength

%  Set to deepwater if (d/L) > 3/2 (to prevent cosh(kd) overflows):
if d/L>1.5
    Hoverd=0.0;
    deptyp = 1;
else
    Hoverd=H/d;
    deptyp = 2;
end

unon=u/sqrt(g*H); %Dimensionless mean velocity 
