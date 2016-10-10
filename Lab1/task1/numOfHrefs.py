import lxml.html
from xml.etree import ElementTree as etree
from xml.etree import ElementTree
from xml.dom import minidom
from StringIO import StringIO
import requests


BASE_URL = "http://xsport.ua/"
tree = requests.get(BASE_URL).content
nav_hrefs = []

def extract_links(url):
    response_text = requests.get(url).content
    html = lxml.html.fromstring(response_text)
    html.make_links_absolute(BASE_URL)
    links = html.xpath('//img/@src')
    return {"url": url, "links": links}

def get_pages():
    response_text = requests.get(BASE_URL).content
    html = lxml.html.fromstring(response_text)
    html.make_links_absolute(BASE_URL)
    links = []
    i = 0
    for link in html.iterlinks():
        links.append(link[2])

    return links


def num_of_hrefs(url):
    parser = etree.XMLParser(encoding='utf-8')
    page = requests.get(url)
    tree = lxml.html.fromstring(page.content)
    count = tree.xpath(('count(//img/@src)'))
    return count

def get_inner_links(base_url, links):
    valid_links = []
    for link in links:
        if link.find(BASE_URL) != -1:
            valid_links.append(link)
    return valid_links

def xsport_clear_links(links):
    valid_links = []
    forbidden_hrefs = ['bitrix', 'include', 'upload', 'profile']
    for link in links:
        good = True
        for fh in forbidden_hrefs:
            if link.find(fh) != -1:
                good = False
        if (good):
            valid_links.append(link)
    return valid_links

def get_links():
    num = 0
    # CREATING LIST WITH UNIQUE LINKS
    links = list(set(xsport_clear_links(extract_links(BASE_URL))))
    return links

def get_list_of_links_on_page_by_url(url):
    parser = etree.XMLParser(encoding='utf-8')
    page = requests.get(url)
    tree = lxml.html.fromstring(page.content)
    links = []
    for i in tree.iterlinks():
        links.append(i)

    return links

def get_number_of_links(xml):
    count = len(xml.getchildren())
    return count

def get_xml_result(pages):
    data = etree.Element('data')
    for page in pages:
        doc = etree.SubElement(data, 'page', {'url': page["url"]})
        for img in page["links"]:
            fragment = etree.SubElement(doc, 'fragment', {"src": img})
    return data

def prettify(elem):
    """Return a pretty-printed XML string for the Element."""
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

def write_xml_to_file(etree, filename):
    with open(filename, 'w') as f:  ## Write document to file
        f.write(prettify(etree))

def task1():
    pages = list(set(get_inner_links(BASE_URL, xsport_clear_links(get_pages()))))
    images = get_images_from_20_links(pages)
    xml = get_xml_result(images)
    print "XML Formet"
    write_xml_to_file(xml, 'task1.xml')
    print "XML has been writted to file"
    num = get_number_of_links(xml)
    print "Number or links: ", num

def get_images_from_20_links(pages):
    images = []
    for i in range(20):
        images.append(extract_links(pages[i]))
    return images

task1()

