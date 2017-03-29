function [geom_data, valid_ids] = Read_geom_files(users, model_param_data_dir)

    geom_data = [];
    valid_ids = [];
    
    load('../../pca_generation/pdm_68_aligned_wild.mat');
    
    for i=1:numel(users)
        
        geom_files = dir([model_param_data_dir, '/' users{i} '*.txt']);
        
        for g=1:numel(geom_files)
            
            m_file = [model_param_data_dir, '/', geom_files(g).name, '.mat'];

            if(~exist(m_file, 'file'))
                res = dlmread([model_param_data_dir, '/', geom_files(g).name], ',', 1, 0);    
                save(m_file, 'res');
            else
                load(m_file);
            end
            
            valid = res(:, 4);        
            res = res(:, 11:end);
        
            actual_locs = res * V';
            res = cat(2, actual_locs, res);

            valid_ids = cat(1, valid_ids, valid);

            geom_data = cat(1, geom_data, res);
        end
    end
end