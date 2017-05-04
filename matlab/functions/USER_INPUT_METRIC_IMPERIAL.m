function [ metric, g ] = USER_INPUT_METRIC_IMPERIAL()
%USER_INPUT_METRIC_IMPERIAL
%   Prompt the user to select metric or imperial units
% Return Values
%   metric - true if using metric units, false if using imperial
%   g - the gravitational constant appropriate to the units

accepted = false;
metric = '';
while accepted == false
    metric=input('Input in imperial or SI units? (I or S): ', 's');

    if strcmp('I', metric);
        accepted = true;
        metric=false;
        
        % Gravitational acceleration constant in feet per second^2
        g=32.17;
    elseif strcmp('S', metric);
        accepted = true;
        metric=true;
        
        % Gravitational acceleration constant in m per second^2
        g=9.81;
    else
        fprintf('I or S only\n');
    end
end

end

