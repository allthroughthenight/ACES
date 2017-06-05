function [ dataList ] = USER_INPUT_MULTI_FILE()
%USER_INPUT_MULTI_FILE
%   Detailed explanation goes here

[filename] = USER_INPUT_FILE_NAME();

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