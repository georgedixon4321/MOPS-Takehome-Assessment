#!/usr/bin/env python
from project.utils.database import VerkadaDB


def test_get_verkada_db():
    dbInstance = VerkadaDB()
    dbInstance.addTable("TestTable")
    assert dbInstance.getVerkadaDB() == {"TestTable": {}}
