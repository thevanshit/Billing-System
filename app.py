import streamlit as st
import io

st.set_page_config(page_title="Restaurant Bill Calculator", page_icon="")

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


def generate_receipt(customer):
    receipt = []
    receipt.append("=" * 30)
    receipt.append("     RESTAURANT BILL RECEIPT")
    receipt.append("=" * 30)
    receipt.append(f"Customer: {customer['name']}")
    receipt.append("-" * 30)
    receipt.append("ITEMS:")
    
    for item, qty, price in customer["items"]:
        receipt.append(f"  {item} x{qty} = ₹{price}")
    
    receipt.append("-" * 30)
    receipt.append(f"Subtotal: ₹{customer['subtotal']}")
    receipt.append("=" * 30)
    return "\n".join(receipt)


st.title("Restaurant Bill Calculator")

with st.sidebar:
    st.header("Settings")
    tax_rate = st.slider("Tax (%)", 0, 20, 10)
    tip_rate = st.slider("Tip (%)", 0, 20, 5)
    if st.button("Reset All"):
        st.session_state.customers = []
        st.session_state.customer_count = 0
        st.rerun()

st.header("Menu")
col1, col2 = st.columns(2)
with col1:
    st.subheader("Food Items")
    for item, price in MENU["Food"].items():
        st.write(f"{item}: Rs.{price}")
with col2:
    st.subheader("Drinks")
    for item, price in MENU["Drinks"].items():
        st.write(f"{item}: Rs.{price}")

st.divider()

st.header("Add Customer Order")

with st.form(key="customer_form"):
    customer_name = st.text_input("Customer Name", value=f"Customer {st.session_state.customer_count + 1}")
    
    st.write("Select Quantity:")
    
    food_quantities = {}
    for item, price in MENU["Food"].items():
        food_quantities[item] = st.number_input(f"{item} (Rs.{price})", min_value=0, max_value=10, key=f"food_{item}", value=0)
    
    drink_quantities = {}
    for item, price in MENU["Drinks"].items():
        drink_quantities[item] = st.number_input(f"{item} (Rs.{price})", min_value=0, max_value=10, key=f"drink_{item}", value=0)
    
    submit_button = st.form_submit_button(label="Add to Bill")

if submit_button:
    total_items = sum(food_quantities.values()) + sum(drink_quantities.values())
    
    if total_items == 0:
        st.warning("Please select at least one item!")
    else:
        items_list = []
        food_total = 0
        drink_total = 0
        
        for item, qty in food_quantities.items():
            if qty > 0:
                price = MENU["Food"][item] * qty
                items_list.append((item, qty, price))
                food_total += price
        
        for item, qty in drink_quantities.items():
            if qty > 0:
                price = MENU["Drinks"][item] * qty
                items_list.append((item, qty, price))
                drink_total += price
        
        customer_bill = {
            "name": customer_name,
            "items": items_list,
            "food_total": food_total,
            "drink_total": drink_total,
            "subtotal": food_total + drink_total
        }
        
        st.session_state.customers.append(customer_bill)
        st.session_state.customer_count += 1
        st.success(f"Added {customer_name}'s order!")
        st.rerun()

st.divider()

if st.session_state.customers:
    st.header("Bill Summary")
    
    total_subtotal = 0
    for i, customer in enumerate(st.session_state.customers):
        with st.expander(f"{customer['name']} - Rs.{customer['subtotal']}", expanded=True):
            st.write("Items Ordered:")
            for item, qty, price in customer["items"]:
                st.write(f"  {item} x{qty} = Rs.{price}")
            
            st.write(f"Food Total: Rs.{customer['food_total']}")
            st.write(f"Drinks Total: Rs.{customer['drink_total']}")
            st.write(f"**Subtotal: Rs.{customer['subtotal']}**")
            
            col1, col2 = st.columns(2)
            with col1:
                receipt_text = generate_receipt(customer)
                st.download_button(
                    label="Download Receipt",
                    data=receipt_text,
                    file_name=f"receipt_{customer['name'].replace(' ', '_')}.txt",
                    key=f"receipt_{i}"
                )
            with col2:
                if st.button(f"Remove {customer['name']}", key=f"remove_{i}"):
                    st.session_state.customers.pop(i)
                    st.rerun()
        
        total_subtotal += customer["subtotal"]
    
    tax_amount = total_subtotal * (tax_rate / 100)
    tip_amount = total_subtotal * (tip_rate / 100)
    grand_total = total_subtotal + tax_amount + tip_amount
    
    st.divider()
    
    st.subheader("Final Bill")
    bill_col1, bill_col2 = st.columns(2)
    with bill_col1:
        st.write(f"Subtotal: Rs.{total_subtotal}")
        st.write(f"Tax ({tax_rate}%): Rs.{tax_amount:.2f}")
        st.write(f"Tip ({tip_rate}%): Rs.{tip_amount:.2f}")
    with bill_col2:
        st.markdown(f"### Grand Total: Rs.{grand_total:.2f}")
    
    if st.button("Confirm & Generate Final Receipt"):
        final_receipt = []
        final_receipt.append("=" * 35)
        final_receipt.append("      FINAL RESTAURANT BILL")
        final_receipt.append("=" * 35)
        
        for customer in st.session_state.customers:
            final_receipt.append(f"\n{customer['name']}:")
            for item, qty, price in customer["items"]:
                final_receipt.append(f"  {item} x{qty} = Rs.{price}")
            final_receipt.append(f"  Subtotal: Rs.{customer['subtotal']}")
        
        final_receipt.append("-" * 35)
        final_receipt.append(f"Subtotal: Rs.{total_subtotal}")
        final_receipt.append(f"Tax ({tax_rate}%): Rs.{tax_amount:.2f}")
        final_receipt.append(f"Tip ({tip_rate}%): Rs.{tip_amount:.2f}")
        final_receipt.append("=" * 35)
        final_receipt.append(f"GRAND TOTAL: Rs.{grand_total:.2f}")
        final_receipt.append("=" * 35)
        
        final_receipt_text = "\n".join(final_receipt)
        st.download_button(
            label="Download Final Receipt",
            data=final_receipt_text,
            file_name="final_bill.txt",
            key="final_receipt"
        )
        st.balloons()
        st.success("Receipt generated successfully!")
else:
    st.info("No customers added yet. Add a customer above to start calculating the bill.")
