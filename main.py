import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                            QPushButton, QLabel, QLineEdit, QMessageBox,
                            QDialog, QFormLayout, QTextEdit, QListWidget,
                            QInputDialog, QHBoxLayout)
from PyQt6.QtCore import Qt
import sqlite3
import hashlib

# --- Окно регистрации и входа ---
class AuthWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Вход / Регистрация")
        self.setGeometry(300, 300, 350, 200)
        layout = QVBoxLayout()

        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        form = QFormLayout()
        form.addRow("Логин:", self.username_input)
        form.addRow("Пароль:", self.password_input)
        layout.addLayout(form)

        btn_layout = QHBoxLayout()
        self.login_btn = QPushButton("Войти")
        self.register_btn = QPushButton("Зарегистрироваться")
        btn_layout.addWidget(self.login_btn)
        btn_layout.addWidget(self.register_btn)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

        self.login_btn.clicked.connect(self.login)
        self.register_btn.clicked.connect(self.register)
        self.user_id = None

    def hash_password(self, password):
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

    def login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text()
        if not username or not password:
            QMessageBox.warning(self, "Ошибка", "Введите логин и пароль")
            return
        conn = sqlite3.connect('voting.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, password_hash FROM users WHERE username=?", (username,))
        row = cursor.fetchone()
        conn.close()
        if row and row[1] == self.hash_password(password):
            self.user_id = row[0]
            self.accept()
        else:
            QMessageBox.warning(self, "Ошибка", "Неверный логин или пароль")

    def register(self):
        username = self.username_input.text().strip()
        password = self.password_input.text()
        if not username or not password:
            QMessageBox.warning(self, "Ошибка", "Введите логин и пароль")
            return
        conn = sqlite3.connect('voting.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE username=?", (username,))
        if cursor.fetchone():
            QMessageBox.warning(self, "Ошибка", "Пользователь с таким логином уже существует")
            conn.close()
            return
        password_hash = self.hash_password(password)
        cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, password_hash))
        conn.commit()
        conn.close()
        QMessageBox.information(self, "Успех", "Пользователь зарегистрирован! Теперь войдите.")

class CreateVoteWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Создание голосования")
        self.setGeometry(200, 200, 600, 400)
        
        layout = QVBoxLayout()
        
        # Форма для ввода данных
        form_layout = QFormLayout()
        
        self.title_input = QLineEdit()
        self.description_input = QTextEdit()
        self.options_list = QListWidget()
        
        form_layout.addRow("Название голосования:", self.title_input)
        form_layout.addRow("Описание:", self.description_input)
        form_layout.addRow("Варианты ответов:", self.options_list)
        
        # Кнопки для управления вариантами ответов
        options_buttons_layout = QVBoxLayout()
        add_option_btn = QPushButton("Добавить вариант")
        remove_option_btn = QPushButton("Удалить вариант")
        
        add_option_btn.clicked.connect(self.add_option)
        remove_option_btn.clicked.connect(self.remove_option)
        
        options_buttons_layout.addWidget(add_option_btn)
        options_buttons_layout.addWidget(remove_option_btn)
        
        # Кнопка сохранения
        save_btn = QPushButton("Создать голосование")
        save_btn.clicked.connect(self.save_vote)
        
        # Добавляем все элементы на форму
        layout.addLayout(form_layout)
        layout.addLayout(options_buttons_layout)
        layout.addWidget(save_btn)
        
        self.setLayout(layout)
    
    def add_option(self):
        option, ok = QInputDialog.getText(self, "Добавить вариант", "Введите вариант ответа:")
        if ok and option:
            self.options_list.addItem(option)
    
    def remove_option(self):
        current_item = self.options_list.currentItem()
        if current_item:
            self.options_list.takeItem(self.options_list.row(current_item))
    
    def save_vote(self):
        title = self.title_input.text()
        description = self.description_input.toPlainText()
        options = [self.options_list.item(i).text() for i in range(self.options_list.count())]
        
        if not title:
            QMessageBox.warning(self, "Ошибка", "Введите название голосования")
            return
        
        if not options:
            QMessageBox.warning(self, "Ошибка", "Добавьте хотя бы один вариант ответа")
            return
        
        try:
            conn = sqlite3.connect('voting.db')
            cursor = conn.cursor()
            
            # Сохраняем голосование
            cursor.execute('''
                INSERT INTO votes (title, description)
                VALUES (?, ?)
            ''', (title, description))
            
            vote_id = cursor.lastrowid
            
            # Сохраняем варианты ответов
            for option in options:
                cursor.execute('''
                    INSERT INTO options (vote_id, option_text)
                    VALUES (?, ?)
                ''', (vote_id, option))
            
            conn.commit()
            QMessageBox.information(self, "Успех", "Голосование успешно создано!")
            self.accept()
            
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при сохранении: {str(e)}")
        finally:
            conn.close()

class VotingSystem(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Система онлайн-голосования")
        self.setGeometry(100, 100, 800, 600)
        
        # Создаем центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Заголовок
        title = QLabel("Система онлайн-голосования")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin: 20px;")
        layout.addWidget(title)
        
        # Кнопки для разных действий
        self.create_vote_btn = QPushButton("Создать голосование")
        self.view_votes_btn = QPushButton("Просмотр голосований")
        self.vote_btn = QPushButton("Проголосовать")
        
        # Добавляем кнопки на форму
        layout.addWidget(self.create_vote_btn)
        layout.addWidget(self.view_votes_btn)
        layout.addWidget(self.vote_btn)
        
        # Подключаем сигналы к слотам
        self.create_vote_btn.clicked.connect(self.create_vote)
        self.view_votes_btn.clicked.connect(self.view_votes)
        self.vote_btn.clicked.connect(self.vote)
        
        # Инициализация базы данных
        self.init_database()
    
    def init_database(self):
        conn = sqlite3.connect('voting.db')
        cursor = conn.cursor()
        
        # --- Новая таблица пользователей ---
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL
            )
        ''')
        
        # --- Остальные таблицы ---
        # Создаем таблицу для голосований
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS votes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Создаем таблицу для вариантов ответов
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS options (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                vote_id INTEGER,
                option_text TEXT NOT NULL,
                votes_count INTEGER DEFAULT 0,
                FOREIGN KEY (vote_id) REFERENCES votes (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def create_vote(self):
        dialog = CreateVoteWindow(self)
        dialog.exec()
    
    def view_votes(self):
        # TODO: Реализовать просмотр голосований
        QMessageBox.information(self, "Информация", "Функция просмотра голосований будет реализована")
    
    def vote(self):
        # TODO: Реализовать процесс голосования
        QMessageBox.information(self, "Информация", "Функция голосования будет реализована")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # --- Показываем окно авторизации ---
    auth = AuthWindow()
    if auth.exec() == QDialog.DialogCode.Accepted:
        window = VotingSystem()
        window.show()
        sys.exit(app.exec())