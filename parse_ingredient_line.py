1#!/usr/bin/python
import re

measurements = {
    'cup' : ['c','c.','cup','cups'],
    'jar' : ['jar','j','j.'],
    'can' : ['can','cans'],
    'tsp' : ['tsp','tsp.','teaspoon','teaspoons'],
    'tbsp' : ['tbsp','tbsp.','tablespoon','tablespoons'],
    'clove' : ['clove','cloves'],
    'lb' : ['lb','lb.','lbs','lbs.','pound','pounds'],
    'slice' : ['slice','slices'],
    'oz' : ['oz','oz.','ounce','ounces'],
    'stalk' : ['stalk','stalks'],
    'pkg' : ['pkg','pkg.','pkgs','pkgs.','package','packages'],
    'bag' : ['bag','bags','bg','bg.','bgs','bgs.'],
    'quart' : ['quart','quarts','qt','qt.','qts','qts.'],
    'pint' : ['pint','pints','pt','pts','pt.','pts.'],
    'gal' : ['gal','gals','gal.','gals.','gallon','gallons'],
    'pinch' : ['pinch','pinches']
}

number_map = {
    'one' : '1',
    'two' : '2',
    'three' : '3',
    'four' : '4',
    'five' : '5',
    'six' : '6',
    'seven' : '7',
    'eight' : '8',
    'nine' : '9',
    'ten' : '10'
    # Anything more than this, and you're feeding an army
}

sizes = {
    'small': ['small','sm','sm.'],
    'medium': ['medium','med','med.'],
    'large': ['large','lg','lg.']
}

def parse_ingredient_line(line):
    ingredient = {}
    ingredient['notes'] = []
    line = line.lower()
    # Parse out special cases
    # Case 1: '1/2 to 1...'
    if re.match('^[0-9]+(\/)?([0-9]+)? to [0-9]+(\/)?([0-9]+)?',line):
        # Change to '1/2-1' format so we can parse it later on
        line = line.replace(' to ','-')
    # Case 2: Parse out size
    if '(' in line:
        size = line[line.find('(')+1:line.find(')')]
        ingredient['size'] = size
        line = line.replace('({})'.format(size),'')
    # Case 3: remove ';'
    line = line.replace(';','')
    # Case 4: 1 1/2
    if re.match('^[0-9]+ [0-9]+(\/)?([0-9]+)?',line):
        parts = line.split(' ')
        ingredient['amount'] = "{} {}".format(parts[0],parts[1])
        parts = parts[2:]
        line = " ".join(parts)
    parts = line.split(' ')
    # Parse out measurement
    for measurement in measurements:
        for alias in measurements[measurement]:
            if alias in parts:
                ingredient['measurement'] = measurement
                parts.remove(alias)
    # Parse out size words
    for size in sizes.keys():
        for size_word in sizes[size]:
            if size_word in parts:
                # If we already parsed 'size' from parentheses, then
                # that was probably just a note
                if 'size' in ingredient.keys():
                    ingredient['notes'].append(ingredient['size'])
                ingredient['size'] = size_word
                line = line.lower().replace(size_word, '')
    # Parse amount
    for part in parts:
        if re.match('^[0-9]+\/[0-9]+$',part) or re.match('^[0-9]+$',part):
            ingredient['amount'] = part
            parts.remove(part)
            break
        if re.match('^[0-9]+(\/)?([0-9]+)?\-[0-9]+(\/)?([0-9]+)?$',part):
            # Make up your mind... just choose an amount
            ingredient['amount'] = part.split('-')[0].strip()
            parts.remove(part)
            break
        for number_word in number_map.keys():
            if part.lower().strip() == number_word:
                ingredient['amount'] = number_map[number_word]
                parts.remove(part)
                break
    main_ingredient = " ".join(parts)
    # Parse out any notes
    if ',' in main_ingredient:
        ingredient['notes'].append(main_ingredient.split(',')[1].strip())
        main_ingredient = main_ingredient.split(',')[0].strip()
    if ' - ' in main_ingredient:
        ingredient['notes'].append(main_ingredient.split(' - ')[1].strip())
        main_ingredient = main_ingredient.split(' - ')[0].strip()
    ingredient['ingredient'] = main_ingredient.strip()
    return ingredient
