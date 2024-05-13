# wbxhzsjwzxhn

Forked from jrmy1/wbxhzshwzxhn

This project reads chinese books from 'sto.cx', parses them, and outputs static html files with the following functionality:

- Chinese text found on the page is parsed into Chinese tokens
- Pinyin of the found token
- A translation of found tokens in the chinese text

### Instructions
1. Clone repo
2. `pip install`
3. `python3 ./src/script.py $book` where $book is the number of a book found on 'sto.cx'
4. Output files are found at ./out/