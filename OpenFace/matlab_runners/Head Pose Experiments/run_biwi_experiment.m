function [output_dir] = run_biwi_experiment(rootDir, biwiDir, verbose, depth, varargin)
% Biwi dataset experiment

if(isunix)
    executable = '"../../build/bin/FeatureExtraction"';
else
    executable = '"../../x64/Release/FeatureExtraction.exe"';
end

output_dir = 'experiments/biwi_out';    

dbSeqDir = dir([rootDir biwiDir]);
   
if(depth)
    output_dir = cat(2, output_dir, '_depth');
end

output_dir = cat(2, output_dir, '/');

offset = 0;

r = 1 + offset;
    
numTogether = 25;


for i=3 + offset:numTogether:numel(dbSeqDir)
    
       
    command = executable;
           
    command = cat(2, command, [' -inroot ' '"' rootDir '"']);
     
    % deal with edge cases
    if(numTogether + i > numel(dbSeqDir))
        numTogether = numel(dbSeqDir) - i + 1;
    end

    for n=0:numTogether-1
        
        inputFile = [biwiDir dbSeqDir(i+n).name '/colour.avi'];
        outputFile = [output_dir dbSeqDir(i+n).name '.txt'];

        command = cat(2, command, [' -f "' inputFile '" -of "' outputFile  '"']);

        if(depth)
            dDir = [biwiDir dbSeqDir(i+n).name '/depthAligned/'];
            command = cat(2, command, [' -fd "' dDir '"']);    
        end

        if(verbose)
            outputVideo = [output_dir dbSeqDir(i).name '.avi'];
            command = cat(2, command, [' -ov "' outputVideo '"']);    
        end
    end    
    command = cat(2, command, [' -fx 505 -fy 505 -cx 320 -cy 240 -no2Dfp -no3Dfp -noMparams -noAUs -noGaze']);
        
    if(any(strcmp('model', varargin)))
        command = cat(2, command, [' -mloc "', varargin{find(strcmp('model', varargin))+1}, '"']);
    end
            
    r = r+1;    
    if(isunix)
        unix(command, '-echo')
    else
        dos(command);
    end
end
