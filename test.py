from supabase import create_client, Client
import json

with open("config.json", "r") as file:
    config = json.load(file)

url = config["SUPABASE_URL"]
key = config["SUPABASE_KEY"]
supabase: Client = create_client(url, key)
offset = 0
limit = 1000
all_data = []

while True:
    response = supabase.table("courses_new").select("course_code").range(offset, offset + limit - 1).execute()
    data = response.data
    if not data:  # Break when no more rows are returned
        break
    all_data.extend(data)
    offset += limit

print(all_data)
print(f"Total rows fetched: {len(all_data)}")
