import luigi

from pypideps import PyPiDeps
import xmlrpclib

class GetRepoRequirements(luigi.Task):
    package = luigi.Parameter()
    
    def run(self):
        ppd = PyPiDeps(self.package)
        with self.output().open('w') as out_file:
            for l in ppd.reqs:
                out_file.write(l + "\n")
            
    def output(self):
        return luigi.LocalTarget('./datastore/%s/required' % self.package)
        
class GatherAllRepoInfo(luigi.Task):
    def requires(self):
        # only one api server so we'll use the deutschland mirror for downloading
        client = xmlrpclib.ServerProxy('https://pypi.python.org/pypi')
        packages = client.list_packages()
        return [GetRepoRequirements(p) for p in packages[:100]]
        
    def run(self):
        pass