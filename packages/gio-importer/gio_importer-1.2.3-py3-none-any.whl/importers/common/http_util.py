#!/bin/env python3
# -*- coding: UTF-8 -*-
import os
import subprocess

import curlify
import requests

import urllib3
import json
import logging

from importers.common.config_util import ApiConfig, SaasConfig, SSLConfig

http = urllib3.PoolManager()


def send_graphql_post(body):
    """
     graphql post请求
    :param body: 请求graphql body
    :return: 响应数据
    """
    headers = {'Content-Type': 'application/json', 'Authorization': ApiConfig.token,
               'X-Project-Id': ApiConfig.project_id,
               'X-Product-Unique-Id': 'DC', 'User-Agent': 'gio-importer'}
    r = requests.post(ApiConfig.oauth2_uri + "/v3/graphql", headers=headers, data=body, verify=SSLConfig.verify)
    logging.debug('request curl: {}'.format(curlify.to_curl(r.request)))
    if r.status_code == 200:
        content = json.loads(r.content)
        if content["data"] is not None:
            return content['data']
        else:
            logging.error('Graphql请求错误,{}'.format(content['errors']))
            exit(-1)
    else:
        logging.error('response content: {}'.format(r.content.decode('utf-8')))
        logging.error('response curl: {}'.format(curlify.to_curl(r.request)))
        re = input("Graphql请求超时或失败,建议检查配置文件的相关token或是否重新请求，请输入yes/no:")
        if str(re).lower() == 'yes':
            send_graphql_post(body)
        else:
            return


def send_restful_get():
    """
    restful get请求
    :return: 响应数据
    """
    params = {
        'offset': 0,
        'limit': 100000,
        'isSystem': 'false',
        'global': 'true'
    }
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Referer': ApiConfig.oauth2_uri + '/dc/projects/' + ApiConfig.project_id + '/event/event-variables',
        'X-Product-Unique-Id': 'DC',
        'X-Project-Id': ApiConfig.project_id,
        'Authorization': ApiConfig.token, 'User-Agent': 'gio-importer'
    }
    response = requests.get(ApiConfig.oauth2_uri + '/api/backend/event-variable/search', headers=headers, params=params, verify=False)
    if response.status_code == 200:
        data = response.json()
        # 获取records中的所有key
        records = data.get('data', {}).get('records', [])
        arrr_all = [record['key'] for record in records]
        # 需要额外添加的key
        extra_keys = ['$user_agent', '$hyperlink', '$ip', '$index', '$package', '$textValue', '$page_count', 'eventId',
                      '$xpath', '$location_latitude', '$location_longitude', '$account_id', '$session', '$sdk_version',
                      '$client_time', '$bot_id', '$duration']

        arrr_all.extend(extra_keys)

        arrr_all_end = list(dict.fromkeys(arrr_all))
        return arrr_all_end
    else:
        logging.error('response content: {}'.format(response.content.decode('utf-8')))
        logging.error('response curl: {}'.format(curlify.to_curl(response.request)))
        re = input("Restful请求超时或失败,建议检查配置文件的相关token或是否重新请求，请输入yes/no:")
        if str(re).lower() == 'yes':
            send_restful_get()
        else:
            return


def send_restful_get():
    """
    restful get请求
    :return: 响应数据
    """
    params = {
        'offset': 0,
        'limit': 100000,
        'isSystem': 'false',
        'global': 'true'
    }
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Referer': ApiConfig.oauth2_uri + '/dc/projects/' + ApiConfig.project_id + '/event/event-variables',
        'X-Product-Unique-Id': 'DC',
        'X-Project-Id': ApiConfig.project_id,
        'Authorization': ApiConfig.token, 'User-Agent': 'gio-importer'
    }
    response = requests.get(ApiConfig.oauth2_uri + '/api/backend/event-variable/search', headers=headers, params=params, verify=False)
    if response.status_code == 200:
        data = response.json()
        # 获取records中的所有key
        records = data.get('data', {}).get('records', [])
        arrr_all = [record['key'] for record in records]
        # 需要额外添加的key
        extra_keys = ['$user_agent', '$hyperlink', '$ip', '$index', '$package', '$textValue', '$page_count', 'eventId',
                      '$xpath', '$location_latitude', '$location_longitude', '$account_id', '$session', '$sdk_version',
                      '$client_time', '$bot_id', '$duration']

        arrr_all.extend(extra_keys)

        arrr_all_end = list(dict.fromkeys(arrr_all))
        return arrr_all_end
    else:
        logging.error('response content: {}'.format(response.content.decode('utf-8')))
        logging.error('response curl: {}'.format(curlify.to_curl(response.request)))
        re = input("Restful请求超时或失败,建议检查配置文件的相关token或是否重新请求，请输入yes/no:")
        if str(re).lower() == 'yes':
            send_restful_get()
        else:
            return



def send_rest_get(url, params):
    """
     http post请求
    :param url: 请求url
    :param params: 请求参数
    :return: 响应数据
    """
    headers = {'Content-Type': 'application/json', 'Authorization': SaasConfig.token}
    # headers = {'Content-Type': 'application/json'}
    r = requests.get(SaasConfig.uri + url, headers=headers, params=params)
    if r.status_code == 200:
        content = json.loads(r.text)
        return content


def put_file_ftp(file_list, target_directory):
    headers = {'Authorization': 'Bearer ' + ApiConfig.token}
    for file in file_list:
        file_splits = file.split('/')
        simple_name = file_splits[len(file_splits) - 1]
        with open(file, 'rb') as fp:
            file_data = fp.read()
            http.request('POST', ApiConfig.oauth2_uri + '/upload', headers=headers,
                         fields={'file': (simple_name, file_data), 'path': target_directory})


def put_file_hdfs(file_list, target_directory):
    for file in file_list:
        os.system(f"hdfs dfs -put {file} {target_directory}")
