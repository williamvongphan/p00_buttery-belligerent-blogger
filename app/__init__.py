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
import render.edit_post as render_edit_post
import render.delete_post as render_delete_post
import render.edit_blog as render_edit_blog
import render.delete_blog as render_delete_blog
import render.four_oh_four as render_404
import render.five_hundred as render_500

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
    if blog is None:
        return flask.abort(404)
    # Get posts by blog ID
    posts = post_table.get_all(cursor=connection.cursor(), blog=blog[0])
    # Get user by ID
    user = user_table.get(cursor=connection.cursor(), username=username)
    # Render blog page
    return render_blog.build_page(username=username, blog=blog, posts=posts, user=user)


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

@app.route('/blog/<blog_slug>/newpost', methods=['GET', 'POST'])
def new_post(blog_slug):
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
            return flask.redirect(flask.url_for('login'))
        else:
            blog = blog_table.get(cursor=connection.cursor(), slug=blog_slug)
            post_table.create(cursor=connection.cursor(), title=title, description=description, subtitle=subtitle, content=content, author=username, blog=blog[0], slug=util.slugify(title))
            # redirects to page
            return flask.redirect(flask.url_for('blog', slug=util.slugify(blog[1])))
    else:
        # get username from session
        username = flask.session.get('username')
        # get user info from database
        user = user_table.get(cursor=connection.cursor(), username=username)
        # get blog info (from slug)
        blog = blog_table.get(cursor=connection.cursor(), slug=blog_slug)
        # check if user is logged in
        if 'username' not in flask.session:
            # Redirect to login
            return flask.redirect(flask.url_for('login'))
        else:
            # check if user is author
            if user[0] != blog[6]:
                # render forbidden page template with 403 status code
                return flask.render_template('403.html'), 403
            else:
                # render edit post page
                return render_newpost.build_page(blog_slug=blog_slug)

@app.route('/blog/<blog_slug>/<post_slug>')
def view_post(blog_slug, post_slug):
    # Get username from session
    username = flask.session.get('username')
    #Get blog info by blogid
    blog = blog_table.get(cursor=connection.cursor(), slug=blog_slug)
    # get blog owner's info
    blog_user = user_table.get(cursor=connection.cursor(), id=blog[6])
    # Get posts by blog ID
    post = post_table.get(cursor=connection.cursor(), slug=post_slug)
    if post is None:
        # Render 404 page
        return flask.abort(404)
    # Get user by ID
    user = user_table.get(cursor=connection.cursor(), username=username)
    #Display post page
    return render_post.build_page(username=username, blog=blog, post=post, user=user, blog_user=blog_user)

@app.route('/blog/<blog_slug>/<post_slug>/edit', methods=['GET', 'POST'])
def edit_post(blog_slug, post_slug):
    # get blog
    blog = blog_table.get(cursor=connection.cursor(), slug=blog_slug)
    # get post
    post = post_table.get(cursor=connection.cursor(), slug=post_slug, blog=blog[0])
    if flask.request.method == 'POST':
        username = flask.session.get('username')
        # Get form database
        title = flask.request.form['title']
        description = flask.request.form['description']
        subtitle = flask.request.form['subtitle']
        content = flask.request.form['content']
        #Check if user exists
        user = user_table.get(cursor=connection.cursor(), username=username)
        # get post
        if user is None:
            # Redirect to login
            return flask.redirect(flask.url_for('login'))
        else:
            if user[1] != post[6]:
                # return forbidden error
                return flask.render_template('403.html'), 403
            else:
                post_table.update(cursor=connection.cursor(), title=title, description=description, subtitle=subtitle, content=content, slug=util.slugify(title), id=post[0])
                # redirects to page
                return flask.redirect(flask.url_for('view_post', blog_slug=blog_slug, post_slug=util.slugify(title)))
    else:
        # check if user is logged in
        if 'username' not in flask.session:
            # Redirect to login
            return flask.redirect(flask.url_for('login'))
        else:
            # check if user is author
            if flask.session['username'] != post[6]:
                print(flask.session['username'])
                print(post[6])
                # render forbidden page template with 403 status code
                return flask.render_template('403.html'), 403
            else:
                # render edit page
                return render_edit_post.build_page(post=post, postid=post_slug)


@app.route('/blog/<blog_slug>/edit', methods=['GET', 'POST'])
def edit_blog(blog_slug):
    # get blog
    blog = blog_table.get(cursor=connection.cursor(), slug=blog_slug)
    # get user from session
    username = flask.session.get('username')
    # get user from database
    user = user_table.get(cursor=connection.cursor(), username=username)
    if flask.request.method == 'POST':
        username = flask.session.get('username')
        # Get form database
        description = flask.request.form['description']
        subtitle = flask.request.form['subtitle']
        #Check if user exists
        user = user_table.get(cursor=connection.cursor(), username=username)
        # get post
        if user is None:
            # Redirect to login
            return flask.redirect(flask.url_for('login'))
        else:
            if user[0] != blog[6]:
                # return forbidden error
                return flask.render_template('403.html'), 403
            else:
                blog_table.update(cursor=connection.cursor(), title=blog[1], description=description, subtitle=subtitle, slug=util.slugify(blog[1]), id=blog[0], author=blog[6])
                # redirects to page
                return flask.redirect(flask.url_for('blog', slug=blog_slug))
    else:
        # check if user is logged in
        if 'username' not in flask.session:
            # Redirect to login
            return flask.redirect(flask.url_for('login'))
        else:
            # check if user is author
            if user[0] != blog[6]:
                # render forbidden page template with 403 status code
                return flask.render_template('403.html'), 403
            else:
                # render edit page
                return render_edit_blog.build_page(blog=blog, blogid=blog_slug)

@app.route('/post/<postid>/delete', methods=['GET', 'POST'])
def delete_post(postid):
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
            return flask.redirect(flask.url_for('login'))
        else:
            if user[0] != post[4]:
                # return forbidden error
                return flask.abort(403)
            else:
                blog = blog_table.get(cursor=connection.cursor(), author=user[0])
                # code that actually deletes from database
                blog_table.delete(cursor=connection.cursor, blogs=postid)
                return flask.redirect(flask.url_for('blog', slug=util.slugify(blog[1])))
    else:
        # check if user is logged in
        if 'username' not in flask.session:
            # Redirect to login
            return flask.redirect(flask.url_for('login'))
        else:
            # check if user is author
            if flask.session['username'] != post[4]:
                # return forbidden error
                return flask.abort(403)
            else:
                # render delete page
                return render_delete.build_page()
    
    

@app.route('/explore')
def explore():
    # Get username from session
    username = flask.session.get('username')
    # Get all blogs
    blogs = blog_table.get_all(cursor=connection.cursor())
    # Get all users
    users = user_table.get_all(cursor=connection.cursor())
    print(blogs)
    return render_homepage.build_page(username=username, blogs=blogs, users=users)

@app.errorhandler(404)
def page_not_found(e):
    return render_404.build_page(), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_500.build_page(), 500

@app.errorhandler(Exception)
def unhandled_exception(e):
    return render_500.build_page(), 500

# Run the app
if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
