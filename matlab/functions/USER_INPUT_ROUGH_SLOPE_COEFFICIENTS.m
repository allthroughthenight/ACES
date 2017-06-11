function [ outputArgs ] = USER_INPUT_ROUGH_SLOPE_COEFFICIENTS(...
    has_rough_slope,...
    has_overtopping,...
    has_runup,...
    inputArgs)
%USER_INPUT_ROUGH_SLOPE_COEFFICIENTS
%   Required input arguments:
%       numCases: the number of cases for multi-case runs (1 for single
%       case)
%
%   Optional input arguments:
%       R_default: the default value for R
%
%   Output arguments:
%       numConsts: the number of constants being returned
%       a:
%       b:
%       alpha:
%       Qstar0:
%       U:
%       R:

outputArgs = struct();

outputArgs.numConsts = 0;
if has_rough_slope
    outputArgs.numConsts = outputArgs.numConsts + 2;
end
if has_overtopping
    outputArgs.numConsts = outputArgs.numConsts + 3;
end
if ~has_runup
    outputArgs.numConsts = outputArgs.numConsts + 1;
end

conversionKnots2mph = 1.15077945; %1 knots = 1.15077945 mph

if outputArgs.numConsts > 0
    fprintf('\nConstant Values:\n');
    
    if has_rough_slope
        %Empirical coefficients for rough slope runup
        outputArgs.a=0.956;
        outputArgs.b=0.398;
        
        fprintf('a = %-6.4f\n', outputArgs.a);
        fprintf('b = %-6.4f\n', outputArgs.b);
    end
    
    if has_overtopping
        %Empirical coefficients and values for overtopping
        outputArgs.alpha=0.076463;
        outputArgs.Qstar0=0.025;
        outputArgs.U=35.0*conversionKnots2mph;
        
        fprintf('alpha = %-6.4f\n', outputArgs.alpha);
        fprintf('Qstar0 = %-6.4f\n', outputArgs.Qstar0);
        fprintf('U = %-6.4f knots\n', outputArgs.U/conversionKnots2mph);
        
        if ~has_runup && isfield(inputArgs, 'R_default')
%         if option==3
%             R=15.0;
%             fprintf('R = %-6.4f\n', R);
%         elseif option==4
%             R=20.0;
%             fprintf('R = %-6.4f\n', R);
%         end
            outputArgs.R = inputArgs.R_default;
            fprintf('R = %-6.4f\n', outputArgs.R);
        end
    end
    
    custom_const = USER_INPUT_FINITE_CHOICE(...
        'Use default constant values or load from file? (D or F): ',...
        {'D', 'd', 'F', 'f'});
    custom_const = strcmp(custom_const, 'F') || strcmp(custom_const, 'f');

    if custom_const
        accepted = false;
        while ~accepted
            [fileData] = USER_INPUT_MULTI_FILE();

            optVarNum = 1;
            if size(fileData, 1) == outputArgs.numConsts
                if size(fileData, 2) == 1
                    accepted = true;

                    if has_rough_slope
                        outputArgs.a = fileData(optVarNum);
                        outputArgs.b = fileData(optVarNum + 1);

                        optVarNum = optVarNum + 2;
                    end

                    if has_overtopping
                        outputArgs.alpha = fileData(optVarNum);
                        outputArgs.Qstar0 = fileData(optVarNum + 1);
                        outputArgs.U = fileData(optVarNum + 2)*conversionKnots2mph;
                        
                        optVarNum = optVarNum + 3;
                    end
                    
                    if ~has_runup
                        outputArgs.R = fileData(optVarNum);
                    end
                elseif size(fileData, 2) == inputArgs.numCases
                    accepted = true;

                    if has_rough_slope
                        outputArgs.aList = fileData(optVarNum, :);
                        outputArgs.bList = fileData(optVarNum + 1, :);

                        optVarNum = optVarNum + 2;
                    end

                    if has_overtopping
                        outputArgs.alphaList = fileData(optVarNum, :);
                        outputArgs.Qstar0List = fileData(optVarNum + 1);
                        outputArgs.UList = fileData(optVarNum + 2, :)*conversionKnots2mph;
                        
                        optVarNum = optVarNum + 3;
                    end
                    
                    if ~has_runup
                        outputArgs.RList = fileData(optVarNum + 3, :);
                    end
                else
                    fprintf('Wrong number of cases. Expected either 1 or %d, found %d.\n',...
                        inputArgs.numCases, size(fileData, 2));
                end
            else
                fprintf('Wrong number of constants. Expected %d, found %d.\n',...
                    outputArgs.numConsts, size(fileData, 1));
            end
        end
    end
end


end