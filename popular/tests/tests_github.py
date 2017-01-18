#get information from github repo
    #get requirements.py file
    #get all packages
        #get all version of packages used
import unittest, logging
from popular.github import Github

import vcr

my_vcr = vcr.VCR(
	serializer = 'yaml',
	cassette_library_dir = 'popular/tests/fixtures/',
	record_mode = 'once',
)

logging.basicConfig() # you need to initialize logging, otherwise you will not see anything from vcrpy
vcr_log = logging.getLogger("vcr")
vcr_log.setLevel(logging.DEBUG)

class TestGitHubExaminer(unittest.TestCase):
    def setUp(self):
        self.test_repo = "https://github.com/kennethreitz/requests"
        self.gh = Github(self.test_repo)
        
        self.not_python_test_repo = "https://github.com/rails/rails"
        self.gh_notpy = Github(self.test_repo)
    
    def test_object_basics(self):
        self.assertEqual( type(self.gh), Github )

    def test_get_requirements_url(self):
        result = 'https://raw.githubusercontent.com/kennethreitz/requests/master/requirements.txt'
        self.assertEqual( self.gh.requirements_url, result)

    @my_vcr.use_cassette('github-tests.json')        
    def test_get_requirements(self):
        desired = open('./popular/tests/fixtures/requests.requirements.txt', 'r').read()
        self.assertEqual( desired, self.gh.get_requirements_txt() )
    
    @my_vcr.use_cassette('github-tests.json')
    def test_get_list_of_python_packages_and_versions(self):
        packages = self.gh.get_packages()
        self.assertEqual( type(packages), list)
        self.assertEqual( packages[0].name, 'alabaster' )
        self.assertEqual( packages[0].specs, [(u'==', u'0.7.9')] )
        self.assertEqual( packages[0].extras, [] )