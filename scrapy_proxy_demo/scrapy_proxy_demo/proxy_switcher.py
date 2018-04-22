from txsocksx.http import SOCKS5Agent
from twisted.internet import reactor
#from scrapy.xlib.tx import TCP4ClientEndpoint # will be deprecated in future, import as the next line
from twisted.internet.endpoints import TCP4ClientEndpoint
from scrapy.core.downloader.webclient import _parse
from scrapy.core.downloader.handlers.http11 import HTTP11DownloadHandler, ScrapyAgent

class Socks5DownloadHandler(HTTP11DownloadHandler):
    def download_request(self, request, spider):
        """Return a deferred for the SOCKS5 or HTTP download"""
        if request.meta['proxy'].startswith('socks'):
            agent = ScrapySocks5Agent(contextFactory=self._contextFactory, pool=self._pool)
        else:
            agent = ScrapyAgent(contextFactory=self._contextFactory, pool=self._pool,
                maxsize=getattr(spider, 'download_maxsize', self._default_maxsize),
                warnsize=getattr(spider, 'download_warnsize', self._default_warnsize))

        return agent.download_request(request)

class ScrapySocks5Agent(ScrapyAgent):
    def _get_agent(self, request, timeout):
        bindAddress = request.meta.get('bindaddress') or self._bindAddress
        proxy = request.meta.get('proxy')
        if proxy:
            _, _, proxyHost, proxyPort, proxyParams = _parse(proxy)
            _, _, host, port, proxyParams = _parse(request.url)
            proxyEndpoint = TCP4ClientEndpoint(reactor, proxyHost, proxyPort,
                                timeout=timeout, bindAddress=bindAddress)
            agent = SOCKS5Agent(reactor, proxyEndpoint=proxyEndpoint)
            return agent
        return self._Agent(reactor, contextFactory=self._contextFactory,
            connectTimeout=timeout, bindAddress=bindAddress, pool=self._pool) 