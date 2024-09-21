import csv
import os
import re

def read_csv_file(file_path):
    with open(file_path, newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        data = list(reader)
    #print (data)
    return data

def get_athlete_files(base_dir, team_dirs=['mens_team', 'womens_team']):
    athlete_files = []
    for team_dir in team_dirs:
        team_path = os.path.join(base_dir, team_dir)
        
        if not os.path.exists(team_path):
            continue
        
        for file_name in os.listdir(team_path):
            if file_name.endswith('.csv'):
                file_path = os.path.join(team_path, file_name)
                athlete_files.append((team_dir, file_name, file_path))
    #print(athlete_files)
    return athlete_files

def find_data_start(data):
    for index, row in enumerate(data):
        if not row:
            continue
        if row[0].strip().lower() == 'name' and len(row) >= 8:
            return index
    return -1

def generate_html(data, start_index, athlete_name):
    if start_index == -1:
        print("Error: Couldn't find the start of the data")
        print(data)
        return None

    if len(data[start_index]) < 8:
        print("Error: CSV data header row has fewer than 8 columns")
        print(data[start_index])
        return None

    actual_data = data[start_index + 1:]

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel = "stylesheet" href = "css/reset.css">
        <link rel = "stylesheet" href = "css/style.css">
        <title>{athlete_name}</title>
    </head>
    <body>
        <h1>Performance Details for {athlete_name}</h1>
        <table>
            <thead>
                <tr>
                    <th>Name</th>
                    <th>Overall Place</th>
                    <th>Grade</th>
                    <th>Time</th>
                    <th>Date</th>
                    <th>Meet</th>
                    <th>Comments</th>
                    <th>Photo</th>
                </tr>
            </thead>
            <tbody>
    """

    for row in actual_data:
        if len(row) < 8:
            continue
        name = row[0]
        overall_place = row[1]
        grade = row[2]
        time = row[3]
        date = row[4]
        meet = row[5]
        comments = row[6]
        photo = row[7]

        html_content += f"""
                <tr>
                    <td>{name}</td>
                    <td>{overall_place}</td>
                    <td>{grade}</td>
                    <td>{time}</td>
                    <td>{date}</td>
                    <td>{meet}</td>
                    <td>{comments}</td>
                    <td><img src='photos/{photo}' alt='Photo of {name}' /></td>
                </tr>
        """

    html_content += """
            </tbody>
        </table>
    </body>
    </html>
    """
    return html_content

def save_html(output_dir, team_dir, athlete_name, html_content):
    output_path = os.path.join(output_dir, team_dir)
    os.makedirs(output_path, exist_ok=True)
    output_file_path = os.path.join(output_path, f'{athlete_name}.html')
    with open(output_file_path, 'w', encoding='utf-8') as html_file:
        html_file.write(html_content)

def create_athlete_web_pages(base_dir, output_dir):
    athlete_files = get_athlete_files(base_dir)
    for team_dir, file_name, file_path in athlete_files:
        csv_data = read_csv_file(file_path)
        start_index = find_data_start(csv_data)
        athlete_name = os.path.splitext(file_name)[0]
        html_content = generate_html(csv_data, start_index, athlete_name)

        if html_content is None:
            print(f"Skipping {file_path} due to errors")
            continue
        
        athlete_name = os.path.splitext(file_name)[0]
        save_html(output_dir, team_dir, athlete_name, html_content)

if __name__ == "__main__":
    base_dir = 'athletes'
    output_dir = 'output'
    create_athlete_web_pages(base_dir, output_dir)