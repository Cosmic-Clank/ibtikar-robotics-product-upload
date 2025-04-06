import streamlit as st
from supabase import create_client

# --- Supabase Setup ---
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

st.title("🗑️ Delete Products")

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Please log in first from the main page.")
    st.stop()


# --- Fetch Products ---
response = supabase.table("products").select("product_id,name").execute()

if not response.data:
    st.warning("No products found.")
    st.stop()

products = response.data

# --- Select a product to delete ---
product_options = {p["name"]: p["product_id"] for p in products}
selected_name = st.selectbox("Select a product to delete", list(product_options.keys()))

if selected_name:
    product_id = product_options[selected_name]

    # Show confirmation
    if st.button(f"🚨 Delete '{selected_name}'"):
        try:

            # Delete the main product
            supabase.table("products").delete().eq("product_id", product_id).execute()
            
            st.success(f"Successfully deleted '{selected_name}' and all related data.")
            st.rerun()
        except Exception as e:
            st.error(f"Error deleting product: {str(e)}")
