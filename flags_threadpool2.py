#!/usr/bin/env python
# -*- coding: utf-8 -*-
import collections
from concurrent import  futures

import requests.exceptions

from test3 import save_flag,get_flag,show,main

MAX_WORKERS = 1000

def download_many(cc_list,base_url,verbose,concur_req):
    counter = collections.Counter()

    with futures.ThreadPoolExecutor(max_workers=concur_req) as executor:
        to_do_map = {}
        for cc in sorted(cc_list):
            future = executor.submit(download_one,cc,base_url,verbose)
            to_do_map[future] = cc
        done_iter = future.as_completed(to_do_map)
        if not verbose:
            done_iter = tqdm.tqdm(done_iter,total=len(cc_list))
        for future in done_iter:
            try:
                res = future.result()
            except requests.exceptions.HTTPError as exc:
                error_msg = 'HTTP {res.status_code} - {res.reson}'
                error_msg = error_msg.format(res=exc.response)
            except requests.exceptions.ConnectionError as exc:
                error_msg = 'Connection error'
            else:
                error_msg = ''
                status = res.status
            if error_msg:
                status = HTTPStatus.error
            counter[status] +=1
            if verbose and error_msg:
                cc = to_do_map[future]
                #