#!/usr/bin/env ./.venv/bin/python3

import argparse
import os
import re
import bs4.element
import requests
from bs4 import BeautifulSoup
from htmlBuilder.attributes import Class as ClassNames, Href, Style as StyleAttr
from htmlBuilder.tags import *
from pypinyin import lazy_pinyin, Style as PYStyle

from chinese.dictionary import LookupResult
from classes import ChineseInfo
from traditionalorsimplified import is_traditional

JS_FILE = "handlers.js"

chinese_info = ChineseInfo(traditional=False)
def build_content(lines):
    content = Div()
    for line in lines:
        content.inner_html.append(build_line(line))
    return [content]

def build_line(s: list[str]) -> list[HtmlTag]:
    container = Div([ClassNames("line")])
    chinese_result = chinese_info.lookup(s)
    for el in chinese_result.tokens(details=True):
        token = el[0]
        container.inner_html.append(build_word(chinese_result, token))
    return container

def build_word(info, token: str) -> HtmlTag:
    word_box = Span([ClassNames("word")])
    detail_box = Div([ClassNames("details hidden")])
    detail_box.inner_html.append(Div([ClassNames("char")], token))
    detail_box.inner_html.append(Div([ClassNames("py")], lazy_pinyin(token, style=PYStyle.TONE, errors=lambda x: [c for c in x])))
    detail_box.inner_html.append(Div([ClassNames("def")], build_definition_section(info[token][0].definitions)))
    word_box.inner_html.append(Span([ClassNames("text")], token))
    word_box.inner_html.append(detail_box)
    return word_box

def build_definition_section(definitions: list[LookupResult]) -> HtmlTag:
    def_list = Ul()
    for definition in definitions:
        def_list.inner_html.append(Li([], definition))
    return def_list

def main():
    parser = argparse.ArgumentParser(description="This program takes a book id appropriate to sto.cx, and outputs an html page with chinese pinyin for the contents of the book.")
    parser.add_argument("book_id", help="A book id to be used with sto.cx to get chinese textual data.")
    args = parser.parse_args()

    BASE_URL = "https://sto.cx"
    START_URL = "/".join([BASE_URL, f"book-{args.book_id}-1.html"])
    OUTPUT_FOLDER = "out"
    HEADERS_MAP = {
        "accept": '*',
        "user-agent": "Mozilla/5.0"
    }
    page = requests.get(START_URL, headers=HEADERS_MAP)
    if page.status_code != 200:
        raise Exception(f"The page didn't return the book's text, page instead returned status code {page.status_code}")
    soup = BeautifulSoup(page.text, 'html.parser')
    title = soup.select(".bookbox")[0].select("h1")[0].text
    book_links = soup.select(".paginator")[0].select("a")
    last_page_link = book_links[len(book_links) - 1].get("href")
    page_num_regex = re.compile(r"-(\d+)\.")
    last_page_number = int(page_num_regex.findall(last_page_link)[0])
    # Determines whether a piece is in traditional and sets ChineseInfo to it
    text = soup.select("#BookContent")[0]
    if not text:
        raise Exception("Could not get data from page.")
    for tag in text:
        potential_str = str(tag.string)
        if type(tag) == bs4.element.NavigableString and potential_str != None and potential_str != "\n" and potential_str != " ":
            chinese_info.traditional = is_traditional(potential_str)
            break

    links_to_other_pages = Div()
    for i in range(1, last_page_number + 1):
        filename = f"{args.book_id}-{i:02}.html"
        a = A([
            Href("/".join([".", filename]))
        ], Text(f"{i:02}"))
        links_to_other_pages.inner_html.append(a)

    for i in range(1, last_page_number + 1):
        url = "/".join([BASE_URL, f"book-{args.book_id}-{i}.html"])
        page = requests.get(url, headers=HEADERS_MAP)
        if page.status_code != 200:
            raise Exception(f"The page didn't return the book's text, page instead returned status code {page.status_code}")
        soup = BeautifulSoup(page.text, 'html.parser')
        text = soup.select("#BookContent")[0]
        cleaned = []
        for tag in text:
            potential_str = str(tag.string)
            if type(tag) == bs4.element.NavigableString and potential_str != None and potential_str != "\n" and potential_str != " ":
                cleaned.append(potential_str)

        body = Body([StyleAttr("font-size: 1.6rem")])
        body.inner_html.append(links_to_other_pages)
        for element in iter(build_content(cleaned)):
                body.inner_html.append(element)
        body.inner_html.append(links_to_other_pages)
        with open("/".join([os.getcwd(), 'src', JS_FILE])) as javascript_file:
            buffer = javascript_file.read()
            body.inner_html.append(Script([], buffer))
        
        html =  Html([], 
                    Head([],
                        Title([],
                            Text(f"{title} - Page {i}"))),
                        Style([], '''
ul {
    padding: 0 0 0 20px;
    margin: 3px 0;
    list-style-type: decimal;
}
.line {
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
}
div.def {
    max-width: 8rem;
    max-height: 8rem;
    overflow: hidden;
}
.details {
    font-size: 1rem;
    border: 1px solid gray;
    border-radius: 5px;
    position: absolute;
    pointer-events: none;
    padding: 5px 12px;
    max-width: 40%;
    background-color: white;
    box-shadow: 3px 3px gray;
}
.hidden {
    visibility: hidden;
}
                            '''),
                    body)
        
        filename = f"{args.book_id}-{i:02}.html"
        with open("/".join([".", OUTPUT_FOLDER, filename]), mode="x") as out:
            out.write(html.render(doctype=True, pretty=True))
            
if __name__ == "__main__":
    main()