from csv import DictReader
from datetime import datetime as dt
from datetime import timedelta
import hashlib
import os

raw = """
.row.project
  .col-md-6.col-9
    p.author #[span.me %%%AUTHOR%%%]
    h4.title.mb-1
      | %%%TITLE%%%
    .btn-group.btn-group-sm(role="group",aria-label="Commands").mt-1
      %%%CALENDAR%%%
      button.btn.btn-primary(type="button",data-bs-toggle="collapse",data-bs-target="#%%%TALK_ID%%%",aria-expanded="false",aria-controls="%%%TALK_ID%%%"%%%DISABLED%%%)
        | #[i.bi.bi-card-text] Abstract%%%SLIDES%%%
  .col-md-2.col-3.date
    h3.mb-0 %%%DAY%%%
    h5.month.mb-0 %%%MONTH%%%
    p %%%HOURS%%%
  .col-md-6
    p.abstract#%%%TALK_ID%%%.collapse.mt-2
        | %%%ABSTRACT%%%"""

raw_upcoming = """
.row.next
  .col-md-6
    h2.title.mb-1.mt-1
      | %%%TITLE%%%
    p.author #[span.me %%%AUTHOR%%%]
  .col-md-2.date
    h1.day %%%DAY%%%
    h4.month.mb-0 %%%MONTH%%%
    p %%%HOURS%%%
  .col-md-6.mt-sm-3.mt-lg-1
      p.abstract
        | %%%ABSTRACT%%%
  .col-md-2.d-grid.gap-2.d-md-block
    %%%CALENDAR%%%
    a(href="%%%MEET%%%").btn.btn-primary.mb-md-3.w-100
      | #[i.bi.bi-camera-reels-fill]Streaming%%%SLIDES%%%
    a(href="https://goo.gl/maps/FL4qcbB3MnMXrYS28",target="_blank").btn.btn-primary.w-100
      | #[i.bi.bi-geo-alt-fill]Pisa CS Dept
      """
calendar_raw = """
      a(href="%%%CALENDAR%%%",target="_blank").btn.btn-primary
        | #[i.bi.bi-calendar-event-fill] Add to Calendar"""

slides_raw = """
      a(href="%%%SLIDES%%%",target="_blank").btn.btn-primary
        | #[i.bi.bi-file-earmark-text-fill] Paper"""

calendar_raw_upcoming = """
    a(href="%%%CALENDAR%%%",target="_blank").btn.btn-primary.mb-md-3.w-100
      | #[i.bi.bi-calendar-event-fill] Add to Calendar"""

slides_raw_upcoming = """
    a(href="%%%SLIDES%%%",target="_blank").btn.btn-primary.mb-md-3.w-100
      | #[i.bi.bi-file-earmark-text-fill] Paper"""


def render_talk(talk, upcoming=False, past=False):
    if upcoming:
        template = raw_upcoming
    else:
        template = raw

    # Parse date
    date = dt.strptime(talk['Date'], '%d/%m/%Y')

    # Get month name
    month = date.strftime('%B')

    # Get cardinal day without leading zero
    day = str(int(date.strftime('%d')))

    # Add suffix to day
    day += suffix(int(day))

    # Build the output
    output = template.replace('%%%DAY%%%', day)
    output = output.replace('%%%MONTH%%%', month)
    output = output.replace('%%%AUTHOR%%%', talk['Name'])

    if talk['Title']:
        output = output.replace('%%%TITLE%%%', talk['Title'])
    else:
        output = output.replace('%%%TITLE%%%', 'TBA')

    # Eventually add room
    if 'Room' in talk and talk['Room']:
        output = output.replace("%%%ROOM%%%", talk['Room'])
    else:
        output = output.replace("%%%ROOM%%%", 'TBA')

    # Eventually add hours
    if 'Hours' in talk and talk['Hours']:
        output = output.replace('%%%HOURS%%%', talk['Hours'])
    else:
        output = output.replace('%%%HOURS%%%', 'Hours TBA')

    # Eventually add abstract
    if talk['Abstract']:
        output = output.replace('%%%ABSTRACT%%%', talk['Abstract'])
        output = output.replace('%%%DISABLED%%%', '')
    else:
        output = output.replace('%%%ABSTRACT%%%', 'No abstract available')
        output = output.replace('%%%DISABLED%%%',
                                ',aria-disabled="true",disabled')

    # Eventually add calendar link
    if not past and not upcoming and 'Calendar' in talk and talk['Calendar']:
        output = output.replace('%%%CALENDAR%%%',
                                calendar_raw.replace('%%%CALENDAR%%%',
                                                   talk['Calendar']))
    elif not past and upcoming and 'Calendar' in talk and talk['Calendar']:
        output = output.replace('%%%CALENDAR%%%',
                                calendar_raw_upcoming.replace('%%%CALENDAR%%%',
                                                   talk['Calendar']))
    else:
        output = output.replace('%%%CALENDAR%%%', '')

    # Eventually add meet link
    if 'Meet' in talk and talk['Meet']:
        output = output.replace('%%%MEET%%%', talk['Meet'])
    else:
        output = output.replace('%%%MEET%%%', '#')

    # Check if the slides are available
    slides_fname = f'slides/{talk["Title"].replace(":","_")}.pdf'
    slides = os.path.isfile('static/'+slides_fname)
    if not slides:
        print(f'No slides for "{talk["Title"]}"')

    # Eventually add slides link
    if slides and not upcoming:
        output = output.replace('%%%SLIDES%%%',
                                slides_raw.replace('%%%SLIDES%%%',
                                                   slides_fname))
    elif slides and upcoming:
        output = output.replace('%%%SLIDES%%%',
                                slides_raw_upcoming.replace('%%%SLIDES%%%',
                                                            slides_fname))
        print('Slides found for talk', talk['Title'])
    else:
        output = output.replace('%%%SLIDES%%%', '')

    # Generate talk ID from the author using md5
    talk_id = hashlib.md5(talk['Name'].encode('utf-8')).hexdigest()

    # DOM Selectors can't start with a number
    talk_id = 'talk-' + talk_id

    # Add talk ID to output
    output = output.replace('%%%TALK_ID%%%', talk_id)

    return output


def suffix(d):
    return 'th' if 11 <= d <= 13 \
            else {1: 'st', 2: 'nd', 3: 'rd'}.get(d % 10, 'th')


if __name__ == '__main__':
    import argparse

    # Parse arguments
    parser = argparse.ArgumentParser(description='Render talks')
    parser.add_argument('-u', '--upcoming', action='store_true',
                        help='Render upcoming talks')
    parser.add_argument('-d', '--date', type=str,
                        help='Render page for a specific date '
                             '(format: DD/MM/YYYY)')
    parser.add_argument('csv_filename', type=str,
                        help='CSV file containing talks',
                        default='Seminars.csv')
    args = parser.parse_args()

    # Parse CSV file into a dictionary
    with open(args.csv_filename, 'r') as fp:
        csv_reader = DictReader(fp)
        talks = list(csv_reader)

    # Get current datetime
    if not args.date:
        now = dt.now()
    else:
        now = dt.strptime(args.date, '%d/%m/%Y')

    # Filter talks
    #timedelta so if rendered the same day of a talk the talk is still upcoming
    talks = [talk for talk in talks if talk['Name']]
    future = [talk for talk in talks if dt.strptime(talk['Date'],
                                                    '%d/%m/%Y') > now-timedelta(days=1)]
    past = [talk for talk in talks if dt.strptime(talk['Date'],
                                                  '%d/%m/%Y') <= now- timedelta(days=1)]

    # Sort future talks by date
    future.sort(key=lambda x: dt.strptime(x['Date'], '%d/%m/%Y'))

    # Assign upcoming
    if future and args.upcoming:
        upcoming = future[0]
        future = future[1:]
    else:
        upcoming = None

    # Render upcoming
    with open('layout/upcoming.pug', 'w') as f:
        if upcoming:
            f.write('.row.mt-4.mb-2\n')
            f.write('  h2 #[span.emoji 🚀] Upcoming\n')
            f.write(render_talk(upcoming, True))
        else:
            f.write('')

    # Render past talks
    with open('layout/past.pug', 'w') as f:
        if past:
            f.write('.row.mt-4.mb-4\n')
            f.write('  h2 #[span.emoji ⌛️] Past Talks\n')
            for talk in past:
                f.write(render_talk(talk, past=True))
        else:
            f.write('')

    # Render future talks
    with open('layout/next.pug', 'w') as f:
        if future:
            f.write('.row.mt-4.mb-4\n')
            f.write('  h2 #[span.emoji 🔮] Next Talks\n')
            for talk in future:
                f.write(render_talk(talk))
        else:
            f.write('')
