# Budget Tracker Pro 💰

A modern, feature-rich personal finance management application built with PyQt6.

## Features

✨ **Core Features**
- Track income and expenses with categories
- Automatic data persistence (saves to JSON)
- Date tracking for all transactions
- Real-time balance calculation
- Categorized expense tracking

📊 **Analytics & Reporting**
- Visual summary cards (Income, Expenses, Balance)
- Interactive transaction history tables
- Detailed budget reports with savings rate
- Bar and pie chart visualizations
- Professional PDF export with charts

🎨 **User Interface**
- Modern, clean design with color-coded cards
- Tabbed interface for easy navigation
- Calendar date pickers
- Confirmation dialogs for deletions
- Responsive layout

## Installation

### Automatic Installation (Recommended)

Simply run the script - it will automatically install all dependencies:

```bash
python budget_tracker.py
```

The script will check for required packages and install:
- PyQt6 (GUI framework)
- matplotlib (charts and visualizations)
- reportlab (PDF generation)

### Manual Installation

If you prefer to install dependencies manually:

```bash
pip install -r requirements.txt
```

Or install individually:

```bash
pip install PyQt6 matplotlib reportlab
```

## Usage

### Running the Application

```bash
python budget_tracker.py
```

### Adding Transactions

1. **Add Income**: Go to the "Add Transactions" tab
   - Enter description (e.g., "Salary", "Freelance")
   - Enter amount
   - Select date
   - Click "Add Income"

2. **Add Expense**: In the same tab
   - Enter description (e.g., "Groceries", "Gas")
   - Enter amount
   - Select category from 15 options
   - Select date
   - Click "Add Expense"

### Viewing History

Navigate to the "Transaction History" tab to:
- View all income entries in a table
- View all expense entries with categories
- Delete individual transactions (with confirmation)

### Reports & Analytics

Go to the "Reports & Analytics" tab to:
- View comprehensive budget summary
- See expense breakdown by category
- Check your savings rate
- Generate visual charts
- Export professional PDF reports

## Data Storage

All data is automatically saved to `budget_data.json` in the same directory as the script. This file is created automatically on first run and updated after every transaction.

## Categories

The app includes 15 preset categories:
- Food & Dining
- Transportation
- Utilities
- Entertainment
- Housing
- Healthcare
- Insurance
- Savings & Investments
- Education
- Travel
- Shopping
- Personal Care
- Debt Payments
- Gifts & Donations
- Miscellaneous

## PDF Reports

Exported PDF reports include:
- Summary table with all key metrics
- Expense breakdown by category with percentages
- Visual bar chart of expenses
- Professional formatting with color-coded sections
- Timestamped filename for easy organization

## System Requirements

- Python 3.7 or higher
- Works on Windows, macOS, and Linux
- No additional system dependencies required

## Tips

- **Backup your data**: The `budget_data.json` file contains all your financial data
- **Regular exports**: Export PDF reports monthly for record-keeping
- **Use dates**: Properly dating transactions helps with time-based analysis
- **Consistent categories**: Use the same categories consistently for better insights

## Troubleshooting

**Dependencies won't install?**
- Make sure you have pip installed: `python -m ensurepip`
- Try upgrading pip: `python -m pip install --upgrade pip`
- On some systems, use `--break-system-packages` flag

**App won't start?**
- Check Python version: `python --version` (need 3.7+)
- Verify all packages installed: `pip list | grep -E "PyQt6|matplotlib|reportlab"`

**Data not saving?**
- Ensure you have write permissions in the directory
- Check that `budget_data.json` is not open in another program

## License

This is free and open-source software. Feel free to modify and distribute.

## Author

Created as a comprehensive personal finance tool with modern design and professional features.

---

**Version**: 2.0  
**Last Updated**: January 2026
