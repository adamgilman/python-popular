import requirements

def _clean_requirements(raw):
    clean = []
    for item in raw:
        try:
            item = requirements.parse(item).next().name
        except:
            pass
        
        if len(item) > 0:
            if ' ' not in item:
                clean.append( item )
    clean = [x for x in clean if not x.startswith('#')]
    clean = [x.strip(' ') for x in clean]
        
    return clean