function [ outputList ] = USER_INPUT_FILE_OUTPUT( reqInput )
%USER_INPUT_FILE_OUTPUT
%   Detailed explanation goes here

accepted = false;

while ~accepted
    response = input('Would you like to save the results to a file? (Y or N): ', 's');
    
    if strcmp(response, 'Y') || strcmp(response, 'y')
        accepted = true;
        createOutputFile = true;
    elseif strcmp(response, 'N') || strcmp(response, 'n')
        accepted = true;
        createOutputFile = false;
    else
        fprintf('Must enter Y or N.\n');
    end
end

outputList = {createOutputFile};

if createOutputFile
    for loopIndex = 1:length(reqInput)
        response = input(reqInput{loopIndex}, 's');
        
        outputList = [outputList {response}];
    end
end

end

