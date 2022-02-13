#Udplatform Assignment

## How to run the project

Clone the project Repository
```
git clone 

```

Enter the project folder and create a virtual environment
``` 
$ cd  

$ python -m venv env

```

Activate the virtual environment
``` 
$ source env/bin/actvate #On linux Or Unix

$ source env/Scripts/activate #On Windows 
 
```

Install all requirements

```
$ pip install -r requirements.txt
```

Run the project in development

``` 
python3 app.py
``` 

##API Description

###Create User:
Method: POST with JSON Data
JSON must contain: username, first_name, last_name, user_type('Parent'/'Child')
For 'Parent' type user additionally provide: street, city, state, zip_code
For 'Children type user additionaly provide: parent
Endpoint:
```
/create
```

###Update User:
Method: POST with JSON Data
Json nust contain: username
Additional fields: Any of the user parameters excluding user_type. Adress attributes(street, city, state, zip_code) of Children type can not be updated. 'parent' attribute of Parent type user can not be updated.
Endpoint:
```
/edit
```

###Delete User:
Method: DELETE
Parameter: username
Endpoint:
```
/delete/<username>
```


