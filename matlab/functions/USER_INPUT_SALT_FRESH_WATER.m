function [ water ] = USER_INPUT_SALT_FRESH_WATER()
%USER_INPUT_SALT_FRESH_WATER
%   Detailed explanation goes here

accepted = false;
water = '';
while accepted == false
    water=input('Fresh or Salt water? (F or S): ', 's');
    
    if strcmp('S', water);
        accepted = true;
        water='S';
    elseif strcmp('F', water);
        accepted = true;
        water='F';
    else
        fprintf('f or m only\n');
    end
end

end

