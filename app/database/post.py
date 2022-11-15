# Post database module

def get(cursor, **kwargs):
    """
    Get post from database
    :param cursor: Database cursor
    :param kwargs: Post data
    :return: Post data
    """
    # Build query
    query = "SELECT * FROM posts WHERE "
    for key, value in kwargs.items():
        query += "{} = '{}' AND ".format(key, value)
    query = query[:-5]
    # Execute query
    cursor.execute(query)
    # Get post
    post = cursor.fetchone()
    return post


def get_all(cursor, **kwargs):
    """
    Get all posts from database
    :param cursor: Database cursor
    :param kwargs: Post data
    :return: Post data
    """
    # Build query
    query = "SELECT * FROM posts WHERE "
    for key, value in kwargs.items():
        query += "{} = '{}' AND ".format(key, value)
    query = query[:-5]
    # Execute query
    cursor.execute(query)
    # Get posts
    posts = cursor.fetchall()
    return posts


def create(cursor, **kwargs):
    """
    Create post in database
    :param cursor: Database cursor
    :param kwargs: Post data
    :return: None
    """
    # Build query
    query = "INSERT INTO posts ("
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
    Update post in database
    :param cursor: Database cursor
    :param kwargs: Post data
    :return: None
    """
    # Build query
    query = "UPDATE posts SET "
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
    Delete post from database
    :param cursor: Database cursor
    :param kwargs: Post data
    :return: None
    """
    # Build query
    query = "DELETE FROM posts WHERE "
    for key, value in kwargs.items():
        query += "{} = '{}' AND ".format(key, value)
    query = query[:-5]
    # Execute query
    cursor.execute(query)
    # Commit changes
    cursor.connection.commit()
    return None
