import pandas as pd
import os.path
from nrclex import NRCLex
import html2text
from Downloader import Downloader

import pdfplumber
import pikepdf


# basic items
dl = Downloader()

h = html2text.HTML2Text()
h.ignore_links = True

report_10k = "10-K"
report_10q = "10-Q"

all_emo_10k = {}
all_emo_10q = {}

path_to_folder_sec = "/Users/vladoo/Work/parser/EDGAR/"
path_to_folder_eu = "/Users/vladoo/Work/parser/EU_reports/"

# ——————————FUNCTIONS—————————————


def get_nasdaq_tickers():
    table = pd.read_html('https://en.wikipedia.org/wiki/NASDAQ-100')[3]
    sliced_table = table[1:]
    header = table.iloc[0]
    corrected_table = sliced_table.rename(columns=header)
    tickers = corrected_table['ATVI'].tolist()
    tickers.append('ATVI')

    return tickers


def get_sp500_tickers():
    table = pd.read_html(
        'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]
    sliced_table = table[1:]
    header = table.iloc[0]
    corrected_table = sliced_table.rename(columns=header)
    tickers = corrected_table['MMM'].tolist()
    tickers.append('MMM')
    return tickers


def get_tickers_E(limit=0, url='https://en.wikipedia.org/wiki/EURO_STOXX_50'):
    data_from_Euro_Stoxx = pd.read_html(url)
    table = data_from_Euro_Stoxx[2]
    column_tickers = table['Ticker']

    tickers = []
    i = 0
    for ticker in column_tickers:
        tickers.append(ticker)
        i += 1
        if limit > 0 and i >= limit:
            break
    return tickers


def print_emotions():
    print("------Emotions of 10K:")
    df_10k = pd.DataFrame.from_dict(all_emo_10k, orient='index', columns=[
        'fear', 'anger', 'trust', 'surprise', 'positive', 'negative', 'sadness', 'disgust', 'joy', 'anticipation'
    ])
    print(df_10k)

    print("\n------Emotions of 10Q:")
    df_10q = pd.DataFrame.from_dict(all_emo_10q, orient='index', columns=[
        'fear', 'anger', 'trust', 'surprise', 'positive', 'negative', 'sadness', 'disgust', 'joy', 'anticipation'
    ])
    print(df_10q)


def check_length(text):
    print("     Checking length")
    ready_text = ""
    for line in range(len(text.split("\n")) - 1):
        if len(text.splitlines()[line]) < 10000:
            ready_text += text.splitlines()[line]
    return ready_text


def get_10K_reports_sec(tick):
    if os.path.isfile(path_to_folder_sec + tick + "/" + report_10k + "/filing-details.html"):
        print("     File exists")
        file_path_10k = path_to_folder_sec + tick + \
            "/" + report_10k + "/filing-details.html"
    else:
        dl.get(report_10k, tick, amount=1)
        if os.path.isfile(path_to_folder_sec + tick + "/" + report_10k + "/filing-details.html"):
            file_path_10k = path_to_folder_sec + tick + \
                "/" + report_10k + "/filing-details.html"
        else:
            return

    html_10k = open(file_path_10k, "r")
    html_10k = h.handle(html_10k.read())
    html_10k_text = check_length(html_10k)

    print("     Reading 10K for emotions")
    emotions_10k = NRCLex(h.handle(html_10k_text))

    print("     Writing 10K emotions")
    all_emo_10k[tick] = emotions_10k.affect_frequencies


def get_10Q_reports_sec(tick):
    if os.path.isfile(path_to_folder_sec + tick + "/" + report_10q + "/filing-details.html"):
        print("     File exists")
        file_path_10q = path_to_folder_sec + tick + \
            "/" + report_10q + "/filing-details.html"
    else:
        dl.get(report_10q, tick, amount=1)
        if os.path.isfile(path_to_folder_sec + tick + "/" + report_10q + "/filing-details.html"):
            file_path_10q = path_to_folder_sec + tick + \
                "/" + report_10q + "/filing-details.html"
        else:
            return

    html_10q = open(file_path_10q, "r")
    html_10q = h.handle(html_10q.read())
    html_10q_text = check_length(html_10q)

    print("     Reading 10Q for emotions")
    emotions_10q = NRCLex(h.handle(html_10q_text))

    print("     Writing 10Q emotions")
    all_emo_10q[tick] = emotions_10q.affect_frequencies


def get_10K_reports_eu(tick):
    if os.path.isfile(path_to_folder_eu + tick + "/" + report_10k + "/filing-details.pdf"):
        file_path_10k = path_to_folder_eu + tick + \
            "/" + report_10k + "/filing-details.pdf"
    else:
        return

    pdf = pikepdf.open(file_path_10k, allow_overwriting_input=True)
    pdf.save(file_path_10k)

    pdf_10k_text = ""
    print("     Reading 10K for text")
    with pdfplumber.open(file_path_10k) as pdf_10k:
        for page in range(len(pdf_10k.pages)):
            if pdf_10k.pages[page].extract_text() != None:
                pdf_10k_text = pdf_10k_text + "\n" + \
                    pdf_10k.pages[page].extract_text()

    pdf_10k.close()

    print("     Reading 10K for emotions")
    emotions_10k = NRCLex(pdf_10k_text)

    print("     Writing 10K emotions")
    all_emo_10k[tick] = emotions_10k.affect_frequencies


def get_10Q_reports_eu(tick):
    if os.path.isfile(path_to_folder_eu + tick + "/" + report_10q + "/filing-details.pdf"):
        file_path_10q = path_to_folder_eu + tick + \
            "/" + report_10q + "/filing-details.pdf"
    else:
        return

    pdf = pikepdf.open(file_path_10q, allow_overwriting_input=True)
    pdf.save(file_path_10q)

    pdf_10q_text = ""
    print("     Reading 10Q for text")
    with pdfplumber.open(file_path_10q) as pdf_10q:
        for page in range(len(pdf_10q.pages)):
            if pdf_10q.pages[page].extract_text() != None:
                pdf_10q_text = pdf_10q_text + "\n" + \
                    pdf_10q.pages[page].extract_text()

    pdf_10q.close()

    print("     Reading 10Q for emotions")
    emotions_10q = NRCLex(pdf_10q_text)

    print("     Writing 10Q emotions")
    all_emo_10q[tick] = emotions_10q.affect_frequencies
# ——————————MAIN—————————————


tickers_sec = list(set(get_nasdaq_tickers() + get_sp500_tickers()))
tickers_eu = list(set(get_tickers_E()))


start = input(
    '''    Отчеты с сайта sev.gov:
1) Скачать отчеты годовые и квартальные\n2) Скачать только годовые \n3) Скачать только кварталаьные\n
    Европейские отчеты:
4) Оценка годовых и квартальных отчетов\n5) Оценка только годовых \n6) Оценка только квартальных
\nВыберите вариант: ''')
n = 1
if start == "1":
    for tick in range(len(tickers_sec)):
        print(str(n) + "/" + str(len(tickers_sec)) + " " + tickers_sec[tick])
        n += 1

        get_10K_reports_sec(tickers_sec[tick])
        get_10Q_reports_sec(tickers_sec[tick])
elif start == "2":
    for tick in range(len(tickers_sec)):
        print(str(n) + "/" + str(len(tickers_sec)) + " " + tickers_sec[tick])
        n += 1

        get_10K_reports_sec(tickers_sec[tick])
elif start == "3":
    for tick in range(len(tickers_sec)):
        print(str(n) + "/" + str(len(tickers_sec)) + " " + tickers_sec[tick])
        n += 1

        get_10Q_reports_sec(tickers_sec[tick])
elif start == "4":
    for tick in range(len(tickers_eu)):
        print(str(n) + "/" + str(len(tickers_eu)) + " " + tickers_eu[tick])
        n += 1

        get_10K_reports_eu(tickers_eu[tick])
        get_10Q_reports_eu(tickers_eu[tick])
elif start == "5":
    for tick in range(len(tickers_eu)):
        print(str(n) + "/" + str(len(tickers_eu)) + " " + tickers_eu[tick])
        n += 1

        get_10K_reports_eu(tickers_eu[tick])
elif start == "6":
    for tick in range(len(tickers_eu)):
        print(str(n) + "/" + str(len(tickers_eu)) + " " + tickers_eu[tick])
        n += 1

        get_10Q_reports_eu(tickers_eu[tick])

print_emotions()
