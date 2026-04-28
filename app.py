import streamlit as st

st.title("🍔 Restaurant Ordering App")

menu = {
    "burger": 10,
    "pizza": 15,
    "fries": 5,
    "cola": 3
}

st.write("### Menu")
for item, price in menu.items():
    st.write(f"{item} - ${price}")

user_input = st.text_input("Type your order (example: 2 burgers and 1 cola)")

def parse_order(text):
    items = ["burger", "pizza", "fries", "cola"]
    order = {}

    words = text.lower().split()

    for i, word in enumerate(words):
        if word.isdigit():
            qty = int(word)
            if i + 1 < len(words):
                item = words[i + 1].rstrip("s")
                if item in items:
                    order[item] = order.get(item, 0) + qty

    for item in items:
        if item in text.lower():
            if item not in order:
                order[item] = 1

    return order

if user_input:
    order = parse_order(user_input)

    if order:
        st.write("### Your Order")
        total = 0

        for item, qty in order.items():
            st.write(f"{item} x {qty}")
            total += menu[item] * qty

        st.write(f"## Total: ${total}")

        if st.button("Confirm Order"):
            st.success("Order placed successfully 🎉")
    else:
        st.error("Could not understand order")