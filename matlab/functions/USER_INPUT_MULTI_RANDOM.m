function [ varDataList ] = USER_INPUT_MULTI_RANDOM( varList )
%USER_INPUT_MULTI_RANDOM
%   Detailed explanation goes here

varDataList = [];

[numCases] = USER_INPUT_DATA_VALUE('Enter the number of cases (1 - 20): ', 1, 20);

for caseIndex = 1:numCases
    fprintf('-- Data Set #%d -------------------------------\n', caseIndex);
    
    varTempList = [];
    for varIndex = 1:size(varList, 1)
        varData = USER_INPUT_DATA_VALUE(...
            ['Enter ' varList{varIndex, 1} ': '],...
            varList{varIndex, 2},...
            varList{varIndex, 3});
        
        varTempList = [varTempList varData];
    end
    
    varDataList = [varDataList; varTempList];
end

varDataList = varDataList';

end