import urllib.request
import csv
import io

def update_github_readme(leaderboard_markdown):
    readme_path = "README.md"
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
    # Ссылка на экспорт листа "Лидерборд" в формате CSV
    spreadsheet_id = "1VyPWRRN-_ychz1TsOnSVZyLQy3SX6StpqJsk212HTwA"
    # gid=1406883204 — это ID листа "Лидерборд" из твоей адресной строки
    url = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/export?format=csv&gid=1406883204"
    
    try:
        response = urllib.request.urlopen(url)
        csv_data = response.read().decode('utf-8')
    except Exception as e:
        print(f"Ошибка при скачивании таблицы: {e}")
        return

    f = io.StringIO(csv_data)
    reader = csv.reader(f)
    data = list(reader)

    if len(data) <= 1:
        print("Лидерборд пуст.")
        return

    markdown_table = "| 🔝 Место | 👤 Участник | 🎯 Всего очков | 🟢 Точный счёт (3 б.) | 🟡 Исходы (1 б.) |\n"
    markdown_table += "| :---: | :--- | :---: | :---: | :---: |\n"
    
    place_counter = 1
    for row in data[1:]:
        if not row or not row[0] or row[0].strip() == "":
            continue
            
        name = row[0].strip()
        
        # Если имя содержит "Друг" и у него 0 очков — не спамим им в таблице
        if "Друг" in name and (len(row) > 1 and (row[1] == "0" or row[1] == "")):
            continue
            
        if name.startswith("Прогноз:"):
            name = name.replace("Прогноз:", "").strip()
            
        total_points = row[1] if len(row) > 1 else "0"
        exact_scores = row[2] if len(row) > 2 else "0"
        outcomes = row[3] if len(row) > 3 else "0"
        
        if place_counter == 1:
            place = "🥇 1"
        elif place_counter == 2:
            place = "🥈 2"
        elif place_counter == 3:
            place = "🥉 3"
        else:
            place = f"{place_counter}"
            
        markdown_table += f"| {place} | {name} | **{total_points}** | {exact_scores} | {outcomes} |\n"
        place_counter += 1

    update_github_readme(markdown_table)

if __name__ == "__main__":
    main()
