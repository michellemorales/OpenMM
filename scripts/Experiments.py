import Fusions
import pandas


def get_earlyfusion():
    print('\nRunning fusion experiments...\n')
    # Get training labels
    train_csv = '/Users/michellemorales/Desktop/MoralesDocs/DAIC_WOZ/Labels/training_split.csv'
    train_df = pandas.read_csv(train_csv)
    train_labels = {}
    for row in train_df.iterrows():
        row = row[1]
        train_labels[str(row['Participant_ID'])] = {'binary': row['PHQ_Binary'],
                                                    'score': row['PHQ_Score'], 'gender': row['Gender']}

    # Get dev labels
    dev_csv = '/Users/michellemorales/Desktop/MoralesDocs/DAIC_WOZ/Labels/dev_split.csv'
    dev_df = pandas.read_csv(dev_csv)
    dev_labels = {}
    for row in dev_df.iterrows():
        row = row[1]
        dev_labels[str(row['Participant_ID'])] = {'binary': row['PHQ_Binary'],
                                                  'score': row['PHQ_Score'], 'gender': row['Gender']}
    print("Done loading data labels...\n")

    # Audio features dir
    audio_dir = '/Users/michellemorales/Desktop/MoralesDocs/DAIC_WOZ/Audio_Features/'
    # Video features dir
    video_dir = '/Users/michellemorales/Desktop/MoralesDocs/DAIC_WOZ/Video_Features/'
    # Ling features dir
    ling_dir = '/Users/michellemorales/Desktop/MoralesDocs/DAIC_WOZ/Ling_Features/'

    # ---------- Perform early fusion (training) ----------- #
    training_data = []
    for i, ID in enumerate(train_labels.keys()):
        mm_files = [audio_dir + ID + '_covarep.csv', video_dir + ID + '_openface.csv', ling_dir + ID + '_ling.csv']
        # This is pretty slow because the feature space is so large > 17,000 features
        mm_names, mm_feats = Fusions.early_fusion(mm_files)
        if i == 0:
            feature_names = ['participant_id'] + mm_names
        training_data.append([ID] + mm_feats)

    new_file = open('train_multimodal_features_avg.csv', 'w')
    new_file.write(','.join(feature_names) + '\n')
    for feat_list in training_data:
        new_file.write(','.join([str(mm) for mm in feat_list]) + '\n')
    new_file.close()

    # ---------- Perform early fusion (dev) ----------- #
    dev_data = []
    for i, ID in enumerate(dev_labels.keys()):
        mm_files = [audio_dir + ID + '_covarep.csv', video_dir + ID + '_openface.csv', ling_dir + ID + '_ling.csv']
        # This is pretty slow because the feature space is so large > 17,000 features
        mm_names, mm_feats = Fusions.early_fusion(mm_files)
        if i == 0:
            feature_names = ['participant_id'] + mm_names
        dev_data.append([ID] + mm_feats)

    new_file = open('dev_multimodal_features_avg.csv', 'w')
    new_file.write(','.join(feature_names) + '\n')
    for feat_list in dev_data:
        new_file.write(','.join([str(mm) for mm in feat_list]) + '\n')
    new_file.close()

    print('Done!')


def run_experiments():
    print('\nRunning SVM experiments...\n')
    # Get training labels
    train_csv = '/Users/michellemorales/Desktop/MoralesDocs/DAIC_WOZ/Labels/training_split.csv'
    train_df = pandas.read_csv(train_csv)
    train_labels = {}
    for row in train_df.iterrows():
        row = row[1]
        train_labels[str(row['Participant_ID'])] = {'binary': row['PHQ_Binary'],
                                                    'score': row['PHQ_Score'], 'gender': row['Gender']}

    # Get dev labels
    dev_csv = '/Users/michellemorales/Desktop/MoralesDocs/DAIC_WOZ/Labels/dev_split.csv'
    dev_df = pandas.read_csv(dev_csv)
    dev_labels = {}
    for row in dev_df.iterrows():
        row = row[1]
        dev_labels[str(row['Participant_ID'])] = {'binary': row['PHQ_Binary'],
                                                  'score': row['PHQ_Score'], 'gender': row['Gender']}
    print("Done loading data labels...\n")

    # Load features for train and dev
    path = "/Users/michellemorales/Desktop/MoralesDocs/DAIC_WOZ/Early_Features/"
    train_data = pandas.read_csv(path+'train_multimodal_features.csv')
    audio_names =  train_data.columns[1:371]
    video_names = train_data.columns[371: 556]
    text_names = train_data.columns[556:]
    dev_data =  pandas.read_csv(path+'dev_multimodal_features.csv')
    print('Done loading data...\n')

    # Get training data & labels for features
    t_labels = []
    t_bin_labels = []
    t_features = []
    for row in train_data.iterrows():
        part_id = str(int(row[1][0]))
        features = row[1][1:].values
        t_features.append(features)
        label = train_labels[part_id]['score']
        b_label = train_labels[part_id]['binary']
        t_labels.append(label)
        t_bin_labels.append(b_label)


    # Get dev data & labels for features
    d_labels = []
    d_bin_labels = []
    d_features = []
    for row in dev_data.iterrows():
        part_id = str(int(row[1][0]))
        features = row[1][1:].values
        d_features.append(features)
        label = dev_labels[part_id]['score']
        b_label = dev_labels[part_id]['binary']
        d_labels.append(label)
        d_bin_labels.append(b_label)

    print 'Random binary baseline = ', float(d_bin_labels.count(0)) / len(d_bin_labels)

    # Early fusion
    print('Early fusion results...\n')
    print Fusions.predict_regression(t_features,d_features,t_labels,d_labels)
    print Fusions.predict_class(t_features,d_features,t_bin_labels,d_bin_labels)

    print('Early fusion with PCA results...\n')
    t_pca, d_pca = Fusions.add_pca(100, t_features, d_features)
    print Fusions.predict_regression(t_pca, d_pca, t_labels, d_labels)
    print Fusions.predict_class(t_pca, d_pca, t_bin_labels, d_bin_labels)
    exit()
    # audio_names =  train_data.columns[1:371]
    # video_names = train_data.columns[371: 556]
    # text_names = train_data.columns[556:]

    # Audio only
    print('Results for audio only...\n')
    audio_t = [feats[:370] for feats in t_features]
    audio_d = [feats[:370] for feats in d_features]
    # print len(audio_d[0])
    # print Fusions.predict_regression(audio_t, audio_d,t_labels,d_labels)
    print Fusions.predict_class(audio_t,audio_d,t_bin_labels,d_bin_labels)

    # Text only
    print('Results for text only...\n')
    text_t = [feats[555:] for feats in t_features]
    text_d = [feats[555:] for feats in d_features]
    # print len(text_t[0])
    # print Fusions.predict_regression(text_t,text_d,t_labels,d_labels)
    print Fusions.predict_class(text_t,text_d,t_bin_labels,d_bin_labels)

    # Video only
    print('Results for video only...\n')
    video_t = [feats[370:555] for feats in t_features]
    video_d = [feats[370:555] for feats in d_features]
    # print len(video_d[0])
    # print Fusions.predict_regression(video_t, video_d, t_labels,d_labels)
    print Fusions.predict_class(video_t, video_d, t_bin_labels,d_bin_labels)

    # Early fusion (Audio + Video)
    print('Results for audio+video only...\n')
    audio_video_t = [feats[:555] for feats in t_features]
    audio_video_d = [feats[:555] for feats in d_features]
    # print len(video_d[0])
    # print Fusions.predict_regression(audio+video_t, audio+video_d, t_labels,d_labels)
    print Fusions.predict_class_forest(audio_video_t, audio_video_d, t_bin_labels,d_bin_labels)

    # Late fusion
    print('Late fusion results ...\n')
    Fusions.predict_class_majorityvote(model1 = (audio_t, audio_d), model2 = (video_t, video_d), model3 = (text_t, text_d), train_labels = t_bin_labels, test_labels = d_bin_labels)



run_experiments()