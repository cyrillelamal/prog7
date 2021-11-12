import re
from collections import namedtuple

import requests
from bs4 import BeautifulSoup
from bs4.element import Tag
from natasha import NewsNERTagger, Doc, NewsEmbedding, Segmenter, NewsMorphTagger, NewsSyntaxParser, PER, ORG
from natasha.doc import DocSpan

ENTRY = 'https://www.herzen.spb.ru/main/facts/nowadays/1558542985/1559574321/'

Page = namedtuple('Page', ['uri', 'html'])
Article = namedtuple('Article', ['uri', 'content'])
TermPack = namedtuple('TermPack', ['article', 'terms'])


def main():
    entry = get_page_content(ENTRY)
    container = get_news_container(entry)

    uris = map(get_href, container.children)
    uris = filter(lambda href: href, uris)

    pages = map(lambda uri: Page(uri, get_page_content(uri)), uris)
    articles = map(lambda page: Article(page.uri, get_article_content(page.html)), pages)

    term_packs = map(lambda article: TermPack(article, extract_crucial_terms(article.content)), articles)

    for pack in term_packs:
        print(pack.terms)

        exit()


def get_page_content(uri: str) -> str:
    response = requests.get(uri)
    response.raise_for_status()
    return response.text


def get_news_container(html: str) -> Tag:
    soup = BeautifulSoup(html, 'html.parser')
    return soup.select('img[src="/uploads/nabrinken/images/news3.jpg"]')[0].parent.parent


def get_href(tag: Tag) -> str:
    txt = str(tag.get_text)
    return parse_href(txt)


def parse_href(html: str) -> str:
    m = re.search(r'<a.*?href="(?P<href>.+?)".*?>.*?</a>', html)
    return '' if m is None else m.group('href')


def get_article_content(html: str) -> str:
    return get_article_container(html).text


def get_article_container(html: str) -> Tag:
    soup = BeautifulSoup(html, 'html.parser')
    return soup.select('td.blockwh')[0]


def extract_crucial_terms(text: str) -> list:
    emb = NewsEmbedding()
    seg = Segmenter()

    doc = Doc(text)
    doc.segment(seg)
    doc.tag_morph(NewsMorphTagger(emb))
    doc.parse_syntax(NewsSyntaxParser(emb))
    doc.tag_ner(NewsNERTagger(emb))

    doc.segment(seg)

    return [
        span.text
        for span in doc.spans  # type: DocSpan
        if span.type in [PER, ORG]
    ]


if __name__ == '__main__':
    main()
