
import json
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build

SPREADSHEET_ID = "1aWbEArzCvxOrEYxfg6Wa4WzNEi6_wtpPqwse9pWxSSo"

credentials_info = json.loads(os.environ["GOOGLE_SERVICE_ACCOUNT"])

credentials = service_account.Credentials.from_service_account_info(
    credentials_info,
    scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"]
)

service = build("sheets", "v4", credentials=credentials)

spreadsheet = service.spreadsheets().get(
    spreadsheetId=SPREADSHEET_ID
).execute()

output = {
    "updated": None,
    "sheets": []
}

for sheet in spreadsheet["sheets"]:
    name = sheet["properties"]["title"]

    result = service.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID,
        range=f"'{name}'"
    ).execute()

    values = result.get("values", [])

    output["sheets"].append({
        "name": name,
        "headers": values[0] if values else [],
        "rows": values[1:] if len(values) > 1 else []
    })

from datetime import datetime, timezone

output["updated"] = datetime.now(timezone.utc).isoformat()

os.makedirs("data", exist_ok=True)

with open("data/data.json", "w", encoding="utf-8") as file:
    json.dump(output, file, indent=2, ensure_ascii=False)

print(f"Updated {len(output['sheets'])} spreadsheet tabs.")
