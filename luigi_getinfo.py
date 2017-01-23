import luigi
import cPickle as pickle

from pypideps import PyPiDeps

class GetRepoRequirements(luigi.Task):
    package = luigi.Parameter()
    
    def run(self):
        ppd = PyPiDeps(self.package)
        with self.output().open('w') as out_file:
            for l in ppd.reqs:
                out_file.write(l + "\n")
            
    def output(self):
        return luigi.LocalTarget('./datastore/%s/required' % self.package)
        

class GetRepoInfo(luigi.Task):
    pickled_packages = luigi.Parameter()
    def requires(self):
        packages = pickle.loads(self.pickled_packages)
        yield [GetRepoRequirements(p) for p in packages]
    def run(self): pass

class GatherAllRepoInfo(luigi.Task):
    def requires(self):
        # only one api server so we'll use the deutschland mirror for downloading
        packages = open('package.list', 'r').read().split("\n")
        #return [GetRepoRequirements(p) for p in packages]
        step = 10
        for i in range(0, len(packages), step):
            package_slice = packages[i:i+step]
            wire_data = pickle.dumps(package_slice)
            yield GetRepoInfo(wire_data)
        
    def run(self):
        pass