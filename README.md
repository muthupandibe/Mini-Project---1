📊 Sales Intelligence Hub
🚀 Project Overview

Sales Intelligence Hub is a web-based Sales Management and Analytics System developed using Python, Streamlit, PostgreSQL, and SQL. The application helps organizations manage sales transactions, track customer payments, monitor branch performance, and generate actionable business insights through interactive dashboards and reports.

The platform supports role-based access control, enabling administrators and branch users to access data relevant to their responsibilities while ensuring data security and operational efficiency.

🎯 Project Objectives
Manage and monitor sales activities across multiple branches.
Track customer payments and pending balances.
Generate real-time sales reports and KPIs.
Analyze branch-wise performance and revenue trends.
Support business decision-making through data-driven insights.
🛠️ Technology Stack
Technology	Purpose
Python	Backend Development
Streamlit	Frontend Dashboard
PostgreSQL	Relational Database
SQL	Data Querying & Analysis
Psycopg2	Database Connectivity
📌 Key Features
🔐 User Authentication
Secure login system.
Role-based access control.
Separate access for Super Admin and Branch Users.
📈 Dashboard

Displays key business metrics:

Total Sales
Received Amount
Pending Amount
💰 Sales Management
Add new sales transactions.
Capture customer details.
Store product and sales information.
💳 Payment Management
Record customer payments.
Support multiple payment methods:
Cash
UPI
Card
📋 Reports
Complete Sales Report
Pending Payment Report
Branch-wise filtering
📊 Analytics
Branch-wise sales comparison.
Interactive visualizations.
Performance monitoring dashboard.
🔍 SQL Insights

Predefined analytical queries:

Top 3 Sales
Monthly Sales Summary
Payment Method Analysis
🗄️ Database Schema
Users Table
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50),
    password VARCHAR(50),
    role VARCHAR(20),
    branch_id INT
);
Customer Sales Table
CREATE TABLE customer_sales (
    sale_id SERIAL PRIMARY KEY,
    branch_id INT,
    sale_date DATE,
    customer_name VARCHAR(100),
    mobile_number VARCHAR(15),
    product_name VARCHAR(50),
    gross_sales NUMERIC,
    received_amount NUMERIC,
    pending_amount NUMERIC,
    status VARCHAR(20)
);
Payment Splits Table
CREATE TABLE payment_splits (
    payment_id SERIAL PRIMARY KEY,
    sale_id INT,
    amount_paid NUMERIC,
    payment_method VARCHAR(20)
);
Branches Table
CREATE TABLE branches (
    branch_id SERIAL PRIMARY KEY,
    branch_name VARCHAR(100)
);
📂 Project Structure
Sales-Intelligence-Hub/
│
├── app.py
├── database/
│   ├── schema.sql
│   └── sample_data.sql
│
├── screenshots/
│   ├── login.png
│   ├── dashboard.png
│   ├── analytics.png
│
├── requirements.txt
├── README.md
└── assets/
⚙️ Installation & Setup
1️⃣ Clone Repository
git clone https://github.com/muthupandibe/Sales-Intelligence-Hub.git
cd Sales-Intelligence-Hub
2️⃣ Create Virtual Environment
python -m venv venv

Activate Environment:

Windows

venv\Scripts\activate

Linux / Mac

source venv/bin/activate
3️⃣ Install Dependencies
pip install -r requirements.txt

Or

pip install streamlit psycopg2
4️⃣ Configure PostgreSQL

Update database credentials in the connection function:

def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="sales_db",
        user="postgres",
        password="your_password",
        port="5432"
    )
5️⃣ Run Application
streamlit run app.py
📈 Dashboard KPIs

The application provides real-time monitoring of:

Total Revenue Generated
Total Amount Collected
Total Outstanding Amount
Branch Performance
Payment Trends
🔍 SQL Concepts Used
Joins
Aggregations
Group By
Order By
Date Functions
Conditional Filtering
KPI Calculations
Role-Based Query Filtering
📊 Business Insights
Key Findings
Certain branches contribute significantly higher revenue.
UPI is the most preferred payment method.
Pending payments impact cash flow management.
Monthly sales trends help identify seasonal demand.
Business Recommendations
Implement automated payment reminders.
Focus marketing efforts on top-performing products.
Monitor branches with high pending collections.
Use monthly trends for sales forecasting and inventory planning.
🔒 Security Features
Parameterized SQL Queries
Session State Management
Role-Based Access Control
Secure Authentication Flow
🚀 Future Enhancements
Password Encryption (bcrypt)
Export Reports to Excel/PDF
Email & SMS Notifications
Customer Segmentation
Sales Forecasting using Machine Learning
Real-Time Performance Monitoring
📷 Application Screenshots
Login Page

Add screenshot here

Dashboard

Add screenshot here

Sales Entry

Add screenshot here

Analytics Dashboard

Add screenshot here

Reports

Add screenshot here

👨‍💻 Author

Muthu Pandi B

Data Analyst
Python Developer
SQL Developer

GitHub: muthupandibe GitHub Profile

⭐ Project Highlights

✔ Multi-Branch Sales Management
✔ PostgreSQL Database Integration
✔ Interactive Streamlit Dashboard
✔ Role-Based Access Control
✔ Payment Tracking System
✔ Analytical Reporting & KPI Monitoring
✔ Business Intelligence Insights
