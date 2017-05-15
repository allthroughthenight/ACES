function [ multi_mode ] = USER_INPUT_MULTI_MODE()
%USER_INPUT_MULTI_MODE

accepted = false;
while ~accepted
    response = input('Enter File mode, Random mode or Increment mode (F, R or I): ', 's');
    
    if strcmp('F', response)
        accepted = true;
        
        multi_mode = 'F';
    elseif strcmp('R', response)
        accepted = true;
        
        multi_mode = 'R';
    elseif strcmp('I', response)
        accepted = true;
        
        multi_mode = 'I';
    else
        fprintf('Must be F, R or I\n');
    end
end

end

