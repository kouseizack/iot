import csv
import queue
from collections import deque 
from threading import Thread
import requests
import time

buffer_queue = queue.Queue()
num_fetch_threads_local = 1
successful_req = 0

def send_request(url , data):
    payload = {'Timestamp': data[0],'Value': data[1] ,'Sensor': data[2] , 'Type': data[3]}
    global successful_req
    #post data to server
    try:
        resp = requests.post(url, data=payload)
        if(resp.status_code == 401):
            buffer_queue.put(data)
        else:
            successful_req += 1
        #print (resp.status_code)
    except requests.exceptions.RequestException as e:
        # catastrophic error. bail.
        buffer_queue.put(data)
    
def requestlocals(bq , url):
    while True:
        #print('%s: Looking for the next local data-point')
        print ('actual_served :' , successful_req , 'buffered :' , buffer_queue.qsize())
        buf_data = bq.get()
        buf_data[3] = "Buffered data"
        #print('Sending:', buf_data)
        #post data to server
        time.sleep(5)
        send_request(url , buf_data)
        bq.task_done()

def main():
    # Declaring deque  
    queue = deque() 
    url = "http://127.0.0.1:5000/add_data"

    for i in range(num_fetch_threads_local):
        worker_5 = Thread(target=requestlocals, args=(buffer_queue , url))
        worker_5.setDaemon(True)
        worker_5.start()

    with open('dataset.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                #print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                line = []
                line.extend([row[0] , row[1] , row[2]])
                queue.append(line)
                line_count += 1

    while(True):
        #buffer_queue.join()
        if(queue):
            stream_data = queue[0]
            stream_data.append('stream data')
            #print (stream_data)
            queue.popleft()
            send_request(url , stream_data)
            time.sleep(60)      

if __name__ == "__main__":
    main()