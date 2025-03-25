from supabase import create_client


supabase = create_client("https://twrtwgxuwycwmrlndkol.supabase.co",
                         "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InR3cnR3Z3h1d3ljd21ybG5ka29sIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0Mjg5NzA1NiwiZXhwIjoyMDU4NDczMDU2fQ.i3kLKtazvyfEoDot59FmNKfzrNeaUTjwhXnBS61wFwU")

product_table_data = {
    "name": "sfd",
    "category": 'asf',
                "description": '',
                "tagline": '',
                "short_description": '',
}
response = supabase.table("products").insert([product_table_data]).execute()
