# User database module

def get(cursor, **kwargs):
    """
    Get user from database
    :param cursor: Database cursor
    :param kwargs: User data
    :return: User data
    """
    # Build query
    query = "SELECT * FROM users WHERE "
    for key, value in kwargs.items():
        query += "{} = '{}' AND ".format(key, value)
    query = query[:-5]
    # Execute query
    cursor.execute(query)
    # Get user
    user = cursor.fetchone()
    return user


def create(cursor, **kwargs):
    """
    Create user in database
    :param cursor: Database cursor
    :param kwargs: User data
    :return: None
    """
    # Build query
    query = "INSERT INTO users ("
    for key, value in kwargs.items():
        query += "{}, ".format(key)
    # add created_at and updated_at
    query += "created_at, updated_at) VALUES ("
    for key, value in kwargs.items():
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
    Update user in database
    :param cursor: Database cursor
    :param kwargs: User data
    :return: None
    """
    # Build query
    query = "UPDATE users SET "
    for key, value in kwargs.items():
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
    Delete user from database
    :param cursor: Database cursor
    :param kwargs: User data
    :return: None
    """
    # Build query
    query = "DELETE FROM users WHERE "
    for key, value in kwargs.items():
        query += "{} = '{}' AND ".format(key, value)
    query = query[:-5]
    # Execute query
    cursor.execute(query)
    # Commit changes
    cursor.connection.commit()
    return None
