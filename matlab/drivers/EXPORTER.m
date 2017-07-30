classdef EXPORTER
    properties
        fId
    end
    
    methods
        function obj = EXPORTER(filename)
            obj.fId = fopen([filename '.csv'], 'wt');
        end
        
        function writeData(obj, dataList)
            for i = 1:length(dataList)
                if ischar(i)
                    data = dataList{i};
                else
                    data = num2str(dataList{i});
                end
                
                if i == 1
                    fprintf(obj.fId, '%s', data);
                else
                    fprintf(obj.fId, ',%s', data);
                end
            end
            
            fprintf(obj.fId, '\n');
        end
        
        function close(obj)
            fclose(obj.fId);
        end
    end
end