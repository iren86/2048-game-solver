requirements.txt file contains a list of all the packages for test environment, and their respective versions.
To install the same packages using the same versions please perform command below:

$ pip install -r requirements.txt

* Recommendation is to perform the command in isolated Python environment (Virtual Environment).
* More information here: http://docs.python-guide.org/en/latest/dev/virtualenvs/

To run test use following command:
$ python -m unittest com.solver.game.test.GamePageTest
