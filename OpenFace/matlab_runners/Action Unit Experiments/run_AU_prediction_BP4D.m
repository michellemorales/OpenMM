clear

bp4d_loc = 'D:/Datasets/FERA_2015/BP4D/BP4D-training/';

out_loc = './out_bp4d/';

if(~exist(out_loc, 'dir'))
    mkdir(out_loc);
end

%%
executable = '"../../x64/Release/FeatureExtraction.exe"';

bp4d_dirs = {'F002', 'F004', 'F006', 'F008', 'F010', 'F012', 'F014', 'F016', 'F018', 'F020', 'F022', 'M002', 'M004', 'M006', 'M008', 'M010', 'M012', 'M014', 'M016', 'M018'};

%% Before running BP4D convert it to a smaller format and move each person to the same directory
% This is done so that dynamic models would work on it as otherwise the
% clips are a bit too short

new_bp4d_dirs = {};

% This might take some time
for i = 1:numel(bp4d_dirs)
    dirs = dir([bp4d_loc, '/', bp4d_dirs{i}, '/T*']);
    
    tmp_dir = [bp4d_loc, '/../tmp/', bp4d_dirs{i}, '/'];
    new_bp4d_dirs = cat(1, new_bp4d_dirs, tmp_dir);
    
    if(~exist(tmp_dir, 'file'))
        mkdir(tmp_dir);
        
        % Move all images and resize them
        for d=1:numel(dirs)
           
            in_files = dir([bp4d_loc, '/', bp4d_dirs{i}, '/', dirs(d).name, '/*.jpg']);
            
            for img_ind=1:numel(in_files)
               
                img_file = [bp4d_loc, '/', bp4d_dirs{i}, '/', dirs(d).name, '/', in_files(img_ind).name];
                img = imread(img_file);
                img = imresize(img, 0.5);
                img_out = [tmp_dir, dirs(d).name, '_', in_files(img_ind).name];
                imwrite(img, img_out);
                
            end
            
        end
        
    end
    
end
%%

parfor f1=1:numel(new_bp4d_dirs)
    
    command = [executable ' -asvid -no2Dfp -no3Dfp -noMparams -noPose -noGaze '];

    [f,~,~] = fileparts(new_bp4d_dirs{f1});
    [~,f,~] = fileparts(f);
    output_file = [out_loc f '.au.txt'];

    command = cat(2, command, [' -fdir "' new_bp4d_dirs{f1} '" -of "' output_file '"']);

    dos(command);

end

%%
addpath('./helpers/');

find_BP4D;

aus_BP4D = [1, 2, 4, 6, 7, 10, 12, 14, 15, 17, 23];

[ labels_gt, valid_ids, vid_ids, filenames] = extract_BP4D_labels(BP4D_dir, bp4d_dirs, aus_BP4D);
labels_gt = cat(1, labels_gt{:});

%% Identifying which column IDs correspond to which AU
tab = readtable([out_loc, bp4d_dirs{1}, '.au.txt']);
column_names = tab.Properties.VariableNames;

% As there are both classes and intensities list and evaluate both of them
aus_pred_int = [];
aus_pred_class = [];

inds_int_in_file = [];
inds_class_in_file = [];

for c=1:numel(column_names)
    if(strfind(column_names{c}, '_r') > 0)
        aus_pred_int = cat(1, aus_pred_int, int32(str2num(column_names{c}(3:end-2))));
        inds_int_in_file = cat(1, inds_int_in_file, c);
    end
    if(strfind(column_names{c}, '_c') > 0)
        aus_pred_class = cat(1, aus_pred_class, int32(str2num(column_names{c}(3:end-2))));
        inds_class_in_file = cat(1, inds_class_in_file, c);
    end
end

%%
inds_au_class = zeros(size(aus_BP4D));

for ind=1:numel(aus_BP4D)  
    if(~isempty(find(aus_pred_class==aus_BP4D(ind), 1)))
        inds_au_class(ind) = find(aus_pred_class==aus_BP4D(ind));
    end
end

preds_all_class = [];

for i=1:numel(new_bp4d_dirs)
   
    [f,~,~] = fileparts(new_bp4d_dirs{i});
    [~,f,~] = fileparts(f);
    
    fname = [out_loc, f, '.au.txt'];
    preds = dlmread(fname, ',', 1, 0);
    
    
    % Read all of the classification AUs
    preds_class = preds(:, inds_class_in_file);
    
    preds_all_class = cat(1, preds_all_class, preds_class);
end

%%
f = fopen('results/BP4D_valid_res_class.txt', 'w');
for au = 1:numel(aus_BP4D)

    if(inds_au_class(au) ~= 0)
        tp = sum(labels_gt(:,au) == 1 & preds_all_class(:, inds_au_class(au)) == 1);
        fp = sum(labels_gt(:,au) == 0 & preds_all_class(:, inds_au_class(au)) == 1);
        fn = sum(labels_gt(:,au) == 1 & preds_all_class(:, inds_au_class(au)) == 0);
        tn = sum(labels_gt(:,au) == 0 & preds_all_class(:, inds_au_class(au)) == 0);

        precision = tp./(tp+fp);
        recall = tp./(tp+fn);

        f1 = 2 * precision .* recall ./ (precision + recall);

        fprintf(f, 'AU%d class, Precision - %.3f, Recall - %.3f, F1 - %.3f\n', aus_BP4D(au), precision, recall, f1);
    end    
    
end
fclose(f);

%%
addpath('./helpers/');

find_BP4D;

aus_BP4D = [6, 10, 12, 14, 17];
[ labels_gt, valid_ids, vid_ids, filenames] = extract_BP4D_labels_intensity(BP4D_dir_int, devel_recs, aus_BP4D);
valid_ids = cat(1, valid_ids{:});
labels_gt = cat(1, labels_gt{:});

%% Identifying which column IDs correspond to which AU
tab = readtable([out_loc, bp4d_dirs{1}, '.au.txt']);
column_names = tab.Properties.VariableNames;

% As there are both classes and intensities list and evaluate both of them
aus_pred_int = [];
inds_int_in_file = [];

for c=1:numel(column_names)
    if(strfind(column_names{c}, '_r') > 0)
        aus_pred_int = cat(1, aus_pred_int, int32(str2num(column_names{c}(3:end-2))));
        inds_int_in_file = cat(1, inds_int_in_file, c);
    end
end

%%
inds_au_int = zeros(size(aus_BP4D));

for ind=1:numel(aus_BP4D)  
    if(~isempty(find(aus_pred_int==aus_BP4D(ind), 1)))
        inds_au_int(ind) = find(aus_pred_int==aus_BP4D(ind));
    end
end

preds_all_int = [];

for i=1:numel(new_bp4d_dirs)
   
    [f,~,~] = fileparts(new_bp4d_dirs{i});
    [~,f,~] = fileparts(f);
    
    fname = [out_loc, f, '.au.txt'];
    preds = dlmread(fname, ',', 1, 0);
    
    % Read all of the intensity AUs
    preds_int = preds(:, inds_int_in_file);    
    preds_all_int = cat(1, preds_all_int, preds_int);
end

%%
f = fopen('results/BP4D_valid_res_int.txt', 'w');
for au = 1:numel(aus_BP4D)
    [ accuracies, F1s, corrs, ccc, rms, classes ] = evaluate_au_prediction_results( preds_all_int(valid_ids, inds_au_int(au)), labels_gt(valid_ids,au));
    fprintf(f, 'AU%d results - rms %.3f, corr %.3f, ccc - %.3f\n', aus_BP4D(au), rms, corrs, ccc);    
end
fclose(f);