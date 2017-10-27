import Fusions
import pandas
import os


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

    new_file = open('train_multimodal_features_revisedAUonly.csv', 'w')
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

    new_file = open('dev_multimodal_features_average.csv', 'w')
    new_file.write(','.join(feature_names) + '\n')
    for feat_list in dev_data:
        new_file.write(','.join([str(mm) for mm in feat_list]) + '\n')
    new_file.close()

    print('Done!')


def run_experiments():
    print('\nRunning SVM experiments...\n')
    path = "/Users/michellemorales/Desktop/MoralesDocs/DAIC_WOZ/"

    # path = "/Users/morales/Desktop/Dissertation/"
    # Get training labels
    # train_csv = path+'Labels/training_split.csv'
    # train_df = pandas.read_csv(train_csv)
    # train_labels = {}
    # for row in train_df.iterrows():
    #     row = row[1]
    #     train_labels[str(row['Participant_ID'])] = {'binary': row['PHQ_Binary'],
    #                                                 'score': row['PHQ_Score'], 'gender': row['Gender']}
    # Get dev labels
    # dev_csv = path+'Labels/dev_split.csv'
    # dev_df = pandas.read_csv(dev_csv)
    # dev_labels = {}
    # for row in dev_df.iterrows():
    #     row = row[1]
    #     dev_labels[str(row['Participant_ID'])] = {'binary': row['PHQ_Binary'],
    #                                               'score': row['PHQ_Score'], 'gender': row['Gender']}
    # print("Done loading data labels...\n")

    # Load features for train and dev
    train_data = pandas.read_csv(path+'Early_Features/train_multimodal_features.csv')
    dev_data =  pandas.read_csv(path+'Early_Features/dev_multimodal_features.csv')

    # print('Done loading data...\n')
    # Get training data & labels for features
    # t_labels = []
    # t_bin_labels = []
    # t_features = []
    # for row in train_data.iterrows():
    #     part_id = str(int(row[1][0]))
    #     features = row[1][1:].values
    #     t_features.append(features)
    #     label = train_labels[part_id]['score']
    #     b_label = train_labels[part_id]['binary']
    #     t_labels.append(label)
    #     t_bin_labels.append(b_label)
    # Get dev data & labels for features
    # d_labels = []
    # d_bin_labels = []
    # d_features = []
    # for row in dev_data.iterrows():
    #     part_id = str(int(row[1][0]))
    #     features = row[1][1:].values # Features will be off by one cell
    #     d_features.append(features)
    #     label = dev_labels[part_id]['score']
    #     b_label = dev_labels[part_id]['binary']
    #     d_labels.append(label)
    #     d_bin_labels.append(b_label)



    # print 'Random binary baseline = ', float(d_bin_labels.count(0)) / len(d_bin_labels)

    audio_names =  train_data.columns[1:371]
    # video_names = train_data.columns[371: 556]
    video_names = train_data.columns[446:546] # Look at AUs only
    text_names = train_data.columns[556:]
    syntax_names = train_data.columns[-85:]

    # ----------------- EXPERIMENT: Evaluating Informed Early Fusion ----------------- #

    # GET LABELS
    train_csv = path+'Labels/training_split.csv'
    train_df = pandas.read_csv(train_csv)
    dev_csv = path+'Labels/dev_split.csv'
    dev_df = pandas.read_csv(dev_csv)
    labels = {}
    for row in train_df.iterrows():
        row = row[1]
        labels[str(row['Participant_ID'])] = {'binary': row['PHQ_Binary'],
                                                    'score': row['PHQ_Score'], 'gender': row['Gender']}
    for row in dev_df.iterrows():
        row = row[1]
        labels[str(row['Participant_ID'])] = {'binary': row['PHQ_Binary'],
                                                  'score': row['PHQ_Score'], 'gender': row['Gender']}

    # Get informed features
    # informed_path = path+'Informed_Features/Informed_Features/'
    informed_path = path+'Informed_Features/'
    informed_files = os.listdir(informed_path)[1:]
    included_ids = []
    informed_features = []
    bin_labels_informed = []
    count = 0

    for i, f in enumerate(informed_files):
        data = pandas.read_csv(informed_path+f)
        informed_names = data.columns
        features = data.iloc[0].values
        my_id = f.replace('_informed.csv','')
        if my_id in labels.keys():
            count += 1
            bin_label = labels[my_id]['binary']
            bin_labels_informed.append(bin_label)
            included_ids.append(my_id)
            informed_features.append(features)

    features = {}
    for row in train_data.iterrows():
        part_id = str(int(row[1][0]))
        if part_id in included_ids:
            feats = row[1][1:].values
            features[part_id] = feats
    for row in dev_data.iterrows():
        part_id = str(int(row[1][0]))
        if part_id in included_ids:
            feats = row[1][1:].values
            features[part_id] = feats

    all_features = []
    bin_labels = []
    for ID in included_ids:
        b_label = labels[ID]['binary']
        bin_labels.append(b_label)
        all_features.append(features[ID])

    # Audio only
    audio = [feats[:370] for feats in all_features]
    print('Results for audio only...\n')
    best_names, best = Fusions.get_best_features(audio, bin_labels, audio_names.tolist())
    # Fusions.plot_coefficients(best, bin_labels, best_names)
    print bin_labels.count(0), bin_labels.count(1)
    # Fusions.predict_class_cv(best, bin_labels)
    # Fusions.predict_class_cv(audio, bin_labels)

    # # Syntax only
    syntax = [feats[-85:] for feats in all_features]
    print('Syntax results...\n')
    # # Fusions.plot_best_features(syntax,bin_labels,syntax_names.tolist())
    best_names, best = Fusions.get_best_features(syntax,bin_labels,syntax_names.tolist())
    # # Fusions.predict_class_cv(best, bin_labels)
    # Fusions.plot_coefficients(syntax, bin_labels, syntax_names.tolist())
    # # Fusions.predict_class_cv(syntax, bin_labels)
    #
    # # Early fusion
    early = []
    for i, f in enumerate(audio):
        early.append(audio[i].tolist() + syntax[i].tolist())
    print('Early fusion results...\n')
    best_names, best = Fusions.get_best_features(early, bin_labels_informed, audio_names.tolist()+syntax_names.tolist())
    # # Fusions.predict_class_cv(best, bin_labels)
    # # Fusions.predict_class_cv(early, bin_labels)
    Fusions.plot_coefficients(best, bin_labels, best_names)
    #
    # # Informed fusion
    print('Informed fusion results...\n')
    # Fusions.predict_class_cv(informed_features, bin_labels_informed)
    best_names, best = Fusions.get_best_features(informed_features, bin_labels_informed, informed_names.tolist())
    # Fusions.predict_class_cv(best, bin_labels_informed)
    # Fusions.plot_best(best,bin_labels_informed, best_names)
    best_names = [s+'_mean' for s in best_names]
    # Fusions.plot_coefficients(best, bin_labels, best_names)

    # # Combine early + informed fusion
    # print('Early + Informed fusion results...\n')
    # combined = []
    # for i, flist in enumerate(early):
    #     combined.append(flist+informed_features[i].tolist())
    # best_names, best = Fusions.get_best_features(combined, bin_labels_informed, audio_names.tolist()+syntax_names.tolist()+informed_names.tolist())
    # Fusions.predict_class_cv(best, bin_labels)
    # # # Fusions.predict_class_cv(combined, bin_labels_informed)
    # Fusions.plot_best(best, bin_labels_informed, best_names)


    # PCA + early

    # Video only
    # Text only
    # print('Results for text only...\n')
    # text_t = [feats[555:] for feats in t_features]
    # text_d = [feats[555:] for feats in d_features]
    # print len(text_t[0])
    # print Fusions.predict_regression(text_t,text_d,t_labels,d_labels)
    # print Fusions.predict_class(text_t,text_d,t_bin_labels,d_bin_labels)
    # Fusions.upsample_data(text_t, t_bin_labels, text_names, text_d, d_bin_labels)
    # Video only
    # print('Results for video only...\n')
    # video_t = [feats[370:555] for feats in t_features]
    # video_d = [feats[370:555] for feats in d_features]
    # Look at AUs only
    # video_t = [feats[445:545] for feats in t_features]
    # print "Number of features", len(video_t[0])
    # video_d = [feats[445:545] for feats in d_features]
    # print len(video_d[0])
    # print Fusions.predict_regression(video_t, video_d, t_labels,d_labels)
    # print Fusions.predict_class(video_t, video_d, t_bin_labels,d_bin_labels)
    # Try upsampling on each unimodal dataset
    # Fusions.upsample_data(video_t, t_bin_labels, video_names, video_d, d_bin_labels)
    #
    # # Early fusion
    # early_train = []
    # early_dev = []
    #
    # for i, f in enumerate(audio_t):
    #     early = audio_t[i].tolist() +video_t[i].tolist()+text_t[i].tolist()
    #     early_train.append(early)
    #
    # for i, f in enumerate(audio_d):
    #     early_dev.append(audio_d[i].tolist() + video_d[i].tolist() + text_d[i].tolist())
    #
    # # print('Early fusion results...\n')
    # # print Fusions.predict_regression(early_train, early_dev, t_labels, d_labels)
    # # print Fusions.predict_class(early_train, early_dev, t_bin_labels, d_bin_labels)
    #
    # print('Early fusion with PCA results...\n')
    # t_pca, d_pca = Fusions.add_pca(1000, early_train, early_dev)
    # print Fusions.predict_regression(t_pca, d_pca, t_labels, d_labels)
    # print Fusions.predict_class(t_pca, d_pca, t_bin_labels, d_bin_labels)
    #
    # # Late fusion
    # # print('Late fusion results ...\n')
    # # Fusions.predict_class_majorityvote(model1 = (audio_t, audio_d), model2 = (video_t, video_d), model3 = (text_t, text_d), train_labels = t_bin_labels, test_labels = d_bin_labels)

run_experiments()

def run_experiments_avg():
    print('\nRunning SVM experiments...\n')
    path = "/Users/michellemorales/Desktop/MoralesDocs/DAIC_WOZ/"

    # path = "/Users/morales/Desktop/Dissertation/"
    # Get training labels
    # train_csv = path+'Labels/training_split.csv'
    # train_df = pandas.read_csv(train_csv)
    # train_labels = {}
    # for row in train_df.iterrows():
    #     row = row[1]
    #     train_labels[str(row['Participant_ID'])] = {'binary': row['PHQ_Binary'],
    #                                                 'score': row['PHQ_Score'], 'gender': row['Gender']}
    # Get dev labels
    # dev_csv = path+'Labels/dev_split.csv'
    # dev_df = pandas.read_csv(dev_csv)
    # dev_labels = {}
    # for row in dev_df.iterrows():
    #     row = row[1]
    #     dev_labels[str(row['Participant_ID'])] = {'binary': row['PHQ_Binary'],
    #                                               'score': row['PHQ_Score'], 'gender': row['Gender']}
    # print("Done loading data labels...\n")

    # Load features for train and dev
    train_data = pandas.read_csv(path+'Early_Features/train_multimodal_features_avg.csv')
    dev_data =  pandas.read_csv(path+'Early_Features/dev_multimodal_features_avg.csv')

    # print('Done loading data...\n')
    # Get training data & labels for features
    # t_labels = []
    # t_bin_labels = []
    # t_features = []
    # for row in train_data.iterrows():
    #     part_id = str(int(row[1][0]))
    #     features = row[1][1:].values
    #     t_features.append(features)
    #     label = train_labels[part_id]['score']
    #     b_label = train_labels[part_id]['binary']
    #     t_labels.append(label)
    #     t_bin_labels.append(b_label)
    # Get dev data & labels for features
    # d_labels = []
    # d_bin_labels = []
    # d_features = []
    # for row in dev_data.iterrows():
    #     part_id = str(int(row[1][0]))
    #     features = row[1][1:].values # Features will be off by one cell
    #     d_features.append(features)
    #     label = dev_labels[part_id]['score']
    #     b_label = dev_labels[part_id]['binary']
    #     d_labels.append(label)
    #     d_bin_labels.append(b_label)



    # print 'Random binary baseline = ', float(d_bin_labels.count(0)) / len(d_bin_labels)

    audio_names =  train_data.columns[1:75]
    # video_names = train_data.columns[371: 556]
    video_names = train_data.columns[446:546] # Look at AUs only
    text_names = train_data.columns[556:]
    syntax_names = train_data.columns[-17:]
    # print audio_names
    # print syntax_names
    # print len(audio_names), len(syntax_names)

    # ----------------- EXPERIMENT: Evaluating Informed Early Fusion ----------------- #

    # GET LABELS
    train_csv = path+'Labels/training_split.csv'
    train_df = pandas.read_csv(train_csv)
    dev_csv = path+'Labels/dev_split.csv'
    dev_df = pandas.read_csv(dev_csv)
    labels = {}
    for row in train_df.iterrows():
        row = row[1]
        labels[str(row['Participant_ID'])] = {'binary': row['PHQ_Binary'],
                                                    'score': row['PHQ_Score'], 'gender': row['Gender']}
    for row in dev_df.iterrows():
        row = row[1]
        labels[str(row['Participant_ID'])] = {'binary': row['PHQ_Binary'],
                                                  'score': row['PHQ_Score'], 'gender': row['Gender']}

    # Get informed features
    # informed_path = path+'Informed_Features/Informed_Features/'
    informed_path = path+'Informed_Features/'
    informed_files = os.listdir(informed_path)[1:]
    included_ids = []
    informed_features = []
    bin_labels_informed = []
    count = 0
    for i, f in enumerate(informed_files):
        data = pandas.read_csv(informed_path+f)
        features = data.iloc[0].values
        my_id = f.replace('_informed.csv','')
        if my_id in labels.keys():
            count += 1
            bin_label = labels[my_id]['binary']
            bin_labels_informed.append(bin_label)
            included_ids.append(my_id)
            informed_features.append(features)

    features = {}
    for row in train_data.iterrows():
        part_id = str(int(row[1][0]))
        if part_id in included_ids:
            feats = row[1][1:].values
            features[part_id] = feats
    for row in dev_data.iterrows():
        part_id = str(int(row[1][0]))
        if part_id in included_ids:
            feats = row[1][1:].values
            features[part_id] = feats

    all_features = []
    bin_labels = []
    for ID in included_ids:
        b_label = labels[ID]['binary']
        bin_labels.append(b_label)
        all_features.append(features[ID])

    # Audio only
    audio = [feats[:74] for feats in all_features]
    print('Results for audio only...\n')
    Fusions.predict_class_cv(audio, bin_labels)


    # Syntax only
    syntax = [feats[-17:] for feats in all_features]
    print('Syntax results...\n')
    # Fusions.plot_best_features(syntax,bin_labels,syntax_names.tolist())
    Fusions.predict_class_cv(syntax, bin_labels)

    # Early fusion
    early = []
    for i, f in enumerate(audio):
        early.append(audio[i].tolist() + syntax[i].tolist())
    print('Early fusion results...\n')
    Fusions.predict_class_cv(early, bin_labels)

    # Informed fusion
    print('Informed fusion results...\n')
    Fusions.predict_class_cv(informed_features, bin_labels_informed)

    # Combine early + informed fusion
    print('Early + Informed fusion results...\n')
    combined = []
    for i, flist in enumerate(early):
        combined.append(flist+informed_features[i].tolist())
    Fusions.predict_class_cv(combined, bin_labels_informed)


    # PCA + early

    # Video only
    # Text only
    # print('Results for text only...\n')
    # text_t = [feats[555:] for feats in t_features]
    # text_d = [feats[555:] for feats in d_features]
    # print len(text_t[0])
    # print Fusions.predict_regression(text_t,text_d,t_labels,d_labels)
    # print Fusions.predict_class(text_t,text_d,t_bin_labels,d_bin_labels)
    # Fusions.upsample_data(text_t, t_bin_labels, text_names, text_d, d_bin_labels)
    # Video only
    # print('Results for video only...\n')
    # video_t = [feats[370:555] for feats in t_features]
    # video_d = [feats[370:555] for feats in d_features]
    # Look at AUs only
    # video_t = [feats[445:545] for feats in t_features]
    # print "Number of features", len(video_t[0])
    # video_d = [feats[445:545] for feats in d_features]
    # print len(video_d[0])
    # print Fusions.predict_regression(video_t, video_d, t_labels,d_labels)
    # print Fusions.predict_class(video_t, video_d, t_bin_labels,d_bin_labels)
    # Try upsampling on each unimodal dataset
    # Fusions.upsample_data(video_t, t_bin_labels, video_names, video_d, d_bin_labels)
    #
    # # Early fusion
    # early_train = []
    # early_dev = []
    #
    # for i, f in enumerate(audio_t):
    #     early = audio_t[i].tolist() +video_t[i].tolist()+text_t[i].tolist()
    #     early_train.append(early)
    #
    # for i, f in enumerate(audio_d):
    #     early_dev.append(audio_d[i].tolist() + video_d[i].tolist() + text_d[i].tolist())
    #
    # # print('Early fusion results...\n')
    # # print Fusions.predict_regression(early_train, early_dev, t_labels, d_labels)
    # # print Fusions.predict_class(early_train, early_dev, t_bin_labels, d_bin_labels)
    #
    # print('Early fusion with PCA results...\n')
    # t_pca, d_pca = Fusions.add_pca(1000, early_train, early_dev)
    # print Fusions.predict_regression(t_pca, d_pca, t_labels, d_labels)
    # print Fusions.predict_class(t_pca, d_pca, t_bin_labels, d_bin_labels)
    #
    # # Late fusion
    # # print('Late fusion results ...\n')
    # # Fusions.predict_class_majorityvote(model1 = (audio_t, audio_d), model2 = (video_t, video_d), model3 = (text_t, text_d), train_labels = t_bin_labels, test_labels = d_bin_labels)
