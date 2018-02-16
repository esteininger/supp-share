from flask import Flask, Blueprint, render_template, request, jsonify, redirect, make_response, session, url_for
import xmltodict, json

from objects.DictBuilder import DictBuilder

dictBuilder = DictBuilder()

app_api = Blueprint('app_api', __name__)

@app_api.route('/api/items/search/<keyword>', methods=['GET'])
def getProductByKeyword(keyword):
    print dictBuilder.buildItemResult(keyword)
    return dictBuilder.buildItemResult(keyword)
