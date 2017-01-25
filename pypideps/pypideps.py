import tarfile, zipfile, re, requests
from StringIO import StringIO

class PyPiDeps(object):
    #using methods from: https://github.com/ogirardot/meta-deps/blob/master/PyPi%20Metadata.ipynb
    def __init__(self, package_name):
        self.package_name = package_name
    
    def _get_requires(self, content):
        results = re.findall("install_requires=\[([\W'a-zA-Z0-9]*?)\]", content, re.M)
        if len(results) == 0:
            results = re.findall("install_requires = \[([\W'a-zA-Z0-9]*?)\]", content, re.M)
        
        if len(results) == 0:
            results = re.findall("requires = \[([\W'a-zA-Z0-9]*?)\]", content, re.M)
            
        if len(results) == 0:
            results = re.findall("requires=\[([\W'a-zA-Z0-9]*?)\]", content, re.M)
            
        return results
    
    
    def _extract_deps(self, content):
        """ Extract dependencies using install_requires directive """
        results = self._get_requires(content)
        deps = []
        if results:
            deps = [a.replace("'", "").strip() for a in results[0].strip().split(",") if a.replace("'", "").strip() != ""]
            deps = [a.replace('"', "") for a in deps]

            for idx, d in enumerate(deps):
                if d[0] in ['<', '>']:
                    #if first letter is symbol, it should be combined with prior
                    deps[idx-1] = deps[idx-1] +","+ deps[idx]
                    del deps[idx]
                
        return deps
    
    def _extract_setup_content(self, package_file, archive_type):
        if archive_type == "tar.gz":
            """Extract setup.py content as string from downladed tar """
            tar_file = tarfile.open(fileobj=package_file)
            setup_candidates = [elem for elem in tar_file.getmembers() if 'setup.py' in elem.name]
            if len(setup_candidates) > 0:
                setup_member = setup_candidates[0]
                content = tar_file.extractfile(setup_member).read()
                return content
            else:
                print "Too few candidates or too many for setup.py in tar" 
                return None
                
        if archive_type == "zip":
            zip_file = zipfile.ZipFile(package_file)
            setup_candidates = [elem for elem in zip_file.namelist() if 'setup.py' in elem]
            #import pdb; pdb.set_trace()
            if len(setup_candidates) > 0:
                setup_member = setup_candidates[0]
                content = zip_file.open(setup_member).read()
                return content
            else:
                print "Too few candidates or too many for setup.py in zip" 
                return None
                
        raise Exception("Incorrect archive type passed")

    
    @property
    def reqs(self):
        response = requests.get("https://pypi.python.org/pypi/%s/json" % self.package_name)
        try:
            pypi_info = response.json()
        except ValueError: #no JSON in response
            import pdb; pdb.set_trace()
        release_url = None
        for downloadable in pypi_info['releases'][pypi_info['info']['version']]:
            if 'tar.gz' in downloadable['url']:
                archive_type = 'tar.gz'
                release_url = downloadable['url']
                break
            else:
                if ('zip' in downloadable['url']) or ('whl' in downloadable['url']):
                    archive_type = 'zip'
                    release_url = downloadable['url']
        if release_url is None:
            return []
        package = requests.get(release_url)
        arc_file = StringIO(package.content)
        content = self._extract_setup_content(arc_file, archive_type)
        reqs = self._extract_deps(content)
        print reqs, "+++++"
        return reqs
