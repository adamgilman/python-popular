import requests, requirements

class Github(object):
    def __init__(self, repo_url):
        self.repo_url = repo_url
        self.requirements_text = None
    
    def get_requirements_txt(self):
        if self.requirements_text is None:
            self.requirements_text = requests.get(self.requirements_url).text
        return self.requirements_text
    
    @property
    def requirements_url(self):
        url = "https://raw.githubusercontent.com/%s/master/requirements.txt"
        return url % self.repo_url.split("github.com/")[1]
        
    def get_packages(self):
        if self.requirements_text is None:
            self.get_requirements_txt()
        return list( requirements.parse(self.requirements_text) )
            
            
        