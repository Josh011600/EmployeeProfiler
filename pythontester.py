from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import webbrowser
from datetime import datetime
app = Flask(__name__)






def open_html_file(file_path):
    webbrowser.open(file_path)

if __name__ == "__main__":
    html_file_path = "htmltester.html"  # Replace this with the actual path to your HTML file
    open_html_file(html_file_path)

if __name__ == '__main__':
    app.run(debug=True)
