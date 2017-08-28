% Perform static model prediction using images

clear

addpath('./helpers');

find_Bosphorus;
out_loc = './out_bosph/';

if(~exist(out_loc, 'dir'))
    mkdir(out_loc);
end

%%
executable = '"../../x64/Release/FaceLandmarkImg.exe"';

bosph_dirs = dir([Bosphorus_dir, '/BosphorusDB/BosphorusDB/bs*']);

%%
parfor f1=1:numel(bosph_dirs)

    command = executable;

    input_dir = [Bosphorus_dir, '/BosphorusDB/BosphorusDB/', bosph_dirs(f1).name];
    command = cat(2, command, [' -fdir "' input_dir '" -ofdir "' out_loc '"']);
    command = cat(2, command, ' -multi_view 1 -wild -q');

    dos(command);

end

%%

aus_Bosph = [1, 2, 4, 5, 6, 7, 9, 10, 12, 14, 15, 17, 20, 23, 25, 26, 45];

[ labels_gt, valid_ids, filenames] = extract_Bosphorus_labels(Bosphorus_dir, all_recs, aus_Bosph);

%% Read the predicted values

% First read the first file to get the ids and line numbers
% au occurences
fid = fopen([out_loc, filenames{1}, '_det_0.pts']);
data = fgetl(fid);

ind = 0;
beg_ind = -1;
end_ind = -1;
aus_det = [];
aus_det_id = [];

while ischar(data)
    if(~isempty(findstr(data, 'au occurences:')))
        num_occurences = str2num(data(numel('au occurences:')+1:end));
        % Skip ahead two lines
        data = fgetl(fid);   
        data = fgetl(fid);   
        ind = ind + 2;
        beg_ind = ind;
    end
    
    if(beg_ind ~= -1 && end_ind == -1)
        if(~isempty(findstr(data, '}')))
            end_ind = ind;
        else
            d = strsplit(data, ' '); 
            aus_det = cat(1, aus_det, str2num(d{1}(3:end)));
            aus_det_id = cat(1, aus_det_id, ind - beg_ind + 1);
        end
    end
    
    data = fgetl(fid);
    ind = ind + 1;
end
fclose(fid);

%%
labels_pred = zeros(size(labels_gt));
for i=1:numel(filenames)

    % Will need to read the relevant AUs only
    if(exist([out_loc, filenames{i}, '_det_0.pts'], 'file'))
        fid = fopen([out_loc, filenames{i}, '_det_0.pts']);
        for k=1:beg_ind
            data = fgetl(fid);
        end

        for k=1:num_occurences
            data = fgetl(fid);
            if(sum(aus_Bosph == aus_det(k))>0)
                d = strsplit(data, ' '); 
                labels_pred(i, aus_Bosph == aus_det(k)) = str2num(d{2});
            end
        end

        fclose(fid);
    end
end

%%
f = fopen('results/Bosphorus_res_class.txt', 'w');
labels_gt_bin = labels_gt;
labels_gt_bin(labels_gt_bin > 1) = 1;
for au = 1:numel(aus_Bosph)
  
    tp = sum(labels_gt_bin(:,au) == 1 & labels_pred(:, au) == 1);
    fp = sum(labels_gt_bin(:,au) == 0 & labels_pred(:, au) == 1);
    fn = sum(labels_gt_bin(:,au) == 1 & labels_pred(:, au) == 0);
    tn = sum(labels_gt_bin(:,au) == 0 & labels_pred(:, au) == 0);

    precision = tp./(tp+fp);
    recall = tp./(tp+fn);

    f1 = 2 * precision .* recall ./ (precision + recall);

    fprintf(f, 'AU%d class, Precision - %.3f, Recall - %.3f, F1 - %.3f\n', aus_Bosph(au), precision, recall, f1);

end
fclose(f);

%% Read the predicted values for intensities

% First read the first file to get the ids and line numbers
% au occurences
fid = fopen([out_loc, filenames{1}, '_det_0.pts']);
data = fgetl(fid);

ind = 0;
beg_ind = -1;
end_ind = -1;
aus_det = [];
aus_det_id = [];

while ischar(data)
    if(~isempty(findstr(data, 'au intensities:')))
        num_occurences = str2num(data(numel('au intensities:')+1:end));
        % Skip ahead two lines
        data = fgetl(fid);   
        data = fgetl(fid);   
        ind = ind + 2;
        beg_ind = ind;
    end
    
    if(beg_ind ~= -1 && end_ind == -1)
        if(~isempty(findstr(data, '}')))
            end_ind = ind;
        else
            d = strsplit(data, ' '); 
            aus_det = cat(1, aus_det, str2num(d{1}(3:end)));
            aus_det_id = cat(1, aus_det_id, ind - beg_ind + 1);
        end
    end
    
    data = fgetl(fid);
    ind = ind + 1;
end
fclose(fid);

%%
labels_pred = zeros(size(labels_gt));
for i=1:numel(filenames)

    % Will need to read the relevant AUs only
    if(exist([out_loc, filenames{i}, '_det_0.pts'], 'file'))
        fid = fopen([out_loc, filenames{i}, '_det_0.pts']);
        for k=1:beg_ind
            data = fgetl(fid);
        end

        for k=1:num_occurences
            data = fgetl(fid);
            if(sum(aus_Bosph == aus_det(k))>0)
                d = strsplit(data, ' '); 
                labels_pred(i, aus_Bosph == aus_det(k)) = str2num(d{2});
            end
        end

        fclose(fid);
    end
end

%%
f = fopen('results/Bosphorus_res_int.txt', 'w');
for au = 1:numel(aus_Bosph)
  
    [ ~, ~, corrs, ccc, rms, ~ ] = evaluate_regression_results( labels_pred(:, au), labels_gt(:, au));
    
    fprintf(f, 'AU%d intensity, Corr - %.3f, RMS - %.3f, CCC - %.3f\n', aus_Bosph(au), corrs, rms, ccc);

end
fclose(f);
