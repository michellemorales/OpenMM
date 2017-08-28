function [geom_data] = Read_geom_files_dynamic(users, hog_data_dir)

    geom_data = [];
    
    load('../../pca_generation/pdm_68_aligned_wild.mat');
    
    for i=1:numel(users)
        
        geom_file = [hog_data_dir, '/../model_params/LeftVideo' users{i} '_comp.txt'];        
        
        res = dlmread(geom_file, ',', 1, 0);        
        valid = logical(res(:,4));
        
        %res_rot = res(:,6:8);
        
        res = res(:,11:end);   
        
        actual_locs = res * V';
        res = cat(2, actual_locs, res);
       
        res = bsxfun(@plus, res, -median(res(valid,:)));

        geom_data = cat(1, geom_data, res);
                
    end
end