from supabase import create_client, Client

url: str = "https://xlizrmqypynlvwwfbogr.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhsaXpybXF5cHlubHZ3d2Zib2dyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDM2MzA0NDcsImV4cCI6MjA1OTIwNjQ0N30.EA6WsCdfbZnb8scxhboXPjmaVh_2HqLHHWdNulwDVjA"
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
