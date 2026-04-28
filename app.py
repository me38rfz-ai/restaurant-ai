import streamlit as st

st.set_page_config(page_title="Restaurant AI", layout="centered")

st.title("🍔 Smart Restaurant Ordering System")

# MENU
menu = {
    "🍔 Burgers": {
        "burger": 10,
        "cheeseburger": 12
    },
    "🍟 Sides": {
        "fries": 5,
        "nuggets": 8
    },
    "🥤 Drinks": {
        "cola": 3,
        "water": 1
    }
}

# CART
if "cart" not in st.session_state:
    st.session_state.cart = {}

st.write("## 🍽️ Menu")

# SHOW MENU WITH BUTTONS
for category, items in menu.items():
    st.subheader(category)

    for item, price in items.items():
        col1, col2 = st.columns([3, 1])

        with col1:
            st.write(f"{item} - ${price}")

        with col2:
            if st.button(f"Add {item}", key=item):
                st.session_state.cart[item] = st.session_state.cart.get(item, 0) + 1

# SHOW CART
st.write("---")
st.write("## 🛒 Your Order")

total = 0

if st.session_state.cart:
    for item, qty in st.session_state.cart.items():
        price = None

        # find price in menu
        for category in menu.values():
            if item in category:
                price = category[item]

        st.write(f"{item} x {qty} = ${price * qty}")
        total += price * qty

    st.write(f"### 💰 Total: ${total}")

    if st.button("✅ Checkout"):
        st.success("🎉 Order placed successfully!")

else:
    st.write("Your cart is empty")