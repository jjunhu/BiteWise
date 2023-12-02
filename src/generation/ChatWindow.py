import sys
import time

from PyQt5.QtWidgets import QApplication, QWidget, QTextEdit, QPushButton, QVBoxLayout, QLineEdit, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtGui import QPixmap, QPalette, QBrush
from ChatBot import ChatBot

class ChatInterface(QWidget):
    def __init__(self, Bot):
        super().__init__()
        self.initUI()
        self.Bot = Bot

    def initUI(self):
        # Set up the main layout
        mainLayout = QVBoxLayout()

        # Chat history layout
        self.chatHistory = QTextEdit(self)
        self.chatHistory.setReadOnly(True)

        # 增加聊天框的高度
        self.chatHistory.setMinimumHeight(500)  # 调整聊天框的高度

        # Input and send button layout
        inputLayout = QHBoxLayout()
        self.inputLine = QLineEdit(self)

        # 增加输入框和发送按钮的高度
        inputHeight = 32  # 输入框和按钮的高度
        self.inputLine.setMinimumHeight(inputHeight)
        self.submitButton = QPushButton('Send', self)
        sendButtonFont = QFont('Segoe UI', 12)  # 设置字体和大小
        self.submitButton.setFont(sendButtonFont)
        self.submitButton.setMinimumHeight(inputHeight)


        self.inputLine.returnPressed.connect(self.onSubmit)
        self.submitButton.clicked.connect(self.onSubmit)
        inputLayout.addWidget(self.inputLine)
        inputLayout.addWidget(self.submitButton)

        # 设定字体和样式
        self.setupFontsAndStyles()
        self.inputLine.setStyleSheet("font-size: 14pt;")  # 例如，字体大小设置为 14pt


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

    def onSubmit(self):
        # Get user input
        userInput = self.get_user_input()
        self.display_message('[Me] ' + userInput, "user")
        # Display user message
        # time.sleep(2)
        gptResponse = self.Bot.chat(userInput)
        self.display_message("[GPT] "+gptResponse.choices[0].message.content, "gpt")

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


    def get_user_input(self):
        # Return the user input from the input box
        userInput = self.inputLine.text()
        self.inputLine.clear()
        return userInput

if __name__ == '__main__':
    Bot = ChatBot()
    app = QApplication(sys.argv)
    ex = ChatInterface(Bot)
    ex.show()
    sys.exit(app.exec_())
