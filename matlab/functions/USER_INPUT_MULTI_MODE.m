function [ varData, numCases ] = USER_INPUT_MULTI_MODE(multiCaseData)
%USER_INPUT_MULTI_MODE

accepted = false;
while ~accepted
    response = input('Enter File mode, Random mode or Increment mode (F, R or I): ', 's');
    
    if strcmp('F', response) || strcmp('f', response)
        accepted = true;
        
        multi_mode = 'F';
    elseif strcmp('R', response) || strcmp('r', response)
        accepted = true;
        
        multi_mode = 'R';
    elseif strcmp('I', response) || strcmp('i', response)
        accepted = true;
        
        multi_mode = 'I';
    else
        fprintf('Must be F, R or I\n');
    end
end

if strcmp('F', multi_mode)
    [varData] = USER_INPUT_MULTI_FILE();
elseif strcmp('R', multi_mode)
    [varData] = USER_INPUT_MULTI_RANDOM(multiCaseData);
elseif strcmp('I', multi_mode)
    [varData] = USER_INPUT_MULTI_INCR(multiCaseData);
end

numCases = size(varData, 2);

end

