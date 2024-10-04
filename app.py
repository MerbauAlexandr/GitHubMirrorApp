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
    structure_html = ""

    with tempfile.TemporaryDirectory() as tmpdirname:
        Repo.clone_from(repo_url, tmpdirname)

        # Получаем имя проекта
        project_name = os.path.basename(repo_url).replace('.git', '')

        # Генерация структуры проекта для отображения
        for root, dirs, files in os.walk(tmpdirname):
            level = root.replace(tmpdirname, '').count(os.sep)  # Определяем уровень вложенности
            indent = ' ' * 4 * (level)  # Отступ для текущего уровня
            if level == 0:  # Если корневой уровень
                structure_html += f"<strong style='background-color: rgba(255, 255, 0, 0.3);'>{project_name}</strong><br>"  # Название проекта с фоном
            else:
                folder_name = os.path.basename(root)
                structure_html += f"{indent}<strong style='background-color: rgba(0, 255, 0, 0.3);'>{folder_name.upper()}/</strong><br>"  # Папки с фоном
            for file in files:
                structure_html += f"{indent}    └── {file}<br>"  # Добавляем файлы

        # Генерация кода для отображения
        for root, dirs, files in os.walk(tmpdirname):
            for file in files:
                file_path = os.path.join(root, file)
                if file.endswith(('.py', '.html', '.txt', '.json', '.yaml', '.yml', '.md')):
                    with open(file_path, 'r', encoding='utf-8') as f:
                        code = f.read()
                        formatter = HtmlFormatter(full=True, linenos=True, cssclass="codehilite")
                        highlighted_code = highlight(code, PythonLexer(), formatter)
                        code_html += f"<h2 class='text-xl font-bold underline'>{project_name}/{file}</h2>" + highlighted_code + "<br><br>"  # Полный путь в заголовке с подчёркиванием
                elif file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                    code_html += f"<h2 class='text-xl font-bold underline'>{project_name}/{file}</h2><img src='{file_path}' alt='{file}' style='max-width: 100%;'><br><br>"  # Подчёркивание и путь для изображений

    return render_template('view_code.html', code_html=code_html, structure_html=structure_html, repo_url=repo_url)

if __name__ == '__main__':
    app.run(debug=True)
