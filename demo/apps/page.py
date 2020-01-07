#!/usr/bin/env python
# encoding: utf-8
'''
@author: qiuyan
@contact: winston@peipeiyun.com
@file: page.py
@time: 2019/1/4 4:28 PM
@desc:
'''

class Paginator():
    """
        系统查询分页工具
    """
    def __init__(self, url_func, page=1, total=0, page_size=10):

        self.url_func = url_func
        self.page = 1 if int(page) < 1 else int(page)   #当前页
        self.total = int(total)   #总条数
        self.page_size = int(page_size)
        #总页数
        self.page_num = (self.total%self.page_size==0) and int(self.total/self.page_size) or int(self.total/self.page_size)+1
        self.page_bars = {}
        #开始数
        self.page_start=(self.page-1)*page_size+1
        #尾数
        self.page_end=self.page*page_size
        self.data = ()
        self.page_data={'page':self.page,
                        'page_size':self.page_size,
                        'total_page':self.page_num,
                        'total':self.total
                        }
        for _page in range(1, self.page_num + 1):
            _index = int(_page / 10)
            if not _index in self.page_bars:
                self.page_bars[_index] = {_page}
            else:
                self.page_bars[_index].add(_page)


    def render(self,form_id=None,paras=None):
        '''
        动态输出html内容

              <div class="page">
                                <div>
                                    <a class="prev" href="">&lt;&lt;</a>
                                    <a class="num" href="">1</a>
                                    <span class="current">2</span>
                                    <a class="num" href="">3</a>
                                    <a class="num" href="">489</a>
                                    <a class="next" href="">&gt;&gt;</a></div>
                            </div>


        '''
        page_bar = self.page_bars.get(int(self.page / 10))
        # if page_bar is None:
        #     return ''

        _htmls = []
        if form_id:
            _htmls.append('''<script>
                function goto_page(form_id,page){
                    var form=document.getElementById(form_id);
                    var page_input = document.createElement("input");
                    page_input.type="hidden";
                    page_input.name="page";
                    page_input.value=page;
                    form.appendChild(page_input);
                    form.submit();
                }</script>''')

        _htmls.append('<div class="page">')
        #_htmls.append('\t<li class="disabled"><a >查询记录数 %s</a></li>' % self.total)

        current_start = self.page
        if current_start == 1:
            _htmls.append('\t <a class="prev" >&lt;&lt;</a>')
            _htmls.append('\t <a class="prev" >&lt;</a>')
        else:
            _htmls.append('\t <a class="prev" href="%s">&lt;&lt;</a>' % self.url_func(1,form_id))
            _htmls.append('\t<a class="prev" href="%s">&lt;</a>' % self.url_func(current_start - 1,form_id))

        if page_bar:
            for page in page_bar:
                # print page
                _page_url = self.url_func(page,form_id)
                if page == self.page:
                    _htmls.append('\t<span class="current">%s</span>' % page)
                else:
                    _htmls.append('\t<a class="num" href="%s">%s</a>' % (_page_url, page))

        current_end = self.page
        if current_end == self.page_num:
            _htmls.append('\t <a class="next" >&gt;</a>')
            _htmls.append('\t <a class="next" >&gt;&gt;</a>')
        else:
            _htmls.append('\t<a class="next" href="%s">&gt;</a>' % self.url_func(current_end + 1,form_id))
            _htmls.append('\t<a class="next" href="%s">&gt;&gt;</a>' % self.url_func(self.page_num,form_id))
        _htmls.append('</div>')
        return '\r\n'.join(_htmls)

    def pagination_html(self,form_id=None,params={}):
        pass
               # '<div class="splitPages" style="display: block;">
               #          <a href="javascript:void(0);">Первая</a>
               #          <a class="prevPage">Далее</a>
               #          <span>1</span>
               #          <a data-page="2" href="javascript:void(0);" class="nextPage">Назад</a>&nbsp;
               #          <a href="javascript:void(0);">末页</a>'

    def to_dict(self):
        return {key:getattr(self,key) for key in ['page','total','page_size','page_num','page_start','page_end']}


    def ajax_render(self, form_id=None, paras=None):
        '''
        动态输出html内容
        '''
        page_bar = self.page_bars.get(int(self.page / 10))
        if page_bar is None:
            return ''

        _htmls = []
        if form_id:
            _htmls.append('''<script>
                function goto_page(form_id,page){
                    var form=document.getElementById(form_id);
                    var page_input = document.createElement("input");
                    page_input.type="hidden";
                    page_input.name="page";
                    page_input.value=page;
                    form.appendChild(page_input);
                    form.submit();
                }</script>''')

        _htmls.append('<div class="pull-right pagination" ><ul class="pagination">')
        _htmls.append('\t<li class="disabled"><a >查询记录数 %s</a></li>' % self.total)

        current_start = self.page
        if current_start == 1:
            _htmls.append('\t<li  class="page-first disabled" ><a >«</a></li>')
            _htmls.append('\t<li  class ="page-first disabled"><a >‹</a></li>')
        else:
            _htmls.append('\t<li class ="page-first"><a href="javascript:ajax_get_items(%s);">«</a></li>' % ("'"+self.url_func(1, form_id)+"'"))
            _htmls.append('\t<li class ="page-pre"><a href="javascript:ajax_get_items(%s);">‹</a></li>' % ("'"+self.url_func(current_start - 1, form_id)+"'"))

        for page in page_bar:
            _page_url = self.url_func(page, form_id)
            if page == self.page:
                _htmls.append(
                    '\t<li class="page-number active"><span>%s <span class="sr-only">{current}</span></span></li>' % page)
            else:
                _htmls.append('\t<li class="page-number" ><a href="javascript:ajax_get_items(%s);">%s</a></li>' % ("'"+_page_url+"'", page))

        current_end = self.page
        if current_end == self.page_num:
            _htmls.append('\t<li class="page-next disabled"><a > › </a></li>')
            _htmls.append('\t<li class="page-last disabled"><a > » </a></li>')
        else:
            _htmls.append('\t<li class="page-next"><a href="javascript:ajax_get_items(%s);"> › </a></li>' % ("'"+self.url_func(current_end + 1, form_id)+"'"))
            _htmls.append('\t<li class="page-last" ><a href="javascript:ajax_get_items(%s);"> » </a></li>' % ("'"+self.url_func(self.page_num, form_id)+"'"))

        _htmls.append('</ul> </div>')

        return '\r\n'.join(_htmls)
