from PyQt5 import QtCore, QtGui, QtWidgets
from ir_backend import InformationRetrieval
import os
import webbrowser
import shutil
import speech_recognition as sr  


class IRSystemGUI(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setStyleSheet("background-color: #f0f2f5;")  

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Title Label
        self.title_label = QtWidgets.QLabel(self.centralwidget)
        self.title_label.setGeometry(QtCore.QRect(200, 20, 400, 60))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(28)
        font.setBold(True)
        self.title_label.setFont(font)
        self.title_label.setAlignment(QtCore.Qt.AlignCenter)
        self.title_label.setText("Mini IR System")
        self.title_label.setStyleSheet("color: #007bff;")

        # Search Box
        self.search_input = QtWidgets.QLineEdit(self.centralwidget)
        self.search_input.setGeometry(QtCore.QRect(150, 100, 400, 50))
        self.search_input.setPlaceholderText("Enter search word here...")
        self.search_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid #007bff;
                border-radius: 25px;
                padding: 10px;
                font-size: 18px;
            }
        """)
        self.search_input.textChanged.connect(self.show_suggestions)

        # Search Button
        self.search_button = QtWidgets.QPushButton(self.centralwidget)
        self.search_button.setGeometry(QtCore.QRect(570, 100, 120, 50))
        self.search_button.setText("Search")
        self.search_button.setStyleSheet(self._button_style("#007bff", "#0056b3"))
        self.search_button.clicked.connect(self.search_word)

        # Voice Search Button
        self.voice_button = QtWidgets.QPushButton(self.centralwidget)
        self.voice_button.setGeometry(QtCore.QRect(700, 100, 50, 50))
        self.voice_button.setText("🎙️")
        self.voice_button.setStyleSheet(self._button_style("#007bff", "#0056b3"))
        self.voice_button.clicked.connect(self.voice_search)

        # Results Table
        self.results_table = QtWidgets.QTableWidget(self.centralwidget)
        self.results_table.setGeometry(QtCore.QRect(50, 180, 700, 300))
        self.results_table.setColumnCount(4)
        self.results_table.setHorizontalHeaderLabels(["Document", "Occurrences", "View", "Download"])
        self.results_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.results_table.setStyleSheet("""
            QTableWidget {
                border: 2px solid #ccc;
                border-radius: 10px;
                font-size: 14px;
                background-color: #ffffff;
            }
            QHeaderView::section {
                background-color: #007bff;
                color: white;
                font-weight: bold;
            }
        """)
        self.results_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.results_table.setColumnWidth(0, 400)  # Larger column for Document Name
        self.results_table.setColumnWidth(1, 80)   # Occurrences column
        self.results_table.setColumnWidth(2, 100)   # View Button column
        self.results_table.setColumnWidth(3, 100)  # Download Button column
        self.results_table.verticalHeader().hide()
        self.results_table.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.results_table.verticalHeader().setDefaultSectionSize(50)  # Increased row height

        MainWindow.setCentralWidget(self.centralwidget)

        # Initialize Information Retrieval Backend
        self.ir_system = InformationRetrieval('./documents/')
        self.ir_system.index_documents()

    def show_suggestions(self):
        """Auto-suggestions are displayed here. No changes needed."""
        pass

    def search_word(self):
        """Perform search and populate the table."""
        query = self.search_input.text()
        self.display_results(query)

    def voice_search(self):
        """Capture voice input and perform search."""
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            QtWidgets.QMessageBox.information(None, "Voice Search", "Speak your query now.")
            try:
                audio = recognizer.listen(source, timeout=5)
                query = recognizer.recognize_google(audio)
                self.search_input.setText(query)  # Populate the search bar
                self.display_results(query)
            except sr.UnknownValueError:
                QtWidgets.QMessageBox.warning(None, "Error", "Sorry, could not understand your voice.")
            except sr.RequestError:
                QtWidgets.QMessageBox.warning(None, "Error", "Could not connect to the recognition service.")
            except Exception as e:
                QtWidgets.QMessageBox.warning(None, "Error", str(e))

    def display_results(self, query):
        """Fetch and display search results."""
        results = self.ir_system.search(query)

        self.results_table.setRowCount(0)  # Clear previous results
        if results:
            for row, (doc, count, snippet) in enumerate(results):
                self.results_table.insertRow(row)

                # Document Name with increased column width
                self.results_table.setItem(row, 0, QtWidgets.QTableWidgetItem(doc))
                self.results_table.setItem(row, 1, QtWidgets.QTableWidgetItem(str(count)))

                # View Button
                view_button = QtWidgets.QPushButton("\ud83d\udc41 View")
                view_button.setStyleSheet(self._button_style("#1750AC", "#003d82"))
                view_button.clicked.connect(lambda _, file=doc: self.view_file(file))
                self.results_table.setCellWidget(row, 2, view_button)

                # Download Button
                download_button = QtWidgets.QPushButton("\ud83d\udcbe Download")
                download_button.setStyleSheet(self._button_style("#1750AC", "#003d82"))
                download_button.clicked.connect(lambda _, file=doc: self.download_file(file))
                self.results_table.setCellWidget(row, 3, download_button)
        else:
            self.results_table.setRowCount(1)
            self.results_table.setItem(0, 0, QtWidgets.QTableWidgetItem("No results found."))
            self.results_table.setSpan(0, 0, 1, 4)

    def view_file(self, file):
        """Open the PDF file using the default PDF viewer."""
        file_path = os.path.join("./documents/", file)
        if os.path.exists(file_path):
            webbrowser.open(os.path.abspath(file_path))

    def download_file(self, file):
        """Download the selected PDF file to the user's current working directory."""
        src_path = os.path.join("./documents/", file)
        dst_path = os.path.join(os.getcwd(), file)
        if os.path.exists(src_path):
            shutil.copy(src_path, dst_path)
            QtWidgets.QMessageBox.information(
                None, "Download Complete", f"{file} has been downloaded to:\n{os.getcwd()}"
            )
        else:
            QtWidgets.QMessageBox.warning(None, "Error", "File not found.")

    def _button_style(self, color, hover_color):
        """Reusable button style."""
        return f"""
            QPushButton {{
                background-color: {color};
                color: white;
                font-size: 14px;
                border-radius: 10px;
                padding: 5px;
            }}
            QPushButton:hover {{
                background-color: {hover_color};
            }}
        """
