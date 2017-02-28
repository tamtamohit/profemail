continent = 'North America'

from re import sub

class university_of_wisconsin_madison:
    def __init__(self):
        self.university_of_wisconsin_madison = {
            'name' : 'University of Wisconsin-Madison',
            'county' : 'USA',
            'continent' : continent,
            'Department': 'computer_science',
            'url' : 'http://www.cs.wisc.edu/people/faculty'
            # 'url' : 'https://directory.engr.wisc.edu/display.php/faculty?page=ece&search=faculty'
        }

    def parser(self,dom):

        base_xpath = '//div[@class="people-list"]/ul/li'

        base_elems = dom.xpath(base_xpath)

        doc = []

        for elem in base_elems:
            dic = {}

            profile_name = elem.xpath('div[@class="views-field views-field-field-full-name"]'
                                          '/div/a')[0]
            dic['prof_name'] = profile_name.text
            dic['prof_url'] = 'http://www.cs.wisc.edu/' + profile_name.attrib['href']
            dic['designation'] = elem.xpath('div[@class="views-field views-field-field-title"]'
                                            '/div/text()')[0]
            dic['email'] = elem.xpath('div[@class="views-field views-field-mail"]'
                                      '//a')[0].attrib['href'][7:].lower()

            dic['contact'] = sub('[()+ -]','',elem.xpath('//div[@class="views-field views-field-field-office-phone"]'
                                        '/div/text()')[0][7:])

            dic2 = self.university_of_wisconsin_madison.copy()
            dic2['prof_data'] = dic
            doc.append(dic2)

        return doc


class university_of_chicago():
    def __init__(self):
        self.university_info = {
            'name' : 'University of Chicago',
            'county': 'USA',
            'continent': continent,
            'Department': 'computer_science',
            'url': 'https://cs.uchicago.edu/directories/full/faculty'
        }

    def parser(self,dom):
        base_xpath = '//div[@id="primary-column"]/div/div[@class="view-content"]/div'

        base_elems = dom.xpath(base_xpath)

        doc = []
        for elem in base_elems:
            dic_temp = {}
            elem = elem.xpath('article/div/div[1]')[0]
            all_elem = elem.xpath('*')
            if len(elem)>0:
                for num,an_elem in enumerate(all_elem):
                    # print an_elem.tag
                    if an_elem.tag == 'h2':
                        try:
                            title = an_elem.text.lower()
                            if 'research' in  title:
                                dic_temp['research'] = all_elem[num+1].text
                            elif 'projects' in title:
                                projects_elem = all_elem[num+1].xpath('li')
                                dic_temp['projects'] = []
                                for i in projects_elem:
                                    temp_dic = {}
                                    try:
                                        tem_web_elem = i.xpath('a')[0]
                                        temp_dic['name'] = tem_web_elem.text
                                        temp_dic['url'] = tem_web_elem.attrib['href']
                                    except:
                                        temp_dic['name'] = i.text
                                    dic_temp['projects'].append(temp_dic)
                            elif 'homepage' in title:
                                dic_temp['personal_homepage'] = all_elem[num + 1].xpath('a').attrib['href']
                            elif 'interests' in title:
                                dic_temp['intrests'] = all_elem[num + 1].text
                        except TypeError: pass
                        except AttributeError: pass
                # print ' '
                # exit()
                try:
                    name = elem.xpath('h2/a')[0]
                    dic_temp['prof_name'] = name.text
                    dic_temp['prof_url'] = 'https://cs.uchicago.edu' + name.attrib['href']
                except:
                    dic_temp['prof_name'] = elem.xpath('h2/text()')[0]
                dic_temp['email'] = elem.xpath('p[@class="email"]/a/text()')[0]
                dic_temp['designation'] = elem.xpath('p[@class="title"]/text()')
                dic2 = self.university_info.copy()
                dic2['prof_data'] = dic_temp
                doc.append(dic2)
        return doc

class university_of_michigan():
    def __init__(self):
        self.university_info = {
            'name' : 'University of Michigan',
            'county': 'USA',
            'continent': continent,
            'Department': 'computer_science',
            'url': 'https://www.cse.umich.edu/eecs/faculty/csefaculty.html'
        }

    def parser(self,dom):
        # base_xpath = '//div[@id="content_body"]/table/tbody/tr/td[2]'

        base_elems = dom.xpath('//div[@id="content_body"]/table/tr')
        doc = []
        # print base_elems
        for elem in base_elems:
            texts = elem.xpath('td[2]//text()')
            if len(texts) > 0:
                for num,text in enumerate(texts):
                    texts[num] = text.replace('\n','')
                texts = filter(None,texts)
                texts[0] = sub('[,]','',texts[0])

                temp_dict = {}
                temp_dict['prof_name'] = texts.pop(0)
                temp_dict['designation'] = []
                for n,i in enumerate(texts):
                    if 'division' in i.lower():
                        break
                    elif 'video' in i.lower() or u'\xa0\xa0' in i:
                        pass
                    else:
                        temp_dict['designation'].append(i)
                for i in xrange(n+5):
                    texts.pop(0)
                temp_dict['email'] = ''
                for n, i in enumerate(texts):
                    if 'umich.edu' in i.lower():
                        temp_dict['email'] = temp_dict['email'] + i
                        break
                    else:
                        temp_dict['email'] = temp_dict['email'] + i
                temp_dict['email'] = sub('[ ]','',temp_dict['email'])
                # for i in xrange(n):
                #     texts.pop(0)
                # print texts
                # print temp_dict
                for num,i in enumerate(texts):
                    if 'Phone:' in i:
                        temp_dict['contact'] = sub('[ ()-]','',texts[num+1])
                    elif 'Interests:' in i:
                        temp_dict['interests'] = texts[num+1]

                try:temp_dict['prof_url'] = elem.xpath('td[2]/a')[0].attrib['href']
                except:pass
                dic2 = self.university_info.copy()
                dic2['prof_data'] = temp_dict
                doc.append(dic2)
        return doc


class university_of_california_san_diego():
    def __init__(self):
        self.university_info = {
            'name':'University of California, San Diego',
            'county': 'USA',
            'continent': continent,
            'Department': 'computer_science',
            'url': 'http://jacobsschool.ucsd.edu/faculty/faculty_bios/findprofile.sfe?department=cse'
        }

    def find_email_and_contact(self,url):
        import requests
        from lxml import html
        response = requests.get(url)
        dom = html.document_fromstring(response.text)
        base_xpath = '//table//tr[1]/td[2]/div/div'
        base_elems = dom.xpath(base_xpath)
        # if len(base_elems) >0:
        #     pass
        # else:
        #     base_xpath = '//table/tr[1]/td[2]/div/div'
        email_found_at = 2
        try:
            email = base_elems[email_found_at].xpath('a/text()')[0]
        except IndexError:
            email_found_at = 1
            try: email = base_elems[email_found_at].xpath('a/text()')[0]
            except:
                email_found_at = 3
                try:email = base_elems[email_found_at].xpath('a/text()')[0]
                except:
                    return None,None
            # print dom.xpath('//table/tr[1]/td[2]/div/div[4]/text()')

        # contact = sub('[ ()-]','',base_elems[ema])

        try:
            personal_homepage = base_elems[email_found_at-1].xpath('strong/a')[0].attrib['href']
        except:
            personal_homepage = None

        return email,personal_homepage


    def parser(self,dom):
        base_xpath = '//table[@id="faclist"]/tr[@valign="top"]'

        base_elems = dom.xpath(base_xpath)

        doc = []
        for elem in base_elems:
            temp_dic = {}
            elem = elem.xpath('td')
            name_elem = elem[1].xpath('p/a')[0]
            # print elem[1].xpath('*')
            temp_dic['prof_name'] = sub('[,]','',name_elem.text)
            temp_dic['prof_url'] = 'http://jacobsschool.ucsd.edu/faculty/faculty_bios/'\
                                   + name_elem.attrib['href']

            temp_dic['designation'] = elem[1].xpath('span/p/em/text()')[0]

            temp_dic['interests'] = elem[2].xpath('text()')[0]
            temp_dic['interests'] = sub('[\n\t\r]','',temp_dic['interests'])

            temp_dic['email'],temp_dic['personal_homepage'] = self.find_email_and_contact(temp_dic['prof_url'])

            if temp_dic['email'] == None:continue
            dic2 = self.university_info.copy()
            dic2['prof_data']  = temp_dic
            doc.append(dic2)

        return doc


class new_york_university():
    def __init__(self):
        self.university_info ={
            'name' : 'New York University',
            'county': 'USA',
            'continent': continent,
            'Department': 'computer_science',
            'url': 'https://www.cs.nyu.edu/dynamic/people/faculty/type/20/#'
        }

    def parser(self,dom):
        base_xpath = '//div[@class="row"]/ul/li'
        base_elem = dom.xpath(base_xpath)

        doc = []
        for elem in base_elem:
            temp_dict = {}
            elem = elem.xpath('span/div')[0]
            try:
                name = elem.xpath('p[@class="name bold"]/a')[0]
                temp_dict['prof_name'] = name.text
                temp_dict['prof_url'] = name.attrib['href']
            except:
                temp_dict['prof_name'] = elem.xpath('p[@class="name bold"]/text()')[0]

            designation_elem = elem.xpath('p[@class="title"]/text()')
            if len(designation_elem)>0:
                # print designation_elem
                temp_dict['designation'] = designation_elem[0]

            elem = elem.xpath('p[@class="info"]')

            if len(elem) == 2:
                temp_dict['education'] = elem[0].text.strip(' \t\n\r')
                text_list = elem[1].xpath('text()')
                # print text_list
                for text in text_list:
                    if 'Email: ' in text:
                        # print 'email', text
                        if len(text) > 0:
                            num = text.index('Email: ')
                            text = text[num+7:]
                            text = text.split(' ')
                            for n,i in enumerate(text):
                                if 'at' == i:
                                    text[n] = '@'
                            text = ''.join(text)
                            temp_dict['email'] = text
                        else:
                            temp_dict['email'] = None
                    elif 'Office: ' in text:
                        # print 'office', text
                        pass
                    elif 'Ext: ' in text:
                        # print 'ext',text
                        pass
                    else:
                        # print 'interests', text.strip(' \t\n\r')
                        if len(text.strip(' \t\n\r')) > 0:
                            temp_dict['interests'] = text.strip(' \t\n\r')
            else:
                print 'error in email'
                exit()
            try:
                if temp_dict['email'] == None: continue
            except KeyError: continue
            dic2 = self.university_info.copy()
            dic2['prof_data'] = temp_dict
            doc.append(dic2)
        return doc




class university_of_texas_at_austin():
    def __init__(self):
        university_info = {
            'name' : 'University of Texas at Austin',
            'county': 'USA',
            'continent': continent,
            'Department': 'computer_science',
            'url': 'http://www.cs.utexas.edu/faculty'
        }

    def parser(self,dom):
        base_xpath = '//div[@class="view-content"]'
        base_elem = dom.xpath(base_xpath)

        doc = []

        for elem in base_elem:
            elem = elem.xpath('div/div[2]/div')
            if len(elem)>0:
                try:
                    name = elem[0].xpath('p/strong/a')
                    name =
                except:
                    name = elem[0].xpath('p/strong')