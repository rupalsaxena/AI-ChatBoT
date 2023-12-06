import pandas as pd
import numpy as np
from statsmodels.stats import inter_rater

#############################################
# etc.
#############################################
def percentile_to_num(p):
    return float(p.split("%")[0])

def reformat_ID(id):
    if ":" in id:
        return id.split(":")[1]
    else:
        return id

#############################################
# Main Functions
#############################################
def formatting(crowd_data:pd.DataFrame):
    crowd_data['LifetimeApprovalRate'] = crowd_data['LifetimeApprovalRate'].apply(percentile_to_num)
    crowd_data['Input1ID'] = crowd_data['Input1ID'].apply(reformat_ID)
    crowd_data['Input2ID'] = crowd_data['Input2ID'].apply(reformat_ID)
    crowd_data['Input3ID'] = crowd_data['Input3ID'].apply(reformat_ID)
    return crowd_data

def filtering_malicious_resp(crowd_data:pd.DataFrame):
    crowd_data = formatting(crowd_data)

    # Set the worktime threshold to detect 'Fast Deceivers'
    # the worktime threshold : 0.25 quantile point value of the group of workers having approval rate above 50%
    wt_golden_sampels = crowd_data.loc[crowd_data['LifetimeApprovalRate']>=50]['WorkTimeInSeconds']
    wt_threshold = wt_golden_sampels.quantile(.25)
    print(f"Worktime threshold : {wt_threshold}")
    # print(f"Counts of 'Malicious responses' by the Worker's Lifetime Approval Rate")
    # print(crowd_data.loc[crowd_data['WorkTimeInSeconds']<wt_threshold].groupby(['LifetimeApprovalRate']).count()['HITId'].sort_index(ascending=False))

    # Filtering 'Fast Deceivers'
    crowd_data_filtered = crowd_data.loc[crowd_data['WorkTimeInSeconds']>=wt_threshold]
    print(f"Total responses remaning after filtering 'Malicious responses'")
    print(f"{len(crowd_data)} -(Filtered)-> {len(crowd_data_filtered)}")
    print("Done! - Filtering Malicious Responses")
    return crowd_data_filtered

def aggregate_crowd_data(crowd_data:pd.DataFrame):
    group_element = ['HITTypeId', 'Input1ID', 'Input2ID', 'Input3ID']
    all_workers = crowd_data['WorkerId'].unique().tolist()
    aux_info = ['CORRECT','INCORRECT','FIXING']

    # Groupped by different type of questions
    grouped = crowd_data.groupby(group_element)
    all_groups = list(grouped.groups.keys())

    # define the crowdsourcing aggregation dataframe
    crowd_data_agg = pd.DataFrame(columns=group_element+all_workers+aux_info) # index=range(len(all_groups))
    for idx, (name, df_group) in enumerate(grouped):

        # Set the question inforamtion
        new_item = dict(zip(group_element, name))

        # Aggregate counts for correct vs incorrect
        worker_corr = set(df_group.loc[df_group['AnswerLabel']=='CORRECT', 'WorkerId'])
        worker_incorr = set(df_group.loc[df_group['AnswerLabel']=='INCORRECT', 'WorkerId'])
        new_item['CORRECT'] = len(list(worker_corr))
        new_item['INCORRECT'] = len(list(worker_incorr))
        
        # Aggregate fixed values if the worker said it is incorrect
        _df_group_has_fix = df_group.loc[df_group['AnswerLabel']=='INCORRECT']
        _df_group_has_fix = _df_group_has_fix.loc[_df_group_has_fix['FixPosition'].isin(['Object', 'Subject', 'Predicate'])]
        _df_group_has_fix = _df_group_has_fix.loc[~(_df_group_has_fix['FixValue'].isna())]
        set_fixval = _df_group_has_fix.groupby(['FixPosition','FixValue'])['HITId'].count().to_dict()
        set_fixval_dict = {}
        for fixval in set_fixval.keys():
            set_fixval_dict['item'] = fixval[0]
            set_fixval_dict['fixval'] = fixval[1]
            set_fixval_dict['count'] = set_fixval[fixval]
        new_item['FIXING'] = set_fixval_dict

        # Mark the workers '1(CORRECT)' / '0(INCORRECT)' / 'None(Not answered)'
        real_workers = df_group['WorkerId'].unique().tolist()
        for w in real_workers:
            w_ans = df_group.loc[df_group['WorkerId']==w]['AnswerLabel']
            real_worker_ans = int((w_ans == 'CORRECT').values[0])
            new_item[w] = real_worker_ans

        crowd_data_agg = pd.concat([crowd_data_agg, pd.DataFrame([new_item])], ignore_index=True)

    # crowd_data_agg.head()
    print("Done! - Aggregating Crowd Responses")
    return crowd_data_agg

def calc_interagreement_score(crowd_agg_data:pd.DataFrame, crowd_data:pd.DataFrame):

    group_element = ['HITTypeId', 'Input1ID', 'Input2ID', 'Input3ID']
    all_workers = crowd_data['WorkerId'].unique().tolist()

    crowd_data_processed = crowd_agg_data.copy()
    crowd_data_processed.drop(all_workers, axis=1, inplace=True)
    crowd_data_processed['SCORE'] = None

    log = {}
    for idx, row in crowd_agg_data.iterrows():

        # Find the workers who answered this question
        ans_workers = row[all_workers].notna()
        ans_workers = ans_workers[ans_workers].index
        # Find other questions which has including the same workers above and leave the answers of ans_workers only
        batch = crowd_agg_data[ans_workers].dropna()
        # Aggregate the count of answer category
        agg_answers = inter_rater.aggregate_raters(batch)[0]
        # Calculate inter-rater agreement score with this values.
        score = inter_rater.fleiss_kappa(agg_answers, method='fleiss')
        score = float("{:.5f}".format(score))
        # Assign the score on each row
        col = crowd_data_processed.columns.get_loc('SCORE')
        crowd_data_processed.iloc[idx, col] = score

        log[score] = (len(batch), ans_workers, crowd_data_processed.iloc[idx][group_element].tolist())
    # print(log)

    for k in log.keys():
        print(f"Score({k}):\t#Qs = {log[k][0]}\t\tWorkers{log[k][1]})")

    print("Done! - Calculating Inter-Rater Aggrement Score")

    return crowd_data_processed

def save_processed_crowd_data(crowd_data_processed:pd.DataFrame):
    path = './data/crowd_data_processed.json'
    mask = (crowd_data_processed['SCORE']>0) & (crowd_data_processed['Input2ID']!='indirectSubclassOf')
    crowd_data_processed = crowd_data_processed.loc[mask]
    crowd_data_processed.reset_index(drop=True, inplace=True)
    crowd_data_processed.to_json(path)
    crowd_data_processed.to_csv(path.replace('.json','.csv'))
    print("Done! - Saving preprocessed crowdsourcing data")
    print(path)

if __name__=="__main__":
    crowd_data = pd.read_table('./data/crowd_data/crowd_data.tsv')

    # Step 1. Filtering Malicious Responses
    print()
    crowd_data_filtered = filtering_malicious_resp(crowd_data)

    # Step 2. Aggregating Crowd Responses
    print()
    crowd_agg_data = aggregate_crowd_data(crowd_data_filtered)

    # Step 3. Calculating Inter-Rater Aggrement Score (Fleiss' Kappa)
    print()
    new_crowd_data = calc_interagreement_score(crowd_agg_data, crowd_data_filtered)

    # Save preprocessed crowdsourcing data
    print()
    save_processed_crowd_data(new_crowd_data)