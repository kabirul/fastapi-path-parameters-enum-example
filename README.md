#Requirements
Python 3.6+

FastAPI stands on the shoulders of giants:

Starlette for the web parts.
Pydantic for the data parts.

pip install fastapi
pip install "uvicorn[standard]"

#The simplest FastAPI file could look like this:

from fastapi import FastAPI
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

Copy that to a file main.py.
Run the live server: uvicorn main:app --reload

#The command uvicorn main:app refers to:
main: the file main.py (the Python "module").
app: the object created inside of main.py with the line app = FastAPI().
--reload: make the server restart after code changes. Only use for development.

In the output, there's a line with something like:
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
That line shows the URL where your app is being served, in your local machine.

Check it
Open your browser at http://127.0.0.1:8000

You will see the JSON response as:
{"message": "Hello World"}

Interactive API docs¶
Now go to http://127.0.0.1:8000/docs
You will see the automatic interactive API documentation (provided by Swagger UI)

Alternative API docs
And now, go to http://127.0.0.1:8000/redoc.
You will see the alternative automatic documentation (provided by ReDoc)

#Templates
You can use any template engine you want with FastAPI.
A common choice is Jinja2, the same one used by Flask and other tools.
There are utilities to configure it easily that you can use directly in your FastAPI application (provided by Starlette).
#Install dependencies
pip install jinja2

#Using Jinja2Templates
Import Jinja2Templates.
Create a templates object that you can re-use later.
Declare a Request parameter in the path operation that will return a template.
Use the templates you created to render and return a TemplateResponse, passing the request as one of the key-value pairs in the Jinja2 "context".

from fastapi.templating import Jinja2Templates

app = FastAPI()
...
templates = Jinja2Templates(directory="templates")

Notice that you have to pass the request as part of the key-value pairs in the context for Jinja2. So, you also have to declare it in your path operation.

By declaring response_class=HTMLResponse the docs UI will be able to know that the response will be HTML.

#Path Parameters
You can declare path "parameters" or "variables" with the same syntax used by Python format strings:

from fastapi import FastAPI
app = FastAPI()

@app.get("/items/{item_id}")
async def read_item(item_id):
    return {"item_id": item_id}

The value of the path parameter item_id will be passed to your function as the argument item_id.
So, if you run this example and go to http://127.0.0.1:8000/items/1, you will see a response of:
{"item_id":"1"}

#Path parameters with types
You can declare the type of a path parameter in the function, using standard Python type annotations:

from fastapi import FastAPI
app = FastAPI()

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}
In this case, item_id is declared to be an int.

#Data conversion
If you run this example and open your browser at http://127.0.0.1:8000/items/3, you will see a response of:
{"item_id":3}

Notice that the value your function received (and returned) is 3, as a Python int, not a string "3".
So, with that type declaration, FastAPI gives you automatic request "parsing".

#Data validation
But if you go to the browser at http://127.0.0.1:8000/items/foo, you will see a nice HTTP error of:

{
    "detail": [
        {
            "loc": [
                "path",
                "item_id"
            ],
            "msg": "value is not a valid integer",
            "type": "type_error.integer"
        }
    ]
}
because the path parameter item_id had a value of "foo", which is not an int.
The same error would appear if you provided a float instead of an int, as in: http://127.0.0.1:8000/items/4.2

So, with the same Python type declaration, FastAPI gives you data validation.
Notice that the error also clearly states exactly the point where the validation didn't pass.
This is incredibly helpful while developing and debugging code that interacts with your API.

#Pydantic
All the data validation is performed under the hood by Pydantic, so you get all the benefits from it. And you know you are in good hands.

You can use the same type declarations with str, float, bool and many other complex data types.


#Order matters
When creating path operations, you can find situations where you have a fixed path.
Like /users/me, let's say that it's to get data about the current user.
And then you can also have a path /users/{user_id} to get data about a specific user by some user ID.
Because path operations are evaluated in order, you need to make sure that the path for /users/me is declared before the one for /users/{user_id}:

from fastapi import FastAPI
app = FastAPI()

@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}

@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}

Otherwise, the path for /users/{user_id} would match also for /users/me, "thinking" that it's receiving a parameter user_id with a value of "me".


#Predefined values
If you have a path operation that receives a path parameter, but you want the possible valid path parameter values to be predefined, you can use a standard Python Enum.

Create an Enum class¶
Import Enum and create a sub-class that inherits from str and from Enum.

By inheriting from str the API docs will be able to know that the values must be of type string and will be able to render correctly.

Then create class attributes with fixed values, which will be the available valid values:

from enum import Enum

from fastapi import FastAPI


class ModelSize(str, Enum):
    small = "S"
    medium = "M"
    large = "L"


app = FastAPI()

@app.get("/models/{model_name}")
async def get_model(model_name: ModelSize):
    if model_name == ModelSize.small:
        return {"model_name": model_name, "message": "Small Size"}

    if model_name.value == "medium":
        return {"model_name": model_name, "message": "Medium Size"}

    return {"model_name": model_name, "message": "Large Size"}

