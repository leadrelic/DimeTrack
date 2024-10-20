import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit,
                             QPushButton, QVBoxLayout, QHBoxLayout,
                             QMessageBox, QComboBox, QGridLayout, QGroupBox)
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


class BudgetTracker(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Budget Tracker")
        self.setGeometry(100, 100, 500, 500)

        self.income = 0
        self.expenses = {}
        self.data = []

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.setSpacing(10)

        # Header
        header = QLabel("Budget Tracker", self)
        header.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(header)

        # Income Group
        income_group = QGroupBox("Income", self)
        income_layout = QVBoxLayout()

        self.income_label_input = QLineEdit(self)
        self.income_label_input.setPlaceholderText("Enter Income Label")
        income_layout.addWidget(QLabel("Income Label:"))
        income_layout.addWidget(self.income_label_input)

        self.income_input = QLineEdit(self)
        self.income_input.setPlaceholderText("Enter Income")
        income_layout.addWidget(QLabel("Income:"))
        income_layout.addWidget(self.income_input)

        income_group.setLayout(income_layout)
        layout.addWidget(income_group)

        # Expense Group
        expense_group = QGroupBox("Expense", self)
        expense_layout = QVBoxLayout()

        self.expense_label_input = QLineEdit(self)
        self.expense_label_input.setPlaceholderText("Enter Expense Label")
        expense_layout.addWidget(QLabel("Expense Label:"))
        expense_layout.addWidget(self.expense_label_input)

        self.expense_input = QLineEdit(self)
        self.expense_input.setPlaceholderText("Enter Expense")
        expense_layout.addWidget(QLabel("Expense:"))
        expense_layout.addWidget(self.expense_input)

        self.category_input = QComboBox(self)
        self.category_input.addItems(["Food", "Transport", "Utilities", "Entertainment", "Housing", "Healthcare", "Insurance", "Savings", "Education", "Travel", "Miscellaneous"])
        expense_layout.addWidget(QLabel("Select Expense Category:"))
        expense_layout.addWidget(self.category_input)

        expense_group.setLayout(expense_layout)
        layout.addWidget(expense_group)

        # Remove Expense Group
        remove_expense_group = QGroupBox("Remove Expense", self)
        remove_layout = QVBoxLayout()

        self.remove_expense_combo = QComboBox(self)
        self.remove_expense_combo.addItems(["Select an expense to remove"])  # Placeholder
        remove_layout.addWidget(QLabel("Select Expense to Remove:"))
        remove_layout.addWidget(self.remove_expense_combo)

        remove_expense_group.setLayout(remove_layout)
        layout.addWidget(remove_expense_group)

        # Buttons
        button_layout = QHBoxLayout()

        add_income_button = QPushButton("Add Income", self)
        add_income_button.setStyleSheet("background-color: #4caf50; color: white; padding: 10px; border-radius: 5px;")
        add_income_button.clicked.connect(self.add_income)
        button_layout.addWidget(add_income_button)

        add_expense_button = QPushButton("Add Expense", self)
        add_expense_button.setStyleSheet("background-color: #f44336; color: white; padding: 10px; border-radius: 5px;")
        add_expense_button.clicked.connect(self.add_expense)
        button_layout.addWidget(add_expense_button)

        remove_expense_button = QPushButton("Remove Expense", self)
        remove_expense_button.setStyleSheet("background-color: #ff9800; color: white; padding: 10px; border-radius: 5px;")
        remove_expense_button.clicked.connect(self.remove_expense)
        button_layout.addWidget(remove_expense_button)

        layout.addLayout(button_layout)

        # Summary and Chart Buttons
        summary_button = QPushButton("Show Summary", self)
        summary_button.setStyleSheet("background-color: #2196f3; color: white; padding: 10px; border-radius: 5px;")
        summary_button.clicked.connect(self.show_summary)
        layout.addWidget(summary_button)

        chart_button = QPushButton("Show Chart", self)
        chart_button.setStyleSheet("background-color: #673ab7; color: white; padding: 10px; border-radius: 5px;")
        chart_button.clicked.connect(self.show_chart)
        layout.addWidget(chart_button)

        export_pdf_button = QPushButton("Export PDF", self)
        export_pdf_button.setStyleSheet("background-color: #9c27b0; color: white; padding: 10px; border-radius: 5px;")
        export_pdf_button.clicked.connect(self.export_pdf)
        layout.addWidget(export_pdf_button)

        self.setLayout(layout)

    def add_income(self):
        try:
            label = self.income_label_input.text()
            income = float(self.income_input.text())
            if income < 0:
                raise ValueError("Income cannot be negative.")
            self.income += income
            self.data.append(("Income", income, label))
            self.income_input.clear()
            self.income_label_input.clear()
        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))

    def add_expense(self):
        try:
            label = self.expense_label_input.text()
            expense = float(self.expense_input.text())
            if expense < 0:
                raise ValueError("Expense cannot be negative.")
            category = self.category_input.currentText()
            if category not in self.expenses:
                self.expenses[category] = []
            self.expenses[category].append((expense, label))
            self.data.append(("Expense", expense, category, label))
            self.expense_input.clear()
            self.expense_label_input.clear()
            self.update_remove_expense_combo()
        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))

    def remove_expense(self):
        selected_expense = self.remove_expense_combo.currentText()
        if selected_expense == "Select an expense to remove":
            QMessageBox.warning(self, "Warning", "Please select an expense to remove.")
            return

        for category, expenses in self.expenses.items():
            for expense, label in expenses:
                if f"{category} - {label}: ${expense:.2f}" == selected_expense:
                    expenses.remove((expense, label))
                    if not expenses:  # Remove category if no expenses left
                        del self.expenses[category]
                    QMessageBox.information(self, "Success", f"Removed {selected_expense}.")
                    self.update_remove_expense_combo()
                    return
        QMessageBox.warning(self, "Warning", "Expense not found.")

    def update_remove_expense_combo(self):
        self.remove_expense_combo.clear()
        self.remove_expense_combo.addItem("Select an expense to remove")
        for category, expenses in self.expenses.items():
            for expense, label in expenses:
                self.remove_expense_combo.addItem(f"{category} - {label}: ${expense:.2f}")

    def show_summary(self):
        balance = self.income - sum(expense[0] for category in self.expenses.values() for expense in category)
        summary = f"Total Income: ${self.income:.2f}\nTotal Expenses: ${sum(expense[0] for category in self.expenses.values() for expense in category):.2f}\nBalance: ${balance:.2f}\n\nDetailed Expenses:\n"

        for category, expenses in self.expenses.items():
            for expense, label in expenses:
                summary += f"{category} - {label}: ${expense:.2f}\n"

        QMessageBox.information(self, "Summary", summary)

    def show_chart(self):
        categories = list(self.expenses.keys())
        values = [sum(expense[0] for expense in self.expenses[cat]) for cat in categories]
        plt.bar(categories, values, color='red')
        plt.axhline(y=self.income, color='green', label='Income')
        plt.title('Expenses by Category')
        plt.ylabel('Amount ($)')
        plt.legend()
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.show()

    def export_pdf(self):
        # Create a PDF document with the summary and chart
        pdf_path = "budget_summary.pdf"
        c = canvas.Canvas(pdf_path, pagesize=letter)

        # Write summary
        c.drawString(100, 750, f"Total Income: ${self.income:.2f}")
        c.drawString(100, 730, f"Total Expenses: ${sum(expense[0] for category in self.expenses.values() for expense in category):.2f}")
        c.drawString(100, 710, f"Balance: ${self.income - sum(expense[0] for category in self.expenses.values() for expense in category):.2f}")

        # Write detailed expenses
        y_position = 690
        for category, expenses in self.expenses.items():
            for expense, label in expenses:
                c.drawString(100, y_position, f"{category} - {label}: ${expense:.2f}")
                y_position -= 20  # Move down for next line

        # Generate and save chart as an image
        self.show_chart()
        plt.savefig("chart.png")  # Save chart as PNG
        plt.close()

        # Add chart to PDF
        c.drawImage("chart.png", 100, y_position - 300, width=400, height=300)

        c.save()
        QMessageBox.information(self, "Export Complete", f"Summary exported to {pdf_path}.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BudgetTracker()
    window.show()
    sys.exit(app.exec())
