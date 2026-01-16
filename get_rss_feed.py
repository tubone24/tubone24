import codecs
import datetime
import locale
import feedparser

RSS_FEEDS = {
    "blog": "https://blog.tubone-project24.xyz/rss.xml",
    "slides": "https://slide-tubone24.pages.dev/rss.xml"
}

PUBLICATIONS = [
    {"title": "やさしいMCP入門", "link": "https://amzn.asia/d/8MyBrsM", "date": "2025/7/1"},
    {"title": "AIエージェント開発／運用入門 ［生成AI深掘りガイド］", "link": "https://amzn.asia/d/4vElt0i", "date": "2025/10/1"},
]

def get_rss(url):
    """指定したURLからRSSフィードを取得し、必要な情報を抽出します"""
    try:
        locale.setlocale(locale.LC_TIME, 'en_US.UTF-8')
    except locale.Error:
        pass
    
    d = feedparser.parse(url)
    results = []
    
    for entry in d.entries:
        if 'published' in entry:
            try:
                date = datetime.datetime.strptime(entry.published, "%a, %d %b %Y %H:%M:%S %Z")
            except ValueError:
                try:
                    date = datetime.datetime.strptime(entry.published, "%Y-%m-%dT%H:%M:%S%z")
                except ValueError:
                    date = datetime.datetime.now()
        else:
            date = datetime.datetime.now()
        
        formatted_date = date.strftime("%Y-%m-%d")
        
        results.append({
            "title": entry.title,
            "link": entry.link,
            "date": formatted_date
        })
    
    return results

def generate_markdown(rss_dict):
    """すべてのRSSフィードのマークダウンを生成します"""
    header = "<table><tr><td valign=\"top\" width=\"100%\">\n\n"
    content = ""

    # Publications section
    content += "### Publications\n\n"
    for item in PUBLICATIONS:
        content += f"- [{item['title']}]({item['link']}) - {item['date']}\n"
    content += "\n"

    for feed_title, feed_items in rss_dict.items():
        content += f"### {feed_title.capitalize()} Latest Posts\n\n"
        # 各フィードの最大5つの項目を一覧表示
        for item in feed_items[:5]:
            content += f"- [{item['title']}]({item['link']}) - {item['date']}\n"
        content += "\n"

    footer = "</td></tr></table>"
    return header + content + footer

def paste_markdown(content):
    """生成したマークダウンをREADME.mdファイルに挿入します"""
    with codecs.open("README.md", "r", "utf-8") as f:
        md = f.read()
        head = md.split("<!-- generate_markdown_start -->")[0]
        end = md.split("<!-- generate_markdown_end -->")[1]
    with codecs.open("README.md", "w", "utf-8") as f:
        f.write(head + "<!-- generate_markdown_start -->\n\n" + content + "\n\n<!-- generate_markdown_end -->" + end)

if __name__ == "__main__":
    rss_items = {}
    for feed_name, feed_url in RSS_FEEDS.items():
        rss_items[feed_name] = get_rss(feed_url)
    
    content = generate_markdown(rss_items)
    print(content)
    paste_markdown(content)
