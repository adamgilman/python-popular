# python-popular
Show the most popular PyPi modules by inclusion in requirements files

Progressive crawler of Python reposistories to determine the popularity 
of python packages

    requiremements = setup.py/egg/requiremements listing

Working backwards
    list of top 100 python packages by order of presence in requiremements
    
    need a count of occcurences of packages 
        
        
create a file for each python package using pypi
    include in the file the name of the package who references it
    don't dedup at first
    