# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage, PDFTextExtractionNotAllowed
from pdfminer.converter import TextConverter, PDFPageAggregator
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdevice import PDFDevice
from pdfminer.layout import LTTextBoxHorizontal, LAParams

import time, io, re, chardet

print(time.time())
infile = 'test.pdf'
outfile = 'test.txt'

inFp = open(infile, 'rb')
outFp = open(outfile, 'w')

# # 创建一个PDF资源管理器对象来存储共享资源,caching = False不缓存
# rsrcmgr = PDFResourceManager(caching=False)
# # 创建一个PDF设备对象
# laparams = LAParams()
# device = TextConverter(rsrcmgr, outFp, codec='utf-8', laparams=laparams)
# # 创建一个PDF解析器对象
# interpreter = PDFPageInterpreter(manager, device)
# for page in PDFPage.get_pages(inFp):
#     interpreter.process_page(page)
#
# device.close()


# parse = PDFParser(inFp)
# document = PDFDocument(parser=parse)
# parse.set_document(doc=document)
# if not document.is_extractable:
#     raise PDFTextExtractionNotAllowed
#
# rsrcmgr = PDFResourceManager(caching=True)
# laparams = LAParams()
# device = PDFPageAggregator(rsrcmgr, laparams=laparams)
# interpreter = PDFPageInterpreter(rsrcmgr, device)
# for page in PDFPage.create_pages(document):
#     # 使用页面解释器来读取
#     interpreter.process_page(page)
#     # 使用聚合器来获取内容
#     layout = device.get_result()
#     for x in layout:
#         if hasattr(x, "get_text"):
#             if isinstance(x, LTTextBoxHorizontal):
#                 str = x.get_text().encode("gbk", "ignore")
#                 # print(type(str).__name__)
#                 # print(str)
#                 # if type(str).__name__ == 'gbk':
#                 #     # str.encode('utf-8')
#                 #     # print(str.replace(u'\xa0', u''))
#                 #     print(1)

inFp.close()
outFp.close()
print(time.time())
