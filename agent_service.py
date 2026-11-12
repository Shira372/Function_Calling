

from openai import OpenAI
from dotenv import load_dotenv
import json
from todo_service import (
    get_tasks,
    add_task,
    update_task,
    delete_task,
    add_task_from_text,
    update_task_by_text,
    delete_task_by_text,
)
load_dotenv()
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)
functions = [
    {
        "name": "get_tasks",
        "description": "שליפת משימות עם סינון לפי סטטוס או סוג",
        "parameters": {
            "type": "object",
            "properties": {
                "filters": {
                    "type": "object",
                    "description": "סינונים כמו סטטוס או סוג",
                    "additionalProperties": {"type": "string"},
                }
            },
            "required": [],
        },
    },
    {
        "name": "add_task",
        "description": "הוספת משימה חדשה (באופן חופשי לפי טקסט)",
        "parameters": {
            "type": "object",
            "properties": {
                "text": {"type": "string"}
            },
            "required": ["text"],
        },
    },

    {
        "name": "update_task_by_text",
         "description": "עדכון שדות של משימה קיימת לפי טקסט המתאר את המשימה. פעולה זו משנה את הסטטוס במערכת.",
  "parameters": {
    "type": "object",
    "properties": {
      "text": {"type": "string", "description": "תיאור או שם המשימה לעדכון"},
      "updated_fields": {
        "type": "object",
        "properties": {
          "status": {
            "type": "string",
            "enum": ["חדש", "בוצע", "מושהה"],
            "description": "סטטוס חדש לעדכון במשימה"
          }
        },
        "required": ["status"],
      }
    },
    "required": ["text", "updated_fields"]
  }
},

    {
        "name": "delete_task_by_text",
        "description": "מחיקת משימה לפי טקסט שמתאר את המשימה",
        "parameters": {
            "type": "object",
            "properties": {
                "text": {"type": "string"},
            },
            "required": ["text"],
        },
    },
]

def parse_status_from_query(query):
    if "בוצע" in query:
        return "בוצע"
    if "לא בוצע" in query:
        return "חדש"
    return None

def agent(query: str):

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": query}],
        functions=functions,
        function_call="auto",
    )

    message = response.choices[0].message

    if hasattr(message, "function_call") and message.function_call:
        func_name = message.function_call.name
        args = json.loads(message.function_call.arguments)


        if func_name == "get_tasks":
            status = parse_status_from_query(query)
            filters = {"status": status} if status else {}
            result = get_tasks(filters)

        elif func_name == "add_task":
            result = add_task_from_text(args.get("text", ""))

        elif func_name == "update_task_by_text":
            text = args.get("text", "")
            updated_fields = args.get("updated_fields", {})
            result = update_task_by_text(text, updated_fields)

        elif func_name == "delete_task_by_text":
            text = args.get("text", "")
            result = delete_task_by_text(text)
        else:
            return "לא הבנתי איזו פעולה לבצע"

        final_response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "אתה עוזר אישי לניהול משימות. הצג משימות לפי סדר אופטימלי, עם קוד, כותרת ותיאור בלבד."},
                {"role": "user", "content": query},
                {"role": "function", "name": func_name, "content": str(result)},
            ],
        )

        return final_response.choices[0].message.content

    else:
        return "לא הצלחתי להבין את הבקשה 😔"



















