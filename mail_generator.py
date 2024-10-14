import csv
from datetime import datetime
import urllib.parse


def read_seminars(file_path):
    seminars = []
    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            seminars.append(row)
    return seminars


def find_next_seminar(seminars, current_date):
    future_seminars = [s for s in seminars if datetime.strptime(s['Date'], '%d/%m/%Y') >= current_date]
    if not future_seminars:
        return None
    return min(future_seminars, key=lambda s: abs(datetime.strptime(s['Date'], '%d/%m/%Y') - current_date))


def create_calendar_link(seminar):
    date = datetime.strptime(f"{seminar['Date']} {seminar['Hours'].split('-')[0]}", '%d/%m/%Y %H:%M')
    end_date = datetime.strptime(f"{seminar['Date']} {seminar['Hours'].split('-')[1]}", '%d/%m/%Y %H:%M')

    event = {
        'text': f"Seminar: {seminar['Title']}",
        'dates': f"{date.strftime('%Y%m%dT%H%M%S')}/{end_date.strftime('%Y%m%dT%H%M%S')}",
        'details': f"Presenter: {seminar['Name']} ({seminar['Institution']})\n\n Join Teams Meeting: {seminar['Meet']}",
        'location': seminar['Room']
    }

    base_url = "https://www.google.com/calendar/render?action=TEMPLATE"
    for key, value in event.items():
        base_url += f"&{key}={urllib.parse.quote(value)}"

    return base_url


def generate_email_content(seminar):
    subject = f"[Seminar] {seminar['Title']}"
    calendar_link = create_calendar_link(seminar)
    body = f"""Dear Causal Clubbers,

We are pleased to invite you to our upcoming seminar:

**Presenter:** {seminar['Name']} ({seminar['Institution']})

**When:** {seminar['Date']}, {seminar['Hours']} [[Add to Calendar]({calendar_link})]

**Where:** {seminar['Room']}, Computer Science Department, University of Pisa

**To join online:** {seminar['Meet']}

**Title:** {seminar['Title']}

**Abstract:** 
{seminar['Abstract']}

We look forward to seeing you at the seminar!

Best,

Causal Club 
"""
    return subject, body


def save_email_to_file(subject, body):
    filename = f"mail.md"
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(f"Subject: {subject}\n\n")
        file.write(body)
    return filename


def main():
    current_date = datetime.now()
    seminars = read_seminars('Seminars.csv')
    next_seminar = find_next_seminar(seminars, current_date)

    if next_seminar:
        subject, body = generate_email_content(next_seminar)
        try:
            filename = save_email_to_file(subject, body)
            print(f"Email content saved successfully to {filename}!")
        except Exception as e:
            print(f"An error occurred while saving the email content: {e}")

    else:
        print("No upcoming seminars found.")


if __name__ == "__main__":
    main()