from flask import Flask, render_template_string, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "supersecret"  # session management

# In-memory storage (reset on restart)
users = {"admin": "password"}  # username:password
products = [
    {"id": 1, "name": "Laptop", "price": 700},
    {"id": 2, "name": "Phone", "price": 300},
    {"id": 3, "name": "Headphones", "price": 50},
]
cart = {}

# Templates inline
home_html = """
<h1>🛒 Mini E-commerce</h1>
{% if 'user' in session %}
  <p>Welcome, {{ session['user'] }} | <a href="{{ url_for('logout') }}">Logout</a></p>
{% else %}
  <a href="{{ url_for('login') }}">Login</a>
{% endif %}
<h2>Products</h2>
<ul>
  {% for p in products %}
    <li>{{ p.name }} - ${{ p.price }}
      {% if 'user' in session %}
        <a href="{{ url_for('add_to_cart', pid=p.id) }}">[Add to Cart]</a>
      {% endif %}
    </li>
  {% endfor %}
</ul>
<a href="{{ url_for('view_cart') }}">View Cart</a>
"""

login_html = """
<h2>Login</h2>
<form method="post">
  <input type="text" name="username" placeholder="Username" required><br>
  <input type="password" name="password" placeholder="Password" required><br>
  <button type="submit">Login</button>
</form>
<p style="color:red;">{{ error }}</p>
<a href="{{ url_for('home') }}">Back</a>
"""

cart_html = """
<h2>Your Cart</h2>
<ul>
  {% for item in cart.values() %}
    <li>{{ item['name'] }} - ${{ item['price'] }} x {{ item['qty'] }}</li>
  {% else %}
    <li>Cart is empty</li>
  {% endfor %}
</ul>
<a href="{{ url_for('home') }}">⬅ Back to Products</a>
"""

@app.route("/")
def home():
    return render_template_string(home_html, products=products)

@app.route("/login/", methods=["GET", "POST"])
def login():
    error = ""
    if request.method == "POST":
        u, p = request.form["username"], request.form["password"]
        if users.get(u) == p:
            session["user"] = u
            return redirect(url_for("home"))
        else:
            error = "Invalid credentials!"
    return render_template_string(login_html, error=error)

@app.route("/logout/")
def logout():
    session.pop("user", None)
    return redirect(url_for("home"))

@app.route("/cart/")
def view_cart():
    return render_template_string(cart_html, cart=cart)

@app.route("/add/<int:pid>/")
def add_to_cart(pid):
    if "user" not in session:
        return redirect(url_for("login"))
    product = next((p for p in products if p["id"] == pid), None)
    if product:
        if pid not in cart:
            cart[pid] = {"name": product["name"], "price": product["price"], "qty": 1}
        else:
            cart[pid]["qty"] += 1
    return redirect(url_for("view_cart"))

if __name__ == "__main__":
    app.run(debug=True)
