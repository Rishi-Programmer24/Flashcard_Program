import sys
import os
import re 
import json
from PyQt5.QtCore import Qt  
from PyQt5.QtWidgets import(
    QApplication, QMainWindow, QStackedWidget, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit,
    QListWidget, QComboBox, QFormLayout, QMessageBox, QInputDialog, QTextEdit, QHBoxLayout, QTableWidget,
    QTableWidgetItem, QDialog, QTreeWidget, QTreeWidgetItem, QDialogButtonBox)
#global imports for the program to run 

# JSON database files
Users_db = 'users.json'
Decks_db = 'decks.json'

def load_json(filename): #method to load the json data
    if os.path.exists(filename):
        with open(filename, 'r') as f: #open the json file
            return json.load(f)
    return {'users': []} if filename == Users_db else {'decks': []} #return the users if the filename is Users_db, otherwise return the decks

def save_json(data, filename): #method to save the json data
    with open(filename, 'w') as f: #open the json file
        json.dump(data, f, indent=2) #save the data to the json file

class User_Auth: #class to authenticate users
    def __init__(self):
        self.users = {}
        self.load_users()
        
    def load_users(self): #method to load users
        data = load_json(Users_db) #load the users from the json file
        self.users = {user['username']: user['password'] for user in data['users']} #set the users to the data
 
    def sign_in(self, username, password): #method to sign in
        if username in self.users:
            return False
        data = load_json(Users_db)
        data['users'].append({'username': username, 'password': password}) #append the username and password to the data
        save_json(data, Users_db)
        self.users[username] = password
        return True

    def login(self, username, password): #method to login
        return self.users.get(username) == password

class Login_Window(QWidget): #initialises the login part
    def __init__(self, auth):
        super().__init__()
        self.resize(800, 550)
        self.setWindowTitle("Login")
        self.layout = QVBoxLayout()
        
        # Create a text input field for the username
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        # Create a text input field for the password
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        # this hides the password
        self.password_input.setEchoMode(QLineEdit.Password) 
        
        # Create a button to login
        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.check_credentials)
        self.signup_button = QPushButton("Sign Up")
        self.signup_button.clicked.connect(self.go_to_signup)
        
        # Add UI elements to the page layout
        login_label = QLabel("Login to Flashcard App")
        login_label.setAlignment(Qt.AlignCenter)
        font = login_label.font()
        font.setPointSize(25)
        login_label.setFont(font)
        
        self.layout.addWidget(login_label) #add the login label
        self.layout.addWidget(self.username_input)
        self.layout.addWidget(self.password_input)
        self.layout.addWidget(self.login_button)
        self.layout.addWidget(self.signup_button)
        self.setLayout(self.layout)
        
        self.auth = auth #set the auth to the auth

    def check_credentials(self): #method to check the credentials
        username = self.username_input.text()
        password = self.password_input.text()
        if self.auth.login(username, password):
            QMessageBox.information(self, "Success", "Login successful!")
            self.open_flashcard_app()
        else:
            QMessageBox.warning(self, "Error", "Invalid credentials.")

    def open_flashcard_app(self): #opens the flashcard app
        self.main_window = Main_Window()
        self.main_window.show()
        self.close()

    #Allows user to go to the sign up page
    def go_to_signup(self):
        self.signup_window = Signup_Window(self.auth)
        self.signup_window.show()
        self.close()

class Signup_Window(QWidget): #initialises the sign up part
    def __init__(self, auth):
        super().__init__()
        self.resize(1280, 720)
        self.setWindowTitle("Sign Up")
        self.layout = QVBoxLayout() 

        self.username_input = QLineEdit() #create a text input field for the username
        self.username_input.setPlaceholderText("Username")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setPlaceholderText("Confirm Password") 
        #tghios cerated a text input for the password confirmation
        self.confirm_password_input.setEchoMode(QLineEdit.Password)

        self.signup_button = QPushButton("Sign Up") #create a button to sign up
        self.signup_button.clicked.connect(self.sign_in_user)
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.go_back)

        signup_label = QLabel("Create a New Account")
        signup_label.setAlignment(Qt.AlignCenter)  # Center the text
        font = signup_label.font()
        font.setPointSize(25)
        signup_label.setFont(font)

        self.layout.addWidget(signup_label) #add the signup label
        self.layout.addWidget(self.username_input)
        self.layout.addWidget(self.password_input)
        self.layout.addWidget(self.confirm_password_input)
        self.layout.addWidget(self.signup_button)
        self.layout.addWidget(self.cancel_button)
        self.setLayout(self.layout)

        self.auth = auth #set the auth to the auth

    def sign_in_user(self): #method to sign in the user
        username = self.username_input.text().strip() #gets the text entered
        password = self.password_input.text().strip() #strip removes any white spaces
        confirm_password = self.confirm_password_input.text().strip()

        if username and password and confirm_password: 
        #if the username, password and confirm password are not empty
            if password == confirm_password:
                if not re.search('[A-Z]', password): #checks if the password has a capital letter
                    QMessageBox.warning(self, "Error", "Password must contain at least one capital letter.")
                    return
                if self.auth.sign_in(username, password):
                    QMessageBox.information(self, "Success", "Account created successfully")
                    self.go_back()
                else:
                    QMessageBox.warning(self, "Error", "Username already exists.")
            else:
                QMessageBox.warning(self, "Error", "Passwords do not match.")
        else:
            QMessageBox.warning(self, "Error", "All fields must be full.")

    def go_back(self): #method to go back
        self.login_window = Login_Window(self.auth)
        self.login_window.show()
        self.close()

class Main_Window(QMainWindow): #initialises the main window
    def __init__(self): #initialises the main window
        super().__init__()
        self.resize(800, 550)
        self.setWindowTitle("Flashcard App")
        self.decks = self.load_decks() #load the decks
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Create the buttons.
        self.create_deck_button = QPushButton("Create New Deck")
        self.create_deck_button.clicked.connect(self.go_to_create_deck)
        self.delete_deck_button = QPushButton("Delete Deck")
        self.delete_deck_button.clicked.connect(self.delete_selected_deck)
        self.add_flashcard_button = QPushButton("Add Flashcard")
        #connect the button to the dialog
        self.add_flashcard_button.clicked.connect(self.show_deck_selection_dialog)
        self.browse_button = QPushButton("Browse")
        self.browse_button.clicked.connect(self.go_to_browse)

        # Create a horizontal layout for the buttons.
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.create_deck_button)
        button_layout.addWidget(self.delete_deck_button)
        button_layout.addWidget(self.add_flashcard_button)
        button_layout.addWidget(self.browse_button)

        # Create a tree widget to display the deck list.
        self.deck_list_widget = QTreeWidget()
        self.deck_list_widget.setHeaderHidden(True)
        self.deck_list_widget.itemDoubleClicked.connect(self.open_flashcards)

        # Create a layout for the deck list page.
        self.deck_list_layout = QVBoxLayout()
        self.deck_list_layout.addLayout(button_layout)         
        self.deck_list_layout.addWidget(self.deck_list_widget) 
        
        # Create a widget to serve as the deck list page.
        self.deck_list_page = QWidget()
        self.deck_list_page.setLayout(self.deck_list_layout)

        # Add pages to the stacked widget.
        self.stacked_widget.addWidget(self.deck_list_page)
        self.create_deck_page = Create_Deck_Page(self)
        self.stacked_widget.addWidget(self.create_deck_page)
        self.flashcard_page = Flashcard_Page(self)
        self.stacked_widget.addWidget(self.flashcard_page)
        self.add_flashcard_page = Add_Flashcard_Page(self)
        self.stacked_widget.addWidget(self.add_flashcard_page)
        self.browse_page = Browse_Page(self)
        self.stacked_widget.addWidget(self.browse_page)

        self.load_deck_list()
        
    def load_decks(self): #method to load the decks
        data = load_json(Decks_db)
        return {deck['name']: [tuple(card) for card in deck['flashcards']] 
                for deck in data['decks']}

    def save_decks(self): #method to save the decks
        decks_data = [{'name': name, 'flashcards': cards} 
                    for name, cards in self.decks.items()]
        save_json({'decks': decks_data}, Decks_db)    

    def load_deck_list(self): #method to load the deck list
        self.deck_list_widget.clear() #clear the deck list
        
        for deck_name in sorted(self.decks.keys()): #sort the deck names
            parts = deck_name.split('::') #split the deck names
            current_parent = self.deck_list_widget.invisibleRootItem()  # Fix here
            for part in parts: #for each part in the parts
                found = None #set found to none
                for i in range(current_parent.childCount()): #for each child in the parent
                    if current_parent.child(i).text(0) == part: #if the child is equal to the part
                        found = current_parent.child(i) #set found to the child
                        break
                if not found: #if found is not found
                    found = QTreeWidgetItem(current_parent) #create a new tree widget item
                    found.setText(0, part) #set the text to the part
                    # Center the text and increase font size
                    font = found.font(0)
                    font.setPointSize(20)
                    found.setFont(0, font)
                    found.setTextAlignment(0, Qt.AlignCenter)
                    found.setText(0, part) #set the text to the part
                current_parent = found
                

    def get_full_deck_name(self, item): #method to get the full deck name
        parts = [] #initialise parts
        while item: #while the item exists
            parts.insert(0, item.text(0)) #insert the item at the beginning of the list
            item = item.parent()
        return '::'.join(parts) #return the parts joined by ::

    def go_to_create_deck(self):
        self.stacked_widget.setCurrentWidget(self.create_deck_page)

    def show_deck_selection_dialog(self): #method to show the deck selection dialog
            if not self.decks:
                QMessageBox.warning(self, "No Decks", "There are no decks available. Please create a deck first.")
                return
            dialog = Deck_Selection_Dialog(list(self.decks.keys()), self) #create a deck selection dialog
            if dialog.exec_() == QDialog.Accepted:
                selected_deck = dialog.selected_deck() #get the selected deck
                self.go_to_add_flashcard(selected_deck, self.deck_list_page)

    def go_to_add_flashcard(self, deck_name, return_page=None): #method to go to the add flashcard page
        self.add_flashcard_page.set_deck(deck_name)
        if return_page is None: #if the return page is none
            return_page = self.flashcard_page #set the return page to the flashcard page
        self.add_flashcard_page.return_page = return_page #set the return page
        self.stacked_widget.setCurrentWidget(self.add_flashcard_page)
        
    def open_flashcards(self): #method to open the flashcards
        item = self.deck_list_widget.currentItem() #get the current item
        if item is None: #if the item is none
            return  # or show an error message
        selected_deck = self.get_full_deck_name(item) #get the full deck name
        self.flashcard_page.load_deck(selected_deck)
        self.stacked_widget.setCurrentWidget(self.flashcard_page)


    def go_to_browse(self):
        self.browse_page.refresh_decks()
        self.stacked_widget.setCurrentWidget(self.browse_page)

    # Modified deck management methods
    def create_deck(self, deck_name):
        if deck_name and deck_name not in self.decks:
            self.decks[deck_name] = []
            self.save_decks()
            return True
        return False
            
    def add_flashcard_to_deck(self, deck_name, question, answer): #method to add a flashcard to the deck
        if deck_name in self.decks:
            self.decks[deck_name].append((question, answer))
            self.save_decks()
            return True
        return False

    def delete_flashcard_from_deck(self, deck_name, index): #method to delete a flashcard from the deck
        if deck_name in self.decks and index < len(self.decks[deck_name]):
            del self.decks[deck_name][index]
            self.save_decks()
            return True
        return False
    #method to update a flashcard in the deck
    def update_flashcard_in_deck(self, deck_name, index, new_question, new_answer): 
        if deck_name in self.decks and index < len(self.decks[deck_name]):
            self.decks[deck_name][index] = (new_question, new_answer)
            self.save_decks()
            return True
        return False

    def delete_selected_deck(self): #method to delete the selected deck
        selected = self.deck_list_widget.currentItem()
        if not selected: #if no deck is selected
            QMessageBox.warning(self, "Error", "No deck selected")
            return 
            
        deck_name = self.get_full_deck_name(selected) #get the full
        subdecks = [name for name in self.decks 
                   if name.startswith(deck_name + "::")] #get the subdecks

        if subdecks: #if there are subdecks
            msg = f"Delete {deck_name} and its {len(subdecks)} subdecks?"
        else: #otherwise
            msg = f"Delete {deck_name}?"
            
        reply = QMessageBox.question(self, "Confirm", msg) #ask the user to confirm
        if reply == QMessageBox.Yes: #if the user clicks yes
            del self.decks[deck_name] #delete the deck
            for sub in subdecks: 
                del self.decks[sub] #delete the subdecks
            self.save_decks()
            self.load_deck_list()
            QMessageBox.information(self, "Success", "Deck(s) deleted successfully")

class Create_Deck_Page(QWidget): #initialises the create deck page
    def __init__(self, main_window): #initialises the main window
        super().__init__()
        self.main_window = main_window
        self.layout = QVBoxLayout()
        self.deck_name_input = QLineEdit()
        self.deck_name_input.setPlaceholderText("Enter deck name")
        self.create_button = QPushButton("Create Deck")
        self.create_button.clicked.connect(self.create_deck)
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.go_back)
  
        create_deck_label = QLabel("Create a New Deck")
        create_deck_label.setAlignment(Qt.AlignCenter)
        font = create_deck_label.font() #change the font size
        font.setPointSize(25)
        create_deck_label.setFont(font) #set the font

        self.layout.addWidget(create_deck_label) #add the create       
        self.layout.addWidget(self.deck_name_input)
        self.layout.addWidget(self.create_button)
        self.layout.addWidget(self.cancel_button)
        self.create_subdeck_button = QPushButton("Create Subdeck")
        self.create_subdeck_button.clicked.connect(self.create_subdeck)
        self.layout.addWidget(self.create_subdeck_button)
        self.setLayout(self.layout)

    def create_deck(self): #method to create a deck
        deck_name = self.deck_name_input.text().strip()
        if self.main_window.create_deck(deck_name):
            self.main_window.load_deck_list()
            self.deck_name_input.clear()
            self.go_back()
            QMessageBox.information(self.main_window, "Success", f"Deck '{deck_name}' created")
        else:
            QMessageBox.warning(self.main_window, "Error", "Deck name must be unique and not empty.")

    def go_back(self): #method to go back
            self.main_window.stacked_widget.setCurrentWidget(self.main_window.deck_list_page)
            
    
    def create_subdeck(self): #method to create a subdeck
        existing_decks = list(self.main_window.decks.keys())
        if not existing_decks:
            QMessageBox.warning(self, "Error", "Create a parent deck first")
            return #return if no decks exist
            
        dialog = Subdeck(self, existing_decks) #create a subdeck dialog
        if dialog.exec_() == QDialog.Accepted: #if the dialog is accepted
            full_name = dialog.get_full_name()
            if not full_name: #if the full name is empty
                QMessageBox.warning(self, "Error", "Invalid deck name")
                return
                
            if self.main_window.create_deck(full_name): #if the deck is created
                self.main_window.load_deck_list()
                QMessageBox.information(self, "Success", f"Created: {full_name}")
            else:
                QMessageBox.warning(self, "Error", "Deck already exists")

class Add_Flashcard_Page(QWidget): #initialises the add flashcard page
    def __init__(self, main_window):
            super().__init__()
            self.main_window = main_window #set the main window
            self.layout = QVBoxLayout()
            self.return_page = None # Add return page attribute
            
            self.question_input = QLineEdit()
            self.question_input.setPlaceholderText("Enter question")
            self.answer_input = QLineEdit()
            self.answer_input.setPlaceholderText("Enter answer")
            
            self.add_button = QPushButton("Add Flashcard")
            self.add_button.clicked.connect(self.add_flashcard)
            
            self.cancel_button = QPushButton("Cancel")
            self.cancel_button.clicked.connect(self.go_back)
            
            self.title_label = QLabel("Add Flashcard to Deck")
            self.title_label.setAlignment(Qt.AlignCenter)  # Center the text
            font = self.title_label.font()  # Get the current font
            font.setPointSize(25)
            self.title_label.setFont(font)  # Apply the new font

            self.layout.addWidget(self.title_label)
            self.layout.addWidget(self.question_input)
            self.layout.addWidget(self.answer_input)
            self.layout.addWidget(self.add_button)
            self.layout.addWidget(self.cancel_button)
            self.setLayout(self.layout)
            
            self.deck_name = ""  # Initialise deck name

    def add_flashcard(self): #method to add a flashcard
        question = self.question_input.text().strip()
        answer = self.answer_input.text().strip()
        if question and answer:
            if self.main_window.add_flashcard_to_deck(self.deck_name, question, answer):
                QMessageBox.information(self, "Success", "Flashcard added successfully")
                self.question_input.clear()
                self.answer_input.clear()
            else:
                QMessageBox.warning(self, "Error", "Failed to add flashcard.")
        else:
            QMessageBox.warning(self, "Error", "Both question and answer fields must be filled.")
    # Add to Add_Flashcard_Page class
    def set_deck(self, deck_name):
        self.deck_name = deck_name

    def go_back(self): #method to go back
        if self.return_page:
            self.main_window.stacked_widget.setCurrentWidget(self.return_page)
        else:
            self.main_window.stacked_widget.setCurrentWidget(self.main_window.deck_list_page)

class Flashcard_Page(QWidget): #initialises the flashcard page
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.layout = QVBoxLayout()

        self.question_label = QLabel("")
        self.answer_label = QLabel("")
        
        #Center the labels
        self.question_label.setAlignment(Qt.AlignCenter)
        self.answer_label.setAlignment(Qt.AlignCenter)
        
        #change the font size
        font = self.question_label.font()
        font.setPointSize(30)
        self.question_label.setFont(font)
        self.answer_label.setFont(font)
        
        self.show_answer_button = QPushButton("Show Answer")
        self.show_answer_button.clicked.connect(self.show_answer)

        self.next_button = QPushButton("Next Flashcard")
        self.next_button.clicked.connect(self.show_next_flashcard)

        self.edit_button = QPushButton("Edit Flashcard")
        self.edit_button.clicked.connect(self.edit_flashcard)

        self.delete_button = QPushButton("Delete Flashcard")
        self.delete_button.clicked.connect(self.delete_flashcard)

        self.add_flashcard_button = QPushButton("Add Flashcard")
        self.add_flashcard_button.clicked.connect(self.add_flashcard)

        self.back_button = QPushButton("Back to Decks")
        self.back_button.clicked.connect(self.go_back)

        self.layout.addWidget(self.question_label)
        self.layout.addWidget(self.answer_label)
        self.layout.addWidget(self.show_answer_button)
        self.layout.addWidget(self.next_button)
        self.layout.addWidget(self.edit_button)
        self.layout.addWidget(self.delete_button)
        self.layout.addWidget(self.back_button)
        self.setLayout(self.layout)
        self.current_index = 0
        self.flashcards = []
        
    def load_deck(self, deck_name): #method to load the deck
        self.deck_name = deck_name
        self.flashcards = self.main_window.decks.get(deck_name, []).copy()
        self.current_index = 0
        self.show_flashcard()

    def show_flashcard(self): #method to show the flashcard
        if self.current_index < len(self.flashcards):
            question, _ = self.flashcards[self.current_index]
            self.question_label.setText(f"Q: {question}")
            self.answer_label.setText("")
            self.show_answer_button.setEnabled(True)
            self.next_button.setEnabled(True)
        else:
            self.question_label.setText("No more flashcards.")
            self.answer_label.setText("")
            self.show_answer_button.setEnabled(False)
            self.next_button.setEnabled(False)

    def show_answer(self): #method to show the answer
        if self.current_index < len(self.flashcards):
            _, answer = self.flashcards[self.current_index]
            self.answer_label.setText(f"A: {answer}")

    def show_next_flashcard(self): #method to show the next flashcard
        self.current_index += 1
        if self.current_index >= len(self.flashcards):
            self.current_index = 0
        self.show_flashcard()

    def add_flashcard(self): #method to add a flashcard
        self.main_window.go_to_add_flashcard(self.deck_name)

    def go_back(self): #method to go back
        self.main_window.stacked_widget.setCurrentWidget(self.main_window.deck_list_page)
                
                
    def showEvent(self, event): #method to show the event
        if hasattr(self, 'deck_name'): #if the deck name is in the deck
            self.flashcards = self.main_window.decks.get(self.deck_name, []).copy()
            # FIX: Prevent negative index for empty decks
            if len(self.flashcards) == 0: #if the length of the flashcards is 0
                self.current_index = 0 #set the current index to 0
            else: #otherwise
                self.current_index = min(self.current_index, len(self.flashcards)-1)
            self.show_flashcard() #show the flashcard
        super().showEvent(event) #show the event

    def edit_flashcard(self): #method to edit the flashcard
        if self.current_index < len(self.flashcards): #if the current index is less than the length of the flashcards
            question, answer = self.flashcards[self.current_index]
            new_question, ok1 = QInputDialog.getText(self, "Edit Question", "Enter new question:", QLineEdit.Normal, question)
            if ok1 and new_question:
                new_answer, ok2 = QInputDialog.getText(self, "Edit Answer", "Enter new answer:", QLineEdit.Normal, answer)
                if ok2 and new_answer: #if the user enters a new answer
                    if self.main_window.update_flashcard_in_deck(
                        self.deck_name, self.current_index, new_question, new_answer):
                        self.flashcards[self.current_index] = (new_question, new_answer)
                        QMessageBox.information(self, "Success", "Flashcard updated successfully!")
                        self.show_flashcard()

    def delete_flashcard(self): #method to delete the flashcard
            if self.current_index < len(self.flashcards):
                reply = QMessageBox.question(
                    self, "Confirm Delete",
                    "Are you sure you want to delete this flashcard?",
                    QMessageBox.Yes | QMessageBox.No
                )
                if reply == QMessageBox.Yes:
                    if self.main_window.delete_flashcard_from_deck(self.deck_name, self.current_index):
                        del self.flashcards[self.current_index]
                        if self.current_index >= len(self.flashcards):
                            self.current_index = 0
                        self.show_flashcard()
                        QMessageBox.information(self, "Success", "Flashcard deleted successfully!")


class Browse_Page(QWidget): # Added Browse_Page class
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.layout = QVBoxLayout()

        # Combo box to select deck
        self.deck_combo = QComboBox()
        self.deck_combo.currentTextChanged.connect(self.load_flashcards)

        self.table = QTableWidget() #table to display flashcards
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Question", "Answer"])
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)

        # Buttons to edit, delete, and go back
        self.edit_button = QPushButton("Edit Flashcard")
        self.edit_button.clicked.connect(self.edit_flashcard)
        self.delete_button = QPushButton("Delete Flashcard")
        self.delete_button.clicked.connect(self.delete_flashcard)
        self.back_button = QPushButton("Back to Decks")
        self.back_button.clicked.connect(self.go_back)
  
        #connect button signals to methods
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.back_button)

        #connect button signals to methods
        self.layout.addWidget(QLabel("Browse Flashcards"))
        self.layout.addWidget(self.deck_combo)
        self.layout.addWidget(self.table)
        self.layout.addLayout(button_layout)
        self.setLayout(self.layout)
        
    def edit_flashcard(self): #method to edit flashcard
            selected_row = self.table.currentRow()
            if selected_row == -1:
                QMessageBox.warning(self, "Error", "No flashcard selected.")
                return

            deck_name = self.deck_combo.currentText() #get the deck name
            question_item = self.table.item(selected_row, 0) #get the question item
            answer_item = self.table.item(selected_row, 1)  #get the answer item
            old_question = question_item.text() #get the old question
            old_answer = answer_item.text() #get the old answer

            # Get new values from user
            new_question, ok1 = QInputDialog.getText(
                self, "Edit Question", "Enter new question:", text=old_question)
            if ok1 and new_question: #if the user enters a new question
                new_answer, ok2 = QInputDialog.getText(
                    self, "Edit Answer", "Enter new answer:", text=old_answer)
                if ok2 and new_answer: #if the user enters a new answer
                    # Update in main window and refresh table
                    if self.main_window.update_flashcard_in_deck(
                        deck_name, selected_row, new_question, new_answer):
                        question_item.setText(new_question)
                        answer_item.setText(new_answer)
                        QMessageBox.information(self, "Success", "Flashcard updated.")

    def refresh_decks(self): #method to refresh decks
        self.deck_combo.clear()
        self.deck_combo.addItems(self.main_window.decks.keys()) #add the decks to the combo box

    def load_flashcards(self, deck_name): #method to load flashcards
        self.table.setRowCount(0) #clear the table
        if deck_name in self.main_window.decks: 
            flashcards = self.main_window.decks[deck_name] #get the flashcards
            for idx, (question, answer) in enumerate(flashcards):
                self.table.insertRow(idx) #insert a row
                self.table.setItem(idx, 0, QTableWidgetItem(question))
                self.table.setItem(idx, 1, QTableWidgetItem(answer))

    def delete_flashcard(self): #method to delete flashcard
        selected_row = self.table.currentRow()
        if selected_row == -1: #if no row is selected
            QMessageBox.warning(self, "Error", "No flashcard selected.")
            return

        deck_name = self.deck_combo.currentText() #get the deck name
        reply = QMessageBox.question( #ask the user if they want to delete the flashcard
            self, "Confirm Delete", "Delete this flashcard?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes: #if the user clicks yes
            if self.main_window.delete_flashcard_from_deck(deck_name, selected_row):
                self.table.removeRow(selected_row) #remove the row
                QMessageBox.information(self, "Success", "Flashcard deleted.")

    def go_back(self): #method to go back
        self.main_window.stacked_widget.setCurrentWidget(self.main_window.deck_list_page)


class Subdeck(QDialog): # Added Subdeck class
    def __init__(self, parent=None, decks=[]): #initialises the subdeck
        super().__init__(parent) #inherits from the parent
        self.setWindowTitle("Create Subdeck")
        self.layout = QVBoxLayout() 
        
        self.parent_combo = QComboBox() #combo box to select parent deck
        self.parent_combo.addItems(decks) 
        
        self.subdeck_name_input = QLineEdit() #text input field for subdeck name
        self.subdeck_name_input.setPlaceholderText("Enter subdeck name")
        
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel) 
        #Create OK and Cancel buttons for the dialog
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        
        self.layout.addWidget(QLabel("Select Parent Deck:")) #add the parent deck label
        self.layout.addWidget(self.parent_combo) #add the parent combo box
        self.layout.addWidget(QLabel("Enter Subdeck Name:")) 
        self.layout.addWidget(self.subdeck_name_input) #add the subdeck name input
        self.layout.addWidget(buttons)
        self.setLayout(self.layout)
    
    def get_full_name(self): #method to get the full name
        parent = self.parent_combo.currentText()
        subdeck = self.subdeck_name_input.text().strip()
        return f"{parent}::{subdeck}" if parent else subdeck #return the parent and subdeck name

class Deck_Selection_Dialog(QDialog): # Added Deck_Selection_Dialog class
    def __init__(self, decks, parent=None): #initialises the deck selection dialog
        super().__init__(parent) #inherits from the parent
        self.setWindowTitle("Select Deck") 
        layout = QVBoxLayout()
        self.combo = QComboBox()
        self.combo.addItems(sorted(decks))  # Sort decks for consistency
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel) #create OK and Cancel buttons
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(QLabel("Select a deck to add flashcards:")) # Add label to layout
        layout.addWidget(self.combo) # Add combo box to layout
        layout.addWidget(buttons)
        self.setLayout(layout)
    
    def selected_deck(self): #method to get the selected deck
        return self.combo.currentText() #return the selected deck

if __name__ == "__main__": #if the name is main
    app = QApplication(sys.argv) #initialise the application
    auth = User_Auth()  # Create an instance of User_Auth
    login_window = Login_Window(auth) 
    login_window.show()
    sys.exit(app.exec_()) # exec the application
# Final Flashcard App
