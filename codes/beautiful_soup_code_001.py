def get_course_details_bs(url,course):
    
    from bs4 import BeautifulSoup
    import requests

#https://stackoverflow.com/questions/22726860/beautifulsoup-webscraping-find-all-finding-exact-match
    try:
        #print(f"URL is {url}")
        req=requests.get(url).text
        soup=BeautifulSoup(req, 'lxml')        


        full_course_title = soup.find_all("span", {"data-bind" : "text : courseDetail.courseTitle"})
        #full_course_title = soup.find_all(attrs={'data-bind': re.compile(r"$courseDetail.courseTitle$")})
        print("Full course title")
        for i in full_course_title:
            fct = i.text

        print("Course objectives")
        course_objectives = soup.find_all("p",  {"data-bind" : "html : courseDetail.courseObjective"})
        for i in course_objectives:
            cobj = i.text

        return fct,cobj
    
    except:
        print(f"Error retrieving course details information for course {course['title_header']}")
        for err in sys.exc_info():
            print(err)

        return "",""