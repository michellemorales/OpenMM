clear
features_exe = '"..\..\..\x64\Release\FeatureExtraction.exe"';

bosph_loc = 'D:\Datasets\Bosphorus\BosphorusDB\BosphorusDB/';

out_loc = 'D:\Datasets\face_datasets/';

% Go two levels deep
bosph_dirs = dir([bosph_loc, '/bs*']);

for f1=1:numel(bosph_dirs)
        
    name = [bosph_dirs(f1).name];

    curr_vids = dir([bosph_loc, '/' name, '/*.png']);

    parfor i=1:numel(curr_vids)
        command = features_exe;
        input_file = [bosph_loc, '/' name '/', curr_vids(i).name];
        [~, curr_name, ~] = fileparts(curr_vids(i).name);
        output_file = [out_loc, '/hog_aligned_rigid_b/',  curr_name, '/'];

        output_hog = [out_loc, '/hog_aligned_rigid_b/',curr_name '.hog'];
        output_params = [out_loc, '/model_params_b/', curr_name '.txt'];

        command = cat(2, command, [' -rigid -f "' input_file '" -simalign "' output_file  '" -simscale 0.7 -simsize 112 ']);
        command = cat(2, command, [' -hogalign "' output_hog '"' ' -of "' output_params ]);
        command = cat(2, command, ['" -no2Dfp -no3Dfp -noAUs -noPose -noGaze -q ']);
        dos(command);
    end
                
end