import sys
from typing import List
from bs4 import BeautifulSoup

from parsebookmark import parse_root_chrome,parse_root_firefox
import tqdm


def update_README( toc: List[str], toc_start="[//]: # (TOCSTART)", toc_end="[//]: # (TOCEND)"):
  
    with open("README.md", "w") as fout:
        fout.write('\n'.join(toc))

def recursive_traversal(prefix,bookmarks,result,level=0):
    children = bookmarks['children']
    
    
    for item in children:
  
        
        if item['type'] == "folder":
            
            result.append(prefix+"<h2>"+str(item['title']).capitalize()+"</h2>")
            if item['children'] != None:
                result.append("<ul>")
                recursive_traversal(prefix+str(""*(level+1)),item,result,level=level+1)
                result.append("</ul>")
        elif item['type'] == "url":
            result.append(prefix+"<li> <a href=\""+item['url']+"\">"+item['url']+"</a></li> ")

            

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
    # result = "".join(result)
    update_README(result)
if __name__ == "__main__":
    main()