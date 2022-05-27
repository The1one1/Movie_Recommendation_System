
def ListOfGenres(genre_json):
    if genre_json:
        genres = []
        genre_str = ", "
        for i in range(0, len(genre_json)):
            genres.append(genre_json[i]['name'])
        return genre_str.join(genres)


def date_convert(s):
    MONTHS = ['January', 'February', 'Match', 'April', 'May', 'June',
            'July', 'August', 'September', 'October', 'November', 'December']
    y = s[:4]
    m = int(s[5:-3])
    d = s[8:]
    month_name = MONTHS[m-1]

    result = month_name + ' ' + d + ' ' + y
    return result


def MinsToHours(duration):
    if duration % 60 == 0:
        return "{:.0f} hours".format(duration/60)
    else:
        return "{:.0f} hours {} minutes".format(duration/60, duration % 60)
