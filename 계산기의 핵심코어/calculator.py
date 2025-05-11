import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout, QPushButton, QLineEdit
from PyQt5.QtCore import Qt


class Calculator:
    def __init__(self):
        self.reset()

    def reset(self):
        self.current = ''
        self.operator = ''
        self.operand = ''
        self.result = ''
        self.decimal_used = False

    def input_digit(self, digit):
        if digit == '.' and self.decimal_used:
            return
        if digit == '.':
            self.decimal_used = True
        self.current += digit

    def set_operator(self, op):
        if self.current:
            self.operand = self.current
            self.operator = op
            self.current = ''
            self.decimal_used = False

    def negative_positive(self):
        if self.current:
            if self.current.startswith('-'):
                self.current = self.current[1:]
            else:
                self.current = '-' + self.current

    def percent(self):
        try:
            value = float(self.current)
            self.current = str(value / 100)
        except ValueError:
            self.current = 'Error'

    def add(self):
        return float(self.operand) + float(self.current)

    def subtract(self):
        return float(self.operand) - float(self.current)

    def multiply(self):
        return float(self.operand) * float(self.current)

    def divide(self):
        if float(self.current) == 0:
            raise ZeroDivisionError
        return float(self.operand) / float(self.current)

    def equal(self):
        try:
            if not self.operator:
                return self.current
            if self.operator == '+':
                self.result = self.add()
            elif self.operator == '-':
                self.result = self.subtract()
            elif self.operator == '*':
                self.result = self.multiply()
            elif self.operator == '/':
                self.result = self.divide()
            if isinstance(self.result, float):
                self.result = round(self.result, 6)
            self.current = str(self.result)
            self.operator = ''
            self.operand = ''
            self.decimal_used = '.' in self.current
        except ZeroDivisionError:
            self.current = 'Cannot divide by zero'
        except OverflowError:
            self.current = 'Overflow'
        except Exception:
            self.current = 'Error'
        return self.current


class CalculatorUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Calculator')
        self.setFixedSize(320, 480)
        self.calc = Calculator()
        self.init_ui()

    def init_ui(self):
        self.display = QLineEdit()
        self.display.setAlignment(Qt.AlignRight)
        self.display.setReadOnly(True)
        self.display.setFixedHeight(80)
        self.display.setStyleSheet('font-size: 32px; padding: 10px;')

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.display)

        grid = QGridLayout()
        buttons = [
            ['AC', '+/-', '%', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['0', '.', '=']
        ]

        for row, row_vals in enumerate(buttons):
            col = 0
            for val in row_vals:
                btn = QPushButton(val)
                btn.setFixedSize(70, 70)
                btn.setStyleSheet('font-size: 20px;')
                btn.clicked.connect(self.on_button_click)
                if val == '0':
                    grid.addWidget(btn, row + 1, col, 1, 2)
                    col += 2
                else:
                    grid.addWidget(btn, row + 1, col)
                    col += 1

        main_layout.addLayout(grid)
        self.setLayout(main_layout)

    def on_button_click(self):
        btn = self.sender()
        text = btn.text()

        if text.isdigit() or text == '.':
            self.calc.input_digit(text)
        elif text in '+-*/':
            self.calc.set_operator(text)
        elif text == '+/-':
            self.calc.negative_positive()
        elif text == '%':
            self.calc.percent()
        elif text == '=':
            self.calc.equal()
        elif text == 'AC':
            self.calc.reset()

        self.update_display()

    def update_display(self):
        value = self.calc.current
        length = len(value)
        if length > 12:
            self.display.setStyleSheet('font-size: 18px; padding: 10px;')
        elif length > 9:
            self.display.setStyleSheet('font-size: 24px; padding: 10px;')
        else:
            self.display.setStyleSheet('font-size: 32px; padding: 10px;')
        self.display.setText(value)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = CalculatorUI()
    ui.show()
    sys.exit(app.exec_())
