📊 Sales & Business Analytics Dashboard

A web-based Sales & Business Analytics Dashboard built using Python Flask, MySQL, Pandas, and Chart.js.

The application helps businesses manage sales data, analyze business performance, visualize important sales metrics, and generate analytical reports.

🚀 Features
🔐 User Login & Authentication
📊 Interactive Sales Dashboard
💰 Total Revenue Tracking
🛒 Total Orders Tracking
👥 Customer Management
📦 Product Management
📈 Sales Analytics
📊 Interactive Charts
📤 CSV/Excel Data Upload
🧹 Automated Data Cleaning
📑 Sales Performance Analysis
📄 PDF Report Generation
💳 Payment Method Analysis
🏆 Top Products Analysis
👤 Top Customer Analysis
📅 Monthly & Daily Sales Analysis
🛠️ Technologies Used
Backend
Python
Flask
MySQL
MySQL Connector
Data Analysis
Pandas
NumPy
Frontend
HTML5
CSS3
Bootstrap 5
JavaScript
Chart.js
Reporting
ReportLab
📁 Project Structure
sales-business-analytics-dashboard/
│
├── app.py
├── requirements.txt
├── README.md
│
├── database/
│   └── database.sql
│
├── templates/
│   ├── login.html
│   ├── dashboard.html
│   ├── upload.html
│   ├── sales.html
│   ├── products.html
│   ├── customers.html
│   └── reports.html
│
├── static/
│   ├── css/
│   │   └── style.css
│   │
│   ├── js/
│   │   ├── dashboard.js
│   │   └── charts.js
│   │
│   └── images/
│
├── uploads/
│   └── sales/
│
├── reports/
│   └── generated/
│
└── utils/
    ├── __init__.py
    ├── data_cleaning.py
    ├── analysis.py
    └── report_generator.py
📊 Dashboard

The dashboard provides an overview of important business metrics such as:

Total Revenue
Total Orders
Total Customers
Total Products
Monthly Sales
Category Performance
Top Products
Top Customers
Payment Methods

Interactive charts are created using Chart.js.

🧹 Data Cleaning

The project includes an automated sales data-cleaning pipeline using Pandas.

The pipeline performs:

Reading CSV/Excel files
Cleaning column names
Validating required columns
Removing duplicate records
Handling missing values
Converting data types
Removing invalid values
Calculating total sales amount

For example:

total_amount = quantity × unit_price
📈 Sales Analysis

The analytics module calculates:

Total Revenue
Total Orders
Total Quantity Sold
Average Order Value
Monthly Sales
Daily Sales
Category Sales
Top Products
Top Customers
Payment Method Performance
