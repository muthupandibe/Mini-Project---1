import streamlit as st                 # Imports Streamlit for the web-based dashboard and UI
import psycopg2                        # Imports PostgreSQL adapter to connect and execute SQL queries

# ==========================================
# DATABASE CONNECTION
# ==========================================
def get_connection():                  # Defines a reusable function to establish a database connection
    return psycopg2.connect(           # Connects to the PostgreSQL server and returns the connection object
        host="localhost",              # Specifies the server address (local machine)
        database="sales_db",           # Specifies the target database name
        user="postgres",               # Specifies the database username
        password="123456",             # Specifies the database password
        port="5432"                    # Specifies the PostgreSQL default port
    )                                  # Ends the connection parameters


# ==========================================
# LOGIN FUNCTION
# ==========================================
def login(username, password):         # Defines the login function taking a username and password

    conn = get_connection()            # Calls the connection function to open a database connection
    cur = conn.cursor()                # Creates a cursor object to execute SQL commands in memory
                                       # Executes a multi-line SQL query
    cur.execute("""                    
        SELECT user_id, role, branch_id
        FROM users
        WHERE username=%s              
        AND password=%s
    """, (username, password))        
                                       # Uses %s placeholders for parameterized queries (prevents SQL injection)
                                       # Passes the user inputs to fill the %s placeholders safely

    user = cur.fetchone()              # Fetches the single matching user record (returns None if no match)

    cur.close()                        # Closes the cursor to free up resources
    conn.close()                       # Closes the database connection

    return user                        # Returns the authenticated user data tuple


# ==========================================
# LOAD DATA 
# ==========================================
def load_data(query, params=None):     # Defines a generic function to fetch data, with optional parameters

    conn = get_connection()            # Opens database connection
    cur = conn.cursor()                # Creates cursor

    cur.execute(query, params)         # Executes the provided SQL query with the provided parameters

    columns = [desc[0] for desc in cur.description]  # Extracts column names from the cursor's description metadata
    rows = cur.fetchall()                  # Retrieves all rows returned by the executed query

    cur.close()                        # Closes cursor
    conn.close()                       # Closes connection

    return columns, rows               # Returns both the column headers and the data rows


# ==========================================
# SESSION STATE
# ==========================================
if "logged_in" not in st.session_state:    # Checks if the "logged_in" variable exists in Streamlit's session memory
    st.session_state.logged_in = False     # If not, initializes it to False (user is logged out by default)


# ==========================================
# LOGIN PAGE
# ==========================================
if not st.session_state.logged_in:         # Checks if the user is currently NOT logged in

    st.title("Sales Management System")    # Displays the main title on the login screen

    username = st.text_input("Username")   # Renders a text input field for the username
    password = st.text_input("Password", type="password") # Renders a masked text input field for the password

    if st.button("Login"):                 # Checks if the "Login" button has been clicked

        user = login(username, password)   # Calls the login function to verify credentials against the DB

        if user:                           # If a valid user record is returned

            st.session_state.logged_in = True  # Updates session state to mark user as logged in
            st.session_state.user_id = user[0] # Stores the user ID in session memory
            st.session_state.role = user[1]    # Stores the user role (e.g., Admin, Super Admin)
            st.session_state.branch_id = user[2] # Stores the branch ID associated with the user

            st.rerun()                     # Instantly refreshes the app to load the dashboard

        else:                              # If the login function returned None (invalid credentials)
            st.error("Invalid Username or Password") # Displays a red error message


# ==========================================
# DASHBOARD
# ==========================================
else:                                      # Executes if the user IS logged in

    role = st.session_state.role           # Retrieves the logged-in user's role from memory
    branch_id = st.session_state.branch_id # Retrieves the logged-in user's branch ID from memory

    st.sidebar.title("Menu")               # Displays a title in the left sidebar

    menu = st.sidebar.radio(               # Creates a radio button menu in the sidebar for navigation
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

    if st.sidebar.button("Logout"):        # Checks if the "Logout" button in the sidebar is clicked
        st.session_state.clear()           # Wipes all session variables (logs user out)
        st.rerun()                         # Refreshes the app to show the login screen

    # ======================================
    # DASHBOARD
    # ======================================
    if menu == "Dashboard":                # Checks if "Dashboard" is selected in the menu

        st.title("Dashboard")              # Displays the page title

        if role == "Super Admin":          # Checks if the user has top-level permissions
                                           # Prepares a query to sum up all sales data across ALL branches
            kpi_query = """                
            SELECT
                SUM(gross_sales),
                SUM(received_amount),
                SUM(pending_amount)
            FROM customer_sales
            """

        else:                              # If the user is a regular Admin
                                           # Prepares a query to sum up sales data ONLY for their specific branch
            kpi_query = """                
            SELECT
                SUM(gross_sales),
                SUM(received_amount),
                SUM(pending_amount)
            FROM customer_sales
            WHERE branch_id=%s             
            """                            # Filters by branch_id

        conn = get_connection()            # Opens database connection
        cur = conn.cursor()                # Creates cursor

        if role == "Super Admin":          # If Super Admin...
            cur.execute(kpi_query)         # Executes query without parameters
        else:                              # If regular Admin...
            cur.execute(kpi_query, (branch_id,)) # Executes query filtered by their session branch_id

        kpi = cur.fetchone()               # Fetches the single row containing the three sums

        cur.close()                        # Closes cursor
        conn.close()                       # Closes connection

        col1, col2, col3 = st.columns(3)   # Splits the Streamlit UI into three equal vertical columns

        col1.metric("Total Sales", kpi[0] or 0)       # Displays the total gross sales metric (defaults to 0 if None)
        col2.metric("Received Amount", kpi[1] or 0)   # Displays the total received amount metric
        col3.metric("Pending Amount", kpi[2] or 0)    # Displays the total pending amount metric

    # ======================================
    # ADD SALES
    # ======================================
    elif menu == "Add Sales":                  # Checks if "Add Sales" is selected in the menu

        st.title("Add Sales")                  # Displays the page title

        if role == "Super Admin":              # If user is a Super Admin...

            branch_id_input = st.number_input( # Allows them to manually input any branch ID
                "Branch ID",
                min_value=1
            )

        else:                                  # If user is a regular Admin...

            branch_id_input = branch_id        # Forces the branch ID to be their assigned branch
            st.info(f"Branch ID : {branch_id}")# Displays an informational message showing their locked branch ID

        sale_date = st.date_input("Sale Date") # Renders a calendar picker for the sale date
        customer_name = st.text_input("Customer Name") # Renders text field for customer name
        mobile = st.text_input("Mobile Number")        # Renders text field for mobile number

        product = st.selectbox(                # Renders a dropdown menu for product selection
            "Product",
            ["DS", "DA", "BA", "FSD"]
        )

        gross_sales = st.number_input(         # Renders a number input for the total sale amount
            "Gross Sales",
            min_value=0.0
        )

        if st.button("Save Sale"):             # Checks if the "Save Sale" button is clicked

            conn = get_connection()            # Opens DB connection
            cur = conn.cursor()                # Creates cursor
                                               # Executes an INSERT query to add the new sale
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
            """,                               # Uses parameter placeholders to prevent SQL injection
            (                                  # Passes the variable inputs into the placeholders
                branch_id_input,
                sale_date,
                customer_name,
                mobile,
                product,
                gross_sales
            ))

            conn.commit()                      # PERMANENTLY saves the transaction to the database

            cur.close()                        # Closes cursor
            conn.close()                       # Closes connection

            st.success("Sale Added Successfully") # Displays a green success alert

    # ======================================
    # ADD PAYMENT
    # ======================================
    elif menu == "Add Payment":                # Checks if "Add Payment" is selected

        st.title("Add Payment")                # Displays the page title

        if role == "Super Admin":              # If user is Super Admin...

            columns, rows = load_data(         # Fetches ALL sale IDs across the entire company
                "SELECT sale_id FROM customer_sales"
            )

        else:                                  # If user is a regular Admin...

            columns, rows = load_data(         # Fetches sale IDs ONLY for their assigned branch
                """
                SELECT sale_id
                FROM customer_sales
                WHERE branch_id=%s
                """,
                [branch_id]
            )

        sale_ids = [row[0] for row in rows]    # Extracts the IDs from the tuples into a flat Python list

        sale_id = st.selectbox(                # Renders a dropdown menu populated with the fetched sale IDs
            "Sale ID",
            sale_ids
        )

        amount = st.number_input(              # Renders a number input for the payment amount
            "Amount",
            min_value=1.0
        )

        payment_method = st.selectbox(         # Renders a dropdown for the payment method
            "Payment Method",
            ["Cash", "UPI", "Card"]
        )

        if st.button("Add Payment"):           # Checks if "Add Payment" button is clicked

            conn = get_connection()            # Opens DB connection
            cur = conn.cursor()                # Creates cursor
                                               # Executes an INSERT query to add the new payment split
            cur.execute("""                    
                INSERT INTO payment_splits
                (
                    sale_id,
                    amount_paid,
                    payment_method
                )
                VALUES (%s,%s,%s)
            """,
            (                                  # Passes variables into placeholders safely
                sale_id,
                amount,
                payment_method
            ))

            conn.commit()                      # Commits the insert to the database

            cur.close()                        # Closes cursor
            conn.close()                       # Closes connection

            st.success("Payment Added Successfully") # Displays green success message

    # ======================================
    # SALES REPORT
    # ======================================
    elif menu == "Sales Report":               # Checks if "Sales Report" is selected

        st.title("Sales Report")               # Displays title

        if role == "Super Admin":              # If Super Admin...
                                               # Prepares query to pull ALL sales records
            query = """                        
            SELECT *
            FROM customer_sales
            """

            columns, rows = load_data(query)   # Executes query and gets data

        else:                                  # If regular Admin...
                                               # Prepares query to pull ONLY their branch's records
            query = """                        
            SELECT *
            FROM customer_sales
            WHERE branch_id=%s
            """

            columns, rows = load_data(         # Executes parameterized query
                query,
                [branch_id]
            )

        data = [                               # Converts the list of tuples into a list of dictionaries
            dict(zip(columns, row))            # Zips column names to their respective row values
            for row in rows
        ] 

        st.dataframe(data)                     # Renders the data as an interactive table on the screen

    # ======================================
    # PENDING PAYMENTS
    # ======================================
    elif menu == "Pending Payments":           # Checks if "Pending Payments" is selected

        st.title("Pending Payments")           # Displays title

        if role == "Super Admin":              # If Super Admin...

            query = """                        
            SELECT *
            FROM customer_sales
            WHERE pending_amount > 0
            """ 

            columns, rows = load_data(query)   # Executes query

        else:                                  # If regular Admin...

            query = """                        
            SELECT *
            FROM customer_sales
            WHERE branch_id=%s
            AND pending_amount > 0
            """

            columns, rows = load_data(         # Executes parameterized query
                query,
                [branch_id]
            )

        data = [                               # Converts data tuples to dictionaries
            dict(zip(columns, row))
            for row in rows
        ]

        st.dataframe(data)                     # Renders the pending payments interactive table

    # ======================================
    # ANALYTICS
    # ======================================
    elif menu == "Analytics":                  # Checks if "Analytics" is selected

        st.title("Analytics")                  # Displays title
                                               # Prepares query to join sales and branches and sum gross sales
        query = """                            
        SELECT
            b.branch_name,
            SUM(cs.gross_sales) AS total_sales
        FROM customer_sales cs
        JOIN branches b
            ON cs.branch_id = b.branch_id
        GROUP BY b.branch_name
        ORDER BY b.branch_name
        """

        columns, rows = load_data(query)       # Executes query to get aggregated data

        chart_data = {                         # Creates a dictionary mapping branch names to their total sales
            row[0]: row[1]
            for row in rows
        }

        st.bar_chart(chart_data, height=500)   # Renders a bar chart visualization of the branch data

    # ======================================
    # SQL QUERIES
    # ======================================
    elif menu == "SQL Queries":                # Checks if "SQL Queries" is selected

        st.title("SQL Analytical Queries")     # Displays title

        query_option = st.selectbox(           # Renders a dropdown for pre-defined analytical views
            "Select Query",
            [
            "All Customer Sales",
            "All Branches",
            "All Payment Splits",
            "Open Sales",
            "Total Gross Sales",
            "Total Received Amount",
            "Total Pending Amount",
            "Sales Per Branch",
            "Average Gross Sales",
            "Sales With Branch Name",
            "Sales With Total Payments",
            "Branch Wise Gross Sales",
            "Sales With Payment Method",
            "Sales With Admin Name",
            "Pending Amount Greater Than 5000",
            "Top 3 Highest Gross Sales",
            "Branch With Highest Total Gross Sales",
            "Monthly Sales Summary",
            "Payment Method Wise Collection"
            ]
        )

        # The following if/elif block assigns the appropriate SQL string based on dropdown selection
        if query_option == "All Customer Sales":
            query = """
            SELECT *
            FROM customer_sales
            """
        elif query_option == "All Branches":
            query = """
            SELECT *
            FROM branches
            """
        elif query_option == "All Payment Splits":
            query = """
            SELECT *
            FROM payment_splits
            """
        elif query_option == "Open Sales":
            query = """
            SELECT *
            FROM customer_sales
            WHERE status = 'Open'
            """
        elif query_option == "Total Gross Sales":
            query = """
            SELECT SUM(gross_sales) AS total_gross_sales
            FROM customer_sales
            """
        elif query_option == "Total Received Amount":
            query = """
            SELECT SUM(received_amount) AS total_received_amount
            FROM customer_sales
            """
        elif query_option == "Total Pending Amount":
            query = """
            SELECT SUM(pending_amount) AS total_pending_amount
            FROM customer_sales
            """
        elif query_option == "Sales Per Branch":
            query = """
            SELECT
                b.branch_name,
                COUNT(cs.sale_id) AS total_sales
            FROM customer_sales cs
            JOIN branches b
            ON cs.branch_id = b.branch_id
            GROUP BY b.branch_name
            ORDER BY total_sales DESC
            """
        elif query_option == "Average Gross Sales":
            query = """
            SELECT AVG(gross_sales) AS average_gross_sales
            FROM customer_sales
            """
        elif query_option == "Sales With Branch Name":
            query = """
            SELECT
                cs.sale_id,
                cs.customer_name,
                cs.product_name,
                cs.gross_sales,
                b.branch_name
            FROM customer_sales cs
            JOIN branches b
            ON cs.branch_id = b.branch_id
            """
        elif query_option == "Sales With Total Payments":
            query = """
            SELECT
                cs.sale_id,
                cs.customer_name,
                SUM(ps.amount_paid) AS total_payment
            FROM customer_sales cs
            JOIN payment_splits ps
            ON cs.sale_id = ps.sale_id
            GROUP BY
                cs.sale_id,
                cs.customer_name
            ORDER BY cs.sale_id
            """
        elif query_option == "Branch Wise Gross Sales":
            query = """
            SELECT
            b.branch_name,
            SUM(cs.gross_sales) AS total_sales
            FROM customer_sales cs
            JOIN branches b
            ON cs.branch_id = b.branch_id
            GROUP BY b.branch_name
            ORDER BY total_sales DESC
            """
        elif query_option == "Sales With Payment Method":
            query = """
            SELECT
                cs.sale_id,
                cs.customer_name,
                ps.payment_method,
                ps.amount_paid
            FROM customer_sales cs
            JOIN payment_splits ps
            ON cs.sale_id = ps.sale_id
            ORDER BY cs.sale_id
            """
        elif query_option == "Sales With Admin Name":
            query = """
            SELECT
                cs.sale_id,
                cs.customer_name,
                b.branch_name,
                u.username AS admin_name
            FROM customer_sales cs
            JOIN branches b
            ON cs.branch_id = b.branch_id
            JOIN users u
            ON b.branch_id = u.branch_id
            WHERE u.role = 'Admin'
            """
        elif query_option == "Pending Amount Greater Than 5000":
            query = """
            SELECT
                sale_id,
                customer_name,
                mobile_number,
                gross_sales,
                received_amount,
                pending_amount
            FROM customer_sales
            WHERE pending_amount > 5000
            ORDER BY pending_amount DESC
            """
        elif query_option == "Top 3 Highest Gross Sales":
            query = """
            SELECT
                sale_id,
                customer_name,
                mobile_number,
                gross_sales
            FROM customer_sales
            ORDER BY gross_sales DESC
            LIMIT 3                        
            """
        elif query_option == "Branch With Highest Total Gross Sales":
            query = """
            SELECT
                b.branch_name,
                SUM(cs.gross_sales) AS total_gross_sales
            FROM customer_sales cs
            JOIN branches b
                ON cs.branch_id = b.branch_id
            GROUP BY b.branch_name
            ORDER BY total_gross_sales DESC
            LIMIT 1                      
            """
        elif query_option == "Monthly Sales Summary":
            query = """
            SELECT
                EXTRACT(YEAR FROM sale_date) AS year,        
                EXTRACT(MONTH FROM sale_date) AS month,      
                COUNT(*) AS total_sales,
                SUM(gross_sales) AS total_gross_sales,
                SUM(received_amount) AS total_received_amount,
                SUM(pending_amount) AS total_pending_amount
            FROM customer_sales
            GROUP BY 1, 2                  
            ORDER BY 1, 2;
            """
        elif query_option == "Payment Method Wise Collection":
            query = """
            SELECT
                payment_method,
                SUM(amount_paid) AS total_collection
            FROM payment_splits
            WHERE payment_method IN ('Cash', 'UPI', 'Card')
            GROUP BY payment_method
            ORDER BY total_collection DESC
            """

        columns, rows = load_data(query)       # Executes the dynamically selected query

        data = [                               # Converts the tuples to a list of dictionaries
            dict(zip(columns, row))
            for row in rows
            ]

        st.dataframe(                          # Renders the custom query result on the screen
            data,
            use_container_width=True           # Forces the table to expand to the full width of the app
            )
