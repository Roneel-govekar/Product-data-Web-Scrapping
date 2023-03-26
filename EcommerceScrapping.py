from requests_html import HTMLSession
import csv

s=HTMLSession()

def get_product_link(page):
    url=f"https://themes.woocommerce.com/storefront/product-category/clothing/page/{page}"

    r=s.get(url)
    #print(r.status_code)

    #print(r.text)
    #print(r.html.find("ul.products.columns-4 li a"))

    products=r.html.find("ul.products.columns-4 li ")
    links=[]
    for i in products:
        #print(i.find("a",first=True).attrs['href'])
        links.append(i.find("a",first=True).attrs['href'])

    return links



def parse_product(url):
    r=s.get(url)
    summary=r.html.find("main.site-main div.summary.entry-summary",first=True)
    #print(summary.find("h1.product_title.entry-title",first=True).text.strip())
    name=summary.find("h1.product_title.entry-title",first=True).text.strip()
    cost=summary.find("p.price",first=True).text.strip().replace('\n'," ")
    cat=summary.find("span.posted_in",first=True).text.strip()
    try:
        sku=summary.find("span.sku",first=True).text.strip()
    except AttributeError as err:
        sku="None"


    product={"name" :name,"cost":cost,"sku":sku, "cat":cat }

    return product



#print(parse_product("https://themes.woocommerce.com/storefront/product/lowepro-slingshot-edge-250-aw/"))
results=[]
for x in range(1,4):
    print("page",x)
    urls=get_product_link(x)
    for url in urls:
        results.append(parse_product(url))
        
    print("total",len(results))

def putincsv(results):
    keys=results[0].keys()
    with open("product_data.csv", 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=keys)
        writer.writeheader()
        writer.writerows(results)
        
            

putincsv(results)