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
list_of_course_codes = []

while True:
    response = supabase.table("courses_new").select("course_code").range(offset, offset + limit - 1).execute()
    data = response.data
    for row in data:
        course_code = row["course_code"]
        if course_code not in list_of_course_codes:
            list_of_course_codes.append(course_code)
    if not data:  # Break when no more rows are returned
        break
    all_data.extend(data)
    offset += limit

print(list_of_course_codes)
print(f"Total rows fetched: {len(all_data)}")
