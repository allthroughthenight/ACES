function [ dataList ] = USER_INPUT_MULTI_FILE()
%USER_INPUT_MULTI_FILE
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

fId = fopen(filename);

dataList = [];
dataLine = fgetl(fId);
while ischar(dataLine)
    dataLineSplit = strsplit(dataLine, ',');
    
    dataNums = [];
    for loopIndex = 1:length(dataLineSplit)
        dataNums = [dataNums str2num(dataLineSplit{loopIndex})];
    end
    
    dataList = [dataList; dataNums];
    
    dataLine = fgetl(fId);
end

fclose(fId);

dataList = dataList';

end