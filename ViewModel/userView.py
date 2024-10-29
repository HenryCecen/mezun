import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5 import uic
import os
from pymongo import MongoClient
import ViewModel.openInterface as mainView
from Helper import Logger, message

class MyUser(QDialog):
    def __init__(self, *args, **kwargs):
        super(MyUser, self).__init__(*args, **kwargs)
        uic.loadUi(os.path.join("../view/Account_Interface.ui"), self)

        self.setWindowIcon(QIcon('C:/Users/ASUS/PycharmProjects/mezun/Helper/login_icon.png'))

        self.Connect_To_MongoDB()

        self.user_types() #making choice for user types
        self.press_button() #for buttons

        #writing logger
        global logging
        logging = Logger.Log()

    def user_types(self):
        self.cmbChoice.addItem("")
        self.cmbChoice.addItem("Operator")
        self.cmbChoice.addItem("Administrator")

    def press_button(self):
        self.btnEnter.clicked.connect(self.enter)

    def Connect_To_MongoDB(self):
        self.client = MongoClient('mongodb://localhost:27017/')

        self.db = self.client['Test']
        self.collection = self.db['Users']

        # Write the information to the logger
        logging = Logger.Log()
        logging.info("Connected to MongoDB.")


    def enter(self):
        selected_role = self.cmbChoice.currentText()

        # If the role box is empty
        if selected_role == "":
            message.message_user_role_error()
            logging.info("It showed that User need to select role type.")
        else: # If the role box is selected
            username_document = self.collection.find_one({'role': selected_role})
            if username_document:
                username = username_document.get('username')
                password = username_document.get('password')
                # print(f"User name: {username}, Password: {password}")
                input_username = self.txtUsername.toPlainText()
                input_password = self.txtPassword.toPlainText()
                if input_username == username:
                    if input_password == password:
                        logging.info("Username and password are correct. Main window is opened!")
                        self.close()
                        self.mainWindow = mainView.MyApp()
                        self.mainWindow.show()
                else:
                    logging.info("User not found.")
                    message.user_not_found()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyUser()
    window.show()
    sys.exit(app.exec_())