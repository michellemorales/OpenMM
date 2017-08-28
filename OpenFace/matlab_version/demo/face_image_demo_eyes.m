clear
addpath('../PDM_helpers/');
addpath(genpath('../fitting/'));
addpath('../models/');
addpath(genpath('../face_detection'));
addpath('../CCNF/');

%% loading the patch experts
   
[clmParams, pdm] = Load_CLM_params_wild();

% An accurate CCNF (or CLNF) model
[patches] = Load_Patch_Experts( '../models/general/', 'ccnf_patches_*_general.mat', [], [], clmParams);
% A simpler (but less accurate SVR)
% [patches] = Load_Patch_Experts( '../models/general/', 'svr_patches_*_general.mat', [], [], clmParams);

% Loading eye PDM and patch experts
[clmParams_eye, pdm_right_eye, pdm_left_eye] = Load_CLM_params_eye_28();
[patches_right_eye] = Load_Patch_Experts( '../models/hierarch/', 'ccnf_patches_*_synth_right_eye.mat', [], [], clmParams_eye);
[patches_left_eye] = Load_Patch_Experts( '../models/hierarch/', 'ccnf_patches_*_synth_left_eye.mat', [], [], clmParams_eye);
clmParams_eye.multi_modal_types  = patches_right_eye(1).multi_modal_types;
right_eye_inds = [43,44,45,46,47,48];
left_eye_inds = [37,38,39,40,41,42];

right_eye_inds_synth = [9 11 13 15 17 19];
left_eye_inds_synth = [9 11 13 15 17 19];

clmParams.multi_modal_types  = patches(1).multi_modal_types;

%%
% root_dir = 'C:\Users\Tadas\Dropbox\AAM\test data\gaze_original\p00/';
% images = dir([root_dir, '*.jpg']);

%root_dir = './sample_eye_imgs/';
%images = dir([root_dir, '/*.png']);
root_dir = '../../samples/';
images = dir([root_dir, '*.jpg']);

verbose = true;

for img=1:numel(images)
    image_orig = imread([root_dir images(img).name]);

    % First attempt to use the Matlab one (fastest but not as accurate, if not present use yu et al.)
    [bboxs, det_shapes] = detect_faces(image_orig, {'cascade', 'yu'});
    % Zhu and Ramanan and Yu et al. are slower, but also more accurate 
    % and can be used when vision toolbox is unavailable
%     [bboxs, det_shapes] = detect_faces(image_orig, {'yu', 'zhu'});
    
    % The complete set that tries all three detectors starting with fastest
    % and moving onto slower ones if fastest can't detect anything
%     [bboxs, det_shapes] = detect_faces(image_orig, {'cascade', 'yu', 'zhu'});
    
    if(size(image_orig,3) == 3)
        image = rgb2gray(image_orig);
    end              

    %%

    if(verbose)
        f = figure;    
        if(max(image(:)) > 1)
            imshow(double(image_orig)/255, 'Border', 'tight');
        else
            imshow(double(image_orig), 'Border', 'tight');
        end
        axis equal;
        hold on;
    end

    for i=1:size(bboxs,2)

        % Convert from the initial detected shape to CLM model parameters,
        % if shape is available
        
        bbox = bboxs(:,i);
        
        if(~isempty(det_shapes))
            shape = det_shapes(:,:,i);
            inds = [1:60,62:64,66:68];
            M = pdm.M([inds, inds+68, inds+68*2]);
            E = pdm.E;
            V = pdm.V([inds, inds+68, inds+68*2],:);
            [ a, R, T, ~, params, err, shapeOrtho] = fit_PDM_ortho_proj_to_2D(M, E, V, shape);
            g_param = [a; Rot2Euler(R)'; T];
            l_param = params;

            % Use the initial global and local params for clm fitting in the image
            [shape,~,~,lhood,lmark_lhood,view_used] = Fitting_from_bb(image, [], bbox, pdm, patches, clmParams, 'gparam', g_param, 'lparam', l_param);
        else
            [shape,~,~,lhood,lmark_lhood,view_used] = Fitting_from_bb(image, [], bbox, pdm, patches, clmParams);
        end
        
        % shape correction for matlab format
        shape = shape + 1;
              
        % Perform eye fitting now
        shape_r_eye = zeros(numel(pdm_right_eye.M)/3, 2);
        shape_r_eye(right_eye_inds_synth,:) = shape(right_eye_inds, :);

        [ a, R, T, ~, l_params] = fit_PDM_ortho_proj_to_2D(pdm_right_eye.M, pdm_right_eye.E, pdm_right_eye.V, shape_r_eye);

        bbox = [min(shape_r_eye(:,1)), min(shape_r_eye(:,2)), max(shape_r_eye(:,1)), max(shape_r_eye(:,2))];

        g_param = [a; Rot2Euler(R)'; T];

        [shape_r_eye] = Fitting_from_bb(image, [], bbox, pdm_right_eye, patches_right_eye, clmParams_eye, 'gparam', g_param, 'lparam', l_params);

        % Perform eye fitting now 
        shape_l_eye = zeros(numel(pdm_right_eye.M)/3, 2);        
        shape_l_eye(left_eye_inds_synth,:) = shape(left_eye_inds, :);

        [ a, R, T, ~, l_params] = fit_PDM_ortho_proj_to_2D(pdm_left_eye.M, pdm_left_eye.E, pdm_left_eye.V, shape_l_eye);

        bbox = [min(shape_l_eye(:,1)), min(shape_l_eye(:,2)), max(shape_l_eye(:,1)), max(shape_l_eye(:,2))];

        g_param = [a; Rot2Euler(R)'; T];

        [shape_l_eye] = Fitting_from_bb(image, [], bbox, pdm_left_eye, patches_left_eye, clmParams_eye, 'gparam', g_param, 'lparam', l_params);

        plot(shape_l_eye(9:20,1), shape_l_eye(9:20,2), '.g', 'MarkerSize',7);
        plot(shape_l_eye(1:8,1), shape_l_eye(1:8,2), '.b', 'MarkerSize',7);

        plot(shape_r_eye(9:20,1), shape_r_eye(9:20,2), '.g', 'MarkerSize',7);
        plot(shape_r_eye(1:8,1), shape_r_eye(1:8,2), '.b', 'MarkerSize',7);
    end
    hold off;
    
end