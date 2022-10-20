# MOPS-Takehome-Assessment
Submission for "MOPS Takehome Assessment: API Integration (python)" https://gist.github.com/humphriesjm/6030cd7857c37318104b5ab90b2cd591

# Brief description of project structure
- I have re-structured the project to have its entry point being `project/main/main.py`; moving general functions and classes to their own util scripts (`project/utils/`).
- This project has a few (not entirely rigorous due to time constraints) tests which are setup to run with github actions. Using `black`, `flake8` and `isort`; `/runtests` will check linting before using `pytest` to run all tests in `project/tests`.
- Functionally, the only used libary is `requests` which is used for the relevant api calls.

# Notes
- I have not put an emphasis on computational efficiency. A lot, if not all of the code in this code base could be improved in that regard, especially the database functions.
- I try to avoid comments where I can, communicating mainly via sensible variable name choices

