import sys
import time

from PyQt5.QtWidgets import QApplication, QWidget, QTextEdit, QPushButton, QVBoxLayout, QLineEdit, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtGui import QPixmap, QPalette, QBrush
from ChatBot import ChatBot
from PyQt5.QtWidgets import QFileDialog, QPushButton, QHBoxLayout

class ChatInterface(QWidget):
    def __init__(self, Bot):
        super().__init__()
        self.initUI()
        self.filePath = None
        self.Bot = Bot

    def initUI(self):
        # Set up the main layout
        mainLayout = QVBoxLayout()

        # Chat history layout
        self.chatHistory = QTextEdit(self)
        self.chatHistory.setReadOnly(True)
        self.chatHistory.setMinimumHeight(500)  # Adjust chat box height

        # Input and send button layout
        inputLayout = QHBoxLayout()

        # Set the height for all input and button elements
        elementHeight = 30  # Height for upload icon, input line, and button

        # Upload button
        self.uploadButton = QPushButton(self)
        uploadButtonIconPath = "./upload.png"  # Icon path
        self.uploadButton.setIcon(QIcon(uploadButtonIconPath))
        self.uploadButton.clicked.connect(self.onUpload)
        self.uploadButton.setFixedHeight(elementHeight)  # Set fixed height

        # Input line
        self.inputLine = QLineEdit(self)
        self.inputLine.setFixedHeight(elementHeight)  # Set fixed height

        # Submit button
        self.submitButton = QPushButton('Send', self)
        sendButtonFont = QFont('Segoe UI', 12)  # Font and size
        self.submitButton.setFont(sendButtonFont)
        self.submitButton.setFixedHeight(elementHeight)  # Set fixed height

        # Connect signals
        self.inputLine.returnPressed.connect(self.onSubmit)
        self.submitButton.clicked.connect(self.onSubmit)

        # Add widgets to input layout
        inputLayout.addWidget(self.uploadButton)
        inputLayout.addWidget(self.inputLine)
        inputLayout.addWidget(self.submitButton)

        # Set fonts and styles
        self.setupFontsAndStyles()
        self.inputLine.setStyleSheet("font-size: 14pt;")  # Font size set to 14pt

        # Add components to main layout
        mainLayout.addWidget(self.chatHistory)
        mainLayout.addLayout(inputLayout)
        self.setLayout(mainLayout)

        # Set window properties
        self.setWindowTitle('Chat Interface')
        self.setGeometry(300, 300, 500, 400)

    def setupFontsAndStyles(self):
        # 设定字体和样式
        chatFont = QFont('Segoe UI', 10)
        self.chatHistory.setFont(chatFont)
        self.inputLine.setFont(chatFont)
        self.chatHistory.setStyleSheet("""
            QTextEdit {
                background-color: #f0f0f0;
                color: #333333;
                font-family: 'Segoe UI';z
                font-size: 12px;
                line-height: 1.5;
            }
        """)
        self.setChatHistoryBackground("./bg.png")

    def setChatHistoryBackground(self, imagePath):
        # 使用样式表设置背景图片
        self.chatHistory.setStyleSheet(f"""
            QTextEdit {{
                background-image: url({imagePath});
                background-repeat: no-repeat;
                background-position: center;
            }}
        """)

    def display_message(self, message, sender):
        # 根据发送者加粗字体和设置消息样式
        if sender == "user":
            color = "#1A1A1A"
            alignment = Qt.AlignLeft
            fontWeight = "bold"  # 用户消息加粗
        else:  # GPT 消息
            color = "#2E8B57"
            alignment = Qt.AlignLeft
            fontWeight = "bold"

        self.chatHistory.setAlignment(alignment)
        self.chatHistory.append(f"<div style='color: {color}; font-weight: {fontWeight}; margin: 2px; padding: 5px; font-size: 14px;'>{message}</div>")

    def onUpload(self):
        # 弹出文件选择对话框
        filePath, _ = QFileDialog.getOpenFileName(self, "Select File")
        if filePath:
            print("Selected file:", filePath)
            self.filePath = filePath  # 保存文件路径

    def get_user_input(self):
        # Return the user input from the input box
        userInput = self.inputLine.text()
        self.inputLine.clear()
        return userInput

    def onSubmit(self):
        # Get user input
        userInput = self.get_user_input()
        self.display_message('[Me] ' + userInput, "user")

        # 如果有文件路径，可以在这里使用它
        if self.filePath:
            with open(self.filePath, 'rb') as file:
                file_content = file.read()
                gptResponse = self.Bot.chat(file_content, userInput)
                self.display_message("[GPT] " + gptResponse.choices[0].message.content, "gpt")
        else:
            gptResponse = self.Bot.chat(None, userInput)
            self.display_message("[GPT] " + gptResponse.choices[0].message.content, "gpt")

if __name__ == '__main__':
    Bot = ChatBot()
    app = QApplication(sys.argv)
    ex = ChatInterface(Bot)
    ex.show()
    sys.exit(app.exec_())
