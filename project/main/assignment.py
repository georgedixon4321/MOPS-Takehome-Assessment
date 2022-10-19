#!/usr/bin/env python

import json

from project.utils.api import (
    get_age_from_agify_api, get_gender_from_genderize_api,
    get_most_likely_nationality_from_nationalize_api, verkada_api_request_post)

# Import any libraries you need

# Do not edit


class VerkadaDB:
    def __init__(self):
        self._data = {}

    # You may add to the class definition below this line
    def getVerkadaDB(self):
        return self._data

    def addTable(self, tableName):
        self._data[tableName] = {}

    def getTable(self, tableName):
        return self._data[tableName]

    def rowCount(self, tableName):
        return len(self._data[tableName])

    def addRow(self, tableName, rowData):
        self._data[tableName][self.rowCount(tableName)] = rowData

    # def getRows(self, tableName, matchingCriteria):
    #     returnedRows = []
    #     for row in self._data[tableName]:
    #         for item in row:
    #             if item in matchingCriteria:
    #                 returnedRows.append(item)
    #     return returnedRows

    # def updateRows(self, tableName, matchingCriteria, updateInformation):
    #     rowsToUpdate = self.getRows(self, tableName, matchingCriteria)

    # def deleteRows(self, tableName, matchingCriteria):
    #     for criteria in matchingCriteria:
    #         if not matchingCriteria in self._data[tableName]:
    #             return False
    #     del self._data[tableName][matchingCriteria]
    #     return True


# Do not edit
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
    verkada_api_request_post(json_output)
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

# Put code for Part 2 here
