from supabase import create_client, PostgrestAPIResponse
from dotenv import load_dotenv
from datetime import date
import os

load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

supabase = create_client(url, key)

def create_user(name: str, email:str) -> PostgrestAPIResponse:
    '''
    To create a new user. (Inside `users` table)
    
    eg:
    create_user("Hadin Abdul Hameed", "hadinabdulhameed@gmail.com")
    '''
    data = {
        "name": name,
        "email": email,
    }

    response = supabase.table("users").insert(data).execute()
    return response

def start_workday(notes: str='regular') -> PostgrestAPIResponse:
    '''
    To start workday. (Inside `workdays` table)

    eg:
    start_workday()
    '''
    data = {
        "notes": notes,
    }

    response = supabase.table("workdays").insert(data).execute()
    return response

def stop_workday(notes: str='regular') -> PostgrestAPIResponse:
    '''
    To stop workday. (Inside `workdays` table)

    eg:
    stop_workday()
    '''
    data = {
        "notes": notes,
    }

    response = supabase.table("workdays").update(data).eq("workday_id", str(date.today())).execute()
    return response

def mark_entry(user_id: str) -> PostgrestAPIResponse:
    '''
    To mark the entry of user. (Inside `entry_logs` table, with `entry=True`)

    eg:
    mark_entry("aad1a0aa-dea4-a1ae-4a1a-aaeaaaa10aaa")
    '''
    data = {
        "user_id": user_id,
        "entry": True,
    }

    response = supabase.table("entry_logs").insert(data).execute()
    return response

def mark_exit(user_id: str) -> PostgrestAPIResponse:
    '''
    To mark the exit of the user. (Inside `entry_logs`, with `entry=False`)

    eg:
    mark_exit("aad1a0aa-dea4-a1ae-4a1a-aaeaaaa10aaa")
    '''
    data = {
        "user_id": user_id,
        "entry": False,
    }

    response = supabase.table("entry_logs").insert(data).execute()
    return response

def mark_task(user_id: str, task: str, tags: str="") -> PostgrestAPIResponse:
    '''
    To mark task, which is done. (Inside `task_logs`)

    eg:
    mark_task("aad1a0aa-dea4-a1ae-4a1a-aaeaaaa10aaa", "Made Database", "{databse, sql, python}")
    '''
    data = {
        "name": task,
        "user_id": user_id,
        "tags": tags,
    }

    response = supabase.table("task_logs").insert(data).execute()
    return response

def get_table_data(table_name: str, **filters) -> PostgrestAPIResponse:
    '''
    To get datas of any table, where key=value.

    eg:
    get_table_data('users', name="Hadin Abdul Hameed")
    '''
    query = supabase.table(table_name).select("*")
    for key, value in filters.items():
        query = query.eq(key, value)
    return query.execute()

def get_user(user_id: str="*", name: str="*", email: str="*") -> PostgrestAPIResponse:
    '''
    To get datas inside `users` table, where key=value(if any).
    
    eg:
    get_user(email="hadinabdulhameed@gmail.com")
    '''
    query = supabase.table("users").select("*")

    if user_id != "*":
        query = query.eq("user_id", user_id)
    if name != "*":
        query = query.eq("name", name)
    if email != "*":
        query = query.eq("email", email)

    response = query.execute()
    return response

def get_workday(workday_id: str="*", notes: str="*", opening_time: str="*", closing_time: str="*") -> PostgrestAPIResponse:
    '''
    To get datas inside `workdays` table, where key=value(if any).
    
    eg:
    get_workday(notes="regular")
    '''
    query = supabase.table("workdays").select("*")

    if workday_id != "*":
        query = query.eq("workday_id", workday_id)
    if notes != "*":
        query = query.eq("notes", notes)
    if opening_time != "*":
        query = query.eq("opening_time", opening_time)
    if closing_time != "*":
        query = query.eq("closing_time", closing_time)

    response = query.execute()
    return response

def get_entry(entry_id: str="*", workday_id: str="*", user_id: str="*") -> PostgrestAPIResponse:
    '''
    To get datas inside `entry_logs` table, where key=value(if any) (With `entry`=False).
    
    eg:
    get_entry(workday_id="2025-04-17")
    '''
    query = supabase.table("entry_logs").select("*").eq("entry", True)

    if entry_id != "*":
        query = query.eq("entry_id", entry_id)
    if workday_id != "*":
        query = query.eq("workday_id", workday_id)
    if user_id != "*":
        query = query.eq("user_id", user_id)

    response = query.execute()
    return response

def get_exit(entry_id: str="*", workday_id: str="*", user_id: str="*") -> PostgrestAPIResponse:
    '''
    To get datas inside `entry_logs` table, where key=value(if any) (With `entry`=False).
    
    eg:
    get_exit(user_id="aad1a0aa-dea4-a1ae-4a1a-aaeaaaa10aaa", workday_id="2025-04-17")
    '''
    query = supabase.table("entry_logs").select("*").eq("entry", False)

    if entry_id != "*":
        query = query.eq("entry_id", entry_id)
    if workday_id != "*":
        query = query.eq("workday_id", workday_id)
    if user_id != "*":
        query = query.eq("user_id", user_id)

    response = query.execute()
    return response

def get_task(id: str="*", workday_id: str="*", user_id: str="*", tags: dict=[], name: str="*") -> PostgrestAPIResponse:
    '''
    To get datas inside `task_logs` table, where key=value(if any).
    
    eg:
    get_task(workday_id="2025-04-1.7", tags=["python"])
    '''
    query = supabase.table("task_logs").select("*")

    if id != "*":
        query = query.eq("id", id)
    if workday_id != "*":
        query = query.eq("workday_id", workday_id)
    if user_id != "*":
        query = query.eq("user_id", user_id)
    if tags != []:
        query = query.contains("tags", tags)
    if name != "*":
        query = query.eq("name", name)
    

    response = query.execute()
    return response

if __name__ == "__main__":
    print(get_task(workday_id="2025-04-17", tags=["python"]))
    pass