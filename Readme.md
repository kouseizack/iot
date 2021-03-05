Contains a server and Edge progrmamme.

Server-side - A flask based server handling post requests sent by client at the route "add_data" and adds data into a csv file on server side "op.csv"
Note: Flask server is run locally.
Server randomly either services the request and sends successful response or sends "401" for unsuccessful request.

Edge: Forever executing Edge programme responsible for reading streaming sensor data (here simulated by an exisiting "dataset.csv" file).

A queue is used to initially act as source of streaming data which contains all the data from "dataset.csv" file.

Main thread is responsible for taking care of streaming data ,if post request for these requests fail, then this data is pushed to local buffer which is sent by another thread worker_5 at a delay of 5 seconds.

