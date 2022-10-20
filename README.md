# MOPS-Takehome-Assessment
Submission for "MOPS Takehome Assessment: API Integration (python)" https://gist.github.com/humphriesjm/6030cd7857c37318104b5ab90b2cd591

# Brief description of project structure
- I have re-structured the project to have its entry point being `project/main/main.py`; moving general functions and classes to their own util scripts (`project/utils/`).
- This project has a few tests for the database class which are setup to run with github actions. Using `black`, `flake8` and `isort`; the `runtests` script will check linting before using `pytest` to run all tests in `project/tests`.
- Functionally, the only used library is `requests` which is used for the relevant api calls.

# Notes
- I have not put an emphasis on computational efficiency. A lot, if not all of the code in this code base could be improved in that regard, especially the database functions. This was partially due to the fact I don't think it entirely necessary for a project such as this, especially with the single api requests as bottleneck. That being said, had I have had more time I would have optimised the database functions, especially the `getRows` function.
- I try to avoid comments where I can, communicating mainly via sensible variable name choices
- I have commented out any post request triggers in `main.py`. Also, have left a few prints within more complex functions if you wish to see how they work visually.

# Local Setup
- To set the project up locally, please install pyenv locally and run the build script in the root directory of this project.
- This will install all relevant dependencies within a virtual environment and you are good to go :)

