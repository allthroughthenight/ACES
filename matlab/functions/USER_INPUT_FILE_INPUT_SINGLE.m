function [ outputDataList ] = USER_INPUT_FILE_INPUT_SINGLE( inputDataList )
%USER_INPUT_FILE_INPUT_SINGLE

[response] = USER_INPUT_FINITE_CHOICE(...
    'Enter data manually or load from file? (M or F): ',...
    {'M', 'm', 'F', 'f'});

if strcmp(response, 'M') || strcmp(response, 'm')
    accepted = true;
    outputDataList = [];

    for varIndex = 1:size(inputDataList, 1)
        varData = USER_INPUT_DATA_VALUE(...
            ['Enter ' inputDataList{varIndex, 1} ': '],...
            inputDataList{varIndex, 2},...
            inputDataList{varIndex, 3});

        outputDataList = [outputDataList varData];
    end
else
    accepted = false;
    while ~accepted
        [filename] = USER_INPUT_FILE_NAME();
        
        fId = fopen(filename);
        
        fileData = textscan(fId, '%f');
        
        fclose(fId);
        
        if length(fileData{1}) >= size(inputDataList, 1)
            accepted = true;
            outputDataList = fileData{1};
        else
            fprintf('%d values are required. Please check your file and try again.\n',...
                size(inputDataList, 1));
        end
    end
end

end