import os
import json
import requests
import sys
import argparse

def execute_supabase_sql(sql_commands, supabase_project_id, supabase_token):
    """
    Execute SQL commands on Supabase using the REST API.
    
    Args:
        sql_commands: SQL commands to execute
        supabase_project_id: Supabase project ID
        supabase_token: Supabase token (anon key)
        
    Returns:
        Dict with results or error
    """
    url = f"https://api.supabase.com/v1/projects/{supabase_project_id}/database/query"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {supabase_token}"
    }

    payload = {
        "query": sql_commands
    }
    
    # Create JSON payload once
    payload_json = json.dumps(payload)
    print(f"URL: {url}")
    print(f"Headers: {headers}")
    print(f"Payload (first 100 chars): {payload_json[:100]}...")
    
    try:
        response = requests.post(url, headers=headers, data=payload_json)
        
        print(f"Response status code: {response.status_code}")
        if response.status_code >= 400:
            print(f"Error response: {response.text}")
            return {"error": f"HTTP error {response.status_code}: {response.text}"}
            
        response.raise_for_status()
        sql_result = response.json()
        return sql_result

    except requests.exceptions.RequestException as e:
        print(f"Request exception: {str(e)}")
        return {"error": str(e)}

def main():
    parser = argparse.ArgumentParser(description='Test Supabase SQL execution')
    parser.add_argument('--use-migration', action='store_true', help='Use the full migration SQL')
    parser.add_argument('--simple-query', action='store_true', help='Use a simple SELECT query')
    args = parser.parse_args()
    
    # Set Supabase credentials
    supabase_project_id = "ijdgpxhosdgcwbmvqmps"  # Replace with your project ID
    supabase_token = "sbp_79808f56e9a7d4fe8d706f12dd5bbf4c2d6095f5"  # Replace with your token 
    
    if args.simple_query:
        # Use a simple SELECT query that won't cause conflicts
        sql_content = "SELECT current_timestamp, current_database();"
        print(f"Using simple test query: {sql_content}")
    else:
        # Read the SQL file
        sql_file_path = "todo-list/migrations/001_auth_setup.sql"
        
        if not os.path.exists(sql_file_path):
            print(f"Error: SQL file not found at {sql_file_path}")
            return
        
        with open(sql_file_path, 'r', encoding='utf-8') as f:
            sql_content = f.read()
        
        print(f"Read SQL file: {sql_file_path}")
        print(f"SQL content length: {len(sql_content)} characters")
    
    # Execute SQL
    print("\nExecuting SQL...")
    result = execute_supabase_sql(sql_content, supabase_project_id, supabase_token)
    
    # Print result
    print("\nResult:")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main() 