function [ choiceValue ] = USER_INPUT_FINITE_CHOICE( promptMsg, choiceList )
%USER_INPUT_FINITE_CHOICE
%   Detailed explanation goes here

accepted = false;

while ~accepted
    choiceValue = input(promptMsg, 's');
    
    if ~isempty(find([choiceList{:}] == choiceValue))
        accepted = true;
    else
        fprintf('Must be one of the choices specified.\n');
    end
end

%end