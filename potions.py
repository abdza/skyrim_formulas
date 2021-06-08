#!/bin/env python3

import csv

def intersect(list1,list2):
    list3 = [ value for value in list1 if value in list2]
    return list3

def category(list1,effects):
    cat = 'Good'
    good = 0
    bad = 0
    for ing in list1:
        if effects[ing]=='Good':
            good += 1
        else:
            bad += 1
    if bad==0:
        return 'Potion'
    elif good==0:
        return 'Poison'
    else:
        return 'Downside'

effects = {}
ingredients = {}
print("Formulating formulas")


with open('ingredients.csv') as csvfile:
    aff = csv.reader(csvfile, delimiter=',')
    for row in aff:
        if row[0] not in effects.keys():
            effects[row[0]] = row[1]
with open('skyrim-ingredients.csv', newline='') as csvfile:
    ingre = csv.reader(csvfile, delimiter=',')
    for row in ingre:
        if row[0] not in ingredients.keys():
            ingredients[row[0]] = [row[1],row[2],row[3],row[4]]

multieffects = {}

for ce in effects:
    curing = []
    for ing in ingredients:
        if ce in ingredients[ing]:
            curing.append(ing)
    for k,curi in enumerate(curing):
        for i in range(k+1,len(curing)):
            cureff = intersect(ingredients[curi],ingredients[curing[i]])
            cureff.sort()
            if len(cureff)>1:
                if curi>curing[i]:
                    curname = curing[i] + ':' + curi
                else:
                    curname = curi + ':' + curing[i]
                multieffects[curname] = cureff

finallist = {}

for me in multieffects:
    curing = me.split(":")
    for ing in ingredients:
        if ing!=curing[0] and ing!=curing[1]:
            eff1 = intersect(ingredients[curing[0]],ingredients[ing])
            eff2 = intersect(ingredients[curing[1]],ingredients[ing])
            if len(eff1)>0 or len(eff2)>0:
                tmpname = [ val for val in curing ]
                tmpname.append(ing)
                tmpname.sort()
                finalname = ":".join(tmpname)
                finallist[finalname] = list(set(multieffects[me] + eff1 + eff2))
                finallist[finalname].sort()

with open('formulas.csv',mode='w') as formula_file:
    formula_writer = csv.writer(formula_file, delimiter=',')

    formula_writer.writerow(['Category','Ingredient 1','Ingredient 2','Ingredient 3','Effect 1','Effect 2','Effect 3','Effect 4','Effect 5'])
    for fl in finallist:
        formula_writer.writerow([category(finallist[fl],effects)] + fl.split(":") + finallist[fl])
    for fl in multieffects:
        formula_writer.writerow([category(multieffects[fl],effects)] + fl.split(":") + [''] + multieffects[fl])
