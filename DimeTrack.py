#!/usr/bin/env python3
"""
Budget Tracker Pro - A comprehensive personal finance management application
Auto-installs all required dependencies on first run
"""

import sys
import subprocess
import importlib.util

def check_and_install_packages():
    """Check for required packages and install them if missing"""
    required_packages = {
        'PyQt6': 'PyQt6',
        'matplotlib': 'matplotlib',
        'reportlab': 'reportlab'
    }
    
    missing_packages = []
    
    print("Checking dependencies...")
    for package_name, pip_name in required_packages.items():
        if importlib.util.find_spec(package_name) is None:
            missing_packages.append(pip_name)
            print(f"  ✗ {package_name} - NOT FOUND")
        else:
            print(f"  ✓ {package_name} - OK")
    
    if missing_packages:
        print(f"\nInstalling missing packages: {', '.join(missing_packages)}")
        print("This may take a minute...\n")
        
        for package in missing_packages:
            try:
                print(f"Installing {package}...")
                subprocess.check_call([
                    sys.executable, 
                    "-m", 
                    "pip", 
                    "install", 
                    "--break-system-packages",
                    package
                ])
                print(f"  ✓ {package} installed successfully\n")
            except subprocess.CalledProcessError as e:
                print(f"  ✗ Failed to install {package}: {e}")
                print(f"\nPlease install manually: pip install {package}")
                sys.exit(1)
        
        print("\n" + "="*60)
        print("All dependencies installed successfully!")
        print("="*60 + "\n")
    else:
        print("\nAll dependencies are already installed!\n")

# Check and install dependencies before importing them
check_and_install_packages()

# Now import the packages
import json
from datetime import datetime
from pathlib import Path
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout,
    QHBoxLayout, QMessageBox, QComboBox, QGroupBox, QTableWidget,
    QTableWidgetItem, QHeaderView, QDateEdit, QTabWidget, QTextEdit
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch


class BudgetData:
    """Model class for managing budget data with persistence"""
    
    def __init__(self, data_file='budget_data.json'):
        self.data_file = Path(data_file)
        self.income_entries = []
        self.expense_entries = []
        self.load_data()
    
    def add_income(self, amount, label, date):
        entry = {
            'amount': amount,
            'label': label,
            'date': date,
            'timestamp': datetime.now().isoformat()
        }
        self.income_entries.append(entry)
        self.save_data()
    
    def add_expense(self, amount, label, category, date):
        entry = {
            'amount': amount,
            'label': label,
            'category': category,
            'date': date,
            'timestamp': datetime.now().isoformat()
        }
        self.expense_entries.append(entry)
        self.save_data()
    
    def remove_expense(self, index):
        if 0 <= index < len(self.expense_entries):
            del self.expense_entries[index]
            self.save_data()
            return True
        return False
    
    def remove_income(self, index):
        if 0 <= index < len(self.income_entries):
            del self.income_entries[index]
            self.save_data()
            return True
        return False
    
    def get_total_income(self):
        return sum(entry['amount'] for entry in self.income_entries)
    
    def get_total_expenses(self):
        return sum(entry['amount'] for entry in self.expense_entries)
    
    def get_balance(self):
        return self.get_total_income() - self.get_total_expenses()
    
    def get_expenses_by_category(self):
        categories = {}
        for entry in self.expense_entries:
            cat = entry['category']
            if cat not in categories:
                categories[cat] = 0
            categories[cat] += entry['amount']
        return categories
    
    def save_data(self):
        data = {
            'income_entries': self.income_entries,
            'expense_entries': self.expense_entries
        }
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_data(self):
        if self.data_file.exists():
            try:
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    self.income_entries = data.get('income_entries', [])
                    self.expense_entries = data.get('expense_entries', [])
            except Exception as e:
                print(f"Error loading data: {e}")


class BudgetTracker(QWidget):
    """Main budget tracker application with enhanced UI and features"""
    
    CATEGORIES = [
        "Food & Dining",
        "Transportation",
        "Utilities",
        "Entertainment",
        "Housing",
        "Healthcare",
        "Insurance",
        "Savings & Investments",
        "Education",
        "Travel",
        "Shopping",
        "Personal Care",
        "Debt Payments",
        "Gifts & Donations",
        "Miscellaneous"
    ]
    
    def __init__(self):
        super().__init__()
        self.data = BudgetData()
        self.init_ui()
        self.refresh_tables()
    
    def init_ui(self):
        self.setWindowTitle("Budget Tracker Pro")
        self.setGeometry(100, 100, 900, 700)
        self.setStyleSheet("""
            QWidget {
                background-color: #f5f5f5;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QGroupBox {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 8px;
                margin-top: 10px;
                padding: 15px;
                font-weight: bold;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
            QLineEdit, QComboBox, QDateEdit {
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 4px;
                background-color: white;
            }
            QLineEdit:focus, QComboBox:focus, QDateEdit:focus {
                border: 2px solid #2196f3;
            }
            QPushButton {
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
                font-weight: bold;
                min-width: 100px;
            }
            QPushButton:hover {
                opacity: 0.9;
            }
            QPushButton:pressed {
                opacity: 0.8;
            }
            QTableWidget {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 4px;
            }
            QHeaderView::section {
                background-color: #2196f3;
                color: white;
                padding: 8px;
                border: none;
                font-weight: bold;
            }
        """)
        
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Header
        header = QLabel("💰 Budget Tracker Pro", self)
        header_font = QFont("Segoe UI", 28, QFont.Weight.Bold)
        header.setFont(header_font)
        header.setStyleSheet("color: #2196f3; padding: 10px;")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(header)
        
        # Summary Cards
        summary_layout = QHBoxLayout()
        self.income_card = self.create_summary_card("Total Income", "$0.00", "#4caf50")
        self.expense_card = self.create_summary_card("Total Expenses", "$0.00", "#f44336")
        self.balance_card = self.create_summary_card("Balance", "$0.00", "#2196f3")
        
        summary_layout.addWidget(self.income_card)
        summary_layout.addWidget(self.expense_card)
        summary_layout.addWidget(self.balance_card)
        main_layout.addLayout(summary_layout)
        
        # Tab Widget for Input and History
        tabs = QTabWidget()
        tabs.addTab(self.create_input_tab(), "📝 Add Transactions")
        tabs.addTab(self.create_history_tab(), "📊 Transaction History")
        tabs.addTab(self.create_reports_tab(), "📈 Reports & Analytics")
        main_layout.addWidget(tabs)
        
        self.setLayout(main_layout)
    
    def create_summary_card(self, title, value, color):
        card = QGroupBox()
        card.setStyleSheet(f"""
            QGroupBox {{
                background-color: {color};
                border: none;
                border-radius: 10px;
                padding: 20px;
            }}
            QLabel {{
                color: white;
            }}
        """)
        
        layout = QVBoxLayout()
        
        title_label = QLabel(title)
        title_label.setFont(QFont("Segoe UI", 12))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        value_label = QLabel(value)
        value_label.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        value_label.setObjectName("value_label")
        
        layout.addWidget(title_label)
        layout.addWidget(value_label)
        card.setLayout(layout)
        
        return card
    
    def create_input_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Income Section
        income_group = QGroupBox("➕ Add Income")
        income_layout = QVBoxLayout()
        
        self.income_label_input = QLineEdit()
        self.income_label_input.setPlaceholderText("e.g., Salary, Freelance, Bonus")
        income_layout.addWidget(QLabel("Description:"))
        income_layout.addWidget(self.income_label_input)
        
        self.income_amount_input = QLineEdit()
        self.income_amount_input.setPlaceholderText("0.00")
        income_layout.addWidget(QLabel("Amount ($):"))
        income_layout.addWidget(self.income_amount_input)
        
        self.income_date_input = QDateEdit()
        self.income_date_input.setDate(QDate.currentDate())
        self.income_date_input.setCalendarPopup(True)
        income_layout.addWidget(QLabel("Date:"))
        income_layout.addWidget(self.income_date_input)
        
        add_income_btn = QPushButton("Add Income")
        add_income_btn.setStyleSheet("background-color: #4caf50; color: white;")
        add_income_btn.clicked.connect(self.add_income)
        income_layout.addWidget(add_income_btn)
        
        income_group.setLayout(income_layout)
        layout.addWidget(income_group)
        
        # Expense Section
        expense_group = QGroupBox("➖ Add Expense")
        expense_layout = QVBoxLayout()
        
        self.expense_label_input = QLineEdit()
        self.expense_label_input.setPlaceholderText("e.g., Groceries, Gas, Netflix")
        expense_layout.addWidget(QLabel("Description:"))
        expense_layout.addWidget(self.expense_label_input)
        
        self.expense_amount_input = QLineEdit()
        self.expense_amount_input.setPlaceholderText("0.00")
        expense_layout.addWidget(QLabel("Amount ($):"))
        expense_layout.addWidget(self.expense_amount_input)
        
        self.category_input = QComboBox()
        self.category_input.addItems(self.CATEGORIES)
        expense_layout.addWidget(QLabel("Category:"))
        expense_layout.addWidget(self.category_input)
        
        self.expense_date_input = QDateEdit()
        self.expense_date_input.setDate(QDate.currentDate())
        self.expense_date_input.setCalendarPopup(True)
        expense_layout.addWidget(QLabel("Date:"))
        expense_layout.addWidget(self.expense_date_input)
        
        add_expense_btn = QPushButton("Add Expense")
        add_expense_btn.setStyleSheet("background-color: #f44336; color: white;")
        add_expense_btn.clicked.connect(self.add_expense)
        expense_layout.addWidget(add_expense_btn)
        
        expense_group.setLayout(expense_layout)
        layout.addWidget(expense_group)
        
        layout.addStretch()
        tab.setLayout(layout)
        return tab
    
    def create_history_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Income History
        income_group = QGroupBox("💵 Income History")
        income_layout = QVBoxLayout()
        
        self.income_table = QTableWidget()
        self.income_table.setColumnCount(4)
        self.income_table.setHorizontalHeaderLabels(["Date", "Description", "Amount", "Actions"])
        self.income_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        income_layout.addWidget(self.income_table)
        
        income_group.setLayout(income_layout)
        layout.addWidget(income_group)
        
        # Expense History
        expense_group = QGroupBox("💳 Expense History")
        expense_layout = QVBoxLayout()
        
        self.expense_table = QTableWidget()
        self.expense_table.setColumnCount(5)
        self.expense_table.setHorizontalHeaderLabels(["Date", "Description", "Category", "Amount", "Actions"])
        self.expense_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        expense_layout.addWidget(self.expense_table)
        
        expense_group.setLayout(expense_layout)
        layout.addWidget(expense_group)
        
        tab.setLayout(layout)
        return tab
    
    def create_reports_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Report Summary
        self.report_text = QTextEdit()
        self.report_text.setReadOnly(True)
        layout.addWidget(self.report_text)
        
        # Action Buttons
        button_layout = QHBoxLayout()
        
        refresh_btn = QPushButton("🔄 Refresh Report")
        refresh_btn.setStyleSheet("background-color: #2196f3; color: white;")
        refresh_btn.clicked.connect(self.update_report)
        button_layout.addWidget(refresh_btn)
        
        chart_btn = QPushButton("📊 View Charts")
        chart_btn.setStyleSheet("background-color: #673ab7; color: white;")
        chart_btn.clicked.connect(self.show_charts)
        button_layout.addWidget(chart_btn)
        
        export_btn = QPushButton("📄 Export PDF Report")
        export_btn.setStyleSheet("background-color: #9c27b0; color: white;")
        export_btn.clicked.connect(self.export_pdf)
        button_layout.addWidget(export_btn)
        
        layout.addLayout(button_layout)
        tab.setLayout(layout)
        return tab
    
    def add_income(self):
        try:
            label = self.income_label_input.text().strip()
            if not label:
                raise ValueError("Please enter a description for the income.")
            
            amount = float(self.income_amount_input.text())
            if amount <= 0:
                raise ValueError("Income must be greater than zero.")
            
            date = self.income_date_input.date().toString("yyyy-MM-dd")
            
            self.data.add_income(amount, label, date)
            
            self.income_label_input.clear()
            self.income_amount_input.clear()
            self.income_date_input.setDate(QDate.currentDate())
            
            self.refresh_tables()
            self.update_summary_cards()
            
            QMessageBox.information(self, "Success", f"Added income: {label} - ${amount:.2f}")
            
        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))
    
    def add_expense(self):
        try:
            label = self.expense_label_input.text().strip()
            if not label:
                raise ValueError("Please enter a description for the expense.")
            
            amount = float(self.expense_amount_input.text())
            if amount <= 0:
                raise ValueError("Expense must be greater than zero.")
            
            category = self.category_input.currentText()
            date = self.expense_date_input.date().toString("yyyy-MM-dd")
            
            self.data.add_expense(amount, label, category, date)
            
            self.expense_label_input.clear()
            self.expense_amount_input.clear()
            self.expense_date_input.setDate(QDate.currentDate())
            
            self.refresh_tables()
            self.update_summary_cards()
            
            QMessageBox.information(self, "Success", f"Added expense: {label} - ${amount:.2f}")
            
        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))
    
    def refresh_tables(self):
        # Refresh income table
        self.income_table.setRowCount(len(self.data.income_entries))
        for i, entry in enumerate(self.data.income_entries):
            self.income_table.setItem(i, 0, QTableWidgetItem(entry['date']))
            self.income_table.setItem(i, 1, QTableWidgetItem(entry['label']))
            self.income_table.setItem(i, 2, QTableWidgetItem(f"${entry['amount']:.2f}"))
            
            delete_btn = QPushButton("🗑️ Delete")
            delete_btn.setStyleSheet("background-color: #ff5252; color: white;")
            delete_btn.clicked.connect(lambda checked, idx=i: self.delete_income(idx))
            self.income_table.setCellWidget(i, 3, delete_btn)
        
        # Refresh expense table
        self.expense_table.setRowCount(len(self.data.expense_entries))
        for i, entry in enumerate(self.data.expense_entries):
            self.expense_table.setItem(i, 0, QTableWidgetItem(entry['date']))
            self.expense_table.setItem(i, 1, QTableWidgetItem(entry['label']))
            self.expense_table.setItem(i, 2, QTableWidgetItem(entry['category']))
            self.expense_table.setItem(i, 3, QTableWidgetItem(f"${entry['amount']:.2f}"))
            
            delete_btn = QPushButton("🗑️ Delete")
            delete_btn.setStyleSheet("background-color: #ff5252; color: white;")
            delete_btn.clicked.connect(lambda checked, idx=i: self.delete_expense(idx))
            self.expense_table.setCellWidget(i, 4, delete_btn)
        
        self.update_summary_cards()
        self.update_report()
    
    def delete_income(self, index):
        reply = QMessageBox.question(
            self, "Confirm Delete",
            "Are you sure you want to delete this income entry?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.data.remove_income(index)
            self.refresh_tables()
    
    def delete_expense(self, index):
        reply = QMessageBox.question(
            self, "Confirm Delete",
            "Are you sure you want to delete this expense entry?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.data.remove_expense(index)
            self.refresh_tables()
    
    def update_summary_cards(self):
        total_income = self.data.get_total_income()
        total_expenses = self.data.get_total_expenses()
        balance = self.data.get_balance()
        
        self.income_card.findChild(QLabel, "value_label").setText(f"${total_income:,.2f}")
        self.expense_card.findChild(QLabel, "value_label").setText(f"${total_expenses:,.2f}")
        self.balance_card.findChild(QLabel, "value_label").setText(f"${balance:,.2f}")
        
        # Update balance card color based on positive/negative
        color = "#4caf50" if balance >= 0 else "#f44336"
        self.balance_card.setStyleSheet(f"""
            QGroupBox {{
                background-color: {color};
                border: none;
                border-radius: 10px;
                padding: 20px;
            }}
            QLabel {{
                color: white;
            }}
        """)
    
    def update_report(self):
        total_income = self.data.get_total_income()
        total_expenses = self.data.get_total_expenses()
        balance = self.data.get_balance()
        
        report = f"""
<h2 style='color: #2196f3;'>Budget Summary Report</h2>
<p><strong>Generated:</strong> {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
<hr>

<h3 style='color: #4caf50;'>Income Overview</h3>
<p><strong>Total Income:</strong> ${total_income:,.2f}</p>
<p><strong>Number of Income Entries:</strong> {len(self.data.income_entries)}</p>

<h3 style='color: #f44336;'>Expense Overview</h3>
<p><strong>Total Expenses:</strong> ${total_expenses:,.2f}</p>
<p><strong>Number of Expense Entries:</strong> {len(self.data.expense_entries)}</p>

<h3 style='color: #2196f3;'>Balance</h3>
<p><strong>Current Balance:</strong> ${balance:,.2f}</p>
<p><strong>Savings Rate:</strong> {(balance/total_income*100) if total_income > 0 else 0:.1f}%</p>

<h3 style='color: #673ab7;'>Expenses by Category</h3>
"""
        
        expenses_by_cat = self.data.get_expenses_by_category()
        if expenses_by_cat:
            report += "<ul>"
            for cat, amount in sorted(expenses_by_cat.items(), key=lambda x: x[1], reverse=True):
                percentage = (amount / total_expenses * 100) if total_expenses > 0 else 0
                report += f"<li><strong>{cat}:</strong> ${amount:,.2f} ({percentage:.1f}%)</li>"
            report += "</ul>"
        else:
            report += "<p><em>No expenses recorded yet.</em></p>"
        
        self.report_text.setHtml(report)
    
    def show_charts(self):
        expenses_by_cat = self.data.get_expenses_by_category()
        
        if not expenses_by_cat:
            QMessageBox.information(self, "No Data", "No expense data available to display.")
            return
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        fig.suptitle('Budget Analysis', fontsize=16, fontweight='bold')
        
        # Bar chart
        categories = list(expenses_by_cat.keys())
        values = list(expenses_by_cat.values())
        colors_list = plt.cm.Set3(range(len(categories)))
        
        ax1.bar(categories, values, color=colors_list, edgecolor='black', linewidth=1.2)
        ax1.axhline(y=self.data.get_total_income(), color='green', linestyle='--', 
                    linewidth=2, label=f'Total Income: ${self.data.get_total_income():,.2f}')
        ax1.set_title('Expenses by Category', fontweight='bold')
        ax1.set_ylabel('Amount ($)', fontweight='bold')
        ax1.set_xlabel('Category', fontweight='bold')
        ax1.legend()
        ax1.grid(axis='y', linestyle='--', alpha=0.3)
        plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        # Pie chart
        ax2.pie(values, labels=categories, autopct='%1.1f%%', startangle=90,
                colors=colors_list, textprops={'fontweight': 'bold'})
        ax2.set_title('Expense Distribution', fontweight='bold')
        
        plt.tight_layout()
        plt.show()
    
    def export_pdf(self):
        try:
            pdf_path = f"budget_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            doc = SimpleDocTemplate(pdf_path, pagesize=letter)
            story = []
            styles = getSampleStyleSheet()
            
            # Title
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                textColor=colors.HexColor('#2196f3'),
                spaceAfter=30,
                alignment=1
            )
            story.append(Paragraph("Budget Summary Report", title_style))
            story.append(Spacer(1, 0.2*inch))
            
            # Summary
            summary_data = [
                ['Metric', 'Value'],
                ['Total Income', f'${self.data.get_total_income():,.2f}'],
                ['Total Expenses', f'${self.data.get_total_expenses():,.2f}'],
                ['Balance', f'${self.data.get_balance():,.2f}'],
                ['Income Entries', str(len(self.data.income_entries))],
                ['Expense Entries', str(len(self.data.expense_entries))]
            ]
            
            summary_table = Table(summary_data, colWidths=[3*inch, 3*inch])
            summary_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2196f3')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 14),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(summary_table)
            story.append(Spacer(1, 0.4*inch))
            
            # Expenses by Category
            story.append(Paragraph("Expenses by Category", styles['Heading2']))
            story.append(Spacer(1, 0.2*inch))
            
            expenses_by_cat = self.data.get_expenses_by_category()
            if expenses_by_cat:
                expense_data = [['Category', 'Amount', 'Percentage']]
                total_exp = self.data.get_total_expenses()
                for cat, amount in sorted(expenses_by_cat.items(), key=lambda x: x[1], reverse=True):
                    pct = (amount / total_exp * 100) if total_exp > 0 else 0
                    expense_data.append([cat, f'${amount:,.2f}', f'{pct:.1f}%'])
                
                expense_table = Table(expense_data, colWidths=[2.5*inch, 2*inch, 1.5*inch])
                expense_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#673ab7')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 12),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                
                story.append(expense_table)
            
            # Generate and add chart
            if expenses_by_cat:
                story.append(Spacer(1, 0.4*inch))
                chart_path = 'temp_chart.png'
                
                fig, ax = plt.subplots(figsize=(8, 5))
                categories = list(expenses_by_cat.keys())
                values = list(expenses_by_cat.values())
                colors_list = plt.cm.Set3(range(len(categories)))
                
                ax.bar(categories, values, color=colors_list, edgecolor='black')
                ax.set_title('Expenses by Category', fontweight='bold', fontsize=14)
                ax.set_ylabel('Amount ($)', fontweight='bold')
                ax.grid(axis='y', linestyle='--', alpha=0.3)
                plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
                plt.tight_layout()
                plt.savefig(chart_path, dpi=150, bbox_inches='tight')
                plt.close()
                
                story.append(Image(chart_path, width=6*inch, height=3.75*inch))
                
                # Clean up temp file
                Path(chart_path).unlink(missing_ok=True)
            
            # Build PDF
            doc.build(story)
            
            QMessageBox.information(self, "Export Complete", 
                                  f"Budget report exported successfully to:\n{pdf_path}")
            
        except Exception as e:
            QMessageBox.critical(self, "Export Error", f"Failed to export PDF: {str(e)}")


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Modern look
    window = BudgetTracker()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
