% This is sort of the unit test for the whole module (needs datasets)
% Will take several hours to run all
clear
tic
%% Head pose
cd('Head Pose Experiments');
run_head_pose_tests_OpenFace;
assert(median(all_errors_biwi_OF(:)) < 2.7);
assert(median(all_errors_bu_OF(:)) < 2.2);
assert(median(all_errors_ict_OF(:)) < 2.1);
cd('../');

%% Features
cd('Feature Point Experiments');
run_OpenFace_feature_point_tests_300W;
assert(median(err_clnf) < 0.041);
assert(median(err_clnf_wild) < 0.041);
run_yt_dataset;
assert(median(clnf_error) < 0.053);
cd('../');

%% AUs
cd('Action Unit Experiments');
run_AU_prediction_DISFA
assert(mean(au_res) > 0.7);

run_AU_prediction_SEMAINE
assert(mean(f1s) > 0.42);

run_AU_prediction_FERA2011
assert(mean(au_res) > 0.5);

cd('../');

%% Gaze
cd('Gaze Experiments');
extract_mpii_gaze_test
assert(mean_error < 9.5)
assert(median_error < 9.0)
cd('../');

%% Demos
cd('Demos');
run_demo_images;
run_demo_videos;
run_demo_video_multi;
feature_extraction_demo_vid;
feature_extraction_demo_img_seq;
gaze_extraction_demo_vid;
cd('../');
toc