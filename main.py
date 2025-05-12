import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                            QPushButton, QLabel, QLineEdit, QMessageBox, QDialog, QFormLayout, QTextEdit, QListWidget, QInputDialog, QStackedWidget, QComboBox, QSizePolicy)
from PyQt6.QtCore import Qt, QTimer, QDateTime
from PyQt6.QtGui import QFont, QPalette, QLinearGradient, QColor, QBrush, QPixmap
import sqlite3
import hashlib

# --- Окно регистрации и входа ---
class AuthWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Авторизация")
        self.setMinimumSize(1200, 800)
        self.setStyleSheet("background: transparent;")
        # Фоновое изображение
        self.bg_label = QLabel(self)
        self.bg_label.setPixmap(QPixmap("map_site.jpg"))
        self.bg_label.setScaledContents(True)
        self.bg_label.setGeometry(0, 0, self.width(), self.height())
        self.bg_label.lower()
        # Основной вертикальный слой
        main_vlayout = QVBoxLayout(self)
        main_vlayout.setContentsMargins(0, 0, 0, 0)
        main_vlayout.setSpacing(0)
        # Header
        header = QLabel("<b>ЭЛЕКТРОННОЕ ГОЛОСОВАНИЕ</b>")
        header.setFont(QFont("Arial", 28, QFont.Weight.Bold))
        header.setStyleSheet("color: #fff; background: rgba(0,0,0,0.35); padding: 24px 0; text-align: center;")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_vlayout.addWidget(header)
        # Центральная часть (карточка по центру)
        center_widget = QWidget()
        center_layout = QHBoxLayout(center_widget)
        center_layout.setContentsMargins(0, 0, 0, 0)
        center_layout.setSpacing(0)
        center_layout.addStretch(1)
        # Белая карточка
        card = QWidget()
        card.setStyleSheet("background: white; border-radius: 24px; box-shadow: 0 8px 32px rgba(0,0,0,0.12);")
        card.setFixedWidth(680)
        card.setFixedHeight(600)
        card_layout = QVBoxLayout(card)
        card_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        card_layout.setContentsMargins(48, 48, 48, 48)
        card_layout.setSpacing(22)
        # Заголовок
        title = QLabel("Авторизация")
        title.setFont(QFont("Arial", 28, QFont.Weight.Bold))
        title.setStyleSheet("color: #222;")
        card_layout.addWidget(title)
        # Описание (многострочный текст)
        desc = QLabel("Пожалуйста, введите свои данные для входа или регистрации.\n\nЛогин — ваш уникальный идентификатор.\nПароль — только для вас.\nКод администратора — только если вы админ (иначе оставьте пустым).")
        desc.setFont(QFont("Arial", 15))
        desc.setStyleSheet("color: #444; margin-bottom: 10px;")
        desc.setAlignment(Qt.AlignmentFlag.AlignLeft)
        desc.setWordWrap(True)
        card_layout.addWidget(desc)
        # Поля с подписями и placeholderText
        login_label = QLabel("Логин:")
        login_label.setFont(QFont("Arial", 13, QFont.Weight.Bold))
        card_layout.addWidget(login_label)
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Например: ivanov123")
        self.username_input.setMinimumHeight(48)
        self.username_input.setFont(QFont("Arial", 16))
        self.username_input.setStyleSheet("QLineEdit { padding-left: 12px; } QLineEdit::placeholder { color: #888; font-size: 15px; }")
        card_layout.addWidget(self.username_input)
        password_label = QLabel("Пароль:")
        password_label.setFont(QFont("Arial", 13, QFont.Weight.Bold))
        card_layout.addWidget(password_label)
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Введите ваш пароль")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setMinimumHeight(48)
        self.password_input.setFont(QFont("Arial", 16))
        self.password_input.setStyleSheet("QLineEdit { padding-left: 12px; } QLineEdit::placeholder { color: #888; font-size: 15px; }")
        card_layout.addWidget(self.password_input)
        admin_label = QLabel("Код администратора (если есть):")
        admin_label.setFont(QFont("Arial", 13, QFont.Weight.Bold))
        card_layout.addWidget(admin_label)
        self.admin_code_input = QLineEdit()
        self.admin_code_input.setPlaceholderText("Оставьте пустым, если не админ")
        self.admin_code_input.setMinimumHeight(48)
        self.admin_code_input.setFont(QFont("Arial", 16))
        self.admin_code_input.setStyleSheet("QLineEdit { padding-left: 12px; } QLineEdit::placeholder { color: #888; font-size: 15px; }")
        card_layout.addWidget(self.admin_code_input)
        # Кнопки
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(18)
        self.login_btn = QPushButton("Войти")
        self.login_btn.setFont(QFont("Arial", 17, QFont.Weight.Bold))
        self.login_btn.setMinimumHeight(52)
        self.login_btn.setStyleSheet("background: #1976d2; color: #fff; border-radius: 10px;")
        self.register_btn = QPushButton("Зарегистрироваться")
        self.register_btn.setFont(QFont("Arial", 17, QFont.Weight.Bold))
        self.register_btn.setMinimumHeight(52)
        self.register_btn.setStyleSheet("background: #43a047; color: #fff; border-radius: 10px;")
        btn_layout.addWidget(self.login_btn)
        btn_layout.addWidget(self.register_btn)
        card_layout.addLayout(btn_layout)
        center_layout.addWidget(card, alignment=Qt.AlignmentFlag.AlignVCenter)
        center_layout.addStretch(1)
        main_vlayout.addWidget(center_widget, stretch=1)
        # Footer
        footer = QLabel("© 2025 Онлайн-голосование. Все права защищены.")
        footer.setFont(QFont("Arial", 14))
        footer.setStyleSheet("color: #fff; background: rgba(0,0,0,0.35); padding: 18px 0; text-align: center;")
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_vlayout.addWidget(footer)
        # Сигналы
        self.login_btn.clicked.connect(self.login)
        self.register_btn.clicked.connect(self.register)
        self.user_id = None

    def resizeEvent(self, event):
        if hasattr(self, 'bg_label') and self.bg_label:
            self.bg_label.setGeometry(0, 0, self.width(), self.height())
        super().resizeEvent(event)

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
        admin_code = self.admin_code_input.text().strip()  # Получаем код админа
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
        is_admin = 1 if admin_code == "admin123" else 0  # Проверяем код админа
        cursor.execute("INSERT INTO users (username, password_hash, is_admin) VALUES (?, ?, ?)", (username, password_hash, is_admin))
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

# --- Окно для голосования ---
class VoteDialog(QDialog):
    def __init__(self, user_id, vote_id, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Голосование")
        self.user_id = user_id
        self.vote_id = vote_id
        self.selected_option_id = None
        layout = QVBoxLayout()
        conn = sqlite3.connect('voting.db')
        cursor = conn.cursor()
        cursor.execute("SELECT title, description FROM votes WHERE id=?", (vote_id,))
        vote = cursor.fetchone()
        if vote:
            layout.addWidget(QLabel(f"<b>{vote[0]}</b>"))
            layout.addWidget(QLabel(vote[1]))
        cursor.execute("SELECT id, option_text FROM options WHERE vote_id=?", (vote_id,))
        self.options = cursor.fetchall()
        self.option_buttons = []
        for opt_id, opt_text in self.options:
            btn = QPushButton(opt_text)
            btn.clicked.connect(lambda checked, oid=opt_id: self.select_option(oid))
            layout.addWidget(btn)
            self.option_buttons.append(btn)
        self.setLayout(layout)
        conn.close()
    def select_option(self, option_id):
        self.selected_option_id = option_id
        self.accept()

# --- Окно просмотра голосований ---
class ResultsDialog(QDialog):
    def __init__(self, vote_id, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Результаты голосования")
        layout = QVBoxLayout()
        conn = sqlite3.connect('voting.db')
        cursor = conn.cursor()
        cursor.execute("SELECT title FROM votes WHERE id=?", (vote_id,))
        vote = cursor.fetchone()
        if vote:
            layout.addWidget(QLabel(f"<b>{vote[0]}</b>"))
        cursor.execute("SELECT option_text, votes_count FROM options WHERE vote_id=?", (vote_id,))
        for opt_text, count in cursor.fetchall():
            layout.addWidget(QLabel(f"{opt_text}: {count} голос(ов)"))
        conn.close()
        self.setLayout(layout)

class ViewVotesWindow(QDialog):
    def __init__(self, user_id, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Список голосований")
        self.user_id = user_id
        layout = QVBoxLayout()
        self.votes_list = QListWidget()
        self.load_votes()
        layout.addWidget(self.votes_list)
        btn_layout = QHBoxLayout()
        vote_btn = QPushButton("Проголосовать")
        results_btn = QPushButton("Результаты")
        vote_btn.clicked.connect(self.vote)
        results_btn.clicked.connect(self.show_results)
        btn_layout.addWidget(vote_btn)
        btn_layout.addWidget(results_btn)
        layout.addLayout(btn_layout)
        self.setLayout(layout)
    def load_votes(self):
        self.votes_list.clear()
        conn = sqlite3.connect('voting.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, title FROM votes")
        for vid, title in cursor.fetchall():
            self.votes_list.addItem(f"{vid}: {title}")
        conn.close()
    def vote(self):
        item = self.votes_list.currentItem()
        if not item:
            QMessageBox.warning(self, "Ошибка", "Выберите голосование")
            return
        vote_id = int(item.text().split(':')[0])
        # Проверяем, голосовал ли уже пользователь
        conn = sqlite3.connect('voting.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM votes_log WHERE user_id=? AND vote_id=?", (self.user_id, vote_id))
        if cursor.fetchone():
            QMessageBox.information(self, "Информация", "Вы уже голосовали в этом голосовании")
            conn.close()
            return
        # Открываем окно голосования
        dlg = VoteDialog(self.user_id, vote_id, self)
        if dlg.exec() == QDialog.DialogCode.Accepted and dlg.selected_option_id:
            # Записываем голос
            try:
                cursor.execute("INSERT INTO votes_log (user_id, vote_id, option_id) VALUES (?, ?, ?)", (self.user_id, vote_id, dlg.selected_option_id))
                cursor.execute("UPDATE options SET votes_count = votes_count + 1 WHERE id=?", (dlg.selected_option_id,))
                conn.commit()
                QMessageBox.information(self, "Успех", "Ваш голос учтён!")
            except sqlite3.IntegrityError:
                QMessageBox.warning(self, "Ошибка", "Вы уже голосовали в этом голосовании")
            finally:
                conn.close()
    def show_results(self):
        item = self.votes_list.currentItem()
        if not item:
            QMessageBox.warning(self, "Ошибка", "Выберите голосование")
            return
        vote_id = int(item.text().split(':')[0])
        dlg = ResultsDialog(vote_id, self)
        dlg.exec()

# --- Окно админ-панели ---
class AdminPanel(QDialog):
    def __init__(self, user_id, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Админ-панель")
        self.user_id = user_id
        layout = QVBoxLayout()
        self.votes_list = QListWidget()
        self.load_votes()
        layout.addWidget(self.votes_list)
        delete_btn = QPushButton("Удалить голосование")
        delete_btn.clicked.connect(self.delete_vote)
        layout.addWidget(delete_btn)
        self.setLayout(layout)
    def load_votes(self):
        self.votes_list.clear()
        conn = sqlite3.connect('voting.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, title FROM votes")
        for vid, title in cursor.fetchall():
            self.votes_list.addItem(f"{vid}: {title}")
        conn.close()
    def delete_vote(self):
        item = self.votes_list.currentItem()
        if not item:
            QMessageBox.warning(self, "Ошибка", "Выберите голосование")
            return
        vote_id = int(item.text().split(':')[0])
        reply = QMessageBox.question(self, "Подтверждение", "Удалить это голосование?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            conn = sqlite3.connect('voting.db')
            cursor = conn.cursor()
            cursor.execute("DELETE FROM votes_log WHERE vote_id=?", (vote_id,))
            cursor.execute("DELETE FROM options WHERE vote_id=?", (vote_id,))
            cursor.execute("DELETE FROM votes WHERE id=?", (vote_id,))
            conn.commit()
            conn.close()
            self.load_votes()
            QMessageBox.information(self, "Успех", "Голосование удалено!")

class MainPage(QWidget):
    def __init__(self, parent, user_id, is_admin):
        super().__init__()
        self.parent = parent
        self.user_id = user_id
        self.is_admin = is_admin
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # Заголовок
        title = QLabel("ЭЛЕКТРОННОЕ ПРЕДВАРИТЕЛЬНОЕ ГОЛОСОВАНИЕ")
        title.setFont(QFont("Arial", 32, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        # Описание
        desc = QLabel("Добро пожаловать в систему онлайн-голосования!\nВыберите действие:")
        desc.setFont(QFont("Arial", 18))
        desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(desc)
        # Кнопки
        btn_layout = QHBoxLayout()
        btn_vote = QPushButton("Голосовать")
        btn_vote.setMinimumHeight(60)
        btn_vote.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        btn_vote.clicked.connect(lambda: self.parent.set_page("vote"))
        btn_layout.addWidget(btn_vote)
        btn_results = QPushButton("Результаты")
        btn_results.setMinimumHeight(60)
        btn_results.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        btn_results.clicked.connect(lambda: self.parent.set_page("results"))
        btn_layout.addWidget(btn_results)
        if self.is_admin:
            btn_admin = QPushButton("Админ-панель")
            btn_admin.setMinimumHeight(60)
            btn_admin.setFont(QFont("Arial", 18, QFont.Weight.Bold))
            btn_admin.clicked.connect(lambda: self.parent.set_page("admin"))
            btn_layout.addWidget(btn_admin)
        layout.addLayout(btn_layout)
        # Таймер (пример)
        self.timer_label = QLabel()
        self.timer_label.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        self.timer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.timer_label)
        self.start_timer()
        self.setLayout(layout)

    def start_timer(self):
        # Пример: до 1 июня 2025 года
        target = QDateTime.fromString("2025-06-01 00:00:00", "yyyy-MM-dd HH:mm:ss")
        self.timer = QTimer(self)
        self.timer.timeout.connect(lambda: self.update_timer(target))
        self.timer.start(1000)
        self.update_timer(target)

    def update_timer(self, target):
        now = QDateTime.currentDateTime()
        secs = now.secsTo(target)
        if secs > 0:
            days = secs // 86400
            hours = (secs % 86400) // 3600
            mins = (secs % 3600) // 60
            s = secs % 60
            self.timer_label.setText(f"До начала голосования: {days} д. {hours} ч. {mins} мин. {s} сек.")
        else:
            self.timer_label.setText("Голосование открыто!")

class StylishMainWindow(QMainWindow):
    def __init__(self, user_id):
        super().__init__()
        self.setWindowTitle("Электронное голосование")
        self.setMinimumSize(1200, 800)
        self.setWindowState(Qt.WindowState.WindowMaximized)
        # Получаем is_admin
        conn = sqlite3.connect('voting.db')
        cursor = conn.cursor()
        cursor.execute("SELECT is_admin FROM users WHERE id=?", (user_id,))
        is_admin = cursor.fetchone()[0]
        conn.close()
        # Слои (страницы)
        self.stack = QStackedWidget()
        self.pages = {}
        # Главная страница
        self.pages["main"] = MainPage(self, user_id, is_admin)
        self.stack.addWidget(self.pages["main"])
        # Страница голосования
        self.pages["vote"] = ViewVotesWindow(user_id, self)
        self.stack.addWidget(self.pages["vote"])
        # Страница результатов
        self.pages["results"] = ResultsDialog(1, self)  # Покажем первый по умолчанию, можно доработать
        self.stack.addWidget(self.pages["results"])
        # Страница админки
        if is_admin:
            self.pages["admin"] = AdminPanel(user_id, self)
            self.stack.addWidget(self.pages["admin"])
        self.setCentralWidget(self.stack)
        self.set_gradient_background()
        self.set_page("main")

    def set_page(self, page):
        if page == "results":
            # Можно сделать выбор голосования для просмотра результатов
            self.pages["results"] = ResultsDialog(1, self)  # TODO: выбор голосования
            self.stack.insertWidget(2, self.pages["results"])
        self.stack.setCurrentWidget(self.pages[page])

    def set_gradient_background(self):
        palette = QPalette()
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0.0, QColor(0, 70, 160))
        gradient.setColorAt(1.0, QColor(0, 30, 80))
        palette.setBrush(QPalette.ColorRole.Window, QBrush(gradient))
        self.setPalette(palette)

def init_database():
    conn = sqlite3.connect('voting.db')
    cursor = conn.cursor()
    print("Инициализация базы данных...")
    # --- Удаляем старую таблицу users ---
    cursor.execute("DROP TABLE IF EXISTS users")
    # --- Новая таблица пользователей ---
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            is_admin BOOLEAN DEFAULT 0
        )
    ''')
    print("Таблица users создана или уже существует.")
    # --- Таблица для логирования голосов ---
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS votes_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            vote_id INTEGER NOT NULL,
            option_id INTEGER NOT NULL,
            UNIQUE(user_id, vote_id),
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (vote_id) REFERENCES votes(id),
            FOREIGN KEY (option_id) REFERENCES options(id)
        )
    ''')
    print("Таблица votes_log создана или уже существует.")
    # --- Остальные таблицы ---
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS votes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS options (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vote_id INTEGER,
            option_text TEXT NOT NULL,
            votes_count INTEGER DEFAULT 0,
            FOREIGN KEY (vote_id) REFERENCES votes(id)
        )
    ''')
    conn.commit()
    conn.close()
    print("База данных инициализирована.")

if __name__ == '__main__':
    init_database()
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setStyleSheet("""
        QMainWindow, QDialog {
            background-color: transparent;
        }
        QLabel {
            font-size: 22px;
            color: #fff;
        }
        QPushButton {
            background-color: #1976d2;
            color: white;
            border: none;
            padding: 16px 32px;
            border-radius: 8px;
            font-size: 20px;
        }
        QPushButton:hover {
            background-color: #1565c0;
        }
        QPushButton:pressed {
            background-color: #0d47a1;
        }
        QLineEdit, QTextEdit {
            padding: 14px;
            border: 1px solid #90caf9;
            border-radius: 8px;
            font-size: 20px;
            background-color: #263859;
            color: #fff;
        }
        QListWidget {
            border: 1px solid #90caf9;
            border-radius: 8px;
            padding: 10px;
            font-size: 20px;
            background-color: #263859;
            color: #fff;
        }
    """)
    auth = AuthWindow()
    if auth.exec() == QDialog.DialogCode.Accepted:
        window = StylishMainWindow(user_id=auth.user_id)
        window.showMaximized()
        sys.exit(app.exec())