import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                            QPushButton, QLabel, QLineEdit, QMessageBox, QDialog, QFormLayout, QTextEdit, QListWidget, QInputDialog, QStackedWidget, QComboBox, QSizePolicy, QToolTip, QTableWidget, QTableWidgetItem)
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
        self.setStyleSheet("background: #eaf6fa;")
        # Фоновый слой (светлый)
        main_vlayout = QVBoxLayout(self)
        main_vlayout.setContentsMargins(0, 0, 0, 0)
        main_vlayout.setSpacing(0)
        main_vlayout.addStretch(1)
        # Центрируем карточку
        center_h = QHBoxLayout()
        center_h.addStretch(1)
        # Карточка
        card = QWidget()
        card.setFixedWidth(420)
        card.setStyleSheet("""
            QWidget {
                background: #fff;
                border-radius: 28px;
                box-shadow: 0 8px 32px rgba(0,0,0,0.10);
            }
        """)
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(36, 36, 36, 36)
        card_layout.setSpacing(18)
        # Иконка сверху (если нужна)
        icon_label = QLabel()
        icon_pix = QPixmap(32, 32)
        icon_pix.fill(Qt.GlobalColor.transparent)
        icon_label.setPixmap(QPixmap(":/qt-project.org/styles/commonstyle/images/dirclosed-128.png").scaled(48, 48, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(icon_label)
        # Заголовок
        title = QLabel("Вход в систему")
        title.setFont(QFont("Arial", 22, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(title)
        # Форма
        form = QVBoxLayout()
        form.setSpacing(12)
        # --- Логин ---
        login_box = QVBoxLayout()
        login_label = QLabel("Имя пользователя")
        login_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        login_box.addWidget(login_label)
        login_field_layout = QHBoxLayout()
        login_icon = QLabel()
        login_icon.setPixmap(QPixmap(":/qt-project.org/styles/commonstyle/images/standardbutton-apply-32.png").scaled(20, 20, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        login_icon.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        login_icon.setToolTip("Только буквы, цифры и символы @/./+/-/_")
        login_field_layout.addWidget(login_icon)
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Введите логин")
        self.username_input.setMinimumHeight(40)
        self.username_input.setFont(QFont("Arial", 14))
        self.username_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid #b6e0fe;
                border-radius: 10px;
                padding-left: 8px;
                background: #fafdff;
                color: #222;
            }
            QLineEdit:focus {
                border: 2px solid #4fc3f7;
                background: #f0faff;
            }
        """)
        login_field_layout.addWidget(self.username_input)
        login_box.addLayout(login_field_layout)
        form.addLayout(login_box)
        # --- Пароль ---
        pass_box = QVBoxLayout()
        pass_label = QLabel("Пароль")
        pass_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        pass_box.addWidget(pass_label)
        pass_field_layout = QHBoxLayout()
        pass_icon = QLabel()
        pass_icon.setPixmap(QPixmap(":/qt-project.org/styles/commonstyle/images/standardbutton-cancel-32.png").scaled(20, 20, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        pass_icon.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        pass_icon.setToolTip("Минимум 8 символов. Не используйте слишком простой пароль.")
        pass_field_layout.addWidget(pass_icon)
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Введите пароль")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setMinimumHeight(40)
        self.password_input.setFont(QFont("Arial", 14))
        self.password_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid #b6e0fe;
                border-radius: 10px;
                padding-left: 8px;
                background: #fafdff;
                color: #222;
            }
            QLineEdit:focus {
                border: 2px solid #4fc3f7;
                background: #f0faff;
            }
        """)
        pass_field_layout.addWidget(self.password_input)
        pass_box.addLayout(pass_field_layout)
        form.addLayout(pass_box)
        # --- Код администратора ---
        admin_box = QVBoxLayout()
        admin_label = QLabel("Код администратора (если есть)")
        admin_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        admin_box.addWidget(admin_label)
        self.admin_code_input = QLineEdit()
        self.admin_code_input.setPlaceholderText("Оставьте пустым, если не админ")
        self.admin_code_input.setMinimumHeight(40)
        self.admin_code_input.setFont(QFont("Arial", 14))
        self.admin_code_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid #b6e0fe;
                border-radius: 10px;
                padding-left: 8px;
                background: #fafdff;
                color: #222;
            }
            QLineEdit:focus {
                border: 2px solid #4fc3f7;
                background: #f0faff;
            }
        """)
        admin_box.addWidget(self.admin_code_input)
        form.addLayout(admin_box)
        card_layout.addLayout(form)
        # Кнопка
        card_layout.addSpacing(10)
        self.login_btn = QPushButton("Войти")
        self.login_btn.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        self.login_btn.setMinimumHeight(48)
        self.login_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #4fc3f7, stop:1 #1976d2);
                color: white;
                border-radius: 12px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #1976d2, stop:1 #4fc3f7);
            }
        """)
        self.register_btn = QPushButton("Зарегистрироваться")
        self.register_btn.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        self.register_btn.setMinimumHeight(48)
        self.register_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #43e97b, stop:1 #38f9d7);
                color: #222;
                border-radius: 12px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #38f9d7, stop:1 #43e97b);
            }
        """)
        card_layout.addWidget(self.login_btn)
        card_layout.addWidget(self.register_btn)
        # Сообщение об авторских правах
        copyright = QLabel("© 2025 Онлайн-голосование")
        copyright.setFont(QFont("Arial", 10))
        copyright.setAlignment(Qt.AlignmentFlag.AlignCenter)
        copyright.setStyleSheet("color: #b0b0b0; margin-top: 10px;")
        card_layout.addWidget(copyright)
        center_h.addWidget(card)
        center_h.addStretch(1)
        main_vlayout.addLayout(center_h)
        main_vlayout.addStretch(1)
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
            show_pretty_message(self, "Ошибка", "Введите логин и пароль", QMessageBox.Icon.Warning)
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
            show_pretty_message(self, "Ошибка", "Неверный логин или пароль")

    def register(self):
        username = self.username_input.text().strip()
        password = self.password_input.text()
        admin_code = self.admin_code_input.text().strip()  # Получаем код админа
        if not username or not password:
            show_pretty_message(self, "Ошибка", "Введите логин и пароль", QMessageBox.Icon.Warning)
            return
        conn = sqlite3.connect('voting.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE username=?", (username,))
        if cursor.fetchone():
            show_pretty_message(self, "Ошибка", "Пользователь с таким логином уже существует")
            conn.close()
            return
        password_hash = self.hash_password(password)
        is_admin = 1 if admin_code == "admin123" else 0  # Проверяем код админа
        cursor.execute("INSERT INTO users (username, password_hash, is_admin) VALUES (?, ?, ?)", (username, password_hash, is_admin))
        conn.commit()
        conn.close()
        show_pretty_message(self, "Успех", "Пользователь зарегистрирован! Теперь войдите.")

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
            show_pretty_message(self, "Ошибка", "Введите название голосования")
            return
        
        if not options:
            show_pretty_message(self, "Ошибка", "Добавьте хотя бы один вариант ответа")
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
            show_pretty_message(self, "Успех", "Голосование успешно создано!")
            self.accept()
            
        except sqlite3.Error as e:
            show_pretty_message(self, "Ошибка", f"Ошибка при сохранении: {str(e)}")
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
            show_pretty_message(self, "Ошибка", "Выберите голосование")
            return
        vote_id = int(item.text().split(':')[0])
        # Проверяем, голосовал ли уже пользователь
        conn = sqlite3.connect('voting.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM votes_log WHERE user_id=? AND vote_id=?", (self.user_id, vote_id))
        if cursor.fetchone():
            show_pretty_message(self, "Информация", "Вы уже голосовали в этом голосовании")
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
                show_pretty_message(self, "Успех", "Ваш голос учтён!")
            except sqlite3.IntegrityError:
                show_pretty_message(self, "Ошибка", "Вы уже голосовали в этом голосовании")
            finally:
                conn.close()
    def show_results(self):
        item = self.votes_list.currentItem()
        if not item:
            show_pretty_message(self, "Ошибка", "Выберите голосование")
            return
        vote_id = int(item.text().split(':')[0])
        dlg = ResultsDialog(vote_id, self)
        dlg.exec()

# --- Окно админ-панели ---
class UsersTableDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Пользователи")
        self.setMinimumSize(500, 400)
        layout = QVBoxLayout(self)
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["ID", "Логин", "Админ"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        layout.addWidget(self.table)
        self.load_users()
    def load_users(self):
        conn = sqlite3.connect('voting.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, is_admin FROM users")
        users = cursor.fetchall()
        self.table.setRowCount(len(users))
        for row, (uid, username, is_admin) in enumerate(users):
            self.table.setItem(row, 0, QTableWidgetItem(str(uid)))
            self.table.setItem(row, 1, QTableWidgetItem(username))
            self.table.setItem(row, 2, QTableWidgetItem("Да" if is_admin else "Нет"))
        conn.close()

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
        # Кнопка пользователей
        users_btn = QPushButton("Пользователи")
        users_btn.clicked.connect(self.show_users)
        layout.addWidget(users_btn)
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
            show_pretty_message(self, "Ошибка", "Выберите голосование")
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
            show_pretty_message(self, "Успех", "Голосование удалено!")
    def show_users(self):
        dlg = UsersTableDialog(self)
        dlg.exec()

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
    # cursor.execute("DROP TABLE IF EXISTS users")  # УДАЛЕНО, чтобы не стирать пользователей
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

def show_pretty_message(parent, title, text, icon=QMessageBox.Icon.Warning):
    msg = QMessageBox(parent)
    msg.setWindowTitle(title)
    msg.setText(text)
    msg.setIcon(icon)
    msg.setStyleSheet('''
        QMessageBox {
            background: #fff;
            border-radius: 16px;
        }
        QLabel {
            color: #222;
            font-size: 18px;
        }
        QPushButton {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #4fc3f7, stop:1 #1976d2);
            color: white;
            border-radius: 10px;
            min-width: 80px;
            min-height: 32px;
            font-size: 16px;
        }
        QPushButton:hover {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #1976d2, stop:1 #4fc3f7);
        }
    ''')
    msg.exec()

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
        QToolTip {
            color: #222;
            background: #fffbe6;
            border: 1px solid #ffd600;
            font-size: 13px;
        }
    """)
    auth = AuthWindow()
    if auth.exec() == QDialog.DialogCode.Accepted:
        window = StylishMainWindow(user_id=auth.user_id)
        window.showMaximized()
        sys.exit(app.exec())