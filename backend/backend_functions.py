from database import *
from os import getcwd

def start_database(name,path=getcwd()):
    database = DataBase(name,path)
    
    if not database.Exists:
        database.create()
        pass
    
    database.connect()
    database.open()
    
    _create_user_table(name,database)
    _create_agend_table(name,database)
    _create_acticity_table(name,database)
    _create_agend_activitys_table(name,database)
    
    database.close()
    database.disconnect()
    return database

def _create_user_table(name,database):
    try:
        database.createTable(
            'Users',
            'username',
            username=[
                SQLiteType.TEXT,
                SQLiteModifiers.NN
            ],
            password=[
                SQLiteType.TEXT,
                SQLiteModifiers.NN
            ]
        )
        pass
    except Exception as ex:
        print(f'Database "{name}" already contains a table "Users"')
        pass
    pass

def _create_agend_table(name,database):
    try:
        database.createTable(
            'Agends',
            'owner',
            owner=[
                SQLiteType.TEXT,
                SQLiteModifiers.NN
            ],
            groupName=[
                SQLiteType.TEXT,
                SQLiteModifiers.NN
            ]
        )
        pass
    except Exception as ex:
        print(f'Database "{name}" already contains a table "Agends"')
        pass
    pass

def _create_acticity_table(name,database):
    try:
        database.createTable(
            'Activitys',
            'Id',
            Id=[
                SQLiteType.TEXT,
                SQLiteModifiers.NN
            ],
            description=[
                SQLiteType.TEXT,
                SQLiteModifiers.NN
            ],
            date=[
                SQLiteType.TEXT,
                SQLiteModifiers.NN
            ]
        )
        pass
    except Exception as ex:
        print(f'Database "{name}" already contains a table "Activitys"')
        pass
    pass

def _create_agend_activitys_table(name,database):
    try:
        database.createTable(
            'AgendActivitys',
            'owner',
            'Id',
            owner=[
                SQLiteType.TEXT,
                SQLiteModifiers.NN
            ],
            Id=[
                SQLiteType.TEXT,
                SQLiteModifiers.NN
            ]
        )
        pass
    except Exception as ex:
        print(f'Database "{name}" already contains a table "Agend-Activitys"')
        pass
    pass