import urllib.request
import csv
import io

def update_github_readme(leaderboard_markdown):
    readme_path = "README.md"
    try:
        with open(readme_path, "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        print("Ошибка: Файл README.md не найден!")
        return

    # Текстовые маркеры, которые соответствуют твоему новому README
    start_marker = "START_LEADERBOARD_HERE"
    end_marker = "END_LEADERBOARD_HERE"
    
    if start_marker in content and end_marker in content:
        start_idx = content.find(start_marker) + len(start_marker)
        end_idx = content.find(end_marker)
        
        new_content = content[:start_idx] + "\n\n" + leaderboard_markdown + "\n" + content[end_idx:]
        
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print("README.md успешно обновлен локально!")
    else:
        print("Ошибка: Текстовые маркеры не найдены в README.md")

def main():
    spreadsheet_id = "1VyPWRRN-_ychz1TsOnSVZyLQy3SX6StpqJsk212HTwA"
    gid = "140688170"
    url = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/export?format=csv&gid={gid}"
    
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
        
        if "Друг" in name and (len(row) > 1 and (row[1] == "0" or row[1] == "")):
            continue
            
        if name.startswith("Прогноз:"):
            name = name.replace("Прогноз:", "").strip()
            
        total_points = row[1] if len(row) > 1 and row[1] != "" else "0"
        exact_scores = row[2] if len(row) > 2 and row[2] != "" else "0"
        outcomes = row[3] if len(row) > 3 and row[3] != "" else "0"
        
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
