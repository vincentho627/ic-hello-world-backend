# WhereThe

## About WhereThe

WhereThe is our team's submission to the IC Hello World 2021 hackaathon at Imperial College London. Our aim is simple: We believe that there is a need for a platform where people in local areas can report lost items, such as wallets, phones, keys etc., and notify others of located items that are potentially being found. We realise that there is an even greater demand for such a platform during times such as the COVID-19 pandemic, where traveling freely and attempting to retrace your steps may not be as easy a task as usual. We believe that with WhereThe, people can locate their lost items more easily through this additional virtual medium,  and retrieve these items with minimal exposure to other people (in the interests of health and safety). 

## Running the back-end of WhereThe

After cloning this repository, install all the required dependencies, such as Flask and SQLite3, with the following command at the root directory: 
```
pip install -r requirements.txt
```
Create SQL databases. 

Now initialise the local databases in Flask with the following commands, and start up the back-end server: 
```
flask drop_all
flask create_all
flask run
```
