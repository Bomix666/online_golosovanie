import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                            QPushButton, QLabel, QLineEdit, QMessageBox, QDialog, QFormLayout, QTextEdit, QListWidget, QInputDialog, QStackedWidget, QComboBox, QSizePolicy, QToolTip, QTableWidget, QTableWidgetItem, QFileDialog, QHeaderView)
from PyQt6.QtCore import Qt, QTimer, QDateTime
from PyQt6.QtGui import QFont, QPalette, QLinearGradient, QColor, QBrush, QPixmap
import sqlite3
import hashlib
import csv
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

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
        
        # Кнопка возврата
        back_btn = QPushButton("Назад")
        back_btn.clicked.connect(self.go_back)
        
        # Добавляем все элементы на форму
        layout.addLayout(form_layout)
        layout.addLayout(options_buttons_layout)
        layout.addWidget(save_btn)
        layout.addWidget(back_btn)
        
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

    def go_back(self):
        self.close()

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
    def __init__(self, vote_id=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Результаты голосований")
        self.setMinimumSize(900, 600)
        layout = QVBoxLayout()

        # Таблица результатов
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Голосование", "Вариант ответа", "Голосов", "%"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)  # Запретить редактирование
        layout.addWidget(self.table)

        self.load_results()

        # Кнопка возврата
        btn_back = QPushButton("Назад")
        btn_back.setMinimumHeight(40)
        btn_back.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        btn_back.clicked.connect(self.go_back)
        layout.addWidget(btn_back)
        self.setLayout(layout)

    def load_results(self):
        conn = sqlite3.connect('voting.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, title FROM votes")
        votes = cursor.fetchall()
        rows = []
        for vote_id, title in votes:
            cursor.execute("SELECT SUM(votes_count) FROM options WHERE vote_id=?", (vote_id,))
            total_votes = cursor.fetchone()[0] or 0
            cursor.execute("SELECT option_text, votes_count FROM options WHERE vote_id=?", (vote_id,))
            for option_text, votes_count in cursor.fetchall():
                percent = (votes_count / total_votes * 100) if total_votes > 0 else 0
                rows.append((title, option_text, votes_count, f"{percent:.1f}%"))
        self.table.setRowCount(len(rows))
        for row, (title, option_text, votes_count, percent) in enumerate(rows):
            self.table.setItem(row, 0, QTableWidgetItem(str(title)))
            self.table.setItem(row, 1, QTableWidgetItem(str(option_text)))
            self.table.setItem(row, 2, QTableWidgetItem(str(votes_count)))
            self.table.setItem(row, 3, QTableWidgetItem(str(percent)))
        conn.close()

    def go_back(self):
        self.close()
        main_window = self.parent()
        while main_window and not isinstance(main_window, StylishMainWindow):
            main_window = main_window.parent()
        if main_window:
            main_window.set_page("main")

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
        # Кнопка возврата
        btn_back = QPushButton("Назад")
        btn_back.setMinimumHeight(40)
        btn_back.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        btn_back.clicked.connect(self.go_back)
        layout.addWidget(btn_back)
        # Кнопка выхода
        btn_logout = QPushButton("Выйти")
        btn_logout.setMinimumHeight(40)
        btn_logout.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        btn_logout.clicked.connect(self.logout)
        layout.addWidget(btn_logout)
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
    def logout(self):
        self.close()
        # Показать окно авторизации
        auth = AuthWindow()
        if auth.exec() == QDialog.DialogCode.Accepted:
            new_window = StylishMainWindow(user_id=auth.user_id)
            new_window.showMaximized()
            QApplication.instance().exec()

    def go_back(self):
        self.close()
        # Find the main window and set the page
        main_window = self.parent()
        while main_window and not isinstance(main_window, StylishMainWindow):
            main_window = main_window.parent()
        if main_window:
            main_window.set_page("main")

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

class EditVoteWindow(QDialog):
    def __init__(self, vote_id, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Редактирование голосования")
        self.setGeometry(200, 200, 600, 400)
        self.vote_id = vote_id
        
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
        save_btn = QPushButton("Сохранить изменения")
        save_btn.clicked.connect(self.save_vote)
        
        # Кнопка возврата
        back_btn = QPushButton("Назад")
        back_btn.clicked.connect(self.go_back)
        
        # Загружаем существующие данные
        self.load_vote_data()
        
        # Добавляем все элементы на форму
        layout.addLayout(form_layout)
        layout.addLayout(options_buttons_layout)
        layout.addWidget(save_btn)
        layout.addWidget(back_btn)
        
        self.setLayout(layout)
    
    def load_vote_data(self):
        conn = sqlite3.connect('voting.db')
        cursor = conn.cursor()
        
        # Загружаем данные голосования
        cursor.execute("SELECT title, description FROM votes WHERE id=?", (self.vote_id,))
        vote_data = cursor.fetchone()
        if vote_data:
            self.title_input.setText(vote_data[0])
            self.description_input.setText(vote_data[1])
        
        # Загружаем варианты ответов
        cursor.execute("SELECT id, option_text FROM options WHERE vote_id=?", (self.vote_id,))
        for option_id, option_text in cursor.fetchall():
            self.options_list.addItem(option_text)
        
        conn.close()
    
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
            
            # Обновляем голосование
            cursor.execute('''
                UPDATE votes 
                SET title = ?, description = ?
                WHERE id = ?
            ''', (title, description, self.vote_id))
            
            # Удаляем старые варианты
            cursor.execute("DELETE FROM options WHERE vote_id=?", (self.vote_id,))
            
            # Добавляем новые варианты
            for option in options:
                cursor.execute('''
                    INSERT INTO options (vote_id, option_text)
                    VALUES (?, ?)
                ''', (self.vote_id, option))
            
            conn.commit()
            show_pretty_message(self, "Успех", "Голосование успешно обновлено!")
            self.accept()
            
        except sqlite3.Error as e:
            show_pretty_message(self, "Ошибка", f"Ошибка при сохранении: {str(e)}")
        finally:
            conn.close()

    def go_back(self):
        self.close()

class VoteStatisticsDialog(QDialog):
    def __init__(self, vote_id, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Статистика голосования")
        self.setMinimumSize(600, 400)
        self.vote_id = vote_id
        
        layout = QVBoxLayout()
        
        # Таблица статистики
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Вариант ответа", "Количество голосов", "Процент"])
        self.table.horizontalHeader().setStretchLastSection(True)
        
        # Загружаем статистику
        self.load_statistics()
        
        layout.addWidget(self.table)
        self.setLayout(layout)
    
    def load_statistics(self):
        conn = sqlite3.connect('voting.db')
        cursor = conn.cursor()
        
        # Получаем общее количество голосов
        cursor.execute("""
            SELECT SUM(votes_count) 
            FROM options 
            WHERE vote_id = ?
        """, (self.vote_id,))
        total_votes = cursor.fetchone()[0] or 0
        
        # Получаем статистику по вариантам
        cursor.execute("""
            SELECT option_text, votes_count 
            FROM options 
            WHERE vote_id = ?
        """, (self.vote_id,))
        
        options = cursor.fetchall()
        self.table.setRowCount(len(options))
        
        for row, (option_text, votes) in enumerate(options):
            percentage = (votes / total_votes * 100) if total_votes > 0 else 0
            
            self.table.setItem(row, 0, QTableWidgetItem(option_text))
            self.table.setItem(row, 1, QTableWidgetItem(str(votes)))
            self.table.setItem(row, 2, QTableWidgetItem(f"{percentage:.1f}%"))
        
        conn.close()

class UserManagementDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Управление пользователями")
        self.setMinimumSize(600, 400)
        
        layout = QVBoxLayout()
        
        # Таблица пользователей
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Логин", "Админ", "Действия"])
        self.table.horizontalHeader().setStretchLastSection(True)
        
        # Загружаем пользователей
        self.load_users()
        
        layout.addWidget(self.table)
        self.setLayout(layout)
    
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
            
            # Кнопка изменения прав
            toggle_btn = QPushButton("Изменить права")
            toggle_btn.clicked.connect(lambda checked, u=uid, a=is_admin: self.toggle_admin_rights(u, a))
            self.table.setCellWidget(row, 3, toggle_btn)
        
        conn.close()
    
    def toggle_admin_rights(self, user_id, current_status):
        try:
            conn = sqlite3.connect('voting.db')
            cursor = conn.cursor()
            
            # Меняем статус админа на противоположный
            new_status = 0 if current_status else 1
            cursor.execute("UPDATE users SET is_admin = ? WHERE id = ?", (new_status, user_id))
            conn.commit()
            
            show_pretty_message(self, "Успех", "Права пользователя обновлены!")
            self.load_users()  # Перезагружаем таблицу
            
        except sqlite3.Error as e:
            show_pretty_message(self, "Ошибка", f"Ошибка при обновлении прав: {str(e)}")
        finally:
            conn.close()

class AdminPanel(QDialog):
    def __init__(self, user_id, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Админ-панель")
        self.user_id = user_id
        layout = QVBoxLayout()
        
        # Список голосований
        self.votes_list = QListWidget()
        self.load_votes()
        layout.addWidget(self.votes_list)
        
        # Кнопки управления голосованиями
        votes_buttons_layout = QHBoxLayout()
        create_vote_btn = QPushButton("Создать голосование")
        edit_vote_btn = QPushButton("Редактировать")
        delete_btn = QPushButton("Удалить голосование")
        stats_btn = QPushButton("Расширенная статистика")
        
        create_vote_btn.clicked.connect(self.create_vote)
        edit_vote_btn.clicked.connect(self.edit_vote)
        delete_btn.clicked.connect(self.delete_vote)
        stats_btn.clicked.connect(self.show_enhanced_statistics)
        
        votes_buttons_layout.addWidget(create_vote_btn)
        votes_buttons_layout.addWidget(edit_vote_btn)
        votes_buttons_layout.addWidget(delete_btn)
        votes_buttons_layout.addWidget(stats_btn)
        layout.addLayout(votes_buttons_layout)
        
        # Кнопка управления пользователями
        users_btn = QPushButton("Расширенное управление пользователями")
        users_btn.clicked.connect(self.show_enhanced_user_management)
        layout.addWidget(users_btn)
        
        # Кнопка возврата
        btn_back = QPushButton("Назад")
        btn_back.setMinimumHeight(40)
        btn_back.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        btn_back.clicked.connect(self.go_back)
        layout.addWidget(btn_back)
        
        # Кнопка выхода
        btn_logout = QPushButton("Выйти")
        btn_logout.setMinimumHeight(40)
        btn_logout.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        btn_logout.clicked.connect(self.logout)
        layout.addWidget(btn_logout)
        
        self.setLayout(layout)

    def create_vote(self):
        dlg = CreateVoteWindow(self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            self.load_votes()  # Обновляем список голосований после создания

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

    def edit_vote(self):
        item = self.votes_list.currentItem()
        if not item:
            show_pretty_message(self, "Ошибка", "Выберите голосование для редактирования")
            return
        vote_id = int(item.text().split(':')[0])
        dlg = EditVoteWindow(vote_id, self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            self.load_votes()

    def show_enhanced_statistics(self):
        item = self.votes_list.currentItem()
        if not item:
            show_pretty_message(self, "Ошибка", "Выберите голосование для просмотра статистики")
            return
        vote_id = int(item.text().split(':')[0])
        dlg = EnhancedVoteStatisticsDialog(vote_id, self)
        dlg.exec()

    def show_enhanced_user_management(self):
        dlg = EnhancedUserManagementDialog(self)
        dlg.exec()

    def logout(self):
        self.close()
        # Показать окно авторизации
        auth = AuthWindow()
        if auth.exec() == QDialog.DialogCode.Accepted:
            new_window = StylishMainWindow(user_id=auth.user_id)
            new_window.showMaximized()
            QApplication.instance().exec()

    def go_back(self):
        self.close()
        # Find the main window and set the page
        main_window = self.parent()
        while main_window and not isinstance(main_window, StylishMainWindow):
            main_window = main_window.parent()
        if main_window:
            main_window.set_page("main")

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
        # Кнопка выхода
        btn_logout = QPushButton("Выйти")
        btn_logout.setMinimumHeight(40)
        btn_logout.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        btn_logout.clicked.connect(self.parent.logout)
        layout.addWidget(btn_logout)
        # Таймер (пример)
        self.timer_label = QLabel()
        self.timer_label.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        self.timer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.timer_label)
        self.start_timer()
        self.setLayout(layout)

    def start_timer(self):
        # Новый дедлайн: 9 июня 2025 года
        target = QDateTime.fromString("2025-06-09 00:00:00", "yyyy-MM-dd HH:mm:ss")
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

    def logout(self):
        self.close()
        # Показать окно авторизации
        auth = AuthWindow()
        if auth.exec() == QDialog.DialogCode.Accepted:
            new_window = StylishMainWindow(user_id=auth.user_id)
            new_window.showMaximized()
            QApplication.instance().exec()

def init_database():
    conn = sqlite3.connect('voting.db')
    cursor = conn.cursor()
    print("Инициализация базы данных...")
    
    # --- Таблица пользователей ---
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            is_admin BOOLEAN DEFAULT 0,
            last_login TIMESTAMP
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
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
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
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            end_date TIMESTAMP
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
    # --- Автоматическое создание тестового администратора ---
    cursor.execute("SELECT id FROM users WHERE username=?", ("admin",))
    if not cursor.fetchone():
        import hashlib
        password_hash = hashlib.sha256("admin12345".encode('utf-8')).hexdigest()
        cursor.execute("INSERT INTO users (username, password_hash, is_admin) VALUES (?, ?, ?)", ("admin", password_hash, 1))
        print("Тестовый администратор создан: admin / admin12345")
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

class EnhancedVoteStatisticsDialog(QDialog):
    def __init__(self, vote_id, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Расширенная статистика голосования")
        self.setMinimumSize(800, 600)
        self.vote_id = vote_id
        layout = QVBoxLayout()
        top_panel = QHBoxLayout()
        export_btn = QPushButton("Экспорт в CSV")
        export_btn.clicked.connect(self.export_to_csv)
        top_panel.addWidget(export_btn)
        layout.addLayout(top_panel)
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Вариант ответа", "Количество голосов", "Процент", "Последнее голосование"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.figure = Figure(figsize=(8, 4))
        self.canvas = FigureCanvas(self.figure)
        self.load_statistics()
        layout.addWidget(self.table)
        layout.addWidget(self.canvas)
        back_btn = QPushButton("Назад")
        back_btn.clicked.connect(self.go_back)
        layout.addWidget(back_btn)
        self.setLayout(layout)
    def load_statistics(self):
        conn = sqlite3.connect('voting.db')
        cursor = conn.cursor()
        cursor.execute("SELECT SUM(votes_count) FROM options WHERE vote_id = ?", (self.vote_id,))
        total_votes = cursor.fetchone()[0] or 0
        cursor.execute("""
            SELECT o.option_text, o.votes_count, 
                   (SELECT MAX(vl.timestamp) FROM votes_log vl WHERE vl.option_id = o.id)
            FROM options o
            WHERE o.vote_id = ?
        """, (self.vote_id,))
        options = cursor.fetchall()
        self.table.setRowCount(len(options))
        labels = []
        sizes = []
        for row, (option_text, votes, last_vote) in enumerate(options):
            percentage = (votes / total_votes * 100) if total_votes > 0 else 0
            if last_vote is None:
                last_vote_str = "Нет голосов"
            elif isinstance(last_vote, str):
                last_vote_str = last_vote.split('.')[0]
            else:
                last_vote_str = str(last_vote)
            self.table.setItem(row, 0, QTableWidgetItem(option_text))
            self.table.setItem(row, 1, QTableWidgetItem(str(votes)))
            self.table.setItem(row, 2, QTableWidgetItem(f"{percentage:.1f}%"))
            self.table.setItem(row, 3, QTableWidgetItem(last_vote_str))
            labels.append(option_text)
            sizes.append(votes)
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        filtered_labels = [l for l, s in zip(labels, sizes) if s > 0]
        filtered_sizes = [s for s in sizes if s > 0]
        if any(filtered_sizes):
            wedges, texts, autotexts = ax.pie(filtered_sizes, labels=None, autopct='%1.1f%%')
            legend = ax.legend(wedges, filtered_labels, title="Варианты", loc="lower center", bbox_to_anchor=(0.5, -0.15), fontsize=10, title_fontsize=11, ncol=2)
            ax.axis('equal')
        else:
            ax.text(0.5, 0.5, 'Нет данных для отображения', ha='center', va='center', fontsize=16)
        self.canvas.draw()
        conn.close()
    def export_to_csv(self):
        file_name, _ = QFileDialog.getSaveFileName(
            self,
            "Сохранить статистику",
            "",
            "CSV Files (*.csv)"
        )
        
        if file_name:
            try:
                with open(file_name, 'w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    # Записываем заголовки
                    writer.writerow(['Вариант ответа', 'Количество голосов', 'Процент', 'Последнее голосование'])
                    
                    # Записываем данные
                    for row in range(self.table.rowCount()):
                        row_data = []
                        for col in range(self.table.columnCount()):
                            item = self.table.item(row, col)
                            row_data.append(item.text() if item else '')
                        writer.writerow(row_data)
                
                show_pretty_message(self, "Успех", "Статистика успешно экспортирована!")
            except Exception as e:
                show_pretty_message(self, "Ошибка", f"Ошибка при экспорте: {str(e)}")
    def go_back(self):
        self.close()

class EnhancedUserManagementDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Управление пользователями")
        self.setMinimumSize(800, 600)
        
        layout = QVBoxLayout()
        
        # Панель поиска
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Поиск пользователей...")
        self.search_input.textChanged.connect(self.filter_users)
        search_layout.addWidget(self.search_input)
        layout.addLayout(search_layout)
        
        # Таблица пользователей
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Логин", "Админ", "Последний вход", "Действия"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setDefaultSectionSize(36)  # уменьшенная высота строк
        self.table.setStyleSheet("QTableWidget { font-size: 16px; } QPushButton { min-width: 120px; min-height: 28px; font-size: 14px; }")
        
        # Загружаем пользователей
        self.load_users()
        
        layout.addWidget(self.table)
        
        # Кнопка возврата
        back_btn = QPushButton("Назад")
        back_btn.clicked.connect(self.go_back)
        layout.addWidget(back_btn)
        
        self.setLayout(layout)
    
    def load_users(self):
        conn = sqlite3.connect('voting.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, is_admin, last_login FROM users")
        users = cursor.fetchall()
        
        self.table.setRowCount(len(users))
        for row, (uid, username, is_admin, last_login) in enumerate(users):
            self.table.setItem(row, 0, QTableWidgetItem(str(uid)))
            self.table.setItem(row, 1, QTableWidgetItem(username))
            self.table.setItem(row, 2, QTableWidgetItem("Да" if is_admin else "Нет"))
            self.table.setItem(row, 3, QTableWidgetItem(last_login if last_login else "—"))
            # Кнопка изменения прав
            toggle_btn = QPushButton("Изменить права")
            toggle_btn.setMinimumWidth(120)
            toggle_btn.setMaximumWidth(140)
            toggle_btn.setMinimumHeight(28)
            toggle_btn.setStyleSheet("font-size: 14px; padding: 2px 8px;")
            toggle_btn.clicked.connect(lambda checked, u=uid, a=is_admin: self.toggle_admin_rights(u, a))
            self.table.setCellWidget(row, 4, toggle_btn)
            self.table.setRowHeight(row, 36)
        conn.close()
    
    def filter_users(self):
        search_text = self.search_input.text().lower()
        for row in range(self.table.rowCount()):
            show_row = False
            for col in range(2):  # Ищем только в колонках ID и Логин
                item = self.table.item(row, col)
                if item and search_text in item.text().lower():
                    show_row = True
                    break
            self.table.setRowHidden(row, not show_row)
    
    def toggle_admin_rights(self, user_id, current_status):
        try:
            conn = sqlite3.connect('voting.db')
            cursor = conn.cursor()
            # Меняем статус админа на противоположный
            new_status = 0 if current_status else 1
            cursor.execute("UPDATE users SET is_admin = ? WHERE id = ?", (new_status, user_id))
            conn.commit()
            show_pretty_message(self, "Успех", "Права пользователя обновлены!")
            self.load_users()  # Перезагружаем таблицу
        except sqlite3.Error as e:
            show_pretty_message(self, "Ошибка", f"Ошибка при обновлении прав: {str(e)}")
        finally:
            conn.close()
    
    def go_back(self):
        self.close()

def fill_it_votes():
    conn = sqlite3.connect('voting.db')
    cursor = conn.cursor()
    # Проверяем, есть ли уже такие голосования
    cursor.execute('SELECT title FROM votes')
    existing_titles = set(row[0] for row in cursor.fetchall())
    votes_to_add = [
        ('Лучший язык программирования', 'Выберите язык, который вы считаете лучшим для разработки.', ['Python', 'JavaScript', 'C++', 'Java', 'Go', 'Rust']),
        ('Любимая среда разработки (IDE)', 'Какой редактор или IDE вы предпочитаете?', ['PyCharm', 'VS Code', 'IntelliJ IDEA', 'Sublime Text', 'Vim', 'Eclipse']),
        ('Лучший веб-фреймворк', 'Выберите веб-фреймворк, который вам больше всего нравится.', ['Django', 'Flask', 'FastAPI', 'Express', 'Spring', 'Ruby on Rails']),
        ('Linux или Windows?', 'Какую ОС вы предпочитаете для работы?', ['Linux', 'Windows', 'macOS', 'BSD']),
        ('Самый полезный IT-скилл', 'Какой навык в IT вы считаете самым важным?', ['Алгоритмы', 'Базы данных', 'DevOps', 'UI/UX', 'Безопасность', 'Soft Skills'])
    ]
    for title, desc, options in votes_to_add:
        if title in existing_titles:
            continue
        cursor.execute('INSERT INTO votes (title, description) VALUES (?, ?)', (title, desc))
        vid = cursor.lastrowid
        for opt in options:
            cursor.execute('INSERT INTO options (vote_id, option_text) VALUES (?, ?)', (vid, opt))
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_database()
    fill_it_votes()
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