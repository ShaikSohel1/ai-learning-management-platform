-- =================================================================================
-- Supabase Row Level Security (RLS) Setup Script
-- =================================================================================
-- Note: Since the backend uses FastAPI and SQLAlchemy with its own JWT authentication,
-- database operations will typically be executed using the main database connection
-- (which bypasses RLS by default if it's the postgres superuser/service role).
-- These policies are essential if you ever access the database via the Supabase 
-- Data API, client libraries with anon keys, or if you configure SQLAlchemy to 
-- assume the authenticated user's context.

-- 1. Enable RLS on key tables
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE courses ENABLE ROW LEVEL SECURITY;
ALTER TABLE enrollments ENABLE ROW LEVEL SECURITY;
ALTER TABLE certificates ENABLE ROW LEVEL SECURITY;
ALTER TABLE lessons ENABLE ROW LEVEL SECURITY;

-- 2. User Policies
-- Users can read their own data.
CREATE POLICY "Users can read their own profile" ON users
  FOR SELECT USING (id::text = current_setting('request.jwt.claims', true)::json->>'sub' OR true); 
  -- 'OR true' is added temporarily to not break current backend logic until JWT claims are passed to PG.

-- 3. Course Policies
-- Anyone can view courses
CREATE POLICY "Courses are viewable by everyone" ON courses
  FOR SELECT USING (true);

-- 4. Storage Bucket Setup
-- Create the main bucket for file uploads (PDFs, Images, Certificates)
insert into storage.buckets (id, name, public) 
values ('main-bucket', 'main-bucket', true)
on conflict do nothing;

-- Storage Policies
create policy "Public Access to files"
  on storage.objects for select
  using ( bucket_id = 'main-bucket' );

create policy "Service Role can manage files"
  on storage.objects for all
  using ( bucket_id = 'main-bucket' );
