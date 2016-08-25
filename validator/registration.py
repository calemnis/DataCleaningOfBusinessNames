#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import json

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

class Registration:

    def __init__(self, account_id, orb_num, alternative, country, ratio):
        if ratio > 1:
            ratio = 1.0
        ratio = round(ratio, 3)

        self.attributes = {'account_id': account_id, 'name': alternative, 'ratio': ratio, 'orb_num': orb_num, 'country': country}

    def __str__(self):
        return json.dumps(self.attributes)

    def __getitem__(self, item):
        return self.attributes[item]


