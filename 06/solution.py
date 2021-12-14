# pylint: disable=C0112,C0103,R0903,C0116,C0114,R0201
from datetime import date

def read_int():
    return int(input())

def read_int_array():
    return [int(ss) for ss in input().split()]

DOW_LANGS = {
        # catalan
        "CA": "dilluns;dimarts;dimecres;dijous;divendres;dissabte;diumenge".split(";"),
        # czech
        "CZ": "pondělí;úterý;středa;čtvrtek;pátek;sobota;neděle".split(";"),
        # german
        "DE": "Montag;Dienstag;Mittwoch;Donnerstag;Freitag;Samstag;Sonntag".split(";"),
        # danish
        "DK": "mandag;tirsdag;onsdag;torsdag;fredag;lørdag;søndag".split(";"),
        # english
        "EN": "monday;tuesday;wednesday;thursday;friday;saturday;sunday".split(";"),
        # spanish
        "ES": "lunes;martes;miércoles;jueves;viernes;sábado;domingo".split(";"),
        # finnish
        "FI": "maanantai;tiistai;keskiviikko;torstai;perjantai;lauantai;sunnuntai".split(";"),
        # french
        "FR": "lundi;mardi;mercredi;jeudi;vendredi;samedi;dimanche".split(";"),
        # icelandic
        "IS": "mánudagur;þriðjudagur;miðvikudagur;fimmtudagur;föstudagur;laugardagur;sunnudagur".split(";"),
        # greek
        "GR": "Δευτέρα;Τρίτη;Τετάρτη;Πέμπτη;Παρασκευή;Σάββατο;Κυριακή".split(";"),
        # hungarian
        "HU": "hétfő;kedd;szerda;csütörtök;péntek;szombat;vasárnap".split(";"),
        # italian
        "IT": "lunedì;martedì;mercoledì;giovedì;venerdì;sabato;domenica".split(";"),
        # dutch
        "NL": "maandag;dinsdag;woensdag;donderdag;vrijdag;zaterdag;zondag".split(";"),
        # vietnamese
        "VI": "thứ hai;thứ ba;thứ tư;thứ năm;thứ sáu;thứ bảy;chủ nhật".split(";"),
        # polish
        "PL": "poniedziałek;wtorek;środa;czwartek;piątek;sobota;niedziela".split(";"),
        # romanian
        "RO": "luni;marţi;miercuri;joi;vineri;sâmbătă;duminică".split(";"),
        # russian
        "RU": "понедельник;вторник;среда;четверг;пятница;суббота;воскресенье".split(";"),
        # swedish
        "SE": "måndag;tisdag;onsdag;torsdag;fredag;lördag;söndag".split(";"),
        # slovenian
        "SI": "Ponedeljek;Torek;Sreda;Četrtek;Petek;Sobota;Nedelja".split(";"),
        # slovak
        "SK": "pondelok;utorok;streda;štvrtok;piatok;sobota;nedeľa".split(";")
        }

def extract_date_tokens(datestr):
    x, y, z = map(int, datestr.split("-"))
    if datestr[2] == "-":
        return x, y, z
    return z, y, x

def solution(inputtxt):
    datestr, lang = inputtxt.split(":")
    d, m, y = extract_date_tokens(datestr)
    try:
        do = date(y, m, d)
        # print(do, do.isoweekday())
        # print(DOW_LANGS["VI"])
        dows = DOW_LANGS.get(lang)
        if dows is None:
            return "INVALID_LANGUAGE"
        dname = dows[do.isoweekday() - 1]
        return dname.lower()
    except ValueError:
        return "INVALID_DATE"

def main():
    t = read_int()

    for i in range(t):
        inputtxt = input().strip()
        s = solution(inputtxt)
        print(f"Case #{ i + 1 }: {s}")

if __name__ == "__main__":
    main()
