import time
import requests


def request_handler(url, method, data=None, json=None, params=None, count=0,retry=5, **kwargs):
    '''
    :param url:url
    :param method: 方法
    :param data: data
    :param json:
    :param params: get使用 参数
    :param count: 初始计数器
    :param retry: 重试次数
    :param kwargs:
    :return: 响应对象  失败None
    '''
    try:
        if method == 'get':
            resp = requests.get(url, params=params, **kwargs)
            return resp
        elif method == 'post':
            resp = requests.post(url, data=data, json=json, **kwargs)
            return resp
        else:
            return '只支持post 和 get'
    except Exception as error:
        if count > retry:
            return None
        time.sleep(2)
        return request_handler(url, method, data=data, json=json, params=params, count=count + 1, **kwargs)


if __name__ == '__main__':
    payload = {'log_performance_metrics': 'true',
               'specs[async_search_results][]': 'Search2_ApiSpecs_WebSearch',
               'specs[async_search_results][1][search_request_params][detected_locale][language]': 'en-US',
               'specs[async_search_results][1][search_request_params][detected_locale][currency_code]': 'USD',
               'specs[async_search_results][1][search_request_params][detected_locale][region]': 'SG',
               'specs[async_search_results][1][search_request_params][locale][language]': 'en-GB',
               'specs[async_search_results][1][search_request_params][locale][currency_code]': 'SGD',
               'specs[async_search_results][1][search_request_params][locale][region]': 'SG',
               'specs[async_search_results][1][search_request_params][name_map][query]': 'q',
               'specs[async_search_results][1][search_request_params][name_map][query_type]': 'qt',
               'specs[async_search_results][1][search_request_params][name_map][results_per_page]': 'result_count',
               'specs[async_search_results][1][search_request_params][name_map][min_price]': 'min',
               'specs[async_search_results][1][search_request_params][name_map][max_price]': 'max',
               'specs[async_search_results][1][search_request_params][parameters][q]': 'hello',
               'specs[async_search_results][1][search_request_params][parameters][order]': 'highest_reviews',
               'specs[async_search_results][1][search_request_params][parameters][page]': 1,
               'specs[async_search_results][1][search_request_params][parameters][limit]': 500,
               'specs[async_search_results][1][search_request_params][parameters][referrer]': f'https://www.etsy.com/sg-en/search?q=hello&order=highest_reviews',
               'specs[async_search_results][1][search_request_params][parameters][ref]': 'pagination',
               'specs[async_search_results][1][search_request_params][parameters][is_prefetch]': 'false',
               'specs[async_search_results][1][search_request_params][parameters][placement]': 'wsg',
               'specs[async_search_results][1][search_request_params][user_id]': '',
               'specs[async_search_results][1][request_type]': 'filters',
               'view_data_event_name': 'search_async_pagination_specview_rendered'
               }
    headers = {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'no-cache',
        'content-length': '11267',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'cookie': 'uaid=vALdkia2LDfMgbYvPPW9-bGQNJpjZACCpE0le2B0tVJpYmaKkpVSrlFgfqR3UniOibNfinNQZpZfVGmUd1V5dkBWqFItAwA.; ; uaid=eo8-UWWho7xAS-creFRm5u_TK9hjZACCpE3la2B0tVJpYmaKkpVSRVhAaXKVmamRU0hVvpGXc2Wqv3-uf3pYaFhimFItAwA.; user_prefs=FZ-cYan82Z6w8l8cFDeSTb0FMvhjZACCpE3ly2F0dF5pTo4OeUQsAwA.',
        'origin': 'https://www.etsy.com',
        'pragma': 'no-cache',
        'referer': 'https://www.etsy.com/sg-en/search?q=stickers+sheet&ref=auto-1',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
        'x-csrf-token': '3:1655862479:r_1ks3WFT-zz5T4dRu4kKzTx56rS:daa2b8a629b5be452a4388373358215fe0e747873eb858438030c0796f3e2069',
        'x-detected-locale': 'SGD|en-GB|SG',
        'x-page-guid': 'f0f5af2e094.021fd51fd81ed8a3660d.00',
        'x-requested-with': 'XMLHttpRequest'
    }
    url = "https://www.etsy.com/api/v3/ajax/bespoke/member/neu/specs/search_async_recs"

    r = request_handler(url, method='post', headers=headers, data=payload, timeout=3,
                        proxies={'http': "http://127.0.0.1:7890", 'https': "http://127.0.0.1:7890"})
    print(r.json())
