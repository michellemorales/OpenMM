function [geom_data, valid_ids] = Read_geom_files_dynamic(users, hog_data_dir)

    geom_data = [];
    valid_ids = [];
    
    load('../../pca_generation/pdm_68_aligned_wild.mat');
    
    for i=1:numel(users)
        
        geom_files = dir([hog_data_dir, '/train/', users{i} '*.params.txt']);
        geom_dir = [hog_data_dir, '/train/'];
        if(isempty(geom_files))
            geom_files = dir([hog_data_dir, '/devel/', users{i} '*.params.txt']);
            geom_dir = [hog_data_dir, '/devel/'];
        end
        
        geom_data_curr = [];
        for h=1:numel(geom_files)
            geom_file = [geom_dir, geom_files(h).name];
                        
            [~, nm, ~] = fileparts(geom_file);
            m_file = [geom_dir, '/' nm '.params.mat'];
              
            if(~exist(m_file, 'file'))
                res = dlmread(geom_file, ',', 1, 0);
                save(m_file, 'res');
            else
                load(m_file);
            end

            valid = res(:, 4);
            res = res(:, 11:end);
                    
            actual_locs = res * V';
            res = cat(2, actual_locs, res);
            
            valid_ids = cat(1, valid_ids, valid);            
            
            geom_data_curr = cat(1, geom_data_curr, res);
        end
        geom_data_curr = bsxfun(@plus, geom_data_curr, -median(geom_data_curr));
        
        geom_data = cat(1, geom_data, geom_data_curr);
                
    end
end