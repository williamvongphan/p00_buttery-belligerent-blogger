# History database module

def get(cursor, **kwargs):
    """
    Get history from database
    :param cursor: Database cursor
    :param kwargs: History data
    :return: History data
    """
    # Build query
    query = "SELECT * FROM history WHERE "
    for key, value in kwargs.items():
        query += "{} = '{}' AND ".format(key, value)
    query = query[:-5]
    # Execute query
    cursor.execute(query)
    # Get history
    history = cursor.fetchone()
    return history


def create(cursor, **kwargs):
    """
    Create history in database
    :param cursor: Database cursor
    :param kwargs: History data
    :return: None
    """
    # Build query
    query = "INSERT INTO history ("
    for key, value in kwargs.items():
        query += "{}, ".format(key)
    # add created_at and updated_at
    query += "created_at, updated_at) VALUES ("
    for key, value in kwargs.items():
        if type(value) == str:
            value = value.replace("'", "''")
        query += "'{}', ".format(value)
    # add created_at and updated_at
    query += "datetime('now'), datetime('now'))"
    # Execute query
    print(query)
    cursor.execute(query)
    # Commit changes
    cursor.connection.commit()
    return None


def update(cursor, id, **kwargs):
    """
    Update history in database
    :param cursor: Database cursor
    :param kwargs: History data
    :return: None
    """
    # Build query
    query = "UPDATE history SET "
    for key, value in kwargs.items():
        if type(value) == str:
            value = value.replace("'", "''")
        query += "{} = '{}', ".format(key, value)
    query += "updated_at = datetime('now')"
    query += " WHERE id = {}".format(id)
    print(query)
    # Execute query
    cursor.execute(query)
    # Commit changes
    cursor.connection.commit()
    return None


def delete(cursor, **kwargs):
    """
    Delete history from database
    :param cursor: Database cursor
    :param kwargs: History data
    :return: None
    """
    # Build query
    query = "DELETE FROM history WHERE "
    for key, value in kwargs.items():
        query += "{} = '{}' AND ".format(key, value)
    query = query[:-5]
    # Execute query
    cursor.execute(query)
    # Commit changes
    cursor.connection.commit()
    return None
