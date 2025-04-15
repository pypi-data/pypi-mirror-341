import asyncio
from collections.abc import Iterator

from loguru import logger

import coocan
from coocan.url import Request


class AirAsyncSpider:
    start_urls = []
    max_requests = 5

    def start_requests(self):
        """初始请求"""
        assert self.start_urls, "没有起始 URL 列表"
        for url in self.start_urls:
            yield coocan.Request(url, self.parse)

    def middleware(self, request: Request):
        request.headers.setdefault("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0")

    async def get_response(self, request: Request):
        """发送请求，获取响应"""
        try:
            self.middleware(request)
            response = await request.send()
            return response
        except Exception as e:
            logger.error("{} {}".format(request.url, e))

    def parse(self, response):
        raise NotImplementedError("没有定义回调函数 {}.parse ".format(self.__class__.__name__))

    async def worker(self, queue, semaphore):
        """工作协程，从队列中获取请求并处理"""
        while True:
            request = await queue.get()

            # 结束信号
            if request is None:
                break

            # 控制并发
            async with semaphore:
                response = await self.get_response(request)
                if response:
                    try:
                        cached = request.callback(response, **request.cb_kwargs)
                        if isinstance(cached, Iterator):
                            for next_request in cached:
                                await queue.put(next_request)  # 将后续请求加入队列
                    except Exception as e:
                        logger.error(e)

            queue.task_done()

    async def run(self):
        """爬取入口"""
        queue = asyncio.Queue()
        semaphore = asyncio.Semaphore(self.max_requests)

        # 工作协程启动...
        workers = [
            asyncio.create_task(self.worker(queue, semaphore))
            for _ in range(self.max_requests)
        ]

        # 将初始请求加入队列
        for req in self.start_requests():
            await queue.put(req)

        # 等待队列中的所有任务完成
        await queue.join()

        # ...停止工作协程
        for _ in range(self.max_requests):
            await queue.put(None)

        # 等待所有工作协程完成
        await asyncio.gather(*workers)

    def go(self):
        asyncio.run(self.run())
