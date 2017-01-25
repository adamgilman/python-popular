import luigi, os
import cPickle as pickle
from pypideps import PyPiDeps, _clean_requirements
import requirements as reqq
import simplejson, datetime

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
        output_requires = {}
        output_required_by = {}
        known_packages = os.listdir("./datastore")
        for idx, package in enumerate(known_packages):
            print "working on [%s:%s]: %s" % (idx, len(known_packages), package)
            try:
                requirements = _clean_requirements( open("./datastore/%s/required" % package).read().split("\n") )
            except IOError:
                continue
            
            output_requires[package] = requirements
            for r in requirements:
                if r in output_required_by:
                    output_required_by[r].append(package)
                else:
                    output_required_by[r] = [package]
        
        counter = 0
        for package, req_by in output_required_by.iteritems():
            counter = counter + 1
            print "writing [%s:%s]: %s" % (counter, len( output_required_by.keys() ), package)
            out = open('./output/%s.json' % package, 'w')
            try:
                out_req = output_requires[package]
            except KeyError:
                out_req = []
            json_out = {
                'generated_at' : datetime.datetime.now(),
                'package' : package,
                'requires' : out_req,
                'required_by' : req_by
            }
            out_content = simplejson.dumps(json_out, default=date_handler)
            out.write(out_content)
            out.close()
            
            
'''
            requirements = _clean_requirements(requirements)
            back_requires[p] = requirements
        
        for r in requirements:
            if required_by.has_key(r):
                required_by[r].append(p)
            else:
                required_by[r] = [p]
                    
        for k,v in required_by.iteritems():
            #out = open('./output/%s' % k, 'w')
            try:
                req_temp = back_requires[k]
            except KeyError:
                req_temp = []
            json_out = {
                'generated_at' : datetime.datetime.now(),
                'package' : k,
                'requires' : req_temp,
                'required_by' : v
            }
            print simplejson.dumps(json_out, default=date_handler)
'''
date_handler = lambda obj: (
    obj.isoformat()
    if isinstance(obj, datetime.datetime)
    or isinstance(obj, datetime.date)
    else None
)