from flask import Flask, render_template, request, redirect, url_for, session

# Initialize the app
app = Flask(__name__)
app.secret_key = "supersecretkey"  # Needed for sessions (to store cart data)

# Dummy data: cafes and menus (each item has a name and price in rupees)
cafes = {
    "Cafe One": [
        {"name": "Coffee", "price": 30},
        {"name": "Sandwich", "price": 50},
        {"name": "Muffin", "price": 40},
    ],
    "Cafe Two": [
        {"name": "Tea", "price": 20},
        {"name": "Burger", "price": 60},
        {"name": "Fries", "price": 40},
    ],
    "Cafe Three": [
        {"name": "Pizza", "price": 80},
        {"name": "Pasta", "price": 70},
        {"name": "Salad", "price": 50},
    ],
    "Hot Chips": [
        {"name": "Hot Chips", "price": 50},
        {"name": "Peri Peri Fries", "price": 60},
        {"name": "Cheese Dip", "price": 30},
    ],
}

@app.route("/")
def home():
    """Show list of cafes"""
    return render_template("index.html", cafes=cafes)

@app.route("/cafe/<name>")
def show_cafe(name):
    """Show menu of a cafe"""
    menu = cafes.get(name, [])
    return render_template("cafe.html", cafe=name, menu=menu)

@app.route("/add_to_cart/<cafe>/<item>")
def add_to_cart(cafe, item):
    """Add an item to the cart (stored in session)"""
    cart = session.get("cart", [])
    menu = cafes.get(cafe, [])
    price = next((i["price"] for i in menu if i["name"] == item), 0)
    cart.append({"cafe": cafe, "item": item, "price": price})
    session["cart"] = cart
    return redirect(url_for("view_cart"))

@app.route("/cart")
def view_cart():
    """View items in cart"""
    cart = session.get("cart", [])
    return render_template("cart.html", cart=cart)

@app.route("/checkout")
def checkout():
    """Clear the cart (no real payment)"""
    session["cart"] = []
    return "Thanks for ordering! Your cart is now empty."

if __name__ == "__main__":
    app.run(debug=True)
