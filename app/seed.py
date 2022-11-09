# Seed database with all necessary tables

import sqlite3
database_file = 'bbb.db'
connection = sqlite3.connect(database_file, check_same_thread=False)

# Create users table
connection.execute('CREATE TABLE IF NOT EXISTS' +
                   ' users (id INTEGER PRIMARY KEY AUTOINCREMENT,' +
                   ' username TEXT KEY,' +
                   ' password TEXT NOT NULL,' +
                   ' email TEXT NOT NULL,' +
                   ' first_name TEXT,' +
                   ' last_name TEXT,' +
                   ' pfp_url TEXT,' +
                   ' created_at INTEGER NOT NULL,' +
                     ' updated_at INTEGER NOT NULL)')
print('Users table created')
connection.commit()

# Create posts table
connection.execute('CREATE TABLE IF NOT EXISTS' +
                     ' posts (id INTEGER PRIMARY KEY AUTOINCREMENT,' +
                        ' title TEXT NOT NULL,' +
                        ' slug TEXT NOT NULL,' +
                        ' subtitle TEXT,' +
                        ' description TEXT,' +
                        ' content TEXT NOT NULL,' +
                        ' author INTEGER NOT NULL,' +
                        ' blog INTEGER NOT NULL,' +
                        ' history TEXT,' +
                        ' created_at INTEGER NOT NULL,' +
                        ' updated_at INTEGER NOT NULL)')
print('Posts table created')
connection.commit()

# Create blogs table
connection.execute('CREATE TABLE IF NOT EXISTS' +
                        ' blogs (id INTEGER PRIMARY KEY AUTOINCREMENT,' +
                        ' title TEXT NOT NULL,' +
                        ' slug TEXT NOT NULL,' +
                        ' subtitle TEXT,' +
                        ' description TEXT,' +
                        ' posts TEXT,' +
                        ' author INTEGER NOT NULL,' +
                        ' history TEXT,' +
                        ' created_at INTEGER NOT NULL,' +
                        ' updated_at INTEGER NOT NULL)')
print('Blogs table created')
connection.commit()

# Create history table
connection.execute('CREATE TABLE IF NOT EXISTS' +
                        ' history (id INTEGER PRIMARY KEY AUTOINCREMENT,' +
                        ' type TEXT NOT NULL,' +
                        ' page integer NOT NULL,' +
                        ' old TEXT NOT NULL,' +
                        ' new TEXT NOT NULL,' +
                        ' author INTEGER NOT NULL,' +
                        ' created_at INTEGER NOT NULL)')
print('History table created')
connection.commit()

# Create comments table
connection.execute('CREATE TABLE IF NOT EXISTS' +
                        ' comments (id INTEGER PRIMARY KEY AUTOINCREMENT,' +
                        ' content TEXT NOT NULL,' +
                        ' author INTEGER NOT NULL,' +
                        ' type TEXT NOT NULL,' +
                        ' page INTEGER NOT NULL,' +
                        ' created_at INTEGER NOT NULL,' +
                        ' updated_at INTEGER NOT NULL)')
print('Comments table created')
connection.commit()