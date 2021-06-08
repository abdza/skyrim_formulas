#!/bin/env python3

import csv

def intersect(list1,list2):
    list3 = [ value for value in list1 if value in list2]
    return list3

effects = {}
ingredients = {}
print("Hello there")
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
    print('Affect:' + ce + '   good/bad:' + effects[ce])
    curing = []
    for ing in ingredients:
        #print('Ing:' + ing)
        #print('Effects:' + str(ingredients[ing]))
        if ce in ingredients[ing]:
            curing.append(ing)
    for k,curi in enumerate(curing):
        print(curi)
        for i in range(k+1,len(curing)):
            cureff = intersect(ingredients[curi],ingredients[curing[i]])
            cureff.sort()
            print('Other:' + curing[i] + ' Affects:' + str(cureff))
            if len(cureff)>1:
                if curi>curing[i]:
                    curname = curing[i] + ':' + curi
                else:
                    curname = curi + ':' + curing[i]
                print('Long formula name:' + curname)
                multieffects[curname] = cureff

finallist = {}

for me in multieffects:
    print(me + ":::" + str(multieffects[me]))
    curing = me.split(":")
    for ing in ingredients:
        if ing!=curing[0] and ing!=curing[1]:
            eff1 = intersect(ingredients[curing[0]],ingredients[ing])
            eff2 = intersect(ingredients[curing[1]],ingredients[ing])
            if len(eff1)>0 or len(eff2)>0:
                print('Add:' + ing)
                print('Effect 1:' + str(eff1))
                print('Effect 2:' + str(eff2))
                tmpname = [ val for val in curing ]
                tmpname.append(ing)
                tmpname.sort()
                print('Curcuring:' + str(tmpname))
                finalname = ":".join(tmpname)
                finallist[finalname] = list(set(eff1 + eff2))
                finallist[finalname].sort()

with open('formulas.csv',mode='w') as formula_file:
    formula_writer = csv.writer(formula_file, delimiter=',')

    formula_writer.writerow(['Ingredient 1','Ingredient 2','Ingredient 3','Effect 1','Effect 2','Effect 3','Effect 4','Effect 5'])
    for fl in finallist:
        formula_writer.writerow(fl.split(":") + finallist[fl])
    for fl in multieffects:
        formula_writer.writerow(fl.split(":") + [''] + multieffects[fl])
