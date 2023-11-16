from flask import Flask, render_template, request
from bs4 import BeautifulSoup
import requests
import os
from docx import Document

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def scrape_and_save():
    url = request.form['url']

    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        p_tags = soup.find_all(['p', 'h1','ul'])

        text = "\n".join(tag.get_text() for tag in p_tags)
        # all_text = "\n".join(soup.stripped_strings)
        # p_tags = soup.find_all(['p', 'h1'])
        # text = "\n".join(tag.get_text() for tag in p_tags)

        output_file = "scraped_text.docx"

        # with open(output_file, 'w', encoding='utf-8') as file:
        #     file.write(text)
        document = Document()
        document.add_paragraph(text)
        document.save(output_file)

        return f"Text extracted and saved to {output_file}"
    else:
        return f"Failed to retrieve the web page. Status code: {response.status_code}"

if __name__ == '__main__':
    app.run()
