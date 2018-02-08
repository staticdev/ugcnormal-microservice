#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify
from normalizer import Normalizer

APP = Flask(__name__)
APP.config['JSON_AS_ASCII'] = False # retrieve UTF-8 messages

NORM = Normalizer()

@APP.route('/reply', methods=['POST'])
def reply():
    params = request.json
    if not params:
        return jsonify({
            "status": "error",
            "error": "Request must be of the application/json type!",
        })

    message = params.get("message")
    method = params.get("method")

    # Make sure the required params are present.
    if message is None or method is None:
        return jsonify({
            "status": "error",
            "error": "message and method are required keys"
        })

    methods = {'token':NORM.tokenizer,
               'spell':NORM.speller,
               'acronym':NORM.acronym_searcher,
               'textese':NORM.untextese,
               'proper_noun':NORM.proper_noun_normalizer
              }

    try:
        reply = methods[method](message)
    except KeyError:
        return jsonify({
            "status": "error",
            "error": "method not valid, try one of the following: token, spell, acronym, textese or proper_noun"
        })

    # Send the response.
    return jsonify({
        "status": "ok",
        "reply": reply
    })
