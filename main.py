import streamlit as st
from supabase import create_client

import utils

st.title("🛒 Product Admin")

# --- Setup Supabase ---
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

# --- Login State ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = True

# --- Login Form ---
if not st.session_state.logged_in:
    with st.form("login_form"):
        pwd = st.text_input("Enter admin password:", type="password")
        login_btn = st.form_submit_button("Login")

        if login_btn:
            if pwd == st.secrets["ADMIN_PASSWORD"]:
                st.success("✅ Logged in!")
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Incorrect password. Try again.")
else:
    st.subheader("Add a New Product")

    # --- Dynamic Feature Count ---
    st.markdown("### 🔧 Product Features")
    feature_count = st.slider("How many features?",
                              min_value=1, max_value=15, value=3)

    if "features" not in st.session_state:
        st.session_state.features = [
            {"name": "", "value": ""} for _ in range(feature_count)]
    elif len(st.session_state.features) != feature_count:
        current = st.session_state.features
        st.session_state.features = current[:feature_count] + [
            {"name": "", "value": ""}] * (feature_count - len(current))

    # --- Dynamic Specification Count ---
    st.markdown("### 📐 Product Specifications")
    spec_count = st.slider("How many specifications?",
                           min_value=1, max_value=15, value=3)

    if "specs" not in st.session_state:
        st.session_state.specs = [{"name": "", "value": ""}
                                  for _ in range(spec_count)]
    elif len(st.session_state.specs) != spec_count:
        current = st.session_state.specs
        st.session_state.specs = current[:spec_count] + \
            [{"name": "", "value": ""}] * (spec_count - len(current))
            
    st.markdown("### 📂 Category Selection")

    categories = [
        "ai service robot",
        "delivery robot",
        "warehouse robot",
        "rental robot",
        "education solution",
        "➕ Add new category..."
    ]

    selected = st.selectbox("Category", categories, key="category_select")

    if selected == "➕ Add new category...":
        new_category = st.text_input("Enter new category", key="custom_category_input")
        category = new_category if new_category else None
    else:
        category = selected

    # --- Product Form ---
    with st.form("product_form"):
        st.markdown("### 📸 Image Thumbnail")

        thumbnails = st.file_uploader(
            "Upload a thumbnail image (image will be compressed to 720p, must be png):",
            type=["png"],
            accept_multiple_files=True
        )

        st.markdown("### 📝 Product Details")

        product_name = st.text_input(
            "Name of product", placeholder="Ex. GreetingBot Mini")
        st.text("Selected Category: " + category if category else "No category selected")
        description = st.text_area(
            "Description", placeholder="Long description of the product")
        tagline = st.text_input(
            "Tagline", placeholder="Short tagline for the product. Ex. Mini But Mighty")
        short_description = st.text_area(
            "Short Description", placeholder="Visible on the product card.")
        description_video = st.text_input(
            "Product Video", placeholder="YouTube embed link")

        # --- Image Gallery Upload ---
        st.markdown("### 📸 Image Gallery")

        description_images = st.file_uploader(
            "Upload product images (you can select multiple), images will be compressed to 720p:",
            type=["jpg", "jpeg", "png"],
            accept_multiple_files=True
        )

        # --- Render Product Features ---
        st.markdown("### 🔧 Product Features")
        for i in range(feature_count):
            f = st.session_state.features[i]
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input(
                    f"Feature {i+1} Name", value=f["name"], key=f"feature_name_{i}")
            with col2:
                value = st.text_input(
                    f"Feature {i+1} Details", value=f["value"], key=f"feature_value_{i}")
            st.session_state.features[i] = {"name": name, "value": value}

        # --- Render Product Specifications ---
        st.markdown("### 📐 Product Specifications")
        for i in range(spec_count):
            s = st.session_state.specs[i]
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input(
                    f"Specification {i+1} Name", value=s["name"], key=f"spec_name_{i}")
            with col2:
                value = st.text_input(
                    f"Specification {i+1} Value", value=s["value"], key=f"spec_value_{i}")
            st.session_state.specs[i] = {"name": name, "value": value}

        # --- Submit Form ---
        submitted = st.form_submit_button("Add Product")

        if submitted:
            product_table_data = {
                # Convert UUID to bigint
                "name": product_name,
                "category": category.lower(),
                "description": description,
                "tagline": tagline,
                "short_description": short_description,
            }

            response = supabase.table("products").insert(
                [product_table_data]).execute()

            product_id = response.data[0]["product_id"]

            # Upload thumbnail image
            thumbnail_urls = utils.upload_thumbnails(thumbnails, supabase)
            media_table_data = []
            for index, thumbnail_url in enumerate(thumbnail_urls):
                media_table_data.append({
                    "product_id": product_id,
                    "media_type": "image",
                    "url": thumbnail_url,
                    "label": "thumbnail" + str(index+1)
                })
            supabase.table("media").insert(media_table_data).execute()

            # Upload description images
            if description_images:
                description_image_urls = utils.upload_description_images(
                    description_images, supabase)
                media_table_data = []
                for index, image_url in enumerate(description_image_urls):
                    media_table_data.append({
                        "product_id": product_id,
                        "media_type": "image",
                        "url": image_url,
                        "label": "description" + str(index+1)
                    })
                supabase.table("media").insert(media_table_data).execute()

            # Upload product video
            if description_video:
                media_table_data = {
                    "product_id": product_id,
                    "media_type": "video",
                    "url": description_video,
                    "label": "description_video"
                }
                supabase.table("media").insert([media_table_data]).execute()

            # Upload product features
            if st.session_state.features:
                feature_table_data = []
                for feature in st.session_state.features:
                    feature_table_data.append({
                        "product_id": product_id,
                        "feature_name": feature["name"],
                        "feature_description": feature["value"]
                    })
                supabase.table("features").insert(
                    feature_table_data).execute()

            # Upload product specifications
            if st.session_state.specs:
                spec_table_data = []
                for spec in st.session_state.specs:
                    spec_table_data.append({
                        "product_id": product_id,
                        "spec_name": spec["name"],
                        "spec_value": spec["value"]
                    })
                supabase.table("product_specifications").insert(
                    spec_table_data).execute()

            st.success("🎉 Product added!")
            st.write("Product data:", product_table_data)
