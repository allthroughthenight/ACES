function [ water, rho ] = USER_INPUT_SALT_FRESH_WATER(metric)
%USER_INPUT_SALT_FRESH_WATER
%   Detailed explanation goes here

accepted = false;
water = '';
while accepted == false
    water=input('Fresh or Salt water? (F or S): ', 's');
    
    if strcmp('S', water);
        accepted = true;
        water='S';
        
        if metric
            rho = 1025.09; % kg/m^3, (sea water)
        else
            rho = 1.989; % rho/g = 63.99/32.17 lb sec^2/ft^4 (sea water)
        end
    elseif strcmp('F', water);
        accepted = true;
        water='F';
        
        if metric
            rho = 999.8; % kg/m^3 ( fresh water)
        else
            rho = 1.940; % rho/g = 62.415475/32.17 lb sec^2/ft^4 (fresh water)
        end
    else
        fprintf('F or S only\n');
    end
end

end

