import feedparser
import bs4
import telepot
import sys
import shelve

url = "http://elcomidista.elpais.com/rss/elcomidista/portada.xml"
rss = feedparser.parse(url)
TOKEN = sys.argv[1]
bot = telepot.Bot(TOKEN)
data = shelve.open("elcomidista_data", writeback=True)

channel_id = sys.argv[2]

for entry in rss['entries'][0:4]:
    if entry['id'] not in data['sent_messages']:
        message = "*" + entry['title'] + "*[.](" + entry['links'][1]['href'] + ") (por " + entry['author'] + ")"
        tags = []
        for tag in entry['tags']:
            tags.append("[" + tag['term'] + "](http://elcomidista.elpais.com/r/elcomidista/tag/" + tag['term'].lower().replace(" ", "_") + "/a/)")
        message += "\n\n*Etiquetas*: " + ", ".join(tags) + "\n"
        message += entry['summary']
        message += " [Comentarios](" + entry['comments'] + ")"
        summary_text = bs4.BeautifulSoup(entry['content'][0]['value'], "lxml")
        message += "\n\n" + summary_text.find_all('p')[0].text
        message += " [(Seguir leyendo...)](" + entry['id'] + ")" + "\n\n"
        message += "_Publicado el " + entry['published'] + "_"
        res = bot.sendMessage(channel_id, message, parse_mode="markdown")
        msg_id = telepot.message_identifier(res)
        data['sent_messages'][entry['id']] = msg_id
    else:
        pass
data.close()
