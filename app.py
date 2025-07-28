from flask import Flask, render_template, request, redirect, url_for
import json
from uuid import uuid4  # For generating unique IDs

app = Flask(__name__)


# Load posts from JSON file
def load_posts():
    try:
        with open('posts.json', 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


# Save posts to JSON file
def save_posts(posts):
    with open('posts.json', 'w') as f:
        json.dump(posts, f, indent=4)


@app.route('/')
def index():
    blog_posts = load_posts()
    return render_template('index.html', posts=blog_posts)

@app.route('/delete/<post_id>', methods=['POST'])
def delete(post_id):
    # Load current posts
    blog_posts = load_posts()
    
    # Find and remove the post with matching ID
    updated_posts = [post for post in blog_posts if post['id'] != post_id]
    
    # Save the updated list
    save_posts(updated_posts)
    
    # Redirect back to home page
    return redirect(url_for('index'))

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        # Get form data
        author = request.form.get('author')
        title = request.form.get('title')
        content = request.form.get('content')

        # Validate form data
        if not all([author, title, content]):
            return "Please fill in all fields", 400

        # Load existing posts
        blog_posts = load_posts()

        # Create new post with unique ID
        new_post = {
            'id': str(uuid4()),  # Generate unique ID
            'author': author,
            'title': title,
            'content': content
        }

        # Add new post and save
        blog_posts.append(new_post)
        save_posts(blog_posts)

        return redirect(url_for('index'))

    return render_template('add.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)
