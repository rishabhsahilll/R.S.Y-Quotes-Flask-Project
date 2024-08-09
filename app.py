'''
Developer Name:- RISHABH SAHIL
App:- R.S.Y | Quotes 
Version:- 1.9
'''

import requests
from flask import Flask, render_template
from bs4 import BeautifulSoup
import json
from googletrans import Translator
import os
import urllib.parse

app = Flask(__name__)

int_lang_var = ["en"]
authorname_2 = []

def rishabh_translate(text,lang="en"):
    lang = lang.replace("bho","hi").replace("sa","hi")
    try:
        translater =Translator()
        result = translater.translate(text=text,dest=lang)
        return result
    except:
        return text


def languages():
    LANGUAGES = {
        'af': 'afrikaans',
        'sq': 'albanian',
        'am': 'amharic',
        'ar': 'arabic',
        'hy': 'armenian',
        'az': 'azerbaijani',
        'eu': 'basque',
        'be': 'belarusian',
        'bn': 'bengali',
        'bho': 'bhojpuri',
        'bs': 'bosnian',
        'bg': 'bulgarian',
        'ca': 'catalan',
        'ceb': 'cebuano',
        'ny': 'chichewa',
        'zh-cn': 'chinese (simplified)',
        'zh-tw': 'chinese (traditional)',
        'co': 'corsican',
        'hr': 'croatian',
        'cs': 'czech',
        'da': 'danish',
        'nl': 'dutch',
        'en': 'english',
        'eo': 'esperanto',
        'et': 'estonian',
        'tl': 'filipino',
        'fi': 'finnish',
        'fr': 'french',
        'fy': 'frisian',
        'gl': 'galician',
        'ka': 'georgian',
        'de': 'german',
        'el': 'greek',
        'gu': 'gujarati',
        'ht': 'haitian creole',
        'ha': 'hausa',
        'haw': 'hawaiian',
        'iw': 'hebrew',
        'he': 'hebrew',
        'hi': 'hindi',
        'hmn': 'hmong',
        'hu': 'hungarian',
        'is': 'icelandic',
        'ig': 'igbo',
        'id': 'indonesian',
        'ga': 'irish',
        'it': 'italian',
        'ja': 'japanese',
        'jw': 'javanese',
        'kn': 'kannada',
        'kk': 'kazakh',
        'km': 'khmer',
        'ko': 'korean',
        'ku': 'kurdish (kurmanji)',
        'ky': 'kyrgyz',
        'lo': 'lao',
        'la': 'latin',
        'lv': 'latvian',
        'lt': 'lithuanian',
        'lb': 'luxembourgish',
        'mk': 'macedonian',
        'mg': 'malagasy',
        'ms': 'malay',
        'ml': 'malayalam',
        'mt': 'maltese',
        'mi': 'maori',
        'mr': 'marathi',
        'mn': 'mongolian',
        'my': 'myanmar (burmese)',
        'ne': 'nepali',
        'no': 'norwegian',
        'or': 'odia',
        'ps': 'pashto',
        'fa': 'persian',
        'pl': 'polish',
        'pt': 'portuguese',
        'pa': 'punjabi',
        'ro': 'romanian',
        'ru': 'russian',
        'sm': 'samoan',
        'sa': 'sanskrit',
        'gd': 'scots gaelic',
        'sr': 'serbian',
        'st': 'sesotho',
        'sn': 'shona',
        'sd': 'sindhi',
        'si': 'sinhala',
        'sk': 'slovak',
        'sl': 'slovenian',
        'so': 'somali',
        'es': 'spanish',
        'su': 'sundanese',
        'sw': 'swahili',
        'sv': 'swedish',
        'tg': 'tajik',
        'ta': 'tamil',
        'te': 'telugu',
        'th': 'thai',
        'tr': 'turkish',
        'uk': 'ukrainian',
        'ur': 'urdu',
        'ug': 'uyghur',
        'uz': 'uzbek',
        'vi': 'vietnamese',
        'cy': 'welsh',
        'xh': 'xhosa',
        'yi': 'yiddish',
        'yo': 'yoruba',
        'zu': 'zulu',
    }
    return LANGUAGES

@app.route('/')
def home():
    response = requests.get('https://zenquotes.io/api/quotes')
    data = response.json()
    data2 = []
    data3 = []
    s_quotes={
        "sharequotes": "none",
        "shared": "none",
        "shareauthor": "none"
    }
    for i in data:
        data3 = {
            'q': i['q'],
            'a': i['a']
        }
        data2.append(data3)
    response2 = requests.get('https://zenquotes.io/api/random/')
    randomq = response2.json()
    for j in randomq:
        random_data= {
            'q': rishabh_translate(j['q'],int_lang_var[-1]).text,
            'a': j['a']
        }
    trans_lang = {
            "translang": int_lang_var[-1]
        }
    for key in get_user_from_json().keys():
        for value in get_extra_quotes(key):
            # Ensure proper capitalization and splitting of author name
            author_parts = key.split('-')
            author_name = ' '.join(part.capitalize() for part in author_parts)
            data3 = {
                'q': value,
                'a': author_name
            }
            data2.append(data3)
    langs = languages()
    return render_template('index.html',s_quotes=s_quotes,random_data=random_data,data=data2,trans_lang=trans_lang,languages=langs)

def get_user_from_json():
    abs_path = os.path.join(os.path.dirname(__file__), 'quote-rs.json')
    with open(abs_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

@app.route('/quote/')
def quote():
    response = requests.get('https://zenquotes.io/api/quotes')
    data = response.json()
    data2 = []
    s_quotes={
        "sharequotes": "none",
        "sharelang": "none",
        "shareauthor": "none"
    }
    for key in get_user_from_json().keys():
        for value in get_extra_quotes(key):
            # Ensure proper capitalization and splitting of author name
            author_parts = key.split('-')
            author_name = ' '.join(part.capitalize() for part in author_parts)
            data3 = {
                'q': value,
                'a': author_name
            }
            data2.append(data3)
    for i in data:
        data3 = {
            'q': str(i['q']).replace("Too many requests. Obtain an auth key for unlimited access.","Please refresh the page"),
            'a': str(i['a']).replace("zenquotes.io","Bug 🐛")
        }
        data2.append(data3)
    response2 = requests.get('https://zenquotes.io/api/random/')
    randomq = response2.json()
    for j in randomq:
        random_data = {
            'q': rishabh_translate(
                str(j['q']).replace("Too many requests. Obtain an auth key for unlimited access.", "Please refresh the page"),
                int_lang_var[-1]
            ).text,
            'a': str(j['a']).replace("zenquotes.io", "Bug 🐛")
        }
    trans_lang = {
            "translang": int_lang_var[-1]
        }
    langs = languages()
    return render_template('index.html',s_quotes=s_quotes,random_data=random_data,data=data2,languages=langs,trans_lang=trans_lang)

@app.route('/quote/<lang>')
def hindi_qoute(lang):
    int_lang_var.append(lang)
    response = requests.get('https://zenquotes.io/api/quotes')
    data = response.json()
    data2 = []
    s_quotes={
        "sharequotes": "none",
        "shared":"none",
        "shareauthor": "none"
    }
    for i in data:
        data3 = {
            'q': str(i['q']).replace("Too many requests. Obtain an auth key for unlimited access.","Please refresh the page"),
            'a': str(i['a']).replace("zenquotes.io","Bug 🐛")
        }
        data2.append(data3)
        
        trans_lang = {
            "translang": int_lang_var[-1]
        }
    for key in get_user_from_json().keys():
        for value in get_extra_quotes(key):
            # Ensure proper capitalization and splitting of author name
            author_parts = key.split('-')
            author_name = ' '.join(part.capitalize() for part in author_parts)
            data3 = {
                'q': value,
                'a': author_name
            }
            data2.append(data3)
    response2 = requests.get('https://zenquotes.io/api/random/')
    randomq = response2.json()
    for j in randomq:
        random_data = {
            'q': rishabh_translate(
                str(j['q']).replace("Too many requests. Obtain an auth key for unlimited access.", "Please refresh the page"),
                int_lang_var[-1]
            ).text,
            'a': str(j['a']).replace("zenquotes.io", "Bug 🐛")
        }
    langs = languages()
    return render_template('quote_hi.html',s_quotes=s_quotes,random_data=random_data,data=data2,languages=langs,trans_lang=trans_lang)

@app.route('/authors')
def author():

    api_url = 'https://zenquotes.io/authors'
    
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            author_cards = soup.select('.card-body.text-center.h-100')
            authors = []

            for card in author_cards:
                author_link = card.find('a', class_='stretched-link')['href']
                author_img = card.find('img')['src']
                author_name = card.find('h6').text.strip()

                quote_data = {
                    'authorLink': author_link.replace("..","").replace("authors",""),
                    'authorImg': author_img,
                    'author': author_name
                }
                authors.append(quote_data)
                
            trans_lang = {
                "translang": int_lang_var[-1]
            }
            langs = languages()
            return render_template('authors.html', authors=authors,trans_lang=trans_lang,languages=langs)
        else:
            return 'Failed to fetch quotes'
    except requests.exceptions.RequestException as e:
        return f'Error fetching quotes: {str(e)}'

def user_data_get(authorname):
    authorname = str(authorname).replace("rishabh-sahil","unknown")
    # Define the URL
    url = f"https://zenquotes.io/authors/{authorname}"

    # Send a GET request to fetch the HTML content
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Find all the author cards
    author_cards = soup.find_all("div", class_="card shadow-sm card-body text-center h-100")

    # Initialize an empty list to store author data
    authors_data = []
    count = 0
    # Loop through each author card and extract information
    for card in author_cards:
        if count>0:
            author_name = card.find("h6").text.strip()
            author_url = card.find("a")["href"].strip("../")
            
            # Check if the img tag is present
            author_image_tag = card.find("img")
            if author_image_tag:
                author_image = author_image_tag["src"].strip()
            # else:
            #     author_image = None  # or any default image URL you want to set

            # Create a dictionary for the current author
            author_dict = {
                "author_name": str(author_name),
                "author_url": str(author_url).replace("..","").replace("authors",""),
                "author_image": author_image
            }
            
            # Append the dictionary to the list
            authors_data.append(author_dict)
            # Increment the counter
        count += 1
            
            # Check if we have reached 12 authors, then break the loop
        if count >= 12:
            break

    # Print the list of dictionaries
    return authors_data

def get_extra_quotes(authorname):
    abs_path = os.path.join(os.path.dirname(__file__), 'quote-rs.json')
    with open(abs_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        extra_quotes = data.get(authorname, [])
    return extra_quotes

@app.route('/quote/authors/<authorname>/<language>')
def author_details(authorname,language):
    quotes = []
    authorname_2.append(authorname)
    int_lang_var.append(language)
    authorlink = str(authorname).replace("-"," ")
    if str(authorname_2[-1]) == "rishabh-sahil":
        for quote in get_extra_quotes(authorname_2[-1]):
            # print(quote)
            quote_data = {
                'authorquote': f"‶{quote}‶",
                'authortiwt': f'{authorlink.capitalize()}',
            }
            quotes.append(quote_data)
    else:
        for quote in get_extra_quotes(authorname_2[-1]):
            # print(quote)
            quote_data = {
                'authorquote': f"‶{quote}‶",
                'authortiwt': f'{authorlink.capitalize()}',
            }
            quotes.append(quote_data)
            print(quotes)
    language = "en"
    # print(authorname_2)

    try:
        api_url = f'https://zenquotes.io/authors/{str(authorname_2[-1]).replace("rishabh-sahil","unknown")}'
        response = requests.get(api_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            author_card = soup.find('div', class_='card shadow-sm card-body text-center h-100')
            author_cards = soup.select('.card.shadow-sm.card-body.text-center.p-3.h-100.quote-block')
            for card in author_cards:
                author_quote = card.find('blockquote').text.strip()
                author_twitlink = card.find('a')['href']
                # print(author_twitlink)
                quote_data = {
                        'authorquote': author_quote,
                        'authortiwt': f'{authorlink.capitalize()}',
                    }
                quotes.append(quote_data)
                # print(quotes)

            if author_card:
                author_name = author_card.find('h1').text.strip()
                author_img = author_card.find('img')['src']
                author_details = {
                    "author_name": author_name,
                    "author_img": author_img
                }
                trans_lang = {"translang": int_lang_var[-1]}  # Example translation language
                langs = languages()
                authors = user_data_get(authorname)
                auth_name={"author_name":authorname_2[-1]}
                linkoutput={"authlink":f"{authorname_2[-1]}/{int_lang_var[-1]}"}
                # print(auth_name)
                return render_template('author_details.html', linkoutput=linkoutput, auth_name=auth_name,authors=authors, author_details=author_details, trans_lang=trans_lang, languages=langs,quotes=quotes)
            else:
                author_details = {
                    "author_name": "No Data",
                    "author_img": "#"
                }
        else:
            print(f"Failed to retrieve data. Status code: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")

    trans_lang = {"translang": int_lang_var[-1]}  # Example translation language
    langs = languages()
    authors = user_data_get(authorname)
    auth_name={"author_name":authorname_2[-1]}
    linkoutput={"authlink":f"{authorname_2[-1]}/{int_lang_var[-1]}"}
    # print(auth_name)
    return render_template('author_details.html', linkoutput=linkoutput, auth_name=auth_name,authors=authors, author_details=author_details, trans_lang=trans_lang, languages=langs,quotes=quotes)

#  Share Function

@app.route('/quote/<shareauthor>/<sharequotes>/<lang>')
def share_quote(shareauthor,sharequotes,lang):
    response = requests.get('https://zenquotes.io/api/quotes')
    data = response.json()
    # print(shareauthor)
    data2 = []
    int_lang_var.append(lang)
    if str(shareauthor)=="rishabh-sahil" or str(shareauthor) == "Rishabh Sahil":
        s_quotes={
            "sharequotes": sharequotes,
            "sharedlang":int_lang_var[-1],
            "shareauthor": "Rishabh Sahil",
            "link": f"/quote/authors/rishabh-sahil/{lang}"
        }
    else:
        authorlink = str(shareauthor).replace(" ","-").lower()
        s_quotes={
            "sharequotes": sharequotes,
            "sharedlang":int_lang_var[-1],
            "shareauthor": shareauthor,
            "link": f"/quote/authors/{authorlink}/{lang}"
        }
    for i in data:
        data3 = {
            'q': str(i['q']).replace("Too many requests. Obtain an auth key for unlimited access.","Please refresh the page"),
            'a': str(i['a']).replace("zenquotes.io","Bug 🐛")
        }
        data2.append(data3)
    response2 = requests.get('https://zenquotes.io/api/random/')
    randomq = response2.json()
    for j in randomq:
        random_data = {
            'q': rishabh_translate(
                str(j['q']).replace("Too many requests. Obtain an auth key for unlimited access.", "Please refresh the page"),
                lang
            ).text,
            'a': str(j['a']).replace("zenquotes.io", "Bug 🐛")
        }
    trans_lang = {
            "translang": int_lang_var[-1]
        }
    langs = languages()
    return render_template('share-quotes.html',s_quotes=s_quotes,random_data=random_data,data=data2,languages=langs,trans_lang=trans_lang)


if __name__ == '__main__':
    app.run(debug=True)
