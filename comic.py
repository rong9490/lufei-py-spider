import aiohttp
import asyncio
import re
import uuid
import datetime
import random

# AiGuoManComic

from typing import Any, AsyncGenerator
from pathlib import Path
from aiohttp import ClientSession
from lxml import etree


class Comic:
    proxies: list[str] = []  # 代理设置

    def __init__(self,
                 comic_url: str | None,
                 req_headers: dict[str, str],
                 client_session: ClientSession,
                 chapter_concurrency: int | None = 1,
                 image_concurrency: int | None = 5,
                 min_wait: int | None = 4,
                 max_wait: int | None = 8,
                 start_chapter: int | str | None = 1,
                 start_img: int | str | None = 1,
                 end_chapter: int | str = None,
                 end_img: int | str = None
                 ) -> None:
        """
        :param comic_url: 漫画首页的URL
        :param req_headers: 请求头
        :param client_session: 客户端的session
        :param chapter_concurrency: 获取章节URl时的最大并发量
        :param image_concurrency: 下载图片时的最大并发量
        :param min_wait: 最小的随机停顿时间
        :param max_wait: 最大的随机停顿时间
        :param start_chapter: 起始的章节数
        :param start_img: 起始的图片数
        :param end_chapter: 结束的章节数
        :param end_img: 结束的图片数
        :return: None
        """

        self.comic_url = comic_url if comic_url is not None else input('请输入漫画网址：')
        self.req_headers = req_headers
        self.client_session = client_session
        self.chapter_concurrency = chapter_concurrency or 1
        self.image_concurrency = image_concurrency or 5
        self.min_wait = min_wait or 4
        self.max_wait = max_wait or 8
        self.start_chapter = start_chapter or 1
        self.start_img = start_img or 1
        self.end_chapter = end_chapter
        self.end_img = end_img
        self.validate_params()  # 用于检查参数

    @classmethod
    def set_cls_atr(cls, cls_atr: dict[str, list[str]] | None):
        """
        用来增加类属性

        :param cls_atr: 需要添加的属性对象
        :return: None
        """
        for atr in cls_atr:
            match atr:
                case None:
                    continue
                case 'proxies':
                    cls.proxies.extend(cls_atr[atr])

    @staticmethod
    def remove_sp_str(content: str) -> str:
        """
        用于去除特殊字符，避免无法保存文件、文件夹

        :param content: 传入的字符串
        :return: 去除特殊字符后的字符串
        """
        return re.sub(r'[\\/:?*<>"|]', '_', content).strip()

    @staticmethod
    def print_false(false_tip: str) -> None:
        """
        用于打印错误提示

        :param false_tip: 需要打印错误提示的字符串
        :return: None
        """
        print(f'****\t{false_tip}\t****')

    @staticmethod
    def print_true(true_tip: str) -> None:
        """
        用于打印正确提示

        :param true_tip: 需要打印正确提示的字符串
        :return: None
        """
        print(f'----\t{true_tip}\t----')

    @staticmethod
    def gen_range(start_num: int, end_num: int | None, limit_num: int) -> tuple[int, int]:
        """
        判断爬取范围，如果爬取范围有误，则自动获取1和最大值
        :param start_num: 起始的数
        :param end_num: 结束的数
        :param limit_num: 边界值
        :return: 最小的值、最大的值
        """
        # 如果 end_num 为 None 或 'all'，则设置为 limit_num
        end_num = limit_num if end_num in (None, 'all') else end_num

        # 如果 start_num 或 end_num 超出有效范围，则重置为默认值
        if not (0 < start_num <= end_num <= limit_num):
            return 1, limit_num

        return start_num, end_num

    def validate_param(self, param_name: str | int, default: int, message: str) -> bool:
        """
        用于检查单个参数是否有误，如果有误则默认重置

        :return: None
        """
        param_value = getattr(self, param_name)  # 先获取对象中的属性值
        # 如果为字符串，就判断是否为all
        if isinstance(param_value, str) and param_value == 'all':
            param_value = default
        # 如果为int类型，就判断是否小于0
        elif isinstance(param_value, int) and param_value <= 0:
            param_value = default
        else:
            return True
        setattr(self, param_name, param_value)  # 上面已经将参数值设置为传入的默认值了，这里就是设置默认值
        self.print_true(message)

    def validate_params(self):
        """
        用于初始化时检查多个参数是否有误，如果有误则默认重置

        :return: None
        """
        self.validate_param('chapter_concurrency', 1, '输入的章节获取最大并发量参数为空/有误，已重置为：1')
        self.validate_param('image_concurrency', 5, '输入的图片下载最大并发量参数为空/有误，已重置为：5')

        if not (0 < self.min_wait <= self.max_wait):  # 随机停顿时间
            self.min_wait, self.max_wait = 4, 8
            self.print_true('输入的停顿时间参数为空/有误，最小停顿时间已重置为：4秒，最大停顿时间已重置为：8秒')

        self.validate_param('start_img', 1, '输入的起始图片获取参数有误，已重置为1')
        self.validate_param('start_chapter', 1, '输入的起始章节参数有误，已重置为1')

    async def random_sleep(self) -> None:
        """
        用于随机产生停顿时间，将心比心，如果自己的网站被爬虫恶意爬取，会是什么感受呢？

        :return: None
        """

        random_time = random.randint(self.min_wait, self.max_wait)
        await asyncio.sleep(random_time)
        self.print_true(f'随机停顿时间：{random_time}秒')

    async def fetch(self, req_url: str, res_type: str, **kwargs: Any) -> str | bytes | None:
        """
        用于发送请求的方法，有两个响应结果：文本、字节码

        :param req_url: 请求的URL
        :param res_type: 响应的类型结果
        :param kwargs: 请求需携带的额外参数
        :return: 返回响应结果
        """
        # 每次请求都随机获取一个代理ip
        proxies = None
        if len(self.proxies) != 0:
            proxies = random.choice(self.proxies)
        async with self.client_session.get(req_url, proxy=proxies, **kwargs) as response:  # 异步上下文管理器
            res_status = int(response.status)  # 相应的状态码
            if res_status in [200, 302]:  # 判断状态码是否正确
                match res_type:  # match匹配对象的响应类型
                    case 'text':
                        return await response.text()
                    case 'file':
                        return await response.content.read()

    async def view_comic_basic_info(self) -> tuple[dict[str, str], int, Any]:
        """
        用于预览漫画中的基本信息、章节总数、html中的所有章节的父级容器

        :return: 漫画的基本信息、章节总数、html中的所有章节的父级容器
        """
        comic_basic_info, chapter_container = await self.get_comic_info()
        # 使用xpath直接计算章节总数，避免额外的类型转换
        chapter_num = chapter_container.xpath('count(./a[@class="detail-list-form-item"])')
        # 确保chapter_num是整数类型
        chapter_num = int(chapter_num) if chapter_num.is_integer() else chapter_num
        return comic_basic_info, chapter_num, chapter_container

    async def get_comic_info(self) -> tuple[dict[str, str], Any]:
        """
        结合view_comic_basic_info()方法使用，用来提取需要的漫画的信息、html中的所有章节的父级容器

        :return: 漫画的基本信息、html中的所有章节的父级容器
        """
        # 获取漫画首页的html
        comic_homepage_html = await self.fetch(self.comic_url, 'text', headers=self.req_headers)
        # 解析为xpath
        etree_html = etree.HTML(comic_homepage_html)

        # 定义一个辅助函数来提取信息并处理空字符串
        def extract_info(xpath_query: str) -> str:
            result = etree_html.xpath(f'string({xpath_query})')
            # 如果说网页中获取到的内容就是为空字符串，我们需特别注明一下，将空字符串变为”空“字
            return '空' if result == '' else result

        # 提取对应的节点数据
        comic_info = {
            'name': self.remove_sp_str(extract_info('//p[@class="detail-info-title"]/text()')),
            'author': extract_info('//p[@class="detail-info-tip"]//a/text()'),
            'cover': extract_info('//img[@class="detail-info-cover"]/@src'),
            'mark': extract_info('//p[@class="detail-info-stars"]/span/span/text()'),
            'updated_status': extract_info('//p[@class="detail-info-tip"]/span[2]/span/text()'),
            'theme': extract_info('//p[@class="detail-info-tip"]/span[3]/span//a/text()'),
            'intro': extract_info('//p[@class="detail-info-content"]/text()')
        }
        # 获取所有章节的父级容器
        chapter_container = etree_html.xpath('//div[@id="chapterlistload"]')
        if not chapter_container:  # 判断章节的父级容器是否存在，如不存在直接抛出异常
            raise IndexError(
                f'****\t获取到的章节容器为空，漫画名：{comic_info["name"]}，网址：{self.comic_url}\t****')

        # 返回漫画信息、所有章节的父级容器
        return comic_info, chapter_container[0]

    async def get_chapter_info(self, chapter_container: Any, start_chapter: int, end_chapter: int) -> \
            AsyncGenerator[list[tuple[int, str, str]], Any]:
        """
        我们从__init__()中可以看到，有一个chapter_concurrency

        即获取章节URl时的最大并发量，也就等同于这里返回的列表长度

        :param chapter_container: 所有章节的容器容器
        :param start_chapter: 起始的章节数
        :param end_chapter: 结束的章节数
        :return: 异步迭代器，返回由章节URl组成的列表
        """
        all_chapter = []
        xpath_rule = './a[@class="detail-list-form-item"]'  # 提取章节节点所需要的xpath规则
        for current_sec_num in range(start_chapter, end_chapter + 1):
            chapter_url = chapter_container.xpath(f'string({xpath_rule}[{current_sec_num}]/@href)')
            chapter_name = chapter_container.xpath(f'string({xpath_rule}[{current_sec_num}]/text())')
            comic_homepage_url = "/".join(self.comic_url.split('/')[:3])  # 漫画网站的根域名，用来拼接URL
            # 由章节顺序、章节标题、章节URl组成的元组
            chapter_info = (current_sec_num, self.remove_sp_str(chapter_name), f'{comic_homepage_url}{chapter_url}')
            all_chapter.append(chapter_info)  # 将元组加入至数组中
            # 判断是否等同于并发量或者已经遍历到最后结束章节了
            if len(all_chapter) == self.chapter_concurrency or current_sec_num == end_chapter:
                yield all_chapter
                all_chapter = []  # 列表赋值清空，才能保证每次返回的不会重复叠加

    async def save_file(self, comic_name: str, chapter_num: int, chapter_name: str, chapter_url: str,
                        req_headers: dict[str, str], sec_img_num: int,
                        sec_img_url: str, save_path: Path) -> None:
        """
        用于保存文件，由于是个协程函数，它会返回一个协程，结合run_comic_coroutine()方法，被存储至列表中

        并且列表长度会等于同self.image_concurrency，即下载图片的最大并发量

        :param comic_name: 漫画名字
        :param chapter_num: 章节顺序
        :param chapter_name: 章节标题
        :param chapter_url: 章节URL
        :param req_headers: 请求头
        :param sec_img_num: 章节中对应的第几张图片
        :param sec_img_url: 章节中每张图片的URL
        :param save_path: 保存路径
        :return: None
        """
        img_res = await asyncio.create_task(self.fetch(sec_img_url, 'file', headers=req_headers))
        # 判断图片响应是否为空
        if img_res is None:
            raise TypeError(
                f'****\t下载图片失败，返回为空，网址：{chapter_url}，漫画名：{comic_name}，章节数：{chapter_num}，第{sec_img_num}张图片\t****')
        img_format = sec_img_url.split('.')[-1]  # 获取图片格式
        with open(rf'{save_path}/（{sec_img_num}）图片-{sec_img_num}.{img_format}', 'wb') as img_file:
            img_file.write(img_res)
            self.print_true(
                f'\t漫画名：{comic_name}，章节数：{chapter_num}，章节名：{chapter_name}，第{sec_img_num}张图片，保存成功\t')

    async def run_comic_coroutine(self, comic_name: str, chapter_num: int, chapter_name: str, chapter_url: str,
                                  start_img: int | None, end_img: int | str | None, save_path: Path) -> None:
        """
        用于调用保存文件的coroutine，即save_file()，将save_file()返回的coroutine保存至列表中

        并且按照最大图片并发量控制执行，避免图片过多爆内存

        :param comic_name: 漫画名字
        :param chapter_num: 章节顺序
        :param chapter_name: 章节标题
        :param chapter_url: 章节的URl
        :param start_img: 章节的起始图片数
        :param end_img: 章节的结束图片数
        :param save_path: 保存路径
        :return: None
        """
        chapter_html = etree.HTML(await self.fetch(chapter_url, 'text', headers=self.req_headers))
        chapter_main = chapter_html.xpath('//ul[@class="main-container"]')  # 获取章节中的元素节点，因为它是漫画图片的父级元素
        if not chapter_main:  # 如果没有父级容器，则直接抛出错误
            raise IndexError(f'****\t获取漫画图片的父级容器失败，漫画名：{comic_name}，章节数：{chapter_name}\t****')
        # 获取漫画图片的数量
        chapter_img_num = int(chapter_main[0].xpath('count(./li[@class="main-item"]/img)'))
        # 获取起始的图片和最终结束的图片
        start_img, end_img = self.gen_range(start_img, end_img, chapter_img_num)
        comic_coroutine = []  # 用于存储下载图片的协程对象（coroutine object）
        # 遍历章节中的图片数量
        for img_num in range(start_img, end_img + 1):
            # 漫画图片的URl
            sec_img_url = chapter_main[0].xpath(f'string(./li[@class="main-item"][{img_num}]/img/@src)')
            # save_file()返回一个coroutine
            save_coroutine = self.save_file(comic_name, chapter_num, chapter_name, chapter_url, self.req_headers,
                                            img_num, sec_img_url, save_path)
            comic_coroutine.append(save_coroutine)  # 增加至列表中
            # 判断并发量
            if len(comic_coroutine) == self.image_concurrency or img_num == end_img:
                await asyncio.gather(*comic_coroutine)
                await self.random_sleep()
                comic_coroutine = []

    async def load_comic_img(self, comic_name: str, chapter_info: list[tuple[int, str, str]]) -> None:
        """
        负责循环遍历，将所需要的漫画信息传递至run_comic_coroutine()

        :param comic_name: 漫画名字
        :param chapter_info: 从形参的类型注解中可以看出，该参数是个由元组组成的列表，[(章节顺序, 章节标题, 章节URL)...]
        :return: None
        """
        for chapter_num, chapter_name, chapter_url in chapter_info:
            # 保存路径，如果不存在则创建
            save_path = Path(Path(
                __file__).parent / '漫画' / '所有漫画' / comic_name / '漫画内容' / f'（{str(chapter_num)}）{chapter_name}')
            if not (save_path.exists() and save_path.is_dir()):
                save_path.mkdir(parents=True, exist_ok=True)
            await self.run_comic_coroutine(comic_name, chapter_num, chapter_name, chapter_url, self.start_img,
                                           self.end_img, save_path)

    async def download(self, chapter_container: Any, start_chapter: int, end_chapter: int,
                       comic_info: dict[str, str]) -> None:
        """
        运行函数，之所以封装为函数，是因为当all_chapter发生变化，不管是True或者False都需要使用该函数的函数体

        避免代码重复，所以封装为函数，直接调用该函数即可

        :param chapter_container: 所有章节的父级容器
        :param start_chapter: 起始的章节数
        :param end_chapter: 结束的章节数
        :param comic_info: 漫画信息，漫画标题、漫画作者等...
        :return: None
        """
        # chapter_info: 由章节顺序、章节标题、章节URl组成的元组
        async for chapter_info in self.get_chapter_info(chapter_container, start_chapter, end_chapter):
            await self.load_comic_img(comic_info['name'], chapter_info)

    async def run(self, start_chapter: int | None, end_chapter: int | None,
                  all_chapter: bool = False) -> None:
        """
        用于外部调用的下载函数

        :param all_chapter: 是否默认即下载全部
        :param start_chapter: 起始的下载章节数
        :param end_chapter: 结束的下载章节数
        :return: None
        """

        comic_info, chapter_num, chapter_container = await self.view_comic_basic_info()  # 获取漫画信息、章节总数、所有章节的父级容器
        self.print_true(
            f'当前爬取的漫画名：{comic_info["name"]}，漫画网址为：{self.comic_url}，总章数为：{chapter_num}')
        # 如果需要下载全部章节，设置起始和结束章节为全部范围
        if all_chapter:
            # 则将起始章节数变为1，最终章节为变成总章节数即可
            start_chapter, end_chapter = 1, chapter_num
        # 如果说需要下载全部
        elif all_chapter:
            # 如果未指定结束章节，提示用户输入
            if end_chapter is None:
                # 进入循环，判断输入是否章节输入是否正确
                while True:
                    try:
                        start_chapter = int(input('请输入起始的章节数：'))
                        end_chapter = int(input('请输入最终的章节数：'))
                        # 判断是否符合范围之内的章节数
                        if 0 < start_chapter <= end_chapter <= chapter_num:
                            break
                        else:
                            # 如果有错误，就重新将start_chapter和end_chapter赋值，并且使用continue跳过本次循环
                            self.print_false(
                                f'输入的章节获取数有误，总章节数为：{chapter_num}，起始章节为：{start_chapter}，结束章节为：{end_chapter}，请重新输入')
                    except ValueError:
                        self.print_false('请输入正确数字！')
            else:
                start_chapter, end_chapter = self.gen_range(start_chapter, end_chapter, chapter_num)
        await self.download(chapter_container, start_chapter, end_chapter, comic_info)
        self.print_true(f'漫画名：{comic_info["name"]}，下载完成')


def load_config(file_path: Path | str, obj_args: tuple[str, ...], cls_args: tuple[str, ...]) \
        -> tuple[dict[str, list[str]] | dict, dict[str, int | list[str]] | dict]:
    """
    获取配置文件中的信息，用来匹配下载漫画中的参数

    :return: 类属性参数、对象属性参数
    """
    import json

    with open(file_path, 'r', encoding='utf-8') as config_file:
        config = json.load(config_file)

    obj_config = {
        key: config[key]
        for key in obj_args
        if key in config
    }  # 对象的属性配置

    cls_config = {
        class_atr: config[class_atr]
        for class_atr in cls_args
        if class_atr in config
    }  # 类的属性对象

    return cls_config, obj_config


async def main() -> None:
    """
    下载漫画的入口函数

    :return: None
    """
    print('漫画平台网址：https://www.aiguoman.com/')

    comic_config_path = Path(__file__).parent / 'config.json'
    comic_obj_params = ('comic_url_list', 'start_chapter', 'end_chapter',
                        'chapter_concurrency', 'image_concurrency',
                        'min_wait', 'max_wait',
                        'start_img', 'end_img')  # 需要的对象参数
    comic_cls_params = ('proxies',)  # 需要的类属性参数
    comic_class_config, comic_obj_config = load_config(comic_config_path, comic_obj_params, comic_cls_params)

    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Referer': 'https://www.aiguoman.com/',
        'Cookie': f'__51vcke__3G6KgmS2foib6VQp={str(uuid.uuid4())};__51vuft__3G6KgmS2foib6VQp={int(datetime.datetime.now().timestamp())}'
    }

    Comic.set_cls_atr(comic_class_config)

    async with aiohttp.ClientSession() as session:
        for comic_url in comic_obj_config.pop('comic_url_list', False) or [None]:
            comic = Comic(comic_url=comic_url, req_headers=headers, client_session=session, **comic_obj_config)
            await comic.run(start_chapter=comic.start_chapter, end_chapter=comic.end_chapter)


if __name__ == '__main__':
    asyncio.run(main())
