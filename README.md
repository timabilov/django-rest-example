# LiveSmart Backend Test

Details of the technical test for potential Backend engineers.


## Objective

We have provided a partially complete django instance, missing some key elements such as models and views.

We would like you to add the necessary components to implement a REST API to get and set details of a blood test.

These details should include a name, unique code, unit of measurement, lower range and upper range of expected results.

On the API response, there should also be a read only field called "ideal_range" that uses the values of upper and lower to build a human readable string.

We have included a testing file in bloodtests/tests/test_bloodtests.py, this will test for some of the functionality outlined in this document and we'd like to see the tests pass once you have completed the implementation. In addition the testing file should provide some information about expected status codes/formats/model names etc, that you can use in addition to the spec below.


## Installation

1. Please use Python 3.6 so make sure that is installed, we have provided a requirements.txt file to use with pip install to install all the necessary python packages for this task, please don't change the versions of any packages used.
3. Create a virtual environment, and activate it.
4. Install the necessary packages with:


```bash
pip install -r requirements.txt
```

5. Make your changes.

6. Django can then be run with:
```bash
python manage.py runserver
```

This will make available the API by default on 127.0.0.1:8000

7. Django can then be tested with:
```bash
pytest bloodtests/tests/test_bloodtests.py
```

Note that steps 6 and 7 will only work after you have made changes. If you run them before making changes you'll likely see errors or failed tests.


### Field requirements

code - varchar up to 4 characters in length
name - varchar up to 100 characters in length
unit - varchar up to 10 characters in length
lower - positive float
upper - positive float
lower or upper can be null but not both. If both are non null then require upper > lower.


## Spec of the API

1. The API has GET and POST methods.
2. It is to be requested with a code parameter on the url e.g. api/bloodtests/test/CHO where CHO is the code.
3. The API supports JSON.
4. The JSON output looks as follows:

```json
{
  "ideal_range": "21.0 <= value <= 45.0",
  "code": "CHO",
  "name": "Cholesterol",
  "unit": "mmol/L",
  "lower": 21,
  "upper": 45
}
```


## Approach

We would like you to ...

1. Implement the neccessary missing components to create this API. 
2. Ensure that the testing file in bloodtests/tests/test_bloodtests.py, when run, passes all tests. Note that if you run the test file before implementing your changes it will either fail the tests or raise errors, but once you've implemented your changes the tests should alll pass. 
3. Please create a repo on a hosting service like github, bitbucket and commit and push the whole project there. Including the files we provide and the ones you create/update. Please do this as you'd normally work, committing as often as you normally would etc.
4. Share this link with us so we can see what you've done and pull it down and run it.

## Additional information

Everything else you need to know to complete the task should be able to be determined from inspection of the code or the testing file.

Please don't modify the test file supplied, though you may of course add your own tests into another file.

As a guide we'd expect this to take around 2-4 hours, but we won't be timing it as such. If you could send a link to a completed repo within a few days that would be fine for us.

You can consult whatever resources you would in a real life situation.

Finally, if there's anything that isn't clear or you have questions, feel free to get in touch with me on brendan@getlivesmart.com.

