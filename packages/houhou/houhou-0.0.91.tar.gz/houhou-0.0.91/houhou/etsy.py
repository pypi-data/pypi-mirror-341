"""
etsy
   获取 关键词产品
        店铺产品
        店铺集合
        产品详情
        产品评论
"""

from lxml import etree
import re
from houhou.request_handler import request_handler


class Etsy():
    def __init__(self, title, search_type='search', proxies=None):
        '''
        :param title: 名称  搜索关键词  店铺名
        :param search_type: 类型   search 或者 shop  分别为 搜索关键词和店铺
        :param proxies: 代理
        :param need_html: 是否需要 html
        '''
        self.title = title
        self.search_type = search_type
        self.proxies = proxies

    def get_search_products(self, page):
        '''
        :param page: 页码
        :return: 返回产品列表   产品详细信息 json
        '''
        data = {
            'code': 0,
            'msg': '',
            'total_count': 0,
            'total_pages': 0,
            'goods_data': [],
        }
        goods_list = []
        # 判断类型
        if self.search_type != 'search':
            data['msg'] = '如果想搜索关键词 search_type为 search'
            return data
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
                   'specs[async_search_results][1][search_request_params][parameters][q]': self.title,
                   'specs[async_search_results][1][search_request_params][parameters][order]': 'highest_reviews',
                   'specs[async_search_results][1][search_request_params][parameters][page]': str(page),
                   'specs[async_search_results][1][search_request_params][parameters][limit]': 500,
                   'specs[async_search_results][1][search_request_params][parameters][referrer]': f'https://www.etsy.com/sg-en/search?q={self.title}&order=highest_reviews',
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
        url1 = "https://www.etsy.com/api/v3/ajax/bespoke/member/neu/specs/async_search_results"
        url = "https://www.etsy.com/api/v3/ajax/bespoke/member/neu/specs/search_async_recs"

        try:
            # 获取listid
            if self.proxies == None:
                resp = request_handler(url1, method='post', headers=headers, data=payload, retry=10,timeout=10)
            else:
                resp = request_handler(url1, method='post', headers=headers, data=payload, retry=10, timeout=10,proxies=self.proxies)

            if resp == None:
                data['msg'] = '获取listing_ids 失败'
                return data

            # 获取返回的id信息
            e = etree.HTML(resp.json()['output']['async_search_results'])

            current_html_goods = e.xpath('//li')
            if current_html_goods == []:
                data['code'] = 1
                data['msg'] = '没有产品'
                return data

            # 将返回数据直接放入产品列表中
            for good in current_html_goods:
                try:
                    good_id = good.xpath('.//a/@data-listing-id')[0]
                    shop_id = good.xpath('.//a/@data-shop-id')[0]
                    html = etree.tostring(good, encoding='utf-8').decode()
                    goods_list.append({'good_id': good_id, 'shop_id': shop_id, 'html': html})
                except Exception as error:
                    pass
            listing_ids = resp.json()['jsData'].get('lazy_loaded_listing_ids')
            logging_ids = resp.json()['jsData'].get('lazy_loaded_logging_keys')
            ad_ids = resp.json()['jsData'].get('lazy_loaded_ad_ids')
            total_count = resp.json()['jsData'].get('organic_listings_count')
            total_pages = resp.json()['jsData'].get('total_pages')
            if total_count != None:
                data['total_count'] = total_count
                data['total_pages'] = total_pages

            if listing_ids == None or listing_ids == []:
                data['code'] = 1
                data['goods_data'] = goods_list
                data['msg'] = ''
                return data

            # 获取所有产品列表的html

            payload = {'log_performance_metrics': 'true',
                       'specs[listingCards][]': 'Search2_ApiSpecs_LazyListingCards',
                       'specs[listingCards][1][listing_ids][]': listing_ids,
                       'specs[listingCards][1][ad_ids][]': ad_ids,
                       'specs[listingCards][1][logging_keys][]': logging_ids,
                       'specs[listingCards][1][search_request_params][detected_locale][language]': 'en-GB',
                       'specs[listingCards][1][search_request_params][detected_locale][currency_code]': 'SGD',
                       'specs[listingCards][1][search_request_params][detected_locale][region]': 'SG',
                       'specs[listingCards][1][search_request_params][locale][language]': 'en-GB',
                       'specs[listingCards][1][search_request_params][locale][currency_code]': 'SGD',
                       'specs[listingCards][1][search_request_params][locale][region]': 'SG',
                       'specs[listingCards][1][search_request_params][name_map][query]': 'q',
                       'specs[listingCards][1][search_request_params][name_map][query_type]': 'qt',
                       'specs[listingCards][1][search_request_params][name_map][results_per_page]': 'result_count',
                       'specs[listingCards][1][search_request_params][name_map][min_price]': 'min',
                       'specs[listingCards][1][search_request_params][name_map][max_price]': 'max',
                       'specs[listingCards][1][search_request_params][parameters][q]': self.title,
                       'specs[listingCards][1][search_request_params][parameters][order]': 'highest_reviews',
                       'specs[listingCards][1][search_request_params][parameters][page]': page,
                       'specs[listingCards][1][search_request_params][parameters][referrer]': f'https://www.etsy.com/sg-en/search?q={self.title}&order=highest_reviews',
                       'specs[listingCards][1][search_request_params][parameters][ref]': '',
                       'specs[listingCards][1][search_request_params][parameters][is_prefetch]': 'false',
                       'specs[listingCards][1][search_request_params][parameters][placement]': 'wsg',
                       'specs[listingCards][1][search_request_params][parameters][page_type]': 'search',
                       'specs[listingCards][1][search_request_params][parameters][bucket_id]': 'k1M5HHCMa8yjo4Lfsko2W-EL_pGl',
                       'specs[listingCards][1][search_request_params][parameters][user_id]': '',
                       'specs[listingCards][1][search_request_params][parameters][eligibility_map][app_os_version]': '',
                       'specs[listingCards][1][search_request_params][parameters][eligibility_map][app_version]': '',
                       'specs[listingCards][1][search_request_params][parameters][eligibility_map][currency]': 'SGD',
                       'specs[listingCards][1][search_request_params][parameters][eligibility_map][device]': '1,0,0,0,0,0,0,0,0,0,0,0,0,0',
                       'specs[listingCards][1][search_request_params][parameters][eligibility_map][environment]': '',
                       'specs[listingCards][1][search_request_params][parameters][eligibility_map][favorited]': '',
                       'specs[listingCards][1][search_request_params][parameters][eligibility_map][first_visit]': '',
                       'specs[listingCards][1][search_request_params][parameters][eligibility_map][http_referrer]': '',
                       'specs[listingCards][1][search_request_params][parameters][eligibility_map][language]': 'en-GB',
                       'specs[listingCards][1][search_request_params][parameters][eligibility_map][last_login]': '',
                       'specs[listingCards][1][search_request_params][parameters][eligibility_map][purchases_awaiting_review]': '',
                       'specs[listingCards][1][search_request_params][parameters][eligibility_map][push_notification_settings]': '',
                       'specs[listingCards][1][search_request_params][parameters][eligibility_map][region]': 'SG',
                       'specs[listingCards][1][search_request_params][parameters][eligibility_map][region_language_match]': '',
                       'specs[listingCards][1][search_request_params][parameters][eligibility_map][seller]': '',
                       'specs[listingCards][1][search_request_params][parameters][eligibility_map][shop_country]': '',
                       'specs[listingCards][1][search_request_params][parameters][eligibility_map][tier]': '',
                       'specs[listingCards][1][search_request_params][parameters][eligibility_map][time]': '',
                       'specs[listingCards][1][search_request_params][parameters][eligibility_map][time_since_last_login]': '',
                       'specs[listingCards][1][search_request_params][parameters][eligibility_map][time_since_last_purchase]': '',
                       'specs[listingCards][1][search_request_params][parameters][eligibility_map][user]': '0',
                       'specs[listingCards][1][search_request_params][parameters][eligibility_map][exclude_groups]': '',
                       'specs[listingCards][1][search_request_params][parameters][eligibility_map][exclude_users]': '',
                       'specs[listingCards][1][search_request_params][parameters][eligibility_map][marketplace]': '',
                       'specs[listingCards][1][search_request_params][parameters][eligibility_map][user_agent]': '',
                       'specs[listingCards][1][search_request_params][parameters][eligibility_map][user_dataset]': '',
                       'specs[listingCards][1][search_request_params][parameters][eligibility_map][geoip]': '',
                       'specs[listingCards][1][search_request_params][parameters][eligibility_map][gdpr]': '',
                       'specs[listingCards][1][search_request_params][parameters][eligibility_map][email]': '',
                       'specs[listingCards][1][search_request_params][parameters][eligibility_map][request_restrictions]': '',
                       'specs[listingCards][1][search_request_params][parameters][eligibility_map][marketing_channel]': '',
                       'specs[listingCards][1][search_request_params][parameters][eligibility_map][page_enum]': '',
                       'specs[listingCards][1][search_request_params][parameters][filter_distracting_content]': 'true',
                       'specs[listingCards][1][search_request_params][parameters][spell_correction_via_mmx]': 'true',
                       'specs[listingCards][1][search_request_params][parameters][interleaving_option]': '',
                       'specs[listingCards][1][search_request_params][parameters][should_pass_user_location_to_thrift]': 'true',
                       'specs[listingCards][1][search_request_params][parameters][result_count]': len(listing_ids),
                       'specs[listingCards][1][search_request_params][user_id]': '',
                       'specs[listingCards][1][is_mobile]': 'false',
                       'specs[listingCards][1][organic_listings_count]': '2502441',
                       'specs[listingCards][1][pred_score]': '',
                       'specs[listingCards][1][is_eligible_for_grid_order_md_fix]': 'false',
                       'view_data_event_name': 'search_lazy_loaded_cards_specview_rendered'}

            headers = {
                'accept': '*/*',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'zh-CN,zh;q=0.9',
                'cache-control': 'no-cache',
                'content-length': '11287',
                'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'cookie': 'user_prefs=OyZhzInkDOfaabnPRPHDKJkHV1ljZACCpJ-rfGB0tFKwu4uSTl5pTo6OUmqerruTkg5QCCpiBKFwEbEMAA..; fve=1660529228.0; ua=531227642bc86f3b5fd7103a0c0b4fd6; _gcl_au=1.1.2129121361.1660530531; exp_hangover=kSsn5seGkTXCF8q0ogp7DYjlSB5jZACCpJ-r_EB0soJke7VSQWpRWox-eWpSfGJRSWZaZnJmYk58TmJJal5yZXyhYbyRgZGRklVaYk5xai0DAA..; _tt_enable_cookie=1; _ttp=ec6a440d-4f26-4c4d-a433-72a6112d83e0; _pin_unauth=dWlkPVpXTmhPREV5WmpJdFlUVmtNUzAwWXpWaExXSXpZekF0TkdGbE5qSTRNbVJpWXpRMg; uaid=HAGLzLG4z4fpW1c8DrQd520psOhjZACCpJ-rfEB0csIR1Wql0sTMFCUrpWxDX1MPD2ffRIvKrHwTn7Ti7HyjcF1Xn_gC9xylWgYA; __pdst=6c5d8db4d8f64d8ca261c0754c787c2b; last_browse_page=https%3A%2F%2Fwww.etsy.com%2F; _gid=GA1.2.1833311463.1667781755; search_options={"prev_search_term":"personalized%20gifts","item_language":null,"language_carousel":null}; pla_spr=0; _ga=GA1.1.1398221447.1660530532; _uetsid=1249f5005e3511edbc0273dc4d698a4a; _uetvid=03c66660f1cd11ecb96c7de5773446f7; _ga_KR3J610VYM=GS1.1.1667781754.85.1.1667781845.60.0.0; tsd=%7B%22gnav_search_focus%22%3A%7B%22event_name%22%3A%22gnav_search_focus%22%2C%22interaction_type%22%3A%22keyboard%22%7D%2C%22gnav_perform_search%22%3A%7B%22event_name%22%3A%22gnav_perform_search%22%2C%22interaction_type%22%3A%22click%22%7D%7D; gift_session_v2=3I-haKyE81LJp2NgJvwS6BaK5kJjZACC5OQCQzCdESZnyAAA; uaid=Bn97D1tacnaHmkcA0MWqE6XCh75jZACC5IwcLhhdrVSamJmiZKXkbRxlGJBbmpRh7BVZke4fWp6VWGmeGeGRGmlepVTLAAA.',
                'origin': 'https://www.etsy.com',
                'pragma': 'no-cache',
                'referer': 'https://www.etsy.com/sg-en/search?q=personalized+gifts+',
                'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
                'x-csrf-token': '3:1667781789:a52do1Syzv-ULdLOLicMRk8cxiZ1:fc62499d014ef51b260d44a6527239e9816f448520a3f3f7634c5e1ed7fad701',
                'x-detected-locale': 'SGD|en-GB|SG',
                'x-page-guid': 'f2b1b695179.ae76f00e3685362de63b.00',
                'x-requested-with': 'XMLHttpRequest'
            }

            # 获取listid
            if self.proxies == None:
                html_resp = request_handler(url, method='post', headers=headers, data=payload, retry=10, timeout=10)
            else:
                html_resp = request_handler(url, method='post', headers=headers, data=payload, retry=10, timeout=10,proxies=self.proxies)
            if html_resp == None:
                data['msg'] = '获取listing_ids的html失败'
                return data

            data['code'] = 1

            html = html_resp.json()['output']['listingCards']

            pro = etree.HTML(html)
            for listing in listing_ids + ad_ids:
                try:
                    pro_html = pro.xpath(f'//div[@data-listing-id="{listing}"]')[0]
                    shop_id = pro_html.xpath(f'./@data-shop-id')[0]
                    goods_list.append({"good_id": listing, 'shop_id': shop_id,
                                       'html': etree.tostring(pro_html, encoding='utf-8').decode()})

                except Exception as error:
                    pass

            data['goods_data'] = goods_list
            return data


        except Exception as error:
            data['msg'] = error
            return data

    def get_shop_categroy_and_shop_id(self):
        '''
            返回店铺分类 集合
        :return:
        '''

        data = {
            'code': 0,
            'msg': '',
            'shop_id': '',
            'section_list': [],
        }
        # 判断类型
        if self.search_type != 'shop':
            data['msg'] = '如果想搜索店铺集合 search_type为 shop'
            return data

        headers = {
            'accept-language': 'zh-CN,zh;q=0.9',
            'x-detected-locale': 'USD|en-US|HK',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36',
        }
        shop_url = f'https://www.etsy.com/sg-en/shop/{self.title}'


        if self.proxies == None:
            resp = request_handler(shop_url, method='get', headers=headers, retry=10, timeout=10)
        else:
            resp = request_handler(shop_url, method='get', headers=headers, retry=10, timeout=10,
                                        proxies=self.proxies)
        if resp == None:
            data['msg'] = '获取店铺分类失败'
            return data

        e = etree.HTML(resp.text)
        all_cate = e.xpath('//button[@class="wt-tab__item wt-ml-md-0 wt-mr-md-0 wt-justify-content-space-between"]')
        cate_list = []
        try:
            data['shop_id'] = re.findall('data-shop-id="(\d+)"', resp.text)[0]
        except Exception as e:
            pass

        for cate in all_cate:
            try:
                cate_id = cate.xpath('./@data-section-id')[0]
                cate_name = ''.join(cate.xpath('.//span[@class="wt-break-word wt-mr-xs-2"]/text()')).strip()
                cate_list.append({'section_id': cate_id, 'section_name': cate_name})
            except Exception as error:
                pass
        data['code'] = 1
        data['section_list'] = cate_list

        return data

    def get_shop_produts(self, shop_id, page, limit=36, section_id=None):
        '''
        :param shop_id: 店铺id
        :param page: 页码
        :param limit: 一页多少数据
        :param section_id: 集合id 如果没有集合不直接全部
        :return: 返回当前页码中的所有数据
        '''
        data = {
            'code': 0,
            'msg': '',
            'total_count': 0,
            'goods_data': [],
        }
        good_list = []
        try:
            offset = int((page - 1) * limit)
        except Exception as e:
            data['msg'] = '请输入正确页码  类型为 int'
            return data

        params = {
            "limit": limit,
            "offset": offset,
            "sort_order": "relevance",
            "path": f"/sg-en/shop/{self.title}",
            "is_edit": False,
            "on_sale_only": True,
            "wider_shop_home_v2": True,
            "show_listing_card_videos": True,
            "referring_listing_id": "900989601",
            "is_paginated_recs_relevance": False
        }
        if section_id != None:
            params['section_id'] = section_id

        url = f'https://www.etsy.com/api/v3/ajax/bespoke/member/shops/{shop_id}/listings-view'
        headers = {
            'accept-language': 'zh-CN,zh;q=0.9',
            'x-detected-locale': 'USD|en-US|HK',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36',
        }
        if self.proxies == None:
            resp = request_handler(url, method='get', params=params, headers=headers, retry=10, timeout=10)
        else:
            resp = request_handler(url, method='get', params=params, headers=headers, retry=10, timeout=10,proxies=self.proxies)

        if resp == None:
            data['msg'] = '请求失败，请重新请求！'
            return data

        resp_dict = resp.json()
        data['total_count'] = resp_dict['total_count']
        e = etree.HTML(resp_dict['html'])
        all = e.xpath('//div[contains(@class,"responsive-listing-grid")]/div')
        for good in all:
            try:
                good_id = good.xpath('.//a/@data-listing-id')[0]
                good_list.append(
                    {"good_id": good_id, 'shop_id': shop_id, 'html': etree.tostring(good, encoding='utf-8').decode()})
            except Exception as error:
                pass
        data['goods_data'] = good_list
        data['code'] = 1
        return data

    # 解析etsy产品详情
    def parse_product(self, html):
        '''
        :param html: 产品html
        :return: 产品数据
        '''
        data = {
            'code': 0,
            'msg': '',
            'product': {}
        }
        good_dict = {}
        try:
            e = etree.HTML(html)
        except Exception as e:
            data['msg'] = e
            return data
        if html == None or e == None:
            data['msg'] = 'html不能为空'
            return data

        # 标题
        good_dict['title'] = ''.join(
            e.xpath('//h1[@class="wt-text-body-03 wt-line-height-tight wt-break-word"]/text()')).strip()
        good_dict['source_platform'] = 'etsy'

        # 价格
        good_dict['price'] = e.xpath('//p[@class="wt-text-title-03 wt-mr-xs-2"]')
        try:
            good_dict['price'] = re.findall('"lowPrice":"(\d+)', html)[0]
        except Exception as error:
            good_dict['price'] = 0
        # 是否是bestseller
        good_dict['is_bestseller'] = 1 if ''.join(
            e.xpath('//span[@class="wt-display-inline-block"]/text()')).strip() == 'Bestseller' else 0

        # 描述
        good_dict['desc'] = ''.join(e.xpath('//div[@data-id="description-text"]//text()')).strip()
        # 图片
        try:
            good_dict['img_url'] = e.xpath(
                '//img[@class="wt-max-width-full wt-horizontal-center wt-vertical-center carousel-image wt-rounded"]/@src')[
                0]
        except Exception as error:
            good_dict['img_url'] = ''
        good_dict['img_url_list'] = []
        img_li = e.xpath('//ul[contains(@class,"wt-list-unstyled wt-overflow-hidden")]/li')

        for imgobj in img_li:
            img = imgobj.xpath('.//img/@data-src')
            if img == []:
                img = imgobj.xpath('.//img/@src')
            try:
                good_dict['img_url_list'].append(img[0])
            except Exception as error:
                pass

        if good_dict['img_url_list'] == []:
            img_li = e.xpath('//ul[contains(@class,"wt-list-unstyled  wt-position-relative carousel-pane-list")]/li')
            for imgobj in img_li:
                img = imgobj.xpath('.//img/@data-src')
                if img == []:
                    img = imgobj.xpath('.//img/@src')
                try:
                    good_dict['img_url_list'].append(img[0])
                except Exception as error:
                    pass

        # 关注数
        good_dict['favorites'] = ''.join(
            re.findall('<a rel="nofollow" class="wt-text-link" href=".*?>.*?(\d+).*?</a>', html, re.S)).strip()
        good_dict['favorites'] = 0 if good_dict['favorites'] == '' else good_dict['favorites']

        # 评论数
        try:
            comment = e.xpath('//span[@class="wt-badge wt-badge--status-02 wt-ml-xs-2"]/text()')[0].replace(',', '')
            good_dict['review_count'] = re.findall(r"\d+\.?\d*", comment)[0]
        except Exception as errror:
            good_dict['review_count'] = 0

        # 变体数据
        good_dict['opt'] = {}
        all_opt = e.xpath('//div[@id="variations"]/div')
        if all_opt == []:
            all_opt = e.xpath('//div[@data-selector="listing-page-variations"]/div')
        for opt in all_opt[:]:
            key = ''.join(opt.xpath('.//label/text()')).strip()
            if opt.xpath('.//textarea') != []:
                continue
            try:
                option = [o.strip() for o in opt.xpath('.//select/option//text()')[1:]]
                good_dict['opt'][key] = option
            except Exception as error:
                pass

        try:
            if good_dict['opt'].get('textarea') == None:
                good_dict['opt']['textarea'] = []
            title = ''.join(e.xpath('//div[@data-selector="listing-page-personalization"]/label/text()')).strip()
            desc = ''.join(e.xpath('//p[@id="personalization-instructions"]/text()')).strip()
            if title != '':
                good_dict['opt']['textarea'].append({'title': title, 'desc': desc})
        except Exception as error:
            pass

        # 最后一次卖出时间
        try:
            t = re.findall('Listed on (\w+) (\d+), (\d+)', html)[0]
            good_dict['listed_time'] = t[0] + ' ' + t[1] + ', ' + t[2]
        except Exception as error:
            pass
        try:
            good_dict['category_etsy_raw'] = ' > '.join(
                e.xpath('//div[@class="wt-text-caption wt-text-center-xs wt-text-left-lg"]/a/text()')[1:])
        except Exception as error:
            good_dict['category_etsy_raw'] = ''

        data['code'] = 1
        data['product'] = good_dict

        return data

    def get_product_reviews(self, page_num, listing_id, shop_id):
        '''
        获取etsy 单个产品的评论
        :param page_num: 页码
        :param listing_id: 产品id
        :param shop_id: 店铺id
        :return:
        '''
        data = {
            'code': 0,
            'msg': '',
            'review_data': None
        }
        try:
            payload = {'log_performance_metrics': 'true',
                       'specs[reviews][]': 'Etsy\Web\ListingPage\Reviews\ApiSpec',
                       'specs[reviews][1][listing_id]': listing_id,
                       'specs[reviews][1][shop_id]': shop_id,
                       'specs[reviews][1][render_complete]': 'true',
                       'specs[reviews][1][active_tab]': 'same_listing_reviews',
                       'specs[reviews][1][should_lazy_load_images]': 'false',
                       'specs[reviews][1][should_use_pagination]': 'true',
                       'specs[reviews][1][page]': str(page_num),
                       'specs[reviews][1][category_path]': ['1250', '1251', '1317', '1322'],
                       'specs[reviews][1][should_show_variations]': 'true',
                       'specs[reviews][1][is_reviews_untabbed_cached]': 'false',
                       'specs[reviews][1][was_landing_from_external_referrer]': 'false',
                       'specs[reviews][1][sort_option]': 'Relevancy',
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
            if self.proxies == None:
                resp = request_handler(url, method='post', data=payload, headers=headers, retry=10, timeout=10)
            else:
                resp = request_handler(url, method='post', data=payload, headers=headers, retry=10, timeout=10,proxies=self.proxies)
            if resp == None:
                data['msg'] = '请求失败，请求重新请求'
                return data
            data['review_data'] = resp.json()
            data['code'] = 1
            return data
        except Exception as e:
            data['msg'] = e
            return data


if __name__ == '__main__':
    proxies = {
        'http': 'http://127.0.0.1:7890',
        'https': 'http://127.0.0.1:7890',
    }

    # 初始化搜索
    etsy_obj = Etsy('hello kitty', search_type='search', proxies=proxies)
    #
    data = etsy_obj.get_search_products(1)

    # #初始化 店铺
    # etsy_obj = Etsy('SamInJapanArt', search_type='shop', proxies=proxies)
    #
    # # data = etsy_obj.get_shop_categroy_and_shop_id()
    #
    # #获取店铺产品
    # data = etsy_obj.get_shop_produts('12308374',limit=500,page=2)

    print(data)
