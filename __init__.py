#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify
from normalizer import Normalizer

def create_app(test_config=None):
    app = Flask(__name__)
    app.config['JSON_AS_ASCII'] = False # retrieve UTF-8 messages

    norm = Normalizer()

    @app.route('/reply', methods=['POST'])
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

        methods = {'token':norm.tokenizer,
                'spell':norm.speller,
                'acronym':norm.acronym_searcher,
                'textese':norm.untextese,
                'proper_noun':norm.proper_noun_normalizer
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

    return app