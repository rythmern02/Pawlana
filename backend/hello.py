from supabase import create_client, Client

# Your Supabase project URL and anon/public key (from Supabase project settings)
SUPABASE_URL="https://zoojytnwqnyftxsuvnar.supabase.co"
SUPABASE_ANON_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inpvb2p5dG53cW55ZnR4c3V2bmFyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTI2NzY0OTgsImV4cCI6MjA2ODI1MjQ5OH0.umQeO8Mod8LjaAD_36QXZGVowWlN1u_rF7Fv3Fu8rHQ"
# Initialize client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

# Sign in with email/password
response = supabase.auth.sign_in_with_password({
    "email": "rythmenagrani@gmail.com",
    "password": "rythmern"
})

# Access the JWT token
access_token = response.session.access_token
print("JWT:", access_token)
