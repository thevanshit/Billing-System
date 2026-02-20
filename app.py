import streamlit as st

st.set_page_config(page_title="Restaurant Bill Calculator", page_icon="🍽️")

MENU = {
    "Food": {
        "Pizza": 599,
        "Burger": 299,
        "Pasta": 499
    },
    "Drinks": {
        "Coke": 99,
        "Coffee": 149,
        "Tea": 79
    }
}

if "customers" not in st.session_state:
    st.session_state.customers = []

if "customer_count" not in st.session_state:
    st.session_state.customer_count = 0

st.title("🍽️ Restaurant Bill Calculator")

with st.sidebar:
    st.header("Settings")
    tax_rate = st.slider("Tax (%)", 0, 20, 10)
    tip_rate = st.slider("Tip (%)", 0, 20, 5)
    if st.button("Reset All"):
        st.session_state.customers = []
        st.session_state.customer_count = 0
        st.rerun()

st.header("📋 Menu")
col1, col2 = st.columns(2)
with col1:
    st.subheader("Food Items")
    for item, price in MENU["Food"].items():
        st.write(f"• {item}: ₹{price}")
with col2:
    st.subheader("Drinks")
    for item, price in MENU["Drinks"].items():
        st.write(f"• {item}: ₹{price}")

st.divider()

st.header("👥 Add Customer Order")

with st.form(key="customer_form"):
    customer_name = st.text_input(f"Customer Name", value=f"Customer {st.session_state.customer_count + 1}")
    
    food_items = st.multiselect(
        "Select Food Items",
        options=list(MENU["Food"].keys()),
        key=f"food_{st.session_state.customer_count}"
    )
    
    drink_items = st.multiselect(
        "Select Drinks",
        options=list(MENU["Drinks"].keys()),
        key=f"drink_{st.session_state.customer_count}"
    )
    
    submit_button = st.form_submit_button(label="Add to Bill")

if submit_button:
    if not food_items and not drink_items:
        st.warning("Please select at least one item!")
    else:
        customer_bill = {
            "name": customer_name,
            "food": food_items,
            "drinks": drink_items,
            "food_total": sum(MENU["Food"][item] for item in food_items),
            "drink_total": sum(MENU["Drinks"][item] for item in drink_items)
        }
        customer_bill["subtotal"] = customer_bill["food_total"] + customer_bill["drink_total"]
        st.session_state.customers.append(customer_bill)
        st.session_state.customer_count += 1
        st.success(f"Added {customer_name}'s order!")
        st.rerun()

st.divider()

if st.session_state.customers:
    st.header("🧾 Bill Summary")
    
    total_subtotal = 0
    for i, customer in enumerate(st.session_state.customers):
        with st.expander(f"{customer['name']} - ₹{customer['subtotal']}", expanded=True):
            col1, col2, col3 = st.columns(3)
            with col1:
                st.write("**Food:**")
                for item in customer["food"]:
                    st.write(f"  {item}: ₹{MENU['Food'][item]}")
            with col2:
                st.write("**Drinks:**")
                for item in customer["drinks"]:
                    st.write(f"  {item}: ₹{MENU['Drinks'][item]}")
            with col3:
                st.write("**Subtotal:**")
                st.write(f"Food: ₹{customer['food_total']}")
                st.write(f"Drinks: ₹{customer['drink_total']}")
                st.write(f"**Total: ₹{customer['subtotal']}**")
            
            if st.button(f"Remove {customer['name']}", key=f"remove_{i}"):
                st.session_state.customers.pop(i)
                st.rerun()
        
        total_subtotal += customer["subtotal"]
    
    tax_amount = total_subtotal * (tax_rate / 100)
    tip_amount = total_subtotal * (tip_rate / 100)
    grand_total = total_subtotal + tax_amount + tip_amount
    
    st.divider()
    
    st.subheader("💰 Final Bill")
    bill_col1, bill_col2 = st.columns(2)
    with bill_col1:
        st.write(f"Subtotal: ₹{total_subtotal}")
        st.write(f"Tax ({tax_rate}%): ₹{tax_amount:.2f}")
        st.write(f"Tip ({tip_rate}%): ₹{tip_amount:.2f}")
    with bill_col2:
        st.markdown(f"### Grand Total: ₹{grand_total:.2f}")
    
    if st.button("Confirm & Generate Receipt"):
        st.balloons()
        st.success("Receipt generated successfully!")
else:
    st.info("No customers added yet. Add a customer above to start calculating the bill.")
