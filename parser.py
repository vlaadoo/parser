import pandas as pd
import os.path

from nrclex import NRCLex
import html2text

from Downloader import Downloader


dl = Downloader()   

h = html2text.HTML2Text()
h.ignore_links = True

report_10k = "10-K"
report_10q = "10-Q"

all_emo_10k = {}
all_emo_10q = {}


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



def santiment(tick):
    if os.path.isfile("/Users/vladoo/Work/parser/EDGAR/" + tick + "/" + report_10k + "/filing-details.html"):
        file_path_10k = "/Users/vladoo/Work/parser/EDGAR/" + tick + "/" + report_10k + "/filing-details.html"
    else:
        return

    if os.path.isfile("/Users/vladoo/Work/parser/EDGAR/" + tick + "/" + report_10q + "/filing-details.html"):
        file_path_10q = "/Users/vladoo/Work/parser/EDGAR/" + tick + "/" + report_10q + "/filing-details.html"
    else:
        return

    html_10k = open(file_path_10k, "r")
    html_10q = open(file_path_10q, "r")
    
    print("     Reading 10K for emotions")
    emotions_10k = NRCLex(h.handle(html_10k.read()))
    print("     Reading 10Q for emotions")
    emotions_10q = NRCLex(h.handle(html_10q.read()))
    
    print("     Writing 10K emotions")
    all_emo_10k[tick] = emotions_10k.affect_frequencies
    print("     Writing 10Q emotions")
    all_emo_10q[tick] = emotions_10q.affect_frequencies


def print_emotions():
    print("------Emotions of 10K:")
    print(pd.DataFrame.from_dict(all_emo_10k, orient='index',columns=[
        'fear', 
        'anger', 
        'trust', 
        'surprise', 
        'positive', 
        'negative', 
        'sadness', 
        'disgust', 
        'joy', 
        'anticipation'
        ]))    

    print("\n------Emotions of 10Q:")
    print(pd.DataFrame.from_dict(all_emo_10q, orient='index',columns=[
        'fear', 
        'anger', 
        'trust', 
        'surprise', 
        'positive', 
        'negative', 
        'sadness', 
        'disgust', 
        'joy', 
        'anticipation'
        ]))

tickers = get_nasdaq_tickers() + get_sp500_tickers()

for tick in range(len(tickers)):
    print(tickers[tick])

    dl.get(report_10k, tickers[tick], amount=1)
    dl.get(report_10q, tickers[tick], amount=1)
    santiment(tickers[tick])


print_emotions()

