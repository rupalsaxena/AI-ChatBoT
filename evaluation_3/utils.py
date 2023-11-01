import os
import csv

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
    
    





