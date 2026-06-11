import streamlit as st                 #web-based dashboard and user interface
import psycopg2                        #connect Python with PostgreSQL database and execute SQL queries

# =========================================
# DATABASE CONNECTION
# ==========================================
def get_connection():                  #Created a reusable function for establishing a PostgreSQL database connection
    return psycopg2.connect(
        host="localhost",
        database="sales_db",
        user="postgres",
        password="123456",
        port="5432"
    )                                  #This avoids writing connection code multiple times
                                       #Every database operation calls this function


# ==========================================
# LOGIN FUNCTION
# ==========================================
def login(username, password):         #Opens database connection

    conn = get_connection()
    cur = conn.cursor()                #Creates cursor object to execute SQL queries

    cur.execute("""
        SELECT user_id, role, branch_id
        FROM users
        WHERE username=%s
        AND password=%s
    """, (username, password))          #Retrieves user details from database, #Uses parameterized query to prevent SQL injection attacks

    user = cur.fetchone()               #Retrieves single matching user record

    cur.close()
    conn.close()

    return user                          #Returns authenticated user information


# ==========================================
# LOAD DATA 
# ==========================================
def load_data(query, params=None):         #Generic function for fetching data from database, #Used throughout the application

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(query, params)             #Executes dynamic SQL query

    columns = [desc[0] for desc in cur.description]  #Extracts column names from query result
    rows = cur.fetchall()                  #Retrieves all record

    cur.close() 
    conn.close()

    return columns, rows                   #Returns both column names and row data


# ==========================================
# SESSION STATE
# ==========================================
if "logged_in" not in st.session_state:     #Maintains user login state.
    st.session_state.logged_in = False      #Prevents user from logging in repeatedly on every page refresh.


# ==========================================
# LOGIN PAGE
# ==========================================
if not st.session_state.logged_in:

    st.title("Sales Management System")

    username = st.text_input("Username")    #Captures user credentials
    password = st.text_input("Password", type="password")

    if st.button("Login"):                  #Executes login validation when button is clicked

        user = login(username, password)    #Calls authentication function

        if user:

            st.session_state.logged_in = True  #Stores logged-in user information, #Used for role-based access control
            st.session_state.user_id = user[0]
            st.session_state.role = user[1]
            st.session_state.branch_id = user[2]

            st.rerun()

        else:
            st.error("Invalid Username or Password")


# ==========================================
# DASHBOARD
# ==========================================
else:

    role = st.session_state.role
    branch_id = st.session_state.branch_id

    st.sidebar.title("Menu")

    menu = st.sidebar.radio(                  #Creates navigation menu
        "Select Option",
        [
            "Dashboard",
            "Add Sales",
            "Add Payment",
            "Sales Report",
            "Pending Payments",
            "Analytics",
            "SQL Queries"
        ]
    )

    if st.sidebar.button("Logout"):
        st.session_state.clear()
        st.rerun()

    # ======================================
    # DASHBOARD
    # ======================================
    if menu == "Dashboard":

        st.title("Dashboard")

        if role == "Super Admin":

            kpi_query = """         
            SELECT
                SUM(gross_sales),
                SUM(received_amount),
                SUM(pending_amount)
            FROM customer_sales
            """                              #Calculates business KPI

        else:

            kpi_query = """
            SELECT
                SUM(gross_sales),
                SUM(received_amount),
                SUM(pending_amount)
            FROM customer_sales
            WHERE branch_id=%s
            """                              #Displays KPI cards on dashboard.

        conn = get_connection()
        cur = conn.cursor()

        if role == "Super Admin":
            cur.execute(kpi_query)
        else:
            cur.execute(kpi_query, (branch_id,))

        kpi = cur.fetchone()

        cur.close()
        conn.close()

        col1, col2, col3 = st.columns(3)

        col1.metric("Total Sales", kpi[0] or 0)
        col2.metric("Received Amount", kpi[1] or 0)
        col3.metric("Pending Amount", kpi[2] or 0)

    # ======================================
    # ADD SALES
    # ======================================
    elif menu == "Add Sales":                # Allows users to create new sales records.

        st.title("Add Sales") 

        if role == "Super Admin":

            branch_id_input = st.number_input(
                "Branch ID",
                min_value=1
            )

        else:

            branch_id_input = branch_id
            st.info(f"Branch ID : {branch_id}")

        sale_date = st.date_input("Sale Date")   #Captures customer and transaction details.

        customer_name = st.text_input("Customer Name")

        mobile = st.text_input("Mobile Number")

        product = st.selectbox(
            "Product",
            ["DS", "DA", "BA", "FSD"]
        )                                        #Product selection dropdown.

        gross_sales = st.number_input(
            "Gross Sales",
            min_value=0.0
        )

        if st.button("Save Sale"):

            conn = get_connection()
            cur = conn.cursor()

            cur.execute("""
                INSERT INTO customer_sales
                (
                    branch_id,
                    sale_date,
                    customer_name,
                    mobile_number,
                    product_name,
                    gross_sales
                )
                VALUES (%s,%s,%s,%s,%s,%s)
            """,
            (
                branch_id_input,
                sale_date,
                customer_name,
                mobile,
                product,
                gross_sales
            ))

            conn.commit()

            cur.close()
            conn.close()

            st.success("Sale Added Successfully")

    # ======================================
    # ADD PAYMENT
    # ======================================
    elif menu == "Add Payment":

        st.title("Add Payment")

        if role == "Super Admin":

            columns, rows = load_data(
                "SELECT sale_id FROM customer_sales"
            )                                    #Loads available sales IDs.

        else:

            columns, rows = load_data(
                """
                SELECT sale_id
                FROM customer_sales
                WHERE branch_id=%s
                """,
                [branch_id]
            )

        sale_ids = [row[0] for row in rows]     #Converts database records into list format.

        sale_id = st.selectbox(
            "Sale ID",
            sale_ids
        )

        amount = st.number_input(
            "Amount",
            min_value=1.0
        )

        payment_method = st.selectbox(
            "Payment Method",
            ["Cash", "UPI", "Card"]
        )

        if st.button("Add Payment"):

            conn = get_connection()
            cur = conn.cursor()

            cur.execute("""
                INSERT INTO payment_splits
                (
                    sale_id,
                    amount_paid,
                    payment_method
                )
                VALUES (%s,%s,%s)
            """,
            (
                sale_id,
                amount,
                payment_method
            ))

            conn.commit()

            cur.close()
            conn.close()

            st.success("Payment Added Successfully")

    # ======================================
    # SALES REPORT
    # ======================================
    elif menu == "Sales Report":

        st.title("Sales Report")

        if role == "Super Admin":

            query = """
            SELECT *
            FROM customer_sales
            """

            columns, rows = load_data(query)

        else:

            query = """
            SELECT *
            FROM customer_sales
            WHERE branch_id=%s
            """

            columns, rows = load_data(
                query,
                [branch_id]
            )

        data = [
            dict(zip(columns, row))
            for row in rows
        ]                                   #Converts SQL rows into dictionary format.

        st.dataframe(data)                  #Displays interactive report.

    # ======================================
    # PENDING PAYMENTS
    # ======================================
    elif menu == "Pending Payments":

        st.title("Pending Payments")

        if role == "Super Admin":

            query = """
            SELECT *
            FROM customer_sales
            WHERE pending_amount > 0
            """                             #Filters only customers with outstanding dues, #Helps finance team focus on collections.

            columns, rows = load_data(query)

        else:

            query = """
            SELECT *
            FROM customer_sales
            WHERE branch_id=%s
            AND pending_amount > 0
            """

            columns, rows = load_data(
                query,
                [branch_id]
            )

        data = [
            dict(zip(columns, row))
            for row in rows
        ]

        st.dataframe(data)

    # ======================================
    # ANALYTICS
    # ======================================
    elif menu == "Analytics":

        st.title("Analytics")

        query = """
        SELECT
            b.branch_name,
            SUM(cs.gross_sales) AS total_sales
        FROM customer_sales cs
        JOIN branches b             
        ON cs.branch_id = b.branch_id
        GROUP BY b.branch_name
        ORDER BY b.branch_name
        """                                  #Combines branch information with sales data.

        columns, rows = load_data(query)

        chart_data = {
            row[0]: row[1]
            for row in rows
        }

        st.bar_chart(chart_data)              #Visualizes branch performance. #Identifies top-performing and underperforming branches.

    # ======================================
    # SQL QUERIES
    # ======================================
    elif menu == "SQL Queries":

        st.title("SQL Queries")

        query_option = st.selectbox(
            "Select Query",
            [
                "Top 3 Sales",
                "Monthly Summary",
                "Payment Method Summary"
            ]                                  #Finds highest-value sales transactions.
        )

        if query_option == "Top 3 Sales":

            query = """
            SELECT
                sale_id,
                customer_name,
                gross_sales
            FROM customer_sales
            ORDER BY gross_sales DESC
            LIMIT 3
            """

        elif query_option == "Monthly Summary":

            query = """
            SELECT
                TO_CHAR(
                    sale_date,
                    'YYYY-MM'
                ) AS month,
                SUM(gross_sales) AS total_sales
            FROM customer_sales
            GROUP BY month
            ORDER BY month
            """                                     #Aggregates sales month-wise

        else:

            query = """
            SELECT
                payment_method,
                SUM(amount_paid) AS total_amount
            FROM payment_splits
            GROUP BY payment_method
            """                                     #Identifies preferred payment modes.

        columns, rows = load_data(query)

        data = [
            dict(zip(columns, row))
            for row in rows
        ]

        st.dataframe(data)
