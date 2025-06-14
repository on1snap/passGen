import sys
import random
import string
import json
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QTextEdit, QMessageBox

def generate_password(length=23):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for i in range(length))

def save_credentials(username, password):
    try:
        with open('credentials.json', 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {}
    data[username] = password
    with open('credentials.json', 'w') as file:
        json.dump(data, file, indent=4)

def get_credentials():
    try:
        with open('credentials.json', 'r') as file:
            data = json.load(file)
        return "\n".join(f"Username: {username}, Password: {password}" for username, password in data.items())
    except FileNotFoundError:
        return "No credentials saved yet."

class passGen(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("Enter username")
        layout.addWidget(self.username_input)

        self.password_output = QTextEdit(self)
        self.password_output.setPlaceholderText("Generated password appears here")
        self.password_output.setReadOnly(True)
        layout.addWidget(self.password_output)

        generate_btn = QPushButton('Generate and Save Password', self)
        generate_btn.clicked.connect(self.generate_and_save_password)
        layout.addWidget(generate_btn)

        retrieve_btn = QPushButton('Retrieve Passwords', self)
        retrieve_btn.clicked.connect(self.display_passwords)
        layout.addWidget(retrieve_btn)

        self.setLayout(layout)
        self.setWindowTitle('passGen')
        self.setGeometry(300, 300, 400, 300)

    def generate_and_save_password(self):
        username = self.username_input.text()
        if username:
            password = generate_password()
            save_credentials(username, password)
            self.password_output.setText(f"{password}")
        else:
            QMessageBox.warning(self, 'Error', 'Username cannot be empty.')

    def display_passwords(self):
        credentials = get_credentials()
        self.password_output.setText(credentials)

def main():
    app = QApplication(sys.argv)
    ex = passGen()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
