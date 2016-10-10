import requests
import codecs
from xml.etree import ElementTree as etree
from bs4 import BeautifulSoup
from xml.dom import minidom


def get_list_of_sofas():
    r = requests.get("http://www.meblium.com.ua/myagkaya-mebel/divany/filter/count=20")
    c = r.content
    encoding = r.encoding if 'charset' in r.headers.get('content-type', '').lower() else None
    soup = BeautifulSoup(c, "lxml", from_encoding=encoding)
    products = soup.find_all("div", "product")
    data = []
    for prod in products:
        sofa = {}
        sofa["name"] = prod.findAll("span", {"class": "product-name"})[0].text
        sofa["img"] = prod.findAll("img", {"class": "img-responsive"})[0].attrs['src']
        sofa["sizes"] = prod.findAll("span", {"class": "product-model"})[1].text.rstrip().strip()
        sofa["price"] = prod.findAll("span", {"class": "old-price"})[0].text
        data.append(sofa)
    return data

def get_xml_from_sofas_list(sofas):
    data = etree.Element('data')
    for i in range(len(sofas)):
        product = etree.SubElement(data, 'product')
        name = etree.SubElement(product, 'name')
        name.text = sofas[i]["name"]
        img = etree.SubElement(product, 'img')
        img.text = sofas[i]["img"]
        sizes = etree.SubElement(product, 'sizes')
        sizes.text = sofas[i]["sizes"]
        price = etree.SubElement(product, 'price')
        price.text = sofas[i]["price"]
    return data

def prettify(elem):
    """Return a pretty-printed XML string for the Element."""
    rough_string = etree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

def write_xml_to_file(etree, filename):
    file = codecs.open(filename, "w", "utf-8")  ## Write document to file
    file.write(prettify(etree))
    file.close()

write_xml_to_file(get_xml_from_sofas_list(get_list_of_sofas()), 'task2.xml')