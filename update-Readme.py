import sys
from bs4 import BeautifulSoup

from parsebookmark import parse_root_chrome,parse_root_firefox



def update_README( toc, toc_start="[//]: # (TOCSTART)", toc_end="[//]: # (TOCEND)"):
    toc_file = open("README.md", "r").read()
    start, end = toc_file.find(toc_start), toc_file.find(toc_end)
    render =  (
        (toc_file[: start + len(toc_start)]) +
        ("\n\n%s\n\n" % toc) + (toc_file[end:])
    )
    with open("README.md", "w") as fout:
        fout.writelines(render)

def recursive_traversal(prefix,bookmarks,result,level=0):
    children = bookmarks['children']
    
    
    for item in children:
        result.append(" \n ")
        
        if item['type'] == "folder":
            result.append(prefix+"## "+item['title'])
            if item['children'] != None:
                recursive_traversal(prefix+(""*(level+1)),item,result,level=level+1)
        elif item['type'] == "url":
            result.append(prefix+" * "+item['url'])

            

def main():
    bookmarks_file = sys.argv[1]
    
    with open(bookmarks_file,encoding='utf8') as file:
        soup = BeautifulSoup(markup=file, features="html5lib", from_encoding="Utf-8")

    heading = soup.find("h1")
    root = soup.find("dl")
    if heading.text == "Bookmarks":
        bookmarks = parse_root_chrome(root)
    elif heading.text == "Bookmarks Menu":
        bookmarks = parse_root_firefox(root)
    
    
    bookmarks = bookmarks[1]
    assert(bookmarks['title'] == "Other Bookmarks")
    result = []
    recursive_traversal(prefix="",bookmarks=bookmarks,result=result)
    result = "".join(result)
    print(result)
    update_README(result)
if __name__ == "__main__":
    main()