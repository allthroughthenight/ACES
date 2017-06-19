function [ sol, z, cosa, sina ] = FWTSOL( dpi, Hoverd, Hnon, unon, number, num, n , deptyp, celdef)
%determine initial solution from linear wave theory
% INPUTS
% dpi:
% Hoverd:
% Hnon:
% unon
% number: 9
% num:
% n

% 
% OUTPUTS
% sol, z 


if deptyp==2
    a = 4 * (dpi^2) * Hnon/Hoverd;
    b = a / sqrt(tanh(a));
    t = tanh(b);
    z(1) = b + (a-b*t)/(t+b*(1 -t^2));
    z(2) = z(1) * Hoverd;
    z(4) = sqrt(tanh(z(1)));
else 
    z(1) = -1.0;
    z(2) = 4 * (dpi^2) * Hnon;
    z(4) = 1.0;
end

z(3) = 2. * dpi / z(4);

if celdef == 1
    z(5) = unon * sqrt(z(2));
    z(6) = 0;
else
    z(6) = unon * sqrt(z(2));
    z(5) = 0;
end

z(7)    = z(4);
z(8)    = 0;
z(9)    = 0.5 * z(7)^2;
% cosa(0) = 1.0;
% sina(0) = 0;
cosa(1) = 1.0;
sina(1) = 0;
z(10)   = 0.5 * z(2);

% for i = 1:n
%     cosa(i)   = cos(i * dpi/n);
%     cosa(i+n) = cos( (i+n) * dpi/n);
%     sina(i)   = sin(i * dpi/n);
%     sina(i+n) = sin( (i+n) * dpi/n);
%     z(n+i+10) = 0;
%     z(i + 10) = 0.5 * z(2) * cosa(i);
% end
for i = 1:n
    cosa(i+1)   = cos(i * dpi/n);
    cosa(i+n+1) = cos( (i+n) * dpi/n);
    sina(i+1)   = sin(i * dpi/n);
    sina(i+n+1) = sin( (i+n) * dpi/n);
    z(n+i+10) = 0;
    z(i + 10) = 0.5 * z(2) * cosa(i+1);
end

z(n+11) = 0.5 * z(2)/z(7);
for i = 1:number
    sol(i,1) = z(i);
end

sol(i,2) = 0;

for i = 10:num
    sol(i,1) = 0;
end

end

