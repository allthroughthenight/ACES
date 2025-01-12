function [ varDataList ] = USER_INPUT_MULTI_INCR( varList )
%USER_INPUT_MULTI_INCR
%   Detailed explanation goes here

varDataList = [];
varTempList = [];
for varIndex = 1:size(varList, 1)
    varMin = USER_INPUT_DATA_VALUE(...
        ['Enter minimum ' varList{varIndex, 1} ': '],...
        varList{varIndex, 2},...
        varList{varIndex, 3});
    
    if varMin == varList{varIndex, 3}
        varMax = varMin;
        fprintf('Maximum %s automatically set to %-6.2f\n', varList{varIndex, 1}, varMin);
    else
        varMax = USER_INPUT_DATA_VALUE(...
            ['Enter maximum ' varList{varIndex, 1} ': '],...
            varMin,...
            varList{varIndex, 3});
    end
    
    varTempList = [varTempList; varMin, varMax];
end

varIncr = USER_INPUT_DATA_VALUE(['Enter the number of increments: '], 1, inf);

for varIndex = 1:size(varTempList, 1)
    min = varTempList(varIndex, 1);
    max = varTempList(varIndex, 2);
    incr = (max - min) / (varIncr - 1);
    
    if min == max
        varDataList(varIndex, 1:varIncr) = max;
    else
        varDataList = [varDataList; min:incr:max];
    end
end

end