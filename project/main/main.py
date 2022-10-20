#!/usr/bin/env python
from project.utils.api import (  # verkada_api_request_post,
    get_age_from_agify_api,
    get_gender_from_genderize_api,
    get_most_likely_nationality_from_nationalize_api,
)
from project.utils.database import VerkadaDB

import json

dbInstance = VerkadaDB()

dbInstance.addTable("Table1")


def lambda_handler(json_input):

    global dbInstance
    json_input_to_python_dict = json.loads(json_input)
    email = json_input_to_python_dict["email"]
    emailSplitByAsperand = email.split("@")
    rootDomainSplitByPoint = emailSplitByAsperand[1].split(".")
    rowDataToBeAddedToDB = {}
    rowDataToBeAddedToDB["name"] = emailSplitByAsperand[0]
    rowDataToBeAddedToDB["email"] = email
    rowDataToBeAddedToDB["domain"] = rootDomainSplitByPoint[0]
    # The following two lines are part 2 additions (Never adds anyone with verkada domain to DB)
    if rowDataToBeAddedToDB["domain"] == "verkada":
        return
    rowDataToBeAddedToDB["topLevelName"] = rootDomainSplitByPoint[1]
    rowDataToBeAddedToDB["age"] = get_age_from_agify_api(
        name=rowDataToBeAddedToDB["name"]
    )
    rowDataToBeAddedToDB["gender"] = get_gender_from_genderize_api(
        name=rowDataToBeAddedToDB["name"]
    )
    rowDataToBeAddedToDB[
        "nationality"
    ] = get_most_likely_nationality_from_nationalize_api(
        name=rowDataToBeAddedToDB["name"]
    )

    dbInstance.addRow(tableName="Table1", rowData=rowDataToBeAddedToDB)

    json_output = json.dumps(rowDataToBeAddedToDB)
    # post request below was used for part 1 submission, have commented out to avoid resubmissions
    # verkada_api_request_post(json_output)
    return json_output


# Do not edit
lambda_handler(json.dumps({"email": "John@acompany.com"}))
lambda_handler(json.dumps({"email": "Willy@bcompany.org"}))
lambda_handler(json.dumps({"email": "Kyle@ccompany.com"}))
lambda_handler(json.dumps({"email": "Georgie@dcompany.net"}))
lambda_handler(json.dumps({"email": "Karen@eschool.edu"}))
lambda_handler(json.dumps({"email": "Annie@usa.gov"}))
lambda_handler(json.dumps({"email": "Elvira@fcompay.org"}))
lambda_handler(json.dumps({"email": "Juan@gschool.edu"}))
lambda_handler(json.dumps({"email": "Julie@hcompany.com"}))
lambda_handler(json.dumps({"email": "Pierre@ischool.edu"}))
lambda_handler(json.dumps({"email": "Ellen@canada.gov"}))
lambda_handler(json.dumps({"email": "Craig@jcompany.org"}))
lambda_handler(json.dumps({"email": "Juan@kcompany.net"}))
lambda_handler(json.dumps({"email": "Jack@verkada.com"}))
lambda_handler(json.dumps({"email": "Jason@verkada.com"}))
lambda_handler(json.dumps({"email": "Billy@verkada.com"}))
lambda_handler(json.dumps({"email": "Brent@verkada.com"}))

# Part 2

# Updating any rows with name of Kyle to be age 26 and from Bosnia (BA)
dbInstance.updateRows(
    tableName="Table1",
    matchingCriteria={"name": "Kyle"},
    updateInformation={"age": 26, "nationality": "BA"},
)
# Removing Craigs from the DB:
dbInstance.deleteRows(tableName="Table1", matchingCriteria={"name": "Craig"})

# Queries to run sequentially
listOfQueryDicts = [
    {"keyToCheck": "age", "operatorChoice": ">", "criteria": 30, "sortBy": True},
    {"keyToCheck": "gender", "operatorChoice": "==", "criteria": "male"},
]

# youngest 4 males older than 30
youngestMalesOlderThanThirty = dbInstance.getRows(
    tableName="Table1", listOfQueryDicts=listOfQueryDicts
)[:4]

# Part 2 Submission data
dataToSubmit = {
    "name": "George Dixon",
    "queryData": json.dumps(youngestMalesOlderThanThirty),
    "databaseContents": json.dumps(dbInstance.getVerkadaDB()),
}
dataToSubmitJSON = json.dumps(dataToSubmit)
# verkada_api_request_post(dataToSubmitJSON)
