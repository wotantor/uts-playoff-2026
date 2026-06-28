import os
import gspread
from google.oauth2.service_account import Credentials

# Настройка доступов к Google Sheets API
scopes = ["https://www.googleapis.com/auth/spreadsheets"]
creds_dict = {
    "type": "service_account",
    "project_id": os.environ.get("GCP_PROJECT_ID"),
    "private_key_id": os.environ.get("GCP_PRIVATE_KEY_ID"),
    "private_key": os.environ.get("GCP_PRIVATE_KEY").replace("\\n", "\n") if os.environ.get("GCP_PRIVATE_KEY") else None,
    "client_email": os.environ.get("GCP_CLIENT_EMAIL"),
}

def update_github_readme(leaderboard_markdown):
    readme_path = "README.md"
    
    if not os.path.exists(readme_path):
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write("# 🏆 UTS Play-off 2026\n\n## 📊 Актуальный Лидерборд\n\n")

    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()

    start_marker = ""
    end_marker = ""
    
    if start_marker in content and end_marker in content:
        before = content.split(start_marker)[0]
        after = content.split(end_marker)[1]
        new_content = f"{before}{start_marker}\n{leaderboard_markdown}\n{end_marker}{after}"
        
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print("README.md успешно обновлен!")
    else:
        print("Маркеры лидерборда не найдены в README.md")

def main():
    if not creds_dict["private_key"]:
        print("Ошибка: Секреты GCP не настроены в GitHub Actions.")
        return

    creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
    client = gspread.authorize(creds)
    
    # Ссылка на твою новую таблицу плей-офф UTS play-off
    spreadsheet_id = "1VyPWRRN-_ychz1TsOnSVZyLQy3SX6StpqJsk212HTwA"
    sheet = client.open_by_key(spreadsheet_id).worksheet("Лидерборд")
    
    data = sheet.get_all_values()
    if len(data) <= 1:
        print("Лидерборд пуст.")
        return

    # Строим Markdown-таблицу плей-офф
    markdown_table = "| 🔝 Место | 👤 Участник | 🎯 Всего очков | 🟢 Точный счёт (3 б.) | 🟡 Исходы (1 б.) |\n"
    markdown_table += "| :---: | :--- | :---: | :---: | :---: |\n"
    
    for index, row in enumerate(data[1:], start=1):
        if not row or not row[0]:
            continue
            
        name = row[0]
        total_points = row[1] if len(row) > 1 else "0"
        exact_scores = row[2] if len(row) > 2 else "0"
        outcomes = row[3] if len(row) > 3 else "0"
        
        if index == 1:
            place = "🥇 1"
        elif index == 2:
            place = "🥈 2"
        elif index == 3:
            place = "🥉 3"
        else:
            place = f"{index}"
            
        markdown_table += f"| {place} | {name} | **{total_points}** | {exact_scores} | {outcomes} |\n"

    update_github_readme(markdown_table)

if __name__ == "__main__":
    main()
