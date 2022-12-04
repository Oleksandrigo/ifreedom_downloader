import os

from docx import Document
from docx.shared import RGBColor
from docx.text.paragraph import Paragraph
from htmldocx import HtmlToDocx

from requests import Response
from requests_html import HTMLSession, HTMLResponse, HTML


def parse_chapers(name_title: str, chapters: list[tuple[str, str]]):
    browser_args = [
        "--no-sandbox",
        "--disable-blink-features=AutomationControlled",
        "--ignore-certificate-errors"
    ]
    session = HTMLSession(browser_args=browser_args)
    doc_file = Document()
    new_parser = HtmlToDocx()

    for num, (name, url_chapt) in enumerate(chapters):
        os.system('cls||clear')
        print(f"{num + 1} / {len(chapters)}")

        chapter: HTMLResponse | Response = session.get(url_chapt)

        if chapter.status_code == 200:
            data = chapter.html.find("div.bun2")[0].find('article')[0]
            chapter_text = data.find("div.entry-content")[0]
            useless_data = chapter_text.find("div.pc-adv")
            for i in chapter_text.find("div.mob-adv"):
                useless_data.append(i)
            chapters_html = chapter_text.html
            for i in useless_data:
                chapters_html = chapters_html.replace(i.html, "")

            title_head: Paragraph = doc_file.add_heading(name, 1)
            title_head.style.font.color.rgb = RGBColor.from_string("000000")
            new_parser.add_html_to_document(chapters_html, doc_file)

        else:
            print("Произошла ошибка, страница скорее всего заблочена из-за слишком частых запросов.")
            print("Попробуйте еще раз, или сделайте issue на гитхабе")
            break

    doc_file.save(f'{name_title} Главы 1 - {len(chapters)}.docx')


def start_parse(link: str):
    print("Подготовка сессии")
    session = HTMLSession()
    print("Отправка запроса")
    res: HTMLResponse | Response = session.get(link)
    print("Получение названия и списка глав")
    title = res.html.find("div.column2 > h1")[0].text

    chapters = res.html.find("div.menu-ranobe")[0].find("a")
    chapters_arr = [(i.text, i.attrs.get("href")) for i in chapters]

    print("Начинаем парсинг глав!")
    parse_chapers(title, chapters_arr[::-1])
    print("Завершено!")


if __name__ == "__main__":
    # input_url = input("Введите ссылку на ранобе в ranobelib.me для парсинга.\n")
    input_url = "https://ifreedom.su/ranobe/rasputnyj-mag/"
    start_parse(input_url)
