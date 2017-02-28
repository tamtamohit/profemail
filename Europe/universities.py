continent = 'Europe'
from re import sub


the_university_of_nottingham = {
    'name' : 'The University of Nottingham',
    'country' : 'England',
    'continent' : continent,
    'Department' : 'computer_science',
    'url' : 'https://www.nottingham.ac.uk/computerscience/people/index.aspx'
}

def the_university_of_nottingham_parser(dom):
    base_xpath = '//div[@class="sys_stafflistsection"]/table[@id="ctl111"]/tbody/tr'

    base = dom.xpath(base_xpath)
    # print dom
    doc = []
    for elem in base:
        dic = {}
        internal_elem = elem.xpath('td')
        if len(internal_elem)>0:

            dic['prof_name'] = internal_elem[0].xpath('a/text()')[0]
            dic['prof_name'] = dic['prof_name'].replace(',','')
            dic['contact'] = sub('[()+ ]','',internal_elem[1].xpath('text()')[0])
            dic['designation'] = internal_elem[2].xpath('text()')[0]
            dic['email'] = internal_elem[3].xpath('a')[0].attrib['href']
            dic['email'] = dic['email'][7:]
            # dic2 = {}
            dic2 = the_university_of_nottingham.copy()
            dic2['prof_data'] = dic
            doc.append(dic2)

    return doc

