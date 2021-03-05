from flask import Flask, request , jsonify
import random
import time
from csv import writer
app = Flask(__name__)

@app.route('/success/<name>')
def success(name):
   return 'welcome %s' % name

@app.route('/add_data',methods = ['POST'])
def add_data():
    p = random.choice([0,1])
    
    if p:
        with open('op.csv', 'a') as f_object: 

            # Pass this file object to csv.writer() 
            # and get a writer object 
            writer_object = writer(f_object) 
        
            # Pass the list as an argument into 
            # the writerow()
            
            l = [request.form['Timestamp'] , request.form['Value'] , request.form['Sensor'] , request.form['Type']]
            writer_object.writerow(l) 
        
            #Close the file object 
            f_object.close()
        return jsonify(status_code="Task added successfully") , 201
    else:
        return jsonify(status_code="Unsuccessful") , 401

if __name__ == '__main__':
   app.run(debug = True)