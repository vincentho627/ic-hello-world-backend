# WhereThe

## About WhereThe

WhereThe is our team's submission to the IC Hello World 2021 hackaathon at Imperial College London. Our aim is simple: We believe that there is a need for a platform where people in local areas can **report lost items**, such as wallets, phones, keys etc., and **notify others of located items** that are potentially being found. We realise that there is an even greater demand for such a platform during times such as the COVID-19 pandemic, where traveling freely and attempting to retrace your steps may not be as easy a task as usual. We believe that with WhereThe, people can locate their lost valuables more easily through this additional virtual medium, and connect with the people who helped find these items with minimal exposure, in the interests of health and safety.

## Running the back-end of WhereThe

### Installing dependencies

After cloning this repository, install all the required dependencies, such as Flask and SQLite3, with the following command at the root directory: 
```
pip install -r requirements.txt
```

### Creating a local SQLite3 database

Then, pick a directory of your choice and run the following commands to create a local SQLite3 database on your device: 
```
sqlite3 ic-hello-world.db
```
Now go into the `config.py` file in the root directory of the repository and edit the `SQL_DATABASE_URI` field to tell Flask where the database you just created is, for example: 
```
# Unix / Mac (Note the four leading slashes)
SQL_DATABASE_URI = sqlite:////absolute/path/to/ic-hello-world.db
# Windows (Note three leading forward slashes and backslash escapes)
SQL_DATABASE_URI = sqlite:///C:\absolute\path\to\ic-hello-world.db
# Windows (Alternative using raw string)
SQL_DATABASE_URI = r'sqlite:///C:\absolute\path\to\ic-hello-world.db'

```

### Running the Flask back-end

Now initialise the local databases in Flask with the following commands, and start up the back-end server: 
```
flask drop_all
flask create_all
flask run
```

# Running the front-end of WhereThe

After completing the steps above, see the [GitHub repository of the front-end of WhereThe](https://github.com/vincentho627/ic-hello-world-frontend) and follow the instructions listed there. You will then have the complete platform set up and ready to test on your local device. 
