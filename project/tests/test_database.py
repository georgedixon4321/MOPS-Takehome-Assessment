#!/usr/bin/env python
from project.utils.database import VerkadaDB


def test_get_verkada_db():
    dbInstance = VerkadaDB()
    dbInstance.addTable("TestTable")
    assert dbInstance.getVerkadaDB() == {"TestTable": {}}


def test_get_table_from_verkada_db():
    dbInstance = VerkadaDB()
    dbInstance.addTable("TestTable")
    dbInstance.addRow("TestTable", {"name": "George", "action": "testing"})
    assert dbInstance.getTable("TestTable") == {
        0: {"name": "George", "action": "testing"}
    }


def test_generate_new_primary_key_verkada_db():
    dbInstance = VerkadaDB()
    dbInstance.addTable("TestTable")
    dbInstance.addRow("TestTable", {"name": "George", "action": "testing"})
    assert list(dbInstance.getTable("TestTable"))[0] == 0
    dbInstance.addRow("TestTable", {"name": "George", "action": "testing again"})
    assert list(dbInstance.getTable("TestTable"))[1] == 1
    dbInstance.deleteRows(tableName="TestTable", matchingCriteria={"name": "George"})
    dbInstance.addRow("TestTable", {"name": "not George", "action": "not testing"})
    assert list(dbInstance.getTable("TestTable"))[0] == 0
    dbInstance.addRow("TestTable", {"name": "Jim", "action": "testing"})
    dbInstance.addRow("TestTable", {"name": "Tim", "action": "testing"})
    dbInstance.deleteRows(tableName="TestTable", matchingCriteria={"name": "Jim"})
    dbInstance.addRow("TestTable", {"name": "New Jim", "action": "testing"})
    assert list(dbInstance.getTable("TestTable"))[2] == 3


def test_delete_items_in_database():
    dbInstance = VerkadaDB()
    dbInstance.addTable("TestTable")
    dbInstance.addRow("TestTable", {"name": "George", "action": "testing"})
    dbInstance.addRow("TestTable", {"name": "Alice", "action": "Not testing"})
    dbInstance.addRow("TestTable", {"name": "Bob", "action": "not not testing"})
    dbInstance.addRow("TestTable", {"name": "Jim", "action": "not not not testing"})
    dbInstance.addRow("TestTable", {"name": "Tim", "action": "not^4 testing"})
    dbInstance.addRow("TestTable", {"name": "Not Jim", "action": "testing"})
    dbInstance.deleteRows(tableName="TestTable", matchingCriteria={"action": "testing"})
    table_after_deletion_keys = dbInstance.getTable("TestTable").keys()
    assert 0 not in table_after_deletion_keys
    assert 5 not in table_after_deletion_keys
    assert 1 in table_after_deletion_keys
    assert 2 in table_after_deletion_keys
    assert 3 in table_after_deletion_keys
    assert 4 in table_after_deletion_keys


def test_update_rows_in_database():
    dbInstance = VerkadaDB()
    dbInstance.addTable("TestTable")
    dbInstance.addRow("TestTable", {"name": "George", "action": "testing"})
    dbInstance.addRow("TestTable", {"name": "Alice", "action": "Not testing"})
    dbInstance.addRow("TestTable", {"name": "Bob", "action": "not not testing"})
    dbInstance.addRow("TestTable", {"name": "Jim", "action": "not not not testing"})
    dbInstance.addRow("TestTable", {"name": "Tim", "action": "not^4 testing"})
    dbInstance.addRow("TestTable", {"name": "Not Jim", "action": "testing"})
    dbInstance.updateRows(
        tableName="TestTable",
        matchingCriteria={},
        updateInformation={"action": "testing"},
    )
    table_after_update = dbInstance.getTable("TestTable")
    for row in table_after_update:
        assert table_after_update[row]["action"] == "testing"
    dbInstance.updateRows(
        tableName="TestTable",
        matchingCriteria={"name": "Jim"},
        updateInformation={"action": "coding"},
    )
    table_after_update = dbInstance.getTable("TestTable")
    for row in table_after_update:
        if table_after_update[row]["name"] == "Jim":
            assert table_after_update[row]["action"] == "coding"
        else:
            assert table_after_update[row]["action"] == "testing"


def test_get_rows_database_queries():
    dbInstance = VerkadaDB()
    dbInstance.addTable("TestTable")
    dbInstance.addRow("TestTable", {"name": "George", "age": 25, "action": "testing"})
    dbInstance.addRow("TestTable", {"name": "Alice", "age": 22, "action": "testing"})
    dbInstance.addRow("TestTable", {"name": "Bob", "age": 22, "action": "testing"})
    dbInstance.addRow(
        "TestTable", {"name": "Jim", "age": 22, "action": "not not not testing"}
    )
    dbInstance.addRow("TestTable", {"name": "Tim", "age": 4, "action": "testing"})
    dbInstance.addRow("TestTable", {"name": "Not Jim", "age": 103, "action": "testing"})
    # test with no sort, three operations
    list_of_query_dicts = [
        {"keyToCheck": "age", "operatorChoice": ">", "criteria": 21},
        {"keyToCheck": "action", "operatorChoice": "==", "criteria": "testing"},
        {"keyToCheck": "age", "operatorChoice": "<", "criteria": 100},
    ]
    rows = dbInstance.getRows(
        tableName="TestTable", listOfQueryDicts=list_of_query_dicts
    )
    assert len(rows) == 3
    assert rows[0]["name"] == "George"
    assert rows[1]["name"] == "Alice"
    assert rows[2]["name"] == "Bob"
    # Check order of operation does not matter
    list_of_query_dicts = [
        {"keyToCheck": "age", "operatorChoice": "<", "criteria": 100},
        {"keyToCheck": "age", "operatorChoice": ">", "criteria": 21},
        {"keyToCheck": "action", "operatorChoice": "==", "criteria": "testing"},
    ]
    rows = dbInstance.getRows(
        tableName="TestTable", listOfQueryDicts=list_of_query_dicts
    )
    assert len(rows) == 3
    assert rows[0]["name"] == "George"
    assert rows[1]["name"] == "Alice"
    assert rows[2]["name"] == "Bob"
    # Check with sort ordering
    dbInstance.addTable("TestTable2")
    dbInstance.addRow("TestTable2", {"name": "George", "age": 25, "action": "testing"})
    dbInstance.addRow("TestTable2", {"name": "Alice", "age": 22, "action": "testing"})
    dbInstance.addRow("TestTable2", {"name": "Bob", "age": 22, "action": "testing"})
    dbInstance.addRow(
        "TestTable2", {"name": "Jim", "age": 22, "action": "not not not testing"}
    )
    dbInstance.addRow("TestTable2", {"name": "Tim", "age": 4, "action": "testing"})
    dbInstance.addRow(
        "TestTable2", {"name": "Not Jim", "age": 103, "action": "testing"}
    )
    list_of_query_dicts = [
        {"keyToCheck": "age", "operatorChoice": ">", "criteria": 21},
        {"keyToCheck": "action", "operatorChoice": "==", "criteria": "testing"},
        {"keyToCheck": "age", "operatorChoice": "<", "criteria": 100},
    ]
    rows = dbInstance.getRows(
        tableName="TestTable2", listOfQueryDicts=list_of_query_dicts, sortBy="age"
    )
    assert len(rows) == 3
    assert rows[0]["name"] == "Alice"
    assert rows[1]["name"] == "Bob"
    assert rows[2]["name"] == "George"
    # Check with ordering by str rather than int
    dbInstance.addTable("TestTable3")
    dbInstance.addRow("TestTable3", {"name": "Z", "age": 25, "action": "testing"})
    dbInstance.addRow("TestTable3", {"name": "C", "age": 22, "action": "testing"})
    dbInstance.addRow("TestTable3", {"name": "B", "age": 22, "action": "testing"})
    dbInstance.addRow(
        "TestTable3", {"name": "A", "age": 22, "action": "not not not testing"}
    )
    dbInstance.addRow("TestTable3", {"name": "D", "age": 4, "action": "testing"})
    dbInstance.addRow("TestTable3", {"name": "G", "age": 103, "action": "testing"})
    list_of_query_dicts = [
        {"keyToCheck": "age", "operatorChoice": "<", "criteria": 100},
    ]
    rows = dbInstance.getRows(
        tableName="TestTable3", listOfQueryDicts=list_of_query_dicts, sortBy="name"
    )
    assert len(rows) == 5
    assert rows[0]["name"] == "A"
    assert rows[1]["name"] == "B"
    assert rows[2]["name"] == "C"
    assert rows[3]["name"] == "D"
    assert rows[4]["name"] == "Z"
