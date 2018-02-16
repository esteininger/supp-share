import xmltodict, json
from flask import Flask, Blueprint, render_template, request, jsonify, redirect, make_response, session, url_for
from objects.Items import Amazon
from objects.Utilities import Utilities

util = Utilities()

class DictBuilder:
    def __init__(self):
        pass

    def buildItemResult(self, keyword):
        amazon = Amazon(util.amazonKeys()['accesskey'], util.amazonKeys()['secretkey'], util.amazonKeys()['associatetag'])
        xml = amazon.ItemSearch(Keywords=keyword, SearchIndex="All")
        parsedResult = xmltodict.parse(xml)

        items = parsedResult['ItemSearchResponse']['Items']

        iteratedItems = items.iteritems()

        #need to fix this ugh
        next(iteratedItems)
        next(iteratedItems)
        next(iteratedItems)
        next(iteratedItems)


        itemsDict = []
        for key, value in iteratedItems:
            v = value
            itemsDict.append(v)

        # itemDict = []
        # for key, value in d.iteritems():
        #     print key, value

        return jsonify(itemsDict)
