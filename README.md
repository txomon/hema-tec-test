How to use
==========

Code should run in python2 and python3 seamlessly. Tests however require
using pipenv to install and load all the dependencies.

Pipenv is the officially recommended packaging tool for python, and because
it's a best practice (even if people still use requirements.txt), I have 
done the project tests with it.

Go to https://docs.pipenv.org/ for installation instructions

A quick start if you have pipenv properly installed, run 
`pipenv install -d` and `pipenv run py.test` to run the tests.


Some assumptions
----------------

I have assumed that any data integrity error should make the script fail, and
tried my best to give a tip on what's wrong

I have avoided using CSV file reader because the format of the files is
broken, it uses CSV, but the data is structured in rows, not in columns.
This made me think that there might be some other wrong things with files
not in the training set, and have chosen to have full control on the
implementation

I supposed I could use pprint to emulate the output of the task_description

I stopped developing after I reached the 2:30h limit I have self
imposed.

There is 100% coverage, and because I stopped developing, I haven't configured
tox's setup.py requirement, although the code is prepared for it.

In total the project has taken 40mins of coding, 1:30h of testing 100% coverage
 and documenting part of the code that might not be clear 10 mins.
 
I have spent 20 mins creating this documentation, and 5 minutes to enable 100%
python2/3 compatibility, more specifically treatment of strings for tests and
dict ordering, which is a feature in python3.6 (that I am using), but is not
part of python2.7