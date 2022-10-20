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
    email_split_by_asperand = email.split("@")
    root_domain_split_by_point = email_split_by_asperand[1].split(".")
    row_data_to_be_added_to_database = {}
    row_data_to_be_added_to_database["name"] = email_split_by_asperand[0]
    row_data_to_be_added_to_database["email"] = email
    row_data_to_be_added_to_database["domain"] = root_domain_split_by_point[0]
    # The following two lines are part 2 additions (Never adds anyone with verkada domain to DB)
    if row_data_to_be_added_to_database["domain"] == "verkada":
        return
    row_data_to_be_added_to_database["topLevelName"] = root_domain_split_by_point[1]
    row_data_to_be_added_to_database["age"] = get_age_from_agify_api(
        name=row_data_to_be_added_to_database["name"]
    )
    row_data_to_be_added_to_database["gender"] = get_gender_from_genderize_api(
        name=row_data_to_be_added_to_database["name"]
    )
    row_data_to_be_added_to_database[
        "nationality"
    ] = get_most_likely_nationality_from_nationalize_api(
        name=row_data_to_be_added_to_database["name"]
    )

    dbInstance.addRow(tableName="Table1", rowData=row_data_to_be_added_to_database)

    json_output = json.dumps(row_data_to_be_added_to_database)
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
list_of_query_dicts = [
    {"keyToCheck": "age", "operatorChoice": ">", "criteria": 30, "sortBy": True},
    {"keyToCheck": "gender", "operatorChoice": "==", "criteria": "male"},
]


four_youngest_males_older_than_30 = dbInstance.getRows(
    tableName="Table1", listOfQueryDicts=list_of_query_dicts
)[:4]

# Part 2 Submission data
data_to_submit = {
    "name": "George Dixon",
    "queryData": json.dumps(four_youngest_males_older_than_30),
    "databaseContents": json.dumps(dbInstance.getVerkadaDB()),
}
data_to_submit_json = json.dumps(data_to_submit)
# verkada_api_request_post(dataToSubmitJSON)
