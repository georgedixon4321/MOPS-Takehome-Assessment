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


