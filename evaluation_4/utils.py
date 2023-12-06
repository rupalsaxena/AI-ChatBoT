import os
import csv
import re

def remove_special_characters(input_string):
    pattern = r'[^\w\s]'
    clean_string = re.sub(pattern, '', input_string)
    return clean_string

def log_to_csv(filename, msg, msg_time, reply, reply_time):
    if os.path.exists(filename):
        with open(filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerows([[msg, msg_time, reply, reply_time]])
    else:
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['msg', 'msg_time', 'reply', 'reply_time'])
            writer.writerows([[msg, msg_time, reply, reply_time]])
    
    
def remove_substrings(predicates, ids):
    updated_preds = []
    updated_ids = []

    for i in range(len(predicates)):
        current_pred = predicates[i]
        current_id = ids[i]
        is_substring = any(current_pred in other_element for j, other_element in enumerate(predicates) if i != j)
        
        if not is_substring:
            updated_preds.append(current_pred)
            updated_ids.append(current_id)
    return updated_preds, updated_ids