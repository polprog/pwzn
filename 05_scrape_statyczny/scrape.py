#!/usr/bin/env python3
import argparse
from bs4 import BeautifulSoup
import requests
import json
import time
target = "http://bash.org.pl/latest/"
version=1.0


def scrape(args):
    quotes = []
    sess = requests.Session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) Hehe (KHTML, like Gecko)'
    }
    nquotes = 0
    page = 1
    while nquotes < args.num_posts:
        response = requests.get(target + "?page=%d" % page, headers=headers)
        print(response.status_code)
        if response.status_code != 200:
            print("[ERR] Got response %d" % response.status_code)
        
        soup = BeautifulSoup(response.text, features="lxml")
        posts = soup.find_all(class_='post')
        for post in posts:
            quote = {}
            quote["id"]= post.find(class_="qid").text
            quote["text"] = post.find(class_="quote").text.strip()
            quote["date"] = post.find(class_="right").text.strip()

            quotes.append(quote)
            
            nquotes = nquotes + 1
            if(nquotes >= args.num_posts):
                break;
        time.sleep(1)  # bądźmi życzliwi
        page += 1
    return quotes

def dump_quotes(quotes):
    for q in quotes:
        print("\033[1;31m" + q["id"] + "\t\t\033[32m" + q["date"] + "\033[0m")
        print(q["text"])
        print("---"*10)
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='scrape',
        description='Scrape bash.org',
        epilog=f'pwzn23, version {version} ')
    parser.add_argument('-f', '--filename', default=None)
    parser.add_argument('-d', '--dump',
                        help="Dump quotes in human readable format to stdout instead. Pass -f - to dump JSON to stdout", action="store_true")
    parser.add_argument('-n', '--num-posts',
                        help="Number of latest posts to scrape",
                        default=10, type=int)
    args = parser.parse_args()

    quotes = scrape(args)
    if args.dump:
        dump_quotes(quotes)
    elif args.filename != None:
        if args.filename == "-":
            print(json.dumps(quotes))
        else:
            with open(args.filename, 'w') as f:
                json.dump(quotes, f)
