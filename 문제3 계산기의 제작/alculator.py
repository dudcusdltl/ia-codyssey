import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout, QPushButton, QLineEdit
from PyQt5.QtCore import Qt

class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('iPhone Calculator UI')
        self.setFixedSize(320, 500)
        self.init_ui()

    def init_ui(self):
        # 상단 디스플레이
        self.display = QLineEdit()
        self.display.setAlignment(Qt.AlignRight)
        self.display.setReadOnly(True)
        self.display.setFixedHeight(80)
        self.display.setStyleSheet('font-size: 32px; padding: 10px;')

        # 메인 레이아웃 설정
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.display)

        # 버튼 레이아웃
        button_layout = QGridLayout()

        # 버튼 설정
        buttons = [
            ['AC', '+/-', '%', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['0', '.', '=']
        ]
        
        positions = [(i, j) for i in range(5) for j in range(4)]
        for position, button in zip(positions, sum(buttons, [])):
            if button == '':
                continue
            btn = QPushButton(button)
            btn.setFixedSize(70, 70)
            if button == '0':
                button_layout.addWidget(btn, position[0], position[1], 1, 2) # 0 버튼은 두 칸 차지
            else:
                button_layout.addWidget(btn, position[0], position[1])
            btn.setStyleSheet("font-size: 20px; border-radius: 35px; background-color: gray; color: white;")
            btn.clicked.connect(self.button_clicked)
        
        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)
        self.current_input = ''

    def button_clicked(self):
        sender = self.sender()
        text = sender.text()

        if text == 'C':
            self.current_input = ''
            self.display.setText('')
        elif text == '=':
            try:
                result = str(eval(self.current_input))
                self.display.setText(result)
                self.current_input = result
            except:
                self.display.setText('Error')
                self.current_input = ''
        else:
            self.current_input += text
            self.display.setText(self.current_input)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    calc = Calculator()
    calc.show()
    sys.exit(app.exec_())
