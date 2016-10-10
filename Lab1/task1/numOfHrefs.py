import lxml.html
from xml.etree import ElementTree as etree
from xml.etree import ElementTree
from xml.dom import minidom
from StringIO import StringIO
import requests


BASE_URL = "http://xsport.ua/"
tree = requests.get(BASE_URL).content
nav_hrefs = []

def extract_links(response_text, response_url):
    unique_list = []
    html = lxml.html.fromstring(response_text)
    html.make_links_absolute(response_url)
    for i in html.iterlinks():
        unique_list.append(i)
    unique_list = get_inner_links(BASE_URL, unique_list)
    return unique_list

def num_of_hrefs(url):
    parser = etree.XMLParser(encoding='utf-8')
    page = requests.get(url)
    tree = lxml.html.fromstring(page.content)
    count = tree.xpath(('count(//a/@href)'))
    return count

def get_inner_links(base_url, links):
    valid_links = []
    for link in links:
        if not link[2].find(BASE_URL):
            valid_links.append(link[2])
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
    links = list(set(xsport_clear_links(extract_links(tree, BASE_URL))))
    return links

def get_list_of_links_on_page_by_url(url):
    parser = etree.XMLParser(encoding='utf-8')
    page = requests.get(url)
    tree = lxml.html.fromstring(page.content)
    links = []
    for i in tree.iterlinks():
        links.append(i)

    return links


def get_number_of_links():
    links = get_links()
    num = 0
    for i in range(20):
        num += num_of_hrefs(links[i])
    return num

def get_all_links():
    links = get_links()
    all_links = []
    for i in range(20):
        all_links.extend(get_list_of_links_on_page_by_url(links[i]))
    links = list(set(xsport_clear_links(extract_links(tree, BASE_URL))))
    return all_links

def get_xml_result():
    links = get_links()
    data = etree.Element('data')
    for i in range(len(links)):
        page = etree.SubElement(data, 'page', {'url': links[i]})
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
    num = get_number_of_links()
    xml = get_xml_result()
    write_xml_to_file(xml, 'task1.xml')
    print "Number or links: ", num

task1()

