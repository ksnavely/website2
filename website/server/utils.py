from datetime import datetime

import arrow
from arrow.locales import EnglishLocale


def archive_dates(start_year=2016, start_month=3):
    """
    Given a start year/month, return a three tuple of every month
    since that point in the format as seen below:

    [
        ('2016', '03', u'March'),
        ('2016', '04', u'April'),
        ('2016', '05', u'May'),
        ...
    ]
    """
    english_locale = EnglishLocale()
    start = datetime(start_year, start_month, 1)

    dates = []
    for d in arrow.Arrow.range("month", start, arrow.now().datetime):
        dates.append(
            (str(d.year), "{0:02d}".format(d.month), english_locale.month_name(d.month))
        )

    return dates
