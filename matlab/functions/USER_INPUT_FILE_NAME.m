function [ filename ] = USER_INPUT_FILE_NAME()
%USER_INPUT_FILE_NAME
%   Detailed explanation goes here

accepted = false;
while ~accepted
    response = input('Enter the file name to load: ', 's');
    
    if exist(response, 'file') == 2
        accepted = true;
        
        filename = response;
    else
        fprintf('File not found. Please enter a valid file name in a valid folder.\n');
    end
end

end

