from flask import Flask, render_template, request, redirect, url_for
import json
from uuid import uuid4

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this for production

def load_posts():
    try:
        with open('posts.json', 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_posts(posts):
    with open('posts.json', 'w') as f:
        json.dump(posts, f, indent=4)

@app.route('/')
def index():
    blog_posts = load_posts()
    return render_template('index.html', posts=blog_posts)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        author = request.form.get('author')
        title = request.form.get('title')
        content = request.form.get('content')
        
        if not all([author, title, content]):
            return "Please fill in all fields", 400
        
        blog_posts = load_posts()
        new_post = {
            'id': str(uuid4()),
            'author': author,
            'title': title,
            'content': content
        }
        blog_posts.append(new_post)
        save_posts(blog_posts)
        return redirect(url_for('index'))
    
    return render_template('add.html')

@app.route('/update/<post_id>', methods=['GET', 'POST'])
def update(post_id):
    blog_posts = load_posts()
    post_to_update = None
    
    for post in blog_posts:
        if post['id'] == post_id:
            post_to_update = post
            break
    
    if not post_to_update:
        return "Post not found", 404
    
    if request.method == 'POST':
        post_to_update['title'] = request.form.get('title')
        post_to_update['author'] = request.form.get('author')
        post_to_update['content'] = request.form.get('content')
        save_posts(blog_posts)
        return redirect(url_for('index'))
    
    return render_template('update.html', post=post_to_update)

@app.route('/delete/<post_id>', methods=['POST'])
def delete(post_id):
    blog_posts = load_posts()
    blog_posts = [post for post in blog_posts if post['id'] != post_id]
    save_posts(blog_posts)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)
