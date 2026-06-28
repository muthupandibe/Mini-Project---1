# 📊 Sales Intelligence Hub

A comprehensive Sales Management and Analytics Platform built using **Python, Streamlit, PostgreSQL, and SQL**. The application helps organizations manage sales transactions, monitor customer payments, analyze branch performance, and generate business insights through interactive dashboards and reports.

---

## 🚀 Project Overview

Sales Intelligence Hub is a centralized system designed to streamline sales operations across multiple branches. It provides role-based access control, real-time KPI monitoring, payment tracking, sales reporting, and analytical dashboards to support data-driven business decisions.

---

## 🎯 Project Objectives

- Manage sales transactions across multiple branches.
- Track customer payments and pending balances.
- Monitor business performance through KPIs.
- Generate analytical reports for management.
- Support data-driven decision-making.

---

## 🛠️ Technology Stack

| Technology | Purpose |
|------------|---------|
| Python | Backend Development |
| Streamlit | Frontend Dashboard |
| PostgreSQL | Database Management |
| SQL | Data Querying & Analytics |
| Psycopg2 | Database Connectivity |

---

## ✨ Features

### 🔐 User Authentication
- Secure Login System
- Role-Based Access Control
- Super Admin and Branch User Access

### 📈 Dashboard
- Total Sales KPI
- Received Amount KPI
- Pending Amount KPI

### 💰 Sales Management
- Add New Sales
- Capture Customer Details
- Product-wise Sales Tracking

### 💳 Payment Management
- Add Customer Payments
- Multiple Payment Methods
  - Cash
  - UPI
  - Card

### 📋 Reports
- Sales Report
- Pending Payment Report
- Branch-wise Filtering

### 📊 Analytics
- Branch-wise Sales Performance
- Interactive Charts
- Revenue Analysis

### 🔍 SQL Insights
- Top 3 Sales
- Monthly Sales Summary
- Payment Method Summary

---

## 🏗️ System Architecture

```text
Sales Intelligence Hub
│
├── Authentication Module
│
├── Dashboard Module
│   ├── Total Sales
│   ├── Received Amount
│   └── Pending Amount
│
├── Sales Management
│   └── Add Sales
│
├── Payment Management
│   └── Add Payments
│
├── Reporting
│   ├── Sales Report
│   └── Pending Payments
│
├── Analytics
│   └── Branch-wise Analysis
│
└── SQL Insights
    ├── Top Sales
    ├── Monthly Summary
    └── Payment Method Analysis
```

---

## 🗄️ Database Tables

### Users

| Column | Description |
|----------|-------------|
| user_id | User ID |
| username | Login Username |
| password | User Password |
| role | User Role |
| branch_id | Assigned Branch |

### Customer Sales

| Column | Description |
|----------|-------------|
| sale_id | Sale Identifier |
| branch_id | Branch Identifier |
| sale_date | Date of Sale |
| customer_name | Customer Name |
| mobile_number | Mobile Number |
| product_name | Product Name |
| gross_sales | Total Sale Amount |
| received_amount | Amount Received |
| pending_amount | Outstanding Amount |
| status | Payment Status |

### Payment Splits

| Column | Description |
|----------|-------------|
| payment_id | Payment ID |
| sale_id | Related Sale |
| amount_paid | Payment Amount |
| payment_method | Payment Method |

### Branches

| Column | Description |
|----------|-------------|
| branch_id | Branch ID |
| branch_name | Branch Name |

---

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/muthupandibe/Mini-Project---1.git
cd Mini-Project---1
```

### Create Virtual Environment

```bash
python -m venv venv
```

#### Activate Environment

**Windows**

```bash
venv\Scripts\activate
```

**Linux/Mac**

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install streamlit psycopg2
```

or

```bash
pip install -r requirements.txt
```

---

## 🛠️ Database Configuration

Update the PostgreSQL credentials in the application:

```python
def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="sales_db",
        user="postgres",
        password="your_password",
        port="5432"
    )
```

---

## ▶️ Running the Application

```bash
streamlit run app.py
```

---

## 📊 Key Performance Indicators

The dashboard provides:

- Total Revenue
- Total Collections
- Pending Collections
- Branch-wise Sales Performance
- Payment Method Analysis

---

## 🔍 SQL Concepts Used

- Joins
- Aggregations
- Group By
- Order By
- Filtering
- Date Functions
- KPI Calculations
- Role-Based Data Access

---

## 📈 Business Insights

### Key Findings

- Top-performing branches contribute the majority of revenue.
- UPI is the most frequently used payment method.
- Pending payments affect cash flow management.
- Monthly sales trends reveal seasonal demand patterns.

### Recommendations

- Automate payment reminders for pending collections.
- Focus marketing efforts on high-performing products.
- Improve collection processes for overdue payments.
- Use sales trends for demand forecasting and planning.

---

## 🔒 Security Features

- Parameterized SQL Queries
- Role-Based Access Control
- Session State Management
- Secure Login Validation

---

## 🚀 Future Enhancements

- Password Encryption (bcrypt)
- PDF/Excel Report Export
- Email Notifications
- SMS Payment Reminders
- Customer Segmentation
- Machine Learning-Based Sales Forecasting

---

## 👨‍💻 Author

**Muthu Pandi **

- Data Analyst
- Python Developer
- SQL Developer

GitHub: https://github.com/muthupandibe

---

## 📜 License

This project is developed for educational, learning, and portfolio purposes.
