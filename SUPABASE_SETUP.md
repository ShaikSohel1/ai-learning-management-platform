# Supabase Setup Guide

This document outlines the step-by-step process for configuring your Supabase project for the AI Learning Management Platform.

## 1. Create a Supabase Project
1. Go to the [Supabase Dashboard](https://app.supabase.com/) and create a new project.
2. Store your Database Password securely.
3. Wait for the database provisioning to complete.

## 2. Obtain Credentials
1. Go to **Project Settings -> Database**.
2. Under "Connection string", select "URI" and copy the URL. It should look like:
   `postgresql://postgres.[PROJECT_REF]:[PASSWORD]@aws-0-[REGION].pooler.supabase.com:6543/postgres`
3. Go to **Project Settings -> API**.
4. Copy the `anon` `public` key and the `service_role` `secret` key.
5. Add these credentials to your `backend/.env` file:
   ```env
   DATABASE_URL=your_database_url_here
   SUPABASE_URL=https://[PROJECT_REF].supabase.co
   SUPABASE_ANON_KEY=your_anon_key
   SUPABASE_SERVICE_ROLE_KEY=your_service_role_key
   ```

## 3. Storage Configuration
1. Open the Supabase SQL Editor in your dashboard.
2. Open the `backend/supabase_setup.sql` file from your project.
3. Copy the contents and execute them in the Supabase SQL Editor.
4. This script automatically:
   - Creates the `main-bucket` storage bucket.
   - Configures public read access policies.
   - Configures authenticated write access policies.

## 4. Row Level Security (RLS)
The `supabase_setup.sql` script also enables RLS on your core tables. Since the backend interacts with the database via SQLAlchemy using a service/superuser role, RLS policies act as a safety net against direct API access and do not interfere with your FastAPI logic.

## 5. Verify the Connection
Start your FastAPI backend locally. If it starts without connection errors, your setup is complete!
