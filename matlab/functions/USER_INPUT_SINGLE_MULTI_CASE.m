function [ single_case ] = USER_INPUT_SINGLE_MULTI_CASE()
%USER_INPUT_SINGLE_MULTI_CASE
%   Prompts the user to select single or multi case

% Ask user for single or multi-input (from a file)
accepted = false;
single_case = '';
while accepted == false
    single_case=input('Single or Multi-case? (s or m): ', 's');
    
    if strcmp('s',single_case) || strcmp('S',single_case)
        accepted = true;
        single_case=true;
    elseif strcmp('m', single_case) || strcmp('M', single_case)
        accepted = true;
        single_case=false;
    else
        fprintf('s or m only\n');
    end
end

end