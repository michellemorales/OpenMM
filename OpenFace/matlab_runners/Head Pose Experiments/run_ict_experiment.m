function [output_dir] = run_ict_experiment(rootDir, ictDir, verbose, depth, varargin)
%EVALUATEICTDATABASE Summary of this function goes here
%   Detailed explanation goes here

if(isunix)
    executable = '"../../build/bin/FeatureExtraction"';
else
    executable = '"../../x64/Release/FeatureExtraction.exe"';
end

output_dir = 'experiments/ict_out';    

dbSeqDir = dir([rootDir ictDir]);
   
if(depth)
    output_dir = cat(2, output_dir, '_depth');
end

output_dir = cat(2, output_dir, '/');

numTogether = 10;

for i=3:numTogether:numel(dbSeqDir)
        
    command = [executable  ' -fx 535 -fy 536 -cx 327 -cy 241 -no2Dfp -no3Dfp -noMparams -noAUs -noGaze '];

    command = cat(2, command, [' -inroot ' '"' rootDir '/"']);

    % deal with edge cases
    if(numTogether + i > numel(dbSeqDir))
        numTogether = numel(dbSeqDir) - i + 1;
    end
    
    for n=0:numTogether-1
        
        inputFile = [ictDir dbSeqDir(i+n).name '/colour undist.avi'];
        outputFile = [output_dir dbSeqDir(i+n).name '.txt'];
        
        command = cat(2, command,  [' -f "' inputFile '" -of "' outputFile  '" ']);
        
        if(depth)
            dDir = [ictDir dbSeqDir(i+n).name '/depthAligned/'];
            command = cat(2, command, [' -fd "' dDir '"']);
        end
        
        if(verbose)
            outputVideo = [output_dir dbSeqDir(i+n).name '.avi'];
            command = cat(2, command, [' -ov "' outputVideo '"']);
        end
    end
    
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

