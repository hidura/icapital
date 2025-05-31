import asyncio
import json
from playwright.sync_api import Page, expect,sync_playwright
import argparse
import codecs


class Scrap:

    def __init__(self, url, link):
        self.url=url
        self.link=link
        #Here I store the filters
        self.department={}
        self.offices={}
        self.employment_type={}
        self.job_level={}
        #And here I give the filters positions so it can be easly filtered
        self.department_pos={}
        self.offices_pos={}
        self.employment_type_pos={}
        self.job_level_pos={}
        #Here the variable that will be included in the help verbose to allow the user to choose the filter
        self.department_help=""
        self.offices_help=""
        self.employment_type_help=""
        self.job_level_help=""


        with sync_playwright() as interface:
            self.portal = interface.chromium.launch()
            self.site = self.portal.new_page()
            self.site.goto(self.url)
            self.site.click(self.link)
            self.site.wait_for_load_state("networkidle")
            
            for select in self.site.query_selector_all("select"):
                
                cont_id=0
                
                for option in select.query_selector_all("option"):
                    if select.get_attribute("id") == 'filter_dep':
                        
                        self.department[option.inner_text()]=option.get_attribute("value")
                        self.department_pos[str(cont_id)]=option.inner_text()
                        self.department_help += f"{cont_id}-{option.inner_text()},\n"
                        if option.get_attribute("value") !=None:
                            # I do this just to add all the jobs in the "All" option which is always the first option
                            self.department[self.department_pos["0"]]+=option.get_attribute("value")+","
                        else:
                            self.department[self.department_pos["0"]]=""
                    elif select.get_attribute("id") == 'filter_office':
                        self.offices[option.inner_text()]=option.get_attribute("value")
                        self.offices_pos[str(cont_id)]=option.inner_text()
                        self.offices_help += f"{cont_id}-{option.inner_text()},\n"
                        if option.get_attribute("value") !=None:
                            # I do this just to add all the jobs in the "All" option which is always the first option
                            self.offices[self.offices_pos["0"]]+=option.get_attribute("value")+","
                        else:
                            self.offices[self.offices_pos["0"]]=""

                    elif select.get_attribute("id") == 'filter_emp_type':
                        self.employment_type[option.inner_text()]=option.get_attribute("value")
                        self.employment_type_pos[str(cont_id)]=option.inner_text()
                        self.employment_type_help += f"{cont_id}-{option.inner_text()},\n"
                        if option.get_attribute("value") !=None:
                            # I do this just to add all the jobs in the "All" option which is always the first option
                            self.employment_type[self.employment_type_pos["0"]]+=option.get_attribute("value")+","
                        else:
                            self.employment_type[self.employment_type_pos["0"]]=""
                    elif select.get_attribute("id") == 'filter_job_level':
                        self.job_level[option.inner_text()]=option.get_attribute("value")
                        self.job_level_pos[str(cont_id)]=option.inner_text()
                        self.job_level_help += f"{cont_id}-{option.inner_text()},\n"
                        if option.get_attribute("value") !=None:
                            # I do this just to add all the jobs in the "All" option which is always the first option
                            self.job_level[self.job_level_pos["0"]]+=option.get_attribute("value")+","
                        else:
                             self.job_level[self.job_level_pos["0"]]=""
                    cont_id+=1
            

            arguments_description ="""This are the arguments that can be passed if not passed the script take the next option\n
            Department: 0 - 'All Departments'\n
            Offices: 1 - 'CA ON - Toronto'\n
            Employment Type: 1 - 'Full-time' \n
            Job Listing Level: 0 - 'All Jobs Levels'\n """

            parser = argparse.ArgumentParser(description=arguments_description)
            
            parser.add_argument("--department", help="The departments aviables: {}".format(self.department_help), type=str, default=0)
            parser.add_argument("--office", help="The office aviables: {}".format(self.offices_help), type=str, default=1)
            parser.add_argument("--employment_type", help="The Employment Type aviables: {}".format(self.employment_type_help), type=str, default=1)
            parser.add_argument("--job_level", help="The Job Level aviables: {}".format(self.job_level_help), type=str, default=0)
            
            args = parser.parse_args()
            self.get_info_filter(args=args)


    def cleanText(self, text):
        return "\n".join(line.strip() for line in text.replace("\t", " ").splitlines())
       
    def get_info_filter(self, args):

        office = self.offices_pos["1"]
        if str(args.office) in self.offices_pos:
            office = self.offices_pos[str(args.office)]
        department = self.department_pos["0"]
        if str(args.department) in self.department_pos:
            department = self.department_pos[str(args.department)]
        employment_type = self.employment_type_pos["1"]
        if str(args.employment_type) in self.employment_type_pos:
            employment_type = self.employment_type_pos[str(args.employment_type)]
        job_level = self.job_level_pos["0"]
        if str(args.job_level) in self.job_level_pos:
            job_level = self.job_level_pos[str(args.job_level)]


        print(office,department,employment_type,job_level)
        url = self.site.url+"?"
        if office != "All Ofices":
            url+=f"office={office}"
        if department != "All Departments":
            url+=f"&department={department}"
        if employment_type != "All Employment Types":
            url+=f"&emp_type={employment_type}"
        if job_level != "All Job Levels":
            url+=f"&job_level={job_level}"
        
        self.site.goto(url)

        # jobs_avaible_filtered= set(self.offices[office].split(",")) & set(self.department[department].split(",")) & \
        #     set(self.employment_type[employment_type].split(",")) & set(self.job_level[job_level].split(","))
        
        job_data = {}
        # for job_id in jobs_avaible_filtered:
        self.site.wait_for_load_state("networkidle")
        jobs_div=self.site.query_selector_all(".jobs")
        pagination=self.site.query_selector("#pagination")
        pages = len(pagination.query_selector_all("[data-filter-page]")) if len(pagination.query_selector_all("[data-filter-page]"))>0 else 1
        cont=1
        for child in range(0,pages):
            for job_div in jobs_div[0].query_selector_all(":scope > *"):
                
                
                if job_div.evaluate(
                    "(el, className) => el.classList.contains(className)",
                    "nojob"
                ):
                    job_data['error']=job_div.inner_text()

                elif not job_div.evaluate(
                    "(el, className) => el.classList.contains(className)",
                    "nojob"
                ) and job_div.evaluate(
                    """(el) => {
                        const style = window.getComputedStyle(el);
                        return style && style.display !== 'none';
                    }"""
                ):
                    title = job_div.query_selector_all(".job_title")
                    location = job_div.query_selector_all(".display_location")
                    job_location = location[0].inner_text()
                    
                    if job_location.split(":")[1] not in job_data:
                        job_data[job_location.split(":")[1]]=[]
                    
                    job_info={"title":title[0].inner_text(),
                                "location":job_location,
                                "job_description": ""}
                    
                    for description in job_div.query_selector_all(".job_description"):
                        job_info["job_description"]+=self.cleanText(description.inner_text())


                    job_data[location[0].inner_text().split(":")[1]].append(job_info)
            cont+=1
            for next_btn in self.site.query_selector_all(f"[data-filter-page='{str(cont)}']"):
                #This have to be made because theres will be 2 at least button data-filter-page=cont and I want just the one that have the inner_text next
                if next_btn.inner_text()=="Next":
                    next_btn.click()
            

        
        with open("jobdata.json", "w") as f:
            f.write(json.dumps(job_data))

        self.site.close()

    
if __name__ == '__main__': 
    icapital=Scrap("https://icapital.com/","li a:text('Careers')")
    #icapital.closePortal()
