import luigi, os
import cPickle as pickle
from pypideps import PyPiDeps, _clean_requirements
import requirements as reqq

class GetRepoRequirements(luigi.Task):
    package = luigi.Parameter()
    
    def run(self):
        ppd = PyPiDeps(self.package)
        with self.output().open('w') as out_file:
            for l in ppd.reqs:
                out_file.write(l + "\n")
            
    def output(self):
        return luigi.LocalTarget('./datastore/%s/required' % self.package)
        

class GenerateRepoUtilisation(luigi.Task):
    def run(self):
        required_by = {}
        known_packages = os.listdir("./datastore")
        for idx, p in enumerate(known_packages):
            print "working on [%s:%s]: %s" % (idx, len(known_packages), p)
            try:
                requirements = open("./datastore/%s/required" % p).read().split("\n")
            except IOError:
                continue
            requirements = _clean_requirements(requirements)
            
            print requirements