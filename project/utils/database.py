#!/usr/bin/env python
from project.utils.queries import run_query


class VerkadaDB:
    def __init__(self):
        self._data = {}

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
            if match is True:
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
        For the first element of the query dictionary takes the "keyToCheck" element of the row of the table and compares the value with "Criteria" using the given "operatorChoice".
        Once matches are found it adds the index to an array, every query iteration after this it will remove non matches from the index list.
        Has optional key "sortBy" which if labeled true will sort the rows in ascending order relative to the "keyToCheck" in that dict.
        If the optional "sortBy" key is provided in more than one dictionary it will use the last one found!
        """
        sortByKeyIndex = next(
            (
                index
                for index, dict in enumerate(listOfQueryDicts)
                if "sortBy" in dict.keys()
            ),
            None,
        )
        if sortByKeyIndex is not None:
            sortByKey = listOfQueryDicts[sortByKeyIndex]["keyToCheck"]
        primaryKeys = []
        sortByValues = []
        table = self.getTable(tableName)
        firstQueryExecuted = False
        for query in listOfQueryDicts:
            for row in table:
                match = run_query(
                    to_be_checked=table[row][query["keyToCheck"]],
                    operator_choice=query["operatorChoice"],
                    criteria=query["criteria"],
                )
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

        sortedPrimaryKeysBasedOnValuePairs = [
            pk for _, pk in sorted(zip(sortByValues, primaryKeys))
        ]
        # print(sortedPrimaryKeysBasedOnValuePairs)
        return [table[row] for row in sortedPrimaryKeysBasedOnValuePairs]
