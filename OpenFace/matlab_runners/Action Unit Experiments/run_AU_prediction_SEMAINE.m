clear

addpath(genpath('helpers/'));
find_SEMAINE;

out_loc = './out_SEMAINE/';

if(~exist(out_loc, 'dir'))
    mkdir(out_loc);
end

if(isunix)
    executable = '"../../build/bin/FeatureExtraction"';
else
    executable = '"../../x64/Release/FeatureExtraction.exe"';
end
%%
parfor f1=1:numel(devel_recs)


    if(isdir([SEMAINE_dir, devel_recs{f1}]))
        
        vid_file = dir([SEMAINE_dir, devel_recs{f1}, '/*.avi']);

        f1_dir = devel_recs{f1};

        command = [executable, ' -fx 800 -fy 800 -q -no2Dfp -no3Dfp -noMparams -noPose -noGaze '];

        curr_vid = [SEMAINE_dir, f1_dir, '/', vid_file.name];

        name = f1_dir;
        output_aus = [out_loc name '.au.txt'];

        command = cat(2, command, [' -f "' curr_vid '" -of "' output_aus, '"']);
        
        if(isunix)
            unix(command, '-echo');
        else
            dos(command);
        end

    end
end

%% Actual model evaluation
[ labels, valid_ids, vid_ids  ] = extract_SEMAINE_labels(SEMAINE_dir, devel_recs, aus_SEMAINE);

labels_gt = cat(1, labels{:});

%% Identifying which column IDs correspond to which AU
tab = readtable([out_loc, devel_recs{1}, '.au.txt']);
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
inds_au_int = zeros(size(aus_SEMAINE));
inds_au_class = zeros(size(aus_SEMAINE));

for ind=1:numel(aus_SEMAINE)  
    if(~isempty(find(aus_pred_int==aus_SEMAINE(ind), 1)))
        inds_au_int(ind) = find(aus_pred_int==aus_SEMAINE(ind));
    end
end

for ind=1:numel(aus_SEMAINE)  
    if(~isempty(find(aus_pred_class==aus_SEMAINE(ind), 1)))
        inds_au_class(ind) = find(aus_pred_class==aus_SEMAINE(ind));
    end
end

preds_all_class = [];
preds_all_int = [];

for i=1:numel(devel_recs)
   
    fname = [out_loc, devel_recs{i}, '.au.txt'];
    preds = dlmread(fname, ',', 1, 0);
    
    % Read all of the intensity AUs
    preds_int = preds(vid_ids(i,1):vid_ids(i,2) - 1, inds_int_in_file);
    
    % Read all of the classification AUs
    preds_class = preds(vid_ids(i,1):vid_ids(i,2) - 1, inds_class_in_file);
    
    preds_all_class = cat(1, preds_all_class, preds_class);
    preds_all_int = cat(1, preds_all_int, preds_int);
end

%%
f = fopen('results/SEMAINE_valid_res.txt', 'w');
f1s = zeros(1, numel(aus_SEMAINE));
for au = 1:numel(aus_SEMAINE)
    
    if(inds_au_class(au) ~= 0)
        tp = sum(labels_gt(:,au) == 1 & preds_all_class(:, inds_au_class(au)) == 1);
        fp = sum(labels_gt(:,au) == 0 & preds_all_class(:, inds_au_class(au)) == 1);
        fn = sum(labels_gt(:,au) == 1 & preds_all_class(:, inds_au_class(au)) == 0);
        tn = sum(labels_gt(:,au) == 0 & preds_all_class(:, inds_au_class(au)) == 0);

        precision = tp./(tp+fp);
        recall = tp./(tp+fn);

        f1 = 2 * precision .* recall ./ (precision + recall);
        f1s(au) = f1;
        fprintf(f, 'AU%d class, Precision - %.3f, Recall - %.3f, F1 - %.3f\n', aus_SEMAINE(au), precision, recall, f1);
    end    
    
end
fclose(f);