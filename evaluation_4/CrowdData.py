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
    crowd_ans_agg = pd.DataFrame(columns=group_element+['WORKERS','CORRECT','INCORRECT']+['FIXING'])

    grouped = crowd_data.groupby(group_element)
    for idx, (name, df_group) in enumerate(grouped):
        new_item = dict(zip(group_element, name))

        # Count the number of answer type ['CORRECT','INCORRECT']
        # and Save the workers who respond this question
        worker_corr = set(df_group.loc[df_group['AnswerLabel']=='CORRECT', 'WorkerId'])
        worker_incorr = set(df_group.loc[df_group['AnswerLabel']=='INCORRECT', 'WorkerId'])
        crowd_ans = {'CORRECT': len(list(worker_corr)), 
                    'INCORRECT': len(list(worker_incorr))}
        crowd_ans['WORKERS'] = worker_corr.union(worker_incorr)

        # Check whether there is a information fixed by workers
        _df_group_has_fix = df_group.loc[df_group['AnswerLabel']=='INCORRECT']
        _df_group_has_fix = _df_group_has_fix.loc[_df_group_has_fix['FixPosition'].isin(['Object', 'Subject', 'Predicate'])]
        _df_group_has_fix = _df_group_has_fix.loc[~(_df_group_has_fix['FixValue'].isna())]
        set_fixval = _df_group_has_fix.groupby(['FixPosition','FixValue'])['HITId'].count().to_dict()
        set_fixval_dict = {}
        for fixval in set_fixval.keys():
            set_fixval_dict['item'] = fixval[0]
            set_fixval_dict['fixval'] = fixval[1]
            set_fixval_dict['count'] = set_fixval[fixval]
        crowd_ans['FIXING'] = set_fixval_dict
        
        # Add aggregated crowd data into new dataframe
        new_item.update(crowd_ans)
        crowd_ans_agg = pd.concat([crowd_ans_agg, pd.DataFrame([new_item])], ignore_index=True)

    crowd_ans_agg.fillna(0,inplace=True) # Replace NaN to 0

    print("Done! - Aggregating Crowd Responses")
    return crowd_ans_agg

def calc_interaggrement_score(crowd_data:pd.DataFrame):
    group_element = ['HITTypeId', 'Input1ID', 'Input2ID', 'Input3ID']
    crowd_ans_data = pd.DataFrame(columns=group_element+['CORRECT','INCORRECT']+['FIXING']+['SCORE'])

    _= {}
    for index, row in crowd_data.iterrows():
        new_item = row[group_element+['CORRECT','INCORRECT','FIXING']].to_dict()

        # Calculate Inter-Rater Agreement Score by the batch having same worker combination.
        ref_workers = row['WORKERS']
        batch = crowd_data.loc[crowd_data['WORKERS']==ref_workers][['CORRECT','INCORRECT']]
        score = inter_rater.fleiss_kappa(batch.to_numpy())
        new_item['SCORE'] = score

        crowd_ans_data = pd.concat([crowd_ans_data, pd.DataFrame([new_item])], ignore_index=True)
        
        _[score] = (len(batch),ref_workers)
    # crowd_ans_data.sort_values('INCORRECT', ascending=False)

    for k in _.keys():
        print(f"Score({k}):\t#Qs = {_[k][0]}\t\tWorkers{_[k][1]})")

    print("Done! - Calculating Inter-Rater Aggrement Score")
    return crowd_ans_data
    


if __name__=="__main__":
    crowd_data = pd.read_table('./data/crowd_data/crowd_data.tsv')

    # Step 1. Filtering Malicious Responses
    print()
    crowd_data = filtering_malicious_resp(crowd_data)

    # Step 2. Aggregating Crowd Responses
    print()
    crowd_data = aggregate_crowd_data(crowd_data)

    # Step 3. Calculating Inter-Rater Aggrement Score (Fleiss' Kappa)
    print()
    new_crowd_data = calc_interaggrement_score(crowd_data)

    # Save preprocessed crowdsourcing data
    new_crowd_data = new_crowd_data.loc[new_crowd_data['SCORE']>0]
    new_crowd_data = new_crowd_data.loc[new_crowd_data['Input2ID']!='indirectSubclassOf']
    new_crowd_data.reset_index(drop=True, inplace=True)
    new_crowd_data.to_csv('./data/crowd_data_processed.csv')
    new_crowd_data.to_json('./data/crowd_data_processed.json')