from __init__ import es, DOM

# from Europe.universities import the_university_of_nottingham, the_university_of_nottingham_parser
from North_America.USA import new_york_university

"""
Europe
"""
# university_url = the_university_of_nottingham['url']


"""
North America
USA
"""
# university = university_of_wisconsin_madison()
# university = university_of_chicago()
# university = university_of_michigan()
# university = university_of_california_san_diego()
# university = new_york_university()

if __name__ == '__main__':
    # for i in xrange(8):
        # print i
        # continue
    # new_url = university.university_info['url'] + '?page='+str(i)
    #     print new_url
    dom = DOM(university.university_info['url'])
    doc = university.parser(dom)
    print doc
    # for i in doc:
#     es.index(index='personal',doc_type='university',body=i,id=i['prof_data']['email'])