#!/usr/bin/env python
from project.utils.api import (
    get_age_from_agify_api,
    get_gender_from_genderize_api,
    get_most_likely_nationality_from_nationalize_api,
    verkada_api_request_post,
)
from project.utils.queries import runQuery

import json


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

    def generateNewPrimaryKey(self, tableName):
        if len(self._data[tableName]) == 0:
            return 0
        else:
            largestExistingKey = max(self._data[tableName].keys())
            return largestExistingKey + 1

    def rowCount(self, tableName):
        return len(self._data[tableName])

    def addRow(self, tableName, rowData):
        self._data[tableName][self.generateNewPrimaryKey(tableName)] = rowData

    def getPrimaryKeysForMatchingRows(self, tableName, matchingCriteria):
        primaryKeys = []
        table = self.getTable(tableName)
        for row in table:
            match = True
            for key, value in matchingCriteria.items():
                if table[row][key] != value:
                    match = False
            if match == True:
                primaryKeys.append(row)
        return primaryKeys

    def updateRows(self, tableName, matchingCriteria, updateInformation):
        rowsToUpdate = self.getPrimaryKeysForMatchingRows(tableName, matchingCriteria)
        table = self.getTable("Table1")
        for rowIndex in rowsToUpdate:
            for key, value in updateInformation.items():
                table[rowIndex][key] = value

    def deleteRows(self, tableName, matchingCriteria):
        rowsToUpdate = self.getPrimaryKeysForMatchingRows(tableName, matchingCriteria)
        table = self.getTable("Table1")
        for rowIndex in rowsToUpdate:
            del table[rowIndex]

    def getRows(self, tableName, listOfQueryDicts):
        """A very basic query system.
            Allows multiple comparison queries.
            Takes a list of dictionaries. Each dict requires "keyToCheck", "operatorChoice", "criteria".
            Takes the "keyToCheck" element of the row of the table and compares the value with "Criteria" using the given "operatorChoice".
            Has optional key "sortBy" which if labeled true will sort the rows in ascending order relative to the "keyToCheck" in that dict.
            If the optional "sortBy" key is provided in more than one dictionary it will use the last one found!
            """
        sortByKeyIndex = next((index for index, dict in enumerate(listOfQueryDicts) if "sortBy" in dict.keys()), None)
        if sortByKeyIndex is not None:
            sortByKey = listOfQueryDicts[sortByKeyIndex]["keyToCheck"]
        primaryKeys = []
        sortByValues = []
        table = self.getTable(tableName)
        firstQueryExecuted = False
        for query in listOfQueryDicts:
            for row in table:
                match = runQuery(toBeChecked=table[row][query["keyToCheck"]], operatorChoice=query["operatorChoice"], criteria=query["criteria"])
                # print(f"{table[row][query['keyToCheck']]} {query['operatorChoice']} {query['criteria']} : {match}")
                if match and not firstQueryExecuted and row not in primaryKeys:
                        primaryKeys.append(row)
                        sortByValues.append(table[row][sortByKey])
                if not match and firstQueryExecuted and row in primaryKeys:
                    # print(f"{table[row]['name']} has index {row} and is being removed from list")
                    indexToBeRemoved = primaryKeys.index(row)
                    primaryKeys.remove(row)
                    del sortByValues[indexToBeRemoved]
                # print(primaryKeys)

            firstQueryExecuted = True


        sortedPrimaryKeysBasedOnValuePairs = [pk for _, pk in sorted(zip(sortByValues, primaryKeys))]
        # print(sortedPrimaryKeysBasedOnValuePairs)
        return [table[row] for row in sortedPrimaryKeysBasedOnValuePairs]


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
    # post request below was used for part 1 submission
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

# Put code for Part 2 here

# Updating any rows with name of Kyle to be age 26 and from Bosnia (BA)
dbInstance.updateRows(
    tableName="Table1",
    matchingCriteria={"name": "Kyle"},
    updateInformation={"age": 26, "nationality": "BA"},
)
# Removing Craigs from the DB:
dbInstance.deleteRows(tableName="Table1", matchingCriteria={"name": "Craig"})

listOfQueryDicts =[{"keyToCheck": "age", "operatorChoice": ">", "criteria":30, "sortBy": True}, {"keyToCheck": "gender", "operatorChoice": "==", "criteria":"male"}]
youngestMalesOlderThanThirty = dbInstance.getRows(tableName='Table1',listOfQueryDicts=listOfQueryDicts)[:4]
# print("{" + "\n".join("{!r}: {!r},".format(k, v) for k, v in dbInstance.getTable('Table1').items()) + "}")
# for dictionary in youngestMalesOlderThanThirty:
#     print(dictionary)

def submitDataToAPI():
    data = {
        "name": "George Dixon",
        "queryData": json.dumps(youngestMalesOlderThanThirty),
        "databaseContents": json.dumps(dbInstance.getVerkadaDB()),
    }
    data_json = json.dumps(data)
    verkada_api_request_post(data_json)

submitDataToAPI()
