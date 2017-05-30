function [ dataValue ] = USER_INPUT_DATA_VALUE( promptMsg, valueMin, valueMax )
%USER_INPUT_DATA_VALUE
%   Detailed explanation goes here

accepted = false;

while ~accepted
    dataValue = input(promptMsg);
    
    if dataValue >= valueMin && dataValue <= valueMax
        accepted = true;
    else
        fprintf('Must be between %-6.2f and %-6.2f.\n', valueMin, valueMax);
    end
end

end