# Restaurant Bill Calculator

A Streamlit web application for calculating restaurant bills with support for multiple customers.

## Features

- **Multiple Customers**: Add orders for multiple customers
- **Quantity Selection**: Order the same item multiple times (0-10 quantity)
- **Individual Bills**: View breakdown for each customer
- **Separate Receipts**: Download receipt for each customer
- **Tax & Tip**: Configurable tax and tip percentages
- **Final Bill**: Combined bill with tax and tip

## Menu Prices

### Food Items
| Item | Price |
|------|-------|
| Pizza | Rs.599 |
| Burger | Rs.299 |
| Pasta | Rs.499 |

### Drinks
| Item | Price |
|------|-------|
| Coke | Rs.99 |
| Coffee | Rs.149 |
| Tea | Rs.79 |

## Installation

1. Clone the repository:
```bash
git clone https://github.com/thevanshit/Billing-System.git
cd Billing-System
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run app.py
```

## Usage

1. Open the application in your browser (http://localhost:8501)
2. Use the sidebar to set tax and tip percentages
3. Enter customer name
4. Select quantity for each item (0-10)
5. Click "Add to Bill" to add customer
6. Download individual receipts or final bill
7. Use "Reset All" to start fresh

## Requirements

- Python 3.8+
- Streamlit 1.28.0+

## License

MIT License
