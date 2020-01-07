from whoosh.fields import Schema, TEXT, ID
from jieba.analyse import ChineseAnalyzer

schema = Schema(title=TEXT, path=ID, content=TEXT(stored=True, analyzer=ChineseAnalyzer()))
import os
from whoosh.index import create_in

if not os.path.exists('index'):
    os.mkdir('index')
idx = create_in("index", schema)

writer = idx.writer()
writer.add_document(title="哈哈哈哈哈，嘻嘻",
                    path="99",
                    content="少时诵诗书大撒所三生三世十里桃花")

writer.commit()

from whoosh.qparser import QueryParser

with idx.searcher() as searcher:
    parser = QueryParser("content", schema=idx.schema)
    q = parser.parse('小孩之')
    results = searcher.search(q)
    print(results)
