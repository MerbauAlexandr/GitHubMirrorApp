# C:\Users\Pavlu4ini\PycharmProjects\GitHubMirrorApp\app.py

from flask import Flask, render_template, request, redirect, url_for
from git import Repo
import os
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
import tempfile

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        repo_url = request.form['repo_url']
        return redirect(url_for('view_code', repo_url=repo_url))

    return render_template('index.html')

@app.route('/view_code')
def view_code():
    repo_url = request.args.get('repo_url')
    code_html = ""

    # Создаем временную папку
    with tempfile.TemporaryDirectory() as tmpdirname:
        Repo.clone_from(repo_url, tmpdirname)  # Клонируем в временную папку

        # Генерация кода для отображения
        for root, dirs, files in os.walk(tmpdirname):
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        code = f.read()
                        formatter = HtmlFormatter(full=True, linenos=True, cssclass="codehilite")
                        highlighted_code = highlight(code, PythonLexer(), formatter)
                        code_html += f"<h2>{file}</h2>" + highlighted_code

    return render_template('view_code.html', code_html=code_html, repo_url=repo_url)

if __name__ == '__main__':
    app.run(debug=True)
