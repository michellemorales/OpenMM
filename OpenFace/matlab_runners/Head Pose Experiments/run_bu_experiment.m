function [output_dir] = run_bu_experiment(bu_dir, verbose, varargin)
   
    if(isunix)
        executable = '"../../build/bin/FeatureExtraction"';
    else
        executable = '"../../x64/Release/FeatureExtraction.exe"';
    end

    output_dir = 'experiments/bu_out/';        

    buFiles = dir([bu_dir '*.avi']);
    
    numTogether = 25;
    
    for i=1:numTogether:numel(buFiles)
        
        command = executable;
        command = cat(2, command, [' -inroot ' '"' bu_dir '/"']);
        
        % BU dataset orientation is in terms of camera plane, instruct the
        % tracker to output it in that format
        command = cat(2, command, [' -cp ']);
        
        % deal with edge cases
        if(numTogether + i > numel(buFiles))
            numTogether = numel(buFiles) - i + 1;
        end
        
        for n=0:numTogether-1
            inputFile = [buFiles(n+i).name];
            [~, name, ~] = fileparts(inputFile);   

            % where to output results
            outputFile = [output_dir name '.txt'];
            
            command = cat(2, command, [' -f "' inputFile '" -of "' outputFile '"']);

            if(verbose)
                outputVideo = ['"' output_dir name '.avi' '"'];
                command = cat(2, command, [' -ov ' outputVideo]);
            end
        end
        
        command = cat(2, command,  ' -fx 500 -fy 500 -cx 160 -cy 120 -no2Dfp -no3Dfp -noMparams -noAUs -noGaze ');        
    
        if(any(strcmp('model', varargin)))
            command = cat(2, command, [' -mloc "', varargin{find(strcmp('model', varargin))+1}, '"']);
        end  
        
        if(isunix)
            unix(command, '-echo')
        else
            dos(command);
        end
    end
            
end