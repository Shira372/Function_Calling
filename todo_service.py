

tasks = []

def get_tasks(filters=None):
    if not filters or "status" not in filters:
        return tasks
    status_filter = filters["status"].strip()
    return [
        task for task in tasks
        if task.get("status", "").strip() == status_filter
    ]


def add_task(task):
    tasks.append(task)
    return task

def update_task(code, updated_fields):
    for task in tasks:
        if task["code"] == code:
            task["status"] = "בוצע"
            return task
    return None

def delete_task(code):
    global tasks
    tasks = [task for task in tasks if task["code"] != code]
    return True

def find_task_code_by_text(text):
    text_lower = text.lower()
    for task in tasks:
        title = task.get("title", "").lower()
        description = task.get("description", "").lower()
        if text_lower in title or text_lower in description:
            return task.get("code")
    return None

def update_task_by_text(text, updated_fields):
    code = find_task_code_by_text(text)
    if not code:
        return None
    return update_task(code, updated_fields)

def delete_task_by_text(text):
    code = find_task_code_by_text(text)
    if not code:
        return False
    return delete_task(code)

def add_task_from_text(text):
    from datetime import datetime, timedelta
    code = f"task{len(tasks) + 1}"
    now = datetime.now()
    task = {
        "code": code,
        "title": text.strip(),
        "description": text.strip(),
        "type": "כללי",
        "start_date": now.strftime("%Y-%m-%d"),
        "end_date": (now + timedelta(days=2)).strftime("%Y-%m-%d"),
        "status": "חדש",  
    }
    return add_task(task)
