from flask import Flask, render_template, url_for, redirect, request, session, flash
import mysql.connector
from mysql.connector import Error
from functools import wraps

from utils.data_cleaning import clean_sales_data

# ============================================
# FLASK APPLICATION
# ============================================

app = Flask(__name__)

# Secret key for sessions
app.secret_key = "sales_dashboard_secret_key"


# ============================================
# MYSQL DATABASE CONFIGURATION
# ============================================

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "root",
    "database": "sales_analytics_db"
}


# ============================================
# DATABASE CONNECTION
# ============================================

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=DB_CONFIG["host"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            database=DB_CONFIG["database"]
        )

        return connection

    except Error as e:
        print("Database connection error:", e)
        return None

# ============================================
# LOGIN REQUIRED DECORATOR
# ============================================

def login_required(function):

    @wraps(function)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))

        return function(*args, **kwargs)
    
    return wrapper  



# ============================================
# HOME / DASHBOARD
# ============================================

@app.route("/")
@login_required
def dashboard():

    connection = get_db_connection()

    if connection is None:
        return "Database connection failed. "
    
    cursor = connection.cursor(dictionary=True)

    #Total sales revenue
    cursor.execute("""SELECT COALESCE(SUM(total_amount), 0) as total_revenue FROM sales""")

    total_revenue = cursor.fetchone()["total_revenue"]


    # TOTAL ORDERS
    cursor.execute("""SELECT COUNT(*) as total_orders FROM sales""")

    total_orders = cursor.fetchone()["total_orders"]

    #TOTAL CUSTOMERS

    cursor.execute("""SELECT COUNT(*) AS total_customers FROM customers""")

    total_customers = cursor.fetchone()["total_customers"]

     # Total products
    cursor.execute("""SELECT COUNT(*) AS total_products FROM products""")

    total_products = cursor.fetchone()["total_products"]

    cursor.close()
    connection.close()

    return render_template(
        "dashboard.html",
        total_revenue = total_revenue,
        total_orders = total_orders,
        total_customers = total_customers,
        total_products = total_products
    )

# ============================================
# LOGIN
# ============================================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        connection = get_db_connection()

        if connection is None:
            flash("Database connection failed. Please try again .", "error")
            return redirect(url_for("login"))

        cursor = connection.cursor(dictionary=True)

        cursor.execute("""SELECT * FROM users WHERE username = %s AND password = %s""", (username, password))

        user = cursor.fetchone()

        cursor.close()
        connection.close()

        if user:

            session["user_id"] = user["id"]
            session["username"] = user["username"]
            session["role"] = user["role"]

            return redirect(url_for("dashboard"))

        else:
            flash("Invalid username or password", "error")

            return redirect(url_for("login"))
            
    return render_template("login.html")



# ============================================
# LOGOUT
# ============================================


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# ============================================
# SALES PAGE
# ============================================

@app.route("/sales")
@login_required
def sales():

    connection = get_db_connection()

    if connection is None:
        return "database connection failed"

    cursor = connection.cursor(dictionary=True)

    cursor.execute("""SELECT sales.sale_id, sales.sale_date, customers.customer_name, products.product_name, products.category, sales.quantity,
    sales.unit_price, sales.total_amount, sales.payment_method FROM sales LEFT JOIN customers ON sales.customer_id = customers.customer_id LEFT JOIN products ON sales.product_id = products.product_id 
    ORDER BY sales.sale_date DESC""")

    sales_data = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template("sales.html", sales=sales_data)



# ============================================
# PRODUCTS PAGE
# ============================================

@app.route("/products")
@login_required
def products():

    connection = get_db_connection()

    if connection is None:
        return "Database connection failed."

    cursor = connection.cursor(dictionary=True)

    cursor.execute("""SELECT * FROM products ORDER BY product_id DESC""")

    products_data = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template("products.html", products=products_data)




# ============================================
# CUSTOMERS PAGE
# ============================================

@app.route("/customers")
@login_required
def customers():

    connection = get_db_connection()

    if connection is None:
        return "Database connection failed."

    cursor = connection.cursor(dictionary=True)

    cursor.execute("""SELECT * FROM customers ORDER BY customer_id DESC""")

    customers_data = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template("customers.html", customers=customers_data)



# ============================================
# REPORTS PAGE
# ============================================

@app.route("/reports")
@login_required
def reports():
    return render_template("reports.html")


# ============================================
# UPLOAD PAGE
# ============================================

@app.route("/upload", methods=["GET", "POST"])
@login_required
def upload():

    if request.method == "POST":

        if "sales_file" not in request.files:
            flash("No file selected.", "error")
            return redirect(url_for("upload"))

        file = request.files["sales_file"]

        if file.filename == "":
            flash("Please select a file.", "error")
            return redirect(url_for("upload"))

        file_path = "uploads/" + file.filename
        file.save(file_path)

        try:

            df = clean_sales_data(file_path)

            print("Cleaned Sales Data:")
            print(df)

            flash(
                "File uploaded and cleaned successfully.",
                "success"
            )

            return render_template(
                "upload.html",
                data=df.to_dict(orient="records")
            )

        except Exception as e:

            flash(
                f"Error processing file: {e}",
                "error"
            )

            return redirect(url_for("upload"))

    return render_template("upload.html")







if __name__== "__main__":
    app.run(debug=True)
