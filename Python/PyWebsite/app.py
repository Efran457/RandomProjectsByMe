from flask import Flask,  render_template
import logging

app = Flask(__name__)

# Disable Flask logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)  # Only show errors, not regular requests

@app.route('/')
def home():
    return render_template('Main.html')

@app.route('/about')
def about():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>About</title>
        <link rel="stylesheet" href="/static/style.css">
    </head>
    <body>
        <div class="container">
            <div class="emoji">📖</div>
            <h1>About</h1>
            <p>This is a simple Flask website built with Python.</p>
            <p>The CSS is now in a separate file for easy customization!</p>
            <div class="nav">
                <a href="/" class="back-link">← Back to Home</a>
            </div>
        </div>
    </body>
    </html>
    """


@app.route('/game')
def game():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Moving Box</title>
        <link rel="stylesheet" href="/static/style.css">
    </head>
    <body>
        <div class="container">
            <h1>Move Your Mouse! 📦</h1>
            <p>The box will follow your cursor wherever you move it!</p>
            <div class="nav">
                <a href="/">← Back to Home</a>
            </div>
        </div>

        <div class="box" id="myBox"></div>

        <script src="/static/Cursor.js"></script>
    </body>
    </html>
    """

# if User tris to visit Unkown website
@app.errorhandler(404)
def page_not_found(e):
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>404 - Page Not Found</title>
        <link rel="stylesheet" href="/static/style.css">
    </head>
    <body>
        <div class="container">
            <div class="emoji">❌</div>
            <h1>404 - Page Not Found!</h1>
            <p>Oops! This page doesn't exist.</p>
            <p>Try going back to the home page.</p>
            <div class="nav">
                <a href="/">← Back to Home</a>
            </div>
        </div>
    </body>
    </html>
    """, 404

if __name__ == '__main__':
    app.run(debug=True)
