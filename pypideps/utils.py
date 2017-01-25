import requirements

def _clean_requirements(raw):
    clean = []
    for item in raw:
        try:
            item = requirements.parse(item).next().name
        except:
            pass
        
        bad_chars = [' ', '!', '<', ')', '=']
        if len(item) > 0:
            if not( any((c in bad_chars) for c in item) ):
                clean.append( item )
    clean = [x for x in clean if not x.startswith('#')]
    clean = [x.strip(' ') for x in clean]
        
    return clean