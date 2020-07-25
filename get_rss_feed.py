import codecs
import datetime
import locale
import feedparser

URL = "https://blog.tubone-project24.xyz/rss.xml"


def get_rss(url):
    locale.setlocale(locale.LC_TIME, 'en_US.UTF-8')
    d = feedparser.parse(url)
    return [{"title": entry["title"], "link": entry["link"], "date": datetime.datetime.strptime(entry["published"], "%a, %d %b %Y %H:%M:%S %Z").strftime("%Y-%m-%d")} for entry in d["entries"]]


def generate_markdown(rss):
    header = "<table><tr><td valign=\"top\" width=\"100%\">\n\n### Blog Ratest Posts\n\n"
    contents = "\n\n".join(["- [" + x["title"] + "](" + x["link"] + ") - " + x["date"] for x in rss][0:5])
    footer = "\n\n</td></tr></table>"
    return header+contents+footer


def paste_markdown(content):
    with codecs.open("README.md", "r", "utf-8") as f:
        md = f.read()
        head = md.split("<!-- generate_markdown_start -->")[0]
        end = md.split("<!-- generate_markdown_end -->")[1]
    with codecs.open("README.md", "w", "utf-8") as f:
        f.write(head + "<!-- generate_markdown_start -->\n\n" + content + "\n\n<!-- generate_markdown_end -->" + end)


if __name__ == "__main__":
    content = generate_markdown(get_rss(URL))
    print(content)
    paste_markdown(content)
