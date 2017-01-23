import unittest

from pypideps import PyPiDeps

class TestGetRequires(unittest.TestCase):
    def setUp(self):
        pass
    
    def test_inceptron(self):
        self.ppd = PyPiDeps('inceptron')
        self.assertItemsEqual( self.ppd.reqs, [] )
    
    def test_requests(self):
        self.ppd = PyPiDeps('requests')
        self.assertItemsEqual( self.ppd.reqs, [] )
        
    def test_dateutil(self):
        self.ppd = PyPiDeps('python-dateutil')
        reqs = ['six >=1.5']    
        self.assertItemsEqual( self.ppd.reqs, reqs )
    
    def test_flask(self):
        reqs = [
        'Werkzeug>=0.7',
        'Jinja2>=2.4',
        'itsdangerous>=0.21',
        'click>=2.0',
        ]
        self.ppd = PyPiDeps('flask')
        self.assertItemsEqual( self.ppd.reqs, reqs )
        
    def test_paramiko(self):
        reqs = [
        'cryptography>=1.1',
        'pyasn1>=0.1.7',
    ]
        self.ppd = PyPiDeps('paramiko')
        self.assertItemsEqual( self.ppd.reqs, reqs )

    def test_jinja(self):
        reqs = ['MarkupSafe>=0.23']
        self.ppd = PyPiDeps('jinja2')
        self.assertItemsEqual( self.ppd.reqs, reqs )

    def test_awscli(self):
        self.ppd = PyPiDeps('awscli')
        reqs = ['botocore==1.5.4',
            'colorama>=0.2.5,<=0.3.7',
            'docutils>=0.10',
            'rsa>=3.1.2,<=3.5.0',
            's3transfer>=0.1.9,<0.2.0',
            'PyYAML>=3.10,<=3.12']
        self.assertItemsEqual( self.ppd.reqs, reqs )
