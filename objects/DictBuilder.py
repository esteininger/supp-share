import xmltodict, json
from flask import Flask, Blueprint, render_template, request, jsonify, redirect, make_response, session, url_for
from objects.Items import Amazon


accesskey = 'AKIAJFIUWEJICEK25LMQ'
secretkey = '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'
associatetag = 'suppshare-20'

class DictBuilder:
    def __init__(self):
        pass

    def buildItemResult(self, keyword):
        amazon = Amazon(accesskey, secretkey, associatetag)
        xml = amazon.ItemSearch(Keywords=keyword, SearchIndex="All")
        parsedResult = xmltodict.parse(xml)

        items = parsedResult['ItemSearchResponse']['Items']

        itemsDict = []
        for key, value in items.iteritems():
            v = value
            itemsDict.append(v)

        # itemDict = []
        # for key, value in d.iteritems():
        #     print key, value

        return jsonify(itemsDict)
