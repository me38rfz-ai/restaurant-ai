import streamlit as st
import sqlite3
from datetime import datetime

# =========================
# DATABASE
# =========================
conn = sqlite3.connect("orders.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    items TEXT,
    total REAL,
    status TEXT,
    time TEXT
)
""")
conn.commit()

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="FastBite Ultimate", layout="wide")

# =========================
# STYLE
# =========================
st.markdown("""
<style>
.main { background-color: #f5f5f5; }
.title { color: #d62300; font-size: 40px; font-weight: bold; }
.stButton>button {
    background-color: #ffcc00;
    color: black;
    border-radius: 8px;
    width: 100%;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='title'>🍔 FastBite Ultimate</div>", unsafe_allow_html=True)

# =========================
# MENU
# =========================
menu = {
    "Burger": {"price": 10, "img": "https://images.unsplash.com/photo-1550547660-d9450f859349"},
    "Cheeseburger": {"price": 12, "img": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd"},
    "Fries": {"price": 5, "img": "https://images.unsplash.com/photo-1541592106381-b31e9677c0e5"},
    "Nuggets": {"price": 8, "img": "https://images.unsplash.com/photo-1606755962773-0e5d1b2d3f3a"},
    "Cola": {"price": 3, "img": "https://images.unsplash.com/photo-1581636625402-29b2a704ef13"},
    "Water": {"price": 1, "img": "https://images.unsplash.com/photo-1502741338009-cac2772e18bc"}
}

# =========================
# CART
# =========================
if "cart" not in st.session_state:
    st.session_state.cart = {}

# =========================
# NAVIGATION
# =========================
page = st.sidebar.selectbox("Navigation", ["🍔 Order Food", "📊 Admin Dashboard"])

# =========================
# ORDER PAGE
# =========================
if page == "🍔 Order Food":

    st.header("Menu")

    # SEARCH
    search = st.text_input("🔍 Search food")

    filtered_menu = {
        item: data for item, data in menu.items()
        if search.lower() in item.lower()
    } if search else menu

    # DISPLAY MENU
    cols = st.columns(3)
    i = 0

    for item, data in filtered_menu.items():
        with cols[i % 3]:
            st.image(data["img"], use_container_width=True)
            st.write(f"**{item}** - ${data['price']}")

            col1, col2 = st.columns(2)

            with col1:
                if st.button("+", key=f"add_{item}"):
                    st.session_state.cart[item] = st.session_state.cart.get(item, 0) + 1

            with col2:
                if st.button("-", key=f"remove_{item}"):
                    if item in st.session_state.cart:
                        st.session_state.cart[item] -= 1
                        if st.session_state.cart[item] <= 0:
                            del st.session_state.cart[item]

        i += 1

    # CART DISPLAY
    st.write("---")
    st.subheader("🛒 Your Order")

    total = 0

    if st.session_state.cart:
        for item, qty in st.session_state.cart.items():
            price = menu[item]["price"]
            st.write(f"{item} x {qty} = ${price * qty}")
            total += price * qty

        st.write(f"### 💰 Total: ${total}")

        # BETTER PAYMENT FLOW
        st.info("1️⃣ Click below to pay")
        st.markdown("[💳 Pay Now](https://buy.stripe.com/test_4gM4gA6Yvg960VVathf7i00)")
        st.info("2️⃣ After payment, click confirm")

        # CONFIRM ORDER
        if st.button("✅ Confirm Order"):
            c.execute(
                "INSERT INTO orders (items, total, status, time) VALUES (?, ?, ?, ?)",
                (str(st.session_state.cart), total, "Paid (manual confirm)", str(datetime.now()))
            )
            conn.commit()

            st.success("🎉 Order saved successfully!")
            st.session_state.cart = {}

    else:
        st.write("Cart is empty")

# =========================
# ADMIN DASHBOARD
# =========================
elif page == "📊 Admin Dashboard":

    st.header("Admin Dashboard")

    orders = c.execute("SELECT * FROM orders").fetchall()

    if orders:
        for order in orders:
            st.write(f"### Order #{order[0]}")
            st.write(f"Items: {order[1]}")
            st.write(f"Total: ${order[2]}")
            st.write(f"Status: {order[3]}")
            st.write(f"Time: {order[4]}")

            # MARK AS DONE BUTTON
            if st.button("Mark as Completed", key=f"done_{order[0]}"):
                c.execute("UPDATE orders SET status = ? WHERE id = ?", ("Completed", order[0]))
                conn.commit()
                st.success(f"Order {order[0]} completed!")

            st.write("---")
    else:
        st.write("No orders yet")