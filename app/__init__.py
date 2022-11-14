# __init__.py
# This file is part of the Flask-Blog project

import flask
import sqlite3
import utils.util as util
import database.user as user_table
import database.post as post_table
import database.comment as comment_table
import database.blog as blog_table
import render.index as render_index
import render.login as render_login
import render.register as render_register
import render.onboarding as render_onboarding
import render.create_blog as render_create_blog
import render.newpost as render_newpost
import render.blog as render_blog
import render.post as render_post
import render.homepage as render_homepage

app = flask.Flask(__name__)

app.secret_key = 'super secret key'

database_file = 'bbb.db'

# Connect to database
connection = sqlite3.connect(database_file, check_same_thread=False)

@app.route('/')
def index():
    # Get username from session
    username = flask.session.get('username')
    if username is None:
        return render_index.build_page()
    # Check if user is in database
    user = user_table.get(cursor=connection.cursor(), username=username)
    if user is None:
        # User is not in database, this is a glitch
        return flask.redirect(flask.url_for('logout'))
    # User is in database
    else:
        # Render index flask template
        return render_index.build_page(username=username)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'POST':
        response = ""
        # Get form data
        username = flask.request.form['username']
        password = flask.request.form['password']
        # Check if user exists
        user = user_table.get(cursor=connection.cursor(), username=username)
        if user is None:
            response = "Invalid username or password"
        else:
            # Check if password is correct
            if user[2] == password:
                # Create session
                flask.session['username'] = username
                flask.session['logged_in'] = True
                return flask.redirect(flask.url_for('index'))
            else:
                response = "Invalid username or password"
        return render_login.build_page(data=response)
    else:
        return render_login.build_page(data=None)


@app.route('/logout')
def logout():
    # Remove session
    flask.session.pop('username', None)
    flask.session.pop('logged_in', None)
    return flask.redirect(flask.url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if flask.request.method == 'POST':
        response = ""
        # Get form data
        username = flask.request.form['username']
        password = flask.request.form['password']
        email = flask.request.form['email']
        # Check if user exists
        user = user_table.get(cursor=connection.cursor(), username=username)
        if user is not None:
            response = "Username already exists"
            return render_register.build_page(data=response)
        else:
            # Create user
            user_table.create(cursor=connection.cursor(), username=username, password=password, email=email)
            response = "User created"
            # Set session
            flask.session['username'] = username
            flask.session['logged_in'] = True
            # Redirect to onboarding
            return flask.redirect(flask.url_for('onboarding'))
    else:
        return render_register.build_page(data=None)


@app.route('/onboarding', methods=['GET', 'POST'])
def onboarding():
    if flask.request.method == 'POST':
        response = ""
        # Get user info from session
        username = flask.session['username']
        # Get form data
        first_name = flask.request.form['first_name']
        last_name = flask.request.form['last_name']
        pfp_url = flask.request.form['pfp_url']
        # Check if user exists
        user = user_table.get(cursor=connection.cursor(), username=username)
        if user is None:
            response = "User does not exist"
            return render_onboarding.build_page(data=response)
        else:
            # Update user by ID
            user_table.update(cursor=connection.cursor(), id=user[0], first_name=first_name, last_name=last_name, pfp_url=pfp_url)
            # Redirect to index
            return flask.redirect(flask.url_for('index'))
    else:
        return render_onboarding.build_page(data=None)


@app.route('/blog/create', methods=['GET', 'POST'])
def blog_create():
    if flask.request.method == 'POST':
        response = ""
        # Get user info from session
        username = flask.session['username']
        # Get form data
        title = flask.request.form['title']
        subtitle = flask.request.form['subtitle']
        description = flask.request.form['description']

        # Check if user exists
        user = user_table.get(cursor=connection.cursor(), username=username)
        if user is None:
            # Redirect to login
            return flask.redirect(flask.url_for('login'))
        else:
            # Create blog
            blog_table.create(cursor=connection.cursor(), title=title, description=description, author=user[0], subtitle=subtitle, slug=util.slugify(title))
            # Redirect to blog
            return flask.redirect(flask.url_for('blog', slug=util.slugify(title)))
    else:
        return render_create_blog.build_page(data=None)


@app.route('/blog/<slug>')
def blog(slug):
    # Get username from session
    username = flask.session.get('username')
    # Get blog by slug
    blog = blog_table.get(cursor=connection.cursor(), slug=slug)
    # Get posts by blog ID
    posts = post_table.get_all(cursor=connection.cursor(), blog=blog[0])
    # Get user by ID
    user = user_table.get(cursor=connection.cursor(), username=username)
    # Render blog page
    return render_blog.build_page(username=username, blog=blog, posts=posts, user=user, user_id=user[0])


@app.route('/my_blog')
def my_blog():
    # Get username from session
    username = flask.session.get('username')
    # Get user info from database
    user = user_table.get(cursor=connection.cursor(), username=username)
    # Get blog by user ID
    blog = blog_table.get(cursor=connection.cursor(), author=user[0])
    # Does the user have a blog?
    if blog is None:
        # No
        return flask.redirect(flask.url_for('blog_create'))
    else:
        # Yes
        return flask.redirect(flask.url_for('blog', slug=util.slugify(blog[1])))

@app.route('/blog/<blogid>/newpost', methods=['GET', 'POST'])
def new_post(blogid):
    if flask.request.method == 'POST':
        response = ""
        username = flask.session.get('username')
        # Get form database
        title = flask.request.form['title']
        description = flask.request.form['description']
        subtitle = flask.request.form['subtitle']
        content = flask.request.form['content']
        #Check if user exists
        user = user_table.get(cursor=connection.cursor(), username=username)
        if user is None:
            # Redirect to login
            return flask.redirect(flask.url_for('Login'))
        else:
            blog = blog_table.get(cursor=connection.cursor(), author=user[0])
            # Creates post
            post_table.create(cursor=connection.cursor(), title=title, description=description, subtitle=subtitle, content=content, author=username, blog=blogid, slug=util.slugify(title))
            # Updates blog so post is most recent post
            blog_table.update(cursor=connection.cursor(), author=user[0], posts=title)
            # redirects to page
            return flask.redirect(flask.url_for('blog', slug=util.slugify(blog[1])))
    else:
        return render_newpost.build_page(blogid=blogid)

@app.route('/blog/<blogid>/<post>')
def view_post(blogid, post):
    # Get username from session
    username = flask.session.get('username')
    #Get blog info by blogid
    blog = blog_table.get(cursor=connection.cursor(), id=blogid)
    # Get posts by blog ID
    post = post_table.get(cursor=connection.cursor(), title=post)
    # Get user by ID
    user = user_table.get(cursor=connection.cursor(), username=username)
    #Display post page
    return render_post.build_page(username=username, blog=blogid, user_id=user[0], post=post)

@app.route('/homepage')
def homepage():
    # Get username from session
    username = flask.session.get('username')
    # Get all blogs
    blogs = blog_table.get_all(cursor=connection.cursor())
    # Get all users
    users = user_table.get_all(cursor=connection.cursor())
    print(blogs)
    return render_homepage.build_page(username=username, blogs=blogs, users=users)

# Run the app
if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
