# Comment database module

def get(cursor, **kwargs):
    """
    Get comment from database
    :param cursor: Database cursor
    :param kwargs: Comment data
    :return: Comment data
    """
    # Build query
    query = "SELECT * FROM comments WHERE "
    for key, value in kwargs.items():
        query += "{} = '{}' AND ".format(key, value)
    query = query[:-5]
    # Execute query
    cursor.execute(query)
    # Get comment
    comment = cursor.fetchone()
    return comment


def create(cursor, **kwargs):
    """
    Create comment in database
    :param cursor: Database cursor
    :param kwargs: Comment data
    :return: None
    """
    # Build query
    query = "INSERT INTO comments ("
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
    Update comment in database
    :param cursor: Database cursor
    :param kwargs: Comment data
    :return: None
    """
    # Build query
    query = "UPDATE comments SET "
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
    Delete comment from database
    :param cursor: Database cursor
    :param kwargs: Comment data
    :return: None
    """
    # Build query
    query = "DELETE FROM comments WHERE "
    for key, value in kwargs.items():
        query += "{} = '{}' AND ".format(key, value)
    query = query[:-5]
    # Execute query
    cursor.execute(query)
    # Commit changes
    cursor.connection.commit()
    return None
