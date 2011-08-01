#!/usr/bin/env python
# -*- coding: utf-8 -*-
from kindleclippingsparser import KindleClippingsParser
from cgi import escape
from sys import argv, stdin


pars = KindleClippingsParser(stdin)
foo = pars.parse()
results = dict()


if len(argv) > 1 and argv[1]:
    search_title = unicode()
    search_title=argv[1].decode("utf-8")
else:
    search_title = None

def select_query(a, search_title):
    if search_title:
        from Levenshtein import ratio as ratio
        return (ratio(a['title'].encode("utf-8"),
                      search_title.encode("utf-8")) > 0.50) \
                      and a['text'] and a['author'] \
                      and a['location'] and a['type'] == "Highlight"
    else:
        return a['title'] and a['text'] \
               and a['author'] and a['location'] \
               and a['type'] == "Highlight"
    

for a in foo:
    if select_query(a, search_title):
        if not a.get('author').encode("utf-8") in results:
            results[a.get('author').encode("utf-8")] = {a['title'].encode("utf-8"):
                                    [(a['text'].encode("utf-8"),
                                     a['location'].encode("utf-8"))]}
        elif not a['title'].encode("utf-8") in results[a.get('author').encode("utf-8")]:
            results[a['author'].encode("utf-8")][a['title'.encode("utf-8")]] = [(a['text'].encode("utf-8"),
                                     a['location'].encode("utf-8"))]

        else:
            results[a.get('author').encode("utf-8")][a.get('title').encode("utf-8")] += [(a['text'].encode("utf-8"),
                                     a['location'].encode("utf-8"))]

print '''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <meta http-equiv="Content-Type" content="text/html;charset=utf-8" />
    <title>Clippings from Kindle</title>
</head>
<body>
'''
for author, work in results.iteritems():
    #print author
    print "<h2>%s</h2>" % escape(author)
    for title, location_texts in work.iteritems():
        print "<h3>%s</h3>" % escape(title)
        for text, location in location_texts:
            print "<blockquote><p>%s (%s)</p></blockquote>" % (escape(text), escape(location))
print "</body></html>"


        # print "<blockquote>%s (%s, »%s«, %s)</blockquote>\n" % (a['text'].encode("utf-8"),
        #                              a['author'].encode("utf-8"),
        #                              a['title'].encode("utf-8"),
        #                              a['location'].encode("utf-8"))
