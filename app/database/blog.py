# Blog database module

def get(cursor, **kwargs):
    """
    Get blog from database
    :param cursor: Database cursor
    :param kwargs: Blog data
    :return: Blog data
    """
    # Build query
    query = "SELECT * FROM blogs WHERE "
    for key, value in kwargs.items():
        query += "{} = '{}' AND ".format(key, value)
    query = query[:-5]
    # Execute query
    cursor.execute(query)
    # Get blog
    blog = cursor.fetchone()
    return blog


def create(cursor, **kwargs):
    """
    Create blog in database
    :param cursor: Database cursor
    :param kwargs: Blog data
    :return: None
    """
    # Build query
    query = "INSERT INTO blogs ("
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


def update(cursor, author, **kwargs):
    """
    Update blog in database
    :param cursor: Database cursor
    :param kwargs: Blog data
    :return: None
    """
    # Build query
    query = "UPDATE blogs SET "
    for key, value in kwargs.items():
        query += "{} = '{}', ".format(key, value)
    query += "updated_at = datetime('now')"
    query += " WHERE author = {}".format(author)
    print(query)
    # Execute query
    cursor.execute(query)
    # Commit changes
    cursor.connection.commit()
    return None


def delete(cursor, **kwargs):
    """
    Delete blog from database
    :param cursor: Database cursor
    :param kwargs: Blog data
    :return: None
    """
    # Build query
    query = "DELETE FROM blogs WHERE "
    for key, value in kwargs.items():
        query += "{} = '{}' AND ".format(key, value)
    query = query[:-5]
    # Execute query
    cursor.execute(query)
    # Commit changes
    cursor.connection.commit()
    return None
