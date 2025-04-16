import os
import time
import datetime
import asyncio
from functools import wraps
from enum import Enum

import aiofiles
import httpx
import pandas as pd
import numpy as np
import pyotp
from selenium import webdriver
from pandas import DataFrame
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from .web_drivers import Web_drives
from yhlogin import Yhlogin

# pd.set_option('display.max_columns', None)
pd.set_option('display.width', 200)


class Sqlengine(Enum):
    HIVE = {'engine': '1', 'dsId': 1}
    IMPALA = {'engine': '2', 'dsId': 2}
    CK = {'engine': '3', 'dsId': 14004}


def sync_and_async(async_func):
    """装饰器，使异步函数支持同步和异步调用。"""

    @wraps(async_func)
    def wrapper(*args, **kwargs):
        try:
            # 检查当前是否有运行的事件循环
            asyncio.get_running_loop()
            # 存在运行中的事件循环，返回协程对象，需用户await
            return async_func(*args, **kwargs)
        except RuntimeError:
            # 无事件循环，同步执行
            return asyncio.run(async_func(*args, **kwargs))

    return wrapper


class Olap:
    class LoginError(Exception):
        pass

    class Sql:
        @staticmethod
        def get_sql_type(sql: str):
            """
            获取sql类型
            """
            sql_lines = [s.strip() for s in sql.split('\n') if s.strip() and s.strip()[0:2] != '--']
            if sql_lines:
                sql_first_keywords = sql_lines[0].split(' ')[0]
                return sql_first_keywords.lower()

        @staticmethod
        def sql_var_fill(sql, **kwargs):
            """
            将${参数}转换为值
            """
            for ver in kwargs:
                sql = sql.replace('${%s}' % ver, kwargs[ver])
            return sql

    class Api:
        def __init__(self, pi):
            self.sql = self.Sql(pi)
            self.download = self.Download(pi)
            self.approval = self.Approval(pi)
            self.hdfs = self.Hdfs(pi)
            self.cluster = self.Cluster(pi)

        class Sql:
            def __init__(self, pi):
                self.manager = self.Manager(pi)

            class Manager:
                def __init__(self, pi):
                    self.pi = pi

                @sync_and_async
                async def runSql(self, sql: str, engine: str = '2', dsId: int = 2, params: list = [],
                                 execute_configs: dict = {}):
                    """运行sql"""
                    url = self.pi.base_url + '/sql/manager/runSql'
                    data = {'engine': engine, 'dsId': dsId, 'sql': sql, 'params': params,
                            'executeConfigs': execute_configs}
                    headers = self.pi.headers
                    async with httpx.AsyncClient() as client:
                        resp = await client.post(url=url, json=data, headers=headers)
                        result = resp.json()
                    return result

                @sync_and_async
                async def getLogResult(self, requestId: str):
                    """查看运行日志"""
                    url = self.pi.base_url + '/sql/manager/getLogResult'
                    headers = self.pi.headers
                    data = {'requestId': requestId}
                    async with httpx.AsyncClient() as client:
                        resp = await client.post(url=url, json=data, headers=headers)
                        result = resp.json()
                    return result

                @sync_and_async
                async def getSqlResult(self, requestId: str, page_size: int = 200, page_no: int = 1):
                    """查看运行结果"""
                    url = self.pi.base_url + '/sql/manager/getSqlResult'
                    headers = self.pi.headers
                    data = {'requestId': requestId, 'pageSize': page_size, 'pageNo': page_no}
                    async with httpx.AsyncClient() as client:
                        resp = await client.post(url=url, json=data, headers=headers)
                        result = resp.json()
                    return result

                @sync_and_async
                async def checkState(self, requestId: str):
                    """查看运行结果"""
                    url = self.pi.base_url + '/sql/manager/checkState'
                    headers = self.pi.headers
                    data = {'requestId': requestId}
                    async with httpx.AsyncClient() as client:
                        resp = await client.post(url=url, json=data, headers=headers)
                        result = resp.json()
                    return result

                @sync_and_async
                async def queryHisSqlResult(self, pageNum: int = 1, pageSize: int = 10, sqlKeywords: str = ''):
                    """查看历史"""
                    url = self.pi.base_url + '/sql/manager/queryHisSqlResult'
                    headers = self.pi.headers
                    data = {'pageNum': pageNum, 'pageSize': pageSize, 'sqlKeywords': sqlKeywords}
                    async with httpx.AsyncClient() as client:
                        resp = await client.post(url=url, json=data, headers=headers)
                        result = resp.json()
                    return result

        class Download:
            def __init__(self, pi):
                self.pi = pi

            @sync_and_async
            async def olapResultSimple(self, requestId: str, file_path: str = None):
                """快速下载(1000条)"""
                if not file_path:
                    file_path = f'{requestId}.xlsx'
                url = self.pi.base_url + '/download/olapResultSimple/' + requestId
                headers = self.pi.headers
                async with httpx.AsyncClient() as client:
                    resp = await client.get(url=url, headers=headers)
                async with aiofiles.open(file_path, 'wb') as f:
                    await f.write(resp.content)
                return file_path

            @sync_and_async
            async def refresh(self, downloadId: str):
                url = self.pi.base_url + '/download/refresh?downloadId=%s' % downloadId
                headers = self.pi.headers
                data = {'downloadId': downloadId}
                async with httpx.AsyncClient() as client:
                    resp = await client.post(url=url, json=data, headers=headers)
                    result = resp.json
                return result

            @sync_and_async
            async def olapResult(self, requestId: str, file_path: str = None):
                """下载excel"""
                if not file_path:
                    file_path = f'{requestId}.xlsx'
                url = self.pi.base_url + '/download/olapResult/' + requestId
                headers = self.pi.headers
                async with httpx.AsyncClient() as client:
                    resp = await client.get(url=url, headers=headers)
                async with aiofiles.open(file_path, 'wb') as f:
                    await f.write(resp.content)
                return file_path

            @sync_and_async
            async def downloadToExcel(self, requestId: str, fileName: str, file_path: str = None):
                """下载excel(impala)"""
                if not file_path:
                    file_path = f'{requestId}.xlsx'
                url = f'https://prokongbigdata.yonghui.cn/yh-magpie-bridge-manager/open/api/downloadToExcel?requestId={requestId}&fileName={fileName}'
                headers = self.pi.headers
                async with httpx.AsyncClient() as client:
                    resp = await client.get(url=url, headers=headers)
                async with aiofiles.open(file_path, 'wb') as f:
                    await f.write(resp.content)
                return file_path

        class Approval:
            def __init__(self, pi):
                self.pi = pi

            @sync_and_async
            async def createMiddleDownloadOrder(self, requestId: str, engine: int = 1):
                """创建下载数据(50000条)"""
                url = self.pi.base_url + '/approval/createMiddleDownloadOrder'
                headers = self.pi.headers
                data = {'requestId': requestId, 'engine': engine}
                async with httpx.AsyncClient() as client:
                    resp = await client.put(url=url, json=data, headers=headers)
                    result = resp.json()
                return result

            @sync_and_async
            async def createSkipDownloadOrder(self, requestId: str, engine: int = 1):
                """创建下载全量数据(500000条)"""
                url = self.pi.base_url + '/approval/createSkipDownloadOrder'
                headers = self.pi.headers
                data = {'requestId': requestId, 'engine': engine}
                async with httpx.AsyncClient() as client:
                    resp = await client.put(url=url, json=data, headers=headers)
                    result = resp.json()
                return result

            @sync_and_async
            async def detail(self, approvalId: str):
                """查看下载任务明细"""
                url = self.pi.base_url + '/approval/detail?approvalId=%s' % approvalId
                headers = self.pi.headers
                async with httpx.AsyncClient() as client:
                    resp = await client.get(url=url, headers=headers)
                    result = resp.json()
                return result

        class Hdfs:
            def __init__(self, pi):
                self.pi = pi

            @sync_and_async
            async def moveToTrash(self, path: list):
                """
                删除文件
                :param path: 文件路径列表
                :return:
                """
                url = self.pi.base_url + '/hdfs/moveToTrash'
                headers = self.pi.headers
                data = {'path': path}
                async with httpx.AsyncClient() as client:
                    resp = await client.post(url=url, json=data, headers=headers)
                    result = resp.json()
                return result

            @sync_and_async
            async def get_hdfs_dir(self, path: str, pageNum: int = 1):
                """
                获取目录下文件
                :param path: 目录路径
                :param pageNum:
                :return:
                """
                url = self.pi.base_url + '/hdfs/getHdfsDir'
                headers = self.pi.headers
                data = {'pageNum': pageNum, 'path': path}
                async with httpx.AsyncClient() as client:
                    resp = await client.post(url=url, json=data, headers=headers)
                    result = resp.json()
                return result

            @sync_and_async
            async def upload_single_file(self, hdfsPath: str, file: str):
                """
                上传文件
                :param hdfsPath: 目标目录
                :param file: 需上传的文件路径
                :return:
                """
                url = self.pi.base_url + '/file/uploadSingleFile'
                file_name = os.path.basename(file)
                headers = {'User-Agent': self.pi.UserAgent, 'token': self.pi.token, 'orgCode': self.pi.orgCode}
                async with httpx.AsyncClient(timeout=60) as client:
                    async with aiofiles.open(file, 'rb') as f:
                        file_content = await f.read()
                        files = {
                            "hdfsPath": (None, hdfsPath),
                            "file": (file_name, file_content, "text/csv")
                        }
                        resp = await client.post(url=url, files=files, headers=headers)
                        result = resp.json()
                return result

        class Cluster:
            def __init__(self, pi):
                self.manager = self.Manager(pi)

            class Manager:
                def __init__(self, pi):
                    self.pi = pi

                @sync_and_async
                async def killJob(self, requestId: str, engine: str = '2', dsId: int = 2):
                    url = self.pi.base_url + '/cluster/manager/killJob'
                    headers = self.pi.headers
                    data = {'requestId': requestId, 'engine': engine, 'dsId': dsId}
                    async with httpx.AsyncClient() as client:
                        resp = await client.post(url=url, json=data, headers=headers)
                        result = resp.json()
                    return result

    def __init__(self, token=None):
        self.base_url = 'http://prokong.bigdata.yonghui.cn/yh-olap-web'
        self.UserAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0'
        self.orgCode = 'bgzt000004'
        self.ContentType = 'application/json'
        self.token = token
        self.headers = {'User-Agent': self.UserAgent, 'token': self.token, 'orgCode': self.orgCode,
                        'Content-Type': self.ContentType}
        self.token_get_time = None
        self.username = None
        # api分级
        self.api = self.Api(self)
        self.engines = {'hive': {'engine': '1', 'dsId': 1},
                        'impala': {'engine': '2', 'dsId': 2},
                        'ck': {'engine': '3', 'dsId': 14004}}

    def __set_token(self, token):
        self.token = token
        self.headers['token'] = token

    def __wait_for_page_load(self, driver, timeout=10):
        try:
            WebDriverWait(driver, timeout).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete")
        except TimeoutException:
            print("页面加载超时")

    def __get_webdriver(self):
        try:
            option = webdriver.EdgeOptions()
            option.add_argument("--headless")
            option.add_argument("--disable-gpu")
            option.add_argument('--start-minimized')
            service = EdgeService(Web_drives.edge())
            driver = webdriver.Edge(service=service, options=option)
        except:
            option = webdriver.ChromeOptions()
            option.add_argument('headless')
            service = ChromeService(Web_drives.chrome())
            driver = webdriver.Chrome(service=service, options=option)
        return driver

    def __get_api_data(self, api_result):
        if api_result.get('success'):
            return api_result.get('data')

    def params(self, **kwargs):
        params = [{'key': key, 'value': kwargs[key], 'id': index, 'type': 2} for index, key in enumerate(kwargs.keys())]
        return params

    def login_by_webdrives(self, username, password, otp_key):
        driver = self.__get_webdriver()
        driver.get(
            'http://o2o-support-prod.idaas-cas.gw.yonghui.cn/cas/login?service=http://10.208.134.65:32766/redirect?redirectUrl=http://bigdata.yonghui.cn/#/')
        self.__wait_for_page_load(driver)
        username_text = driver.find_element(by=By.ID, value="username")
        username_text.send_keys(username)
        password_text = driver.find_element(by=By.ID, value="password")
        password_text.send_keys(password)
        submit_button = driver.find_element(by=By.NAME, value="submit")
        submit_button.click()
        self.__wait_for_page_load(driver)
        cookies = driver.get_cookie('token')
        if cookies:
            token = cookies.get('value')
            if token.find('JSESSIONID') != -1:
                self.__set_token(token)
        else:
            for i in range(3):
                try:
                    dynamic_password_text = driver.find_element(by=By.ID, value="dynamicPassword")
                    dynamic_password = pyotp.TOTP(otp_key).now()
                    dynamic_password_text.send_keys(dynamic_password)
                    break
                except:
                    time.sleep(1)
                    pass
            cookies = driver.get_cookie('token')
            token = cookies.get('value')
            self.__set_token(token)
        self.token_get_time = datetime.datetime.now()
        self.username = username
        driver.quit()

    @sync_and_async
    async def login(self, username, password, otp_key):
        yl = Yhlogin()
        await yl.login(username=username, password=password, otp_key=otp_key, service='https://bigdata.yonghui.cn')
        jsessionid = yl.cookies.get('JSESSIONID')
        self.__set_token(f'JSESSIONID={jsessionid}')
        self.token_get_time = datetime.datetime.now()
        self.username = username

    @sync_and_async
    async def wait_run_finish(self, requestId: str, sql_type: str = 'select', get_detail_interval=None):
        @sync_and_async
        async def getLogResult():
            while True:
                log_result_res = await self.api.sql.manager.getLogResult(requestId=requestId)
                log_result_data = self.__get_api_data(log_result_res)
                if log_result_data:
                    if log_result_data.get('finish') == 'run':
                        await asyncio.sleep(get_detail_interval)
                    elif log_result_data.get('finish') == 'ok':
                        error = log_result_data.get('error')
                        if error:
                            raise ValueError(log_result_data.get('data'))
                        else:
                            break
                    else:
                        raise ValueError(log_result_res.get('message'))
                else:
                    raise ValueError(log_result_res.get('message'))

        @sync_and_async
        async def checkState():
            while True:
                check_state_res = await self.api.sql.manager.checkState(requestId=requestId)
                check_state_data = self.__get_api_data(check_state_res)
                if check_state_data:
                    error = check_state_data.get('errMsg')
                    if check_state_data.get('finish') == 'run':
                        await asyncio.sleep(get_detail_interval)
                    elif check_state_data.get('finish') == 'ok':
                        if error.lower().find('error') != -1:
                            raise ValueError(error)
                        else:
                            break
                    else:
                        raise ValueError(error)
                else:
                    raise ValueError(check_state_data.get('message'))

        if sql_type == 'select':
            if not get_detail_interval:
                get_detail_interval = 1
            await getLogResult()
        else:
            if not get_detail_interval:
                get_detail_interval = 5
            await checkState()

    @sync_and_async
    async def wait_task_finish(self, approvalId: str, get_detail_interval=5, retry_num=0):
        while True:
            detail_res = await self.api.approval.detail(approvalId=approvalId)
            detail_data = self.__get_api_data(detail_res)
            if detail_data:
                if detail_data.get('taskState') == 1:  # 数据生成中 一秒后刷新
                    await asyncio.sleep(get_detail_interval)
                elif detail_data.get('taskState') == 2:  # 数据已生成 结束循环
                    return detail_data
                elif detail_data.get('taskState') == 3:  # 数据已生成 结束循环
                    retry_num -= 1
                    if retry_num < 0:
                        raise ValueError(detail_data.get('taskStateName'))
                    else:
                        await self.api.download.refresh(downloadId=approvalId)
                        await asyncio.sleep(get_detail_interval)
                else:
                    await asyncio.sleep(get_detail_interval)
            else:
                raise ValueError(detail_res.get('message'))

    @sync_and_async
    async def execute(self, sql: str, Engine: Sqlengine|str = Sqlengine.IMPALA, params: list = [], execute_configs: dict = {},
                      wait_run_finish=True):
        if Engine.__class__.__name__ == 'str':
            engine = self.engines[Engine]['engine']
            dsId = self.engines[Engine]['dsId']
        else:
            engine = Engine.value['engine']
            dsId = Engine.value['dsId']
        run_sql_req = await self.api.sql.manager.runSql(sql=sql, engine=engine, dsId=dsId, params=params,
                                                        execute_configs=execute_configs)
        run_sql_data = self.__get_api_data(run_sql_req)
        if run_sql_data:
            executeId = run_sql_data.get('executeId')
        else:
            raise ValueError(run_sql_req.get('message'))
        if wait_run_finish:
            sql_type = self.Sql.get_sql_type(sql)
            await self.wait_run_finish(executeId, sql_type=sql_type)
        return executeId

    @sync_and_async
    async def result(self, requestId, page_size=200, page_no=1):
        sql_result_res = await self.api.sql.manager.getSqlResult(requestId=requestId, page_size=page_size,
                                                                 page_no=page_no)
        sql_result_data = self.__get_api_data(sql_result_res)
        if sql_result_data:
            cols = sql_result_data.get('columnNameList')
            rows = sql_result_data.get('list')
            df = DataFrame(rows, columns=cols)
        else:
            raise ValueError(sql_result_res.get('message'))
        df = df.replace('null', np.nan)
        return df

    @sync_and_async
    async def download_excel(self, requestId: str, file_path: str = None, Engine: Sqlengine|str = Sqlengine.IMPALA):
        if Engine.__class__.__name__ == 'str':
            engine = self.engines[Engine]['engine']
        else:
            engine = Engine.value['engine']
        sql_result_res = await self.api.sql.manager.getSqlResult(requestId=requestId)
        sql_result_data = self.__get_api_data(sql_result_res)
        total = 100000
        if sql_result_data:
            if sql_result_data.get('total'):
                total = sql_result_data.get('total')
        if total <= 1000:
            out_file_path = await self.api.download.olapResultSimple(requestId=requestId, file_path=file_path)
        elif total <= 50000:
            cdo_res = await self.api.approval.createMiddleDownloadOrder(requestId=requestId, engine=engine)
            cdo_data = self.__get_api_data(cdo_res)
            if cdo_data:
                id = cdo_data.get('id')
                detail_data = await self.wait_task_finish(approvalId=id)
                dl_engine = detail_data.get('engine')
                dl_requestId = detail_data.get('requestId')
                downLoadRequestId = detail_data.get('downLoadRequestId')
                if dl_engine == 1:
                    out_file_path = await self.api.download.olapResult(requestId=dl_requestId, file_path=file_path)
                elif dl_engine == 2:
                    out_file_path = await self.api.download.downloadToExcel(requestId=downLoadRequestId,
                                                                            fileName=downLoadRequestId,
                                                                            file_path=file_path)
        else:
            cdo_res = await self.api.approval.createSkipDownloadOrder(requestId=requestId, engine=engine)
            cdo_data = self.__get_api_data(cdo_res)
            if cdo_data:
                id = cdo_data.get('id')
                detail_data = await self.wait_task_finish(approvalId=id)
                dl_engine = detail_data.get('engine')
                dl_requestId = detail_data.get('requestId')
                downLoadRequestId = detail_data.get('downLoadRequestId')
                if dl_engine == 1:
                    out_file_path = await self.api.download.olapResult(requestId=dl_requestId, file_path=file_path)
                elif dl_engine == 2:
                    out_file_path = await self.api.download.downloadToExcel(requestId=downLoadRequestId,
                                                                            fileName=downLoadRequestId,
                                                                            file_path=file_path)
        return out_file_path

    @sync_and_async
    async def quick_download_excel(self, sql: str, Engine: Sqlengine|str = Sqlengine.IMPALA, params: list = [],
                                   execute_configs: dict = {}, file_path: str = None):
        """
        跳过运行成功，直接执行下载
        """
        if Engine.__class__.__name__ == 'str':
            engine = self.engines[Engine]['engine']
            dsId = self.engines[Engine]['dsId']
        else:
            engine = Engine.value['engine']
            dsId = Engine.value['dsId']
        executeId = await self.execute(sql=sql, Engine=Engine, params=params, execute_configs=execute_configs,
                                       wait_run_finish=False)
        await self.api.cluster.manager.killJob(requestId=executeId, engine=engine, dsId=dsId)
        file_path = await self.download_excel(requestId=executeId, file_path=file_path, Engine=Engine)
        return file_path

    @sync_and_async
    async def result_full(self, executeId: str):
        file_path = await self.download_excel(executeId=executeId)
        df = pd.read_excel(file_path)
        os.remove(file_path)
        return df

    @sync_and_async
    async def quick_result_full(self, sql: str, Engine: Sqlengine|str = Sqlengine.IMPALA, params: list = [],
                                execute_configs: dict = {}):
        file_path = await self.quick_download_excel(sql=sql, Engine=Engine, params=params,
                                                    execute_configs=execute_configs)
        df = pd.read_excel(file_path)
        os.remove(file_path)
        return df
