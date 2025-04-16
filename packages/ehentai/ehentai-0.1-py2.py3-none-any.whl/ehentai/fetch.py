import json
import requests
import chardet
from bs4 import BeautifulSoup
import os
from ehentai.conf import *
# book
class Gallery:
    name=""#名字
    cover=""#封面
    view_url=""#视图超链接
    cat=""#类别
    tags=[]#标签
    s_tags=[]#simply tags
    def __init__(self,name=None,cover=None,view_url=None,cat=None,tags=None,s_tags=None):
        self.name=name
        self.cover=cover
        self.view_url=view_url
        self.cat=cat
        self.tags=tags
        self.s_tags=s_tags
    
    def __str__(self):
        return f"Cat:{FONT_STYLE.bold.value}{CATS_BG_COLOR[self.cat]}{self.cat:^12}{RESET}\tURL:{FONT_STYLE.underline.value}{self.view_url}{RESET}\nName:\t{self.name}\nTags:\t{self.s_tags}\n{"_"*20}"
    def __repr__(self):
        return f"<{self.name}>"
    
    def download(self,name=None,path=None,img_suffix="webp",show=True):
        if show:
            print("fetching the URL...")
        path=path if path else "./"
            
        view=get_sp(self.view_url)
        # get the html of the image
        images=list(map(lambda x:x.get('href'),view.find('div',id="gdt").find_all('a')))
        while next_view(view):
            view=get_sp(next_view(view).get('href'))
            images.extend(list(map(lambda x:x.get('href'),view.find('div',id="gdt").find_all('a'))))
        
        # images num
        totals=len(images)
        if show:
            print(f"Totals:{totals}")

        fdir=os.path.join(path,name if name else self.name)
        os.makedirs(fdir)

        for i,v in enumerate(images):

            if show:
                print(f"Downloading...{i+1}/{totals}")

            img_src=get_sp(v).find('img',id="img").get('src')
            img=requests.get(img_src,headers=headers)
            with open(os.path.join(fdir,f"{i}.{img_suffix}"),"wb") as f:
                f.write(img.content)
        
        if show:
            print("Completed!!")
    
    # @return:list(author,list[str])
    def comment(self):
        table=get_sp(self.view_url,encoding='utf-8').find_all('div',class_="c1")
        return list(map(lambda v:(v.find('div',class_="c3").find('a').string,v.find('div',class_="c6").strings),table))


class Page:
    def __str__(self):
        return f"{"-"*50}\nPage:{self.search_text}\n{"-"*50}"
    def __init__(self,sp=None,gl_table:list[Gallery]=[],rangebar=None,search_text=None):
        # prevurl,nexturl,maxdate,mindate,rangeurl,rangemin,rangemax,rangespan
        self.rangebar:dict[str:any]={"prevurl":"","nexturl":"","maxdate":"","mindate":"","rangeurl":"","rangemin":"","rangemax":"","rangespan":""}
        self.search_text="Not Found"
        self.gl_table: list[Gallery] = list(
            map(
                lambda v: Gallery(
                    name=v["name"],
                    cover=v["cover"],
                    view_url=v["view_url"],
                    cat=v["cat"],
                    tags=v["tags"],
                    s_tags=v["s_tags"],
                ),
                gl_table,
            )
        )
        if rangebar:
            self.rangebar=rangebar
        if search_text:
            self.search_text=search_text

        if sp:
            if sp.find('head'):
                self.set_rangebar(sp)
                self.set_search_text(sp)
                self.fetch_gl(sp)
            else:
                self.search_text=sp.get_text()

    def set_rangebar(self,sp: BeautifulSoup):
        rangebar_script=sp.find_all('script',type="text/javascript")
        if rangebar_script:
            rangebar_script=rangebar_script[-1].get_text().splitlines()[1:-1]
            for s in rangebar_script:
                self.rangebar[s[s.find(" ")+1:s.find("=")]]=s[s.find("=")+1:-1].strip("\"")
    def set_search_text(self,sp: BeautifulSoup):
        t=sp.find('div',class_="searchtext")
        if t:
            self.search_text=t.get_text()
        # print(search_text)
    def fetch_gl(self,sp: BeautifulSoup):
        table=sp.find('table',class_="itg gltc")
        if table:
            trs=list(filter(lambda x:x.find('td',class_="gl1c glcat"),table.find_all('tr')))
            for tr in trs:
                # ['gl1c glcat','gl2c','gl3c glname','gl4c glhide']
                td=tr.find_all('td')
                self.gl_table.append(Gallery(
                    name=td[2].find('div',class_="glink").get_text(),
                    cover=td[1].find('img').get('data-src'),
                    view_url=td[2].find('a').get('href'),
                    cat=td[0].find('div').get_text(),
                    tags=list(map(lambda x:x.get('title'),td[2].find_all('div',class_="gt"))),
                    s_tags=list(map(lambda x:x.get_text(),td[2].find_all('div',class_="gt"))),
                ))


def keyword(
    f_search: str = None,
    f_cats: int = None,
    advsearch: bool = None,
    f_sh: bool = None,
    f_sto: bool = None,
    f_spf: int = None,
    f_spt: int = None,
    f_srdd: int = None,
    f_sfl: bool = None,
    f_sfu: bool = None,
    f_sft: bool = None,
):

    return {
        # search_kw
        "f_search":f_search,
        # category
        "f_cats":f_cats,
        # advanced search
        # show advanced options
        "advsearch":1 if advsearch or f_sh or f_sto or f_spf or f_spt or f_srdd or f_sfl or f_sfu or f_sft else None,
        # show expunged galleries
        "f_sh":"on" if f_sh else None,
        # require Gallery torrent
        "f_sto":"on" if f_sto else None,
        # between {f_spf} and {f_spt} Pages
        "f_spf":f_spf,
        "f_spt":f_spt,
        # minimum_rating
        "f_srdd":f_srdd,
        # disable filter language
        "f_sfl":"on" if f_sfl else None,
        # disable filter uploader
        "f_sfu":"on" if f_sfu else None,
        # disable filter tags
        "f_sft":"on" if f_sft else None,
    }


def next_view(sp: BeautifulSoup):
    return sp.find('table',class_="ptt").find_all('td')[-1].find('a')

# url:target_URL
# parms:search_keyword
def get_sp(url: str,params=None,encoding=None):
    # set encoding
    respone=requests.get(url,headers=headers,params=params)
    if encoding:
        respone.encoding=encoding
    else:
        encoding=chardet.detect(respone.content)["encoding"]
        respone.encoding=encoding

    return BeautifulSoup(respone.text,"lxml")


# switch categories: doujinshi...
def get_f_cats(cat_code=0b0011111111):
    res=0b1111111111
    for v in list(i.value for i in CATS):
        if cat_code&1:res&=v
        cat_code>>=1
    return res


url="https://e-hentai.org/"

headers={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Referer":"http://www.google.com",
}
