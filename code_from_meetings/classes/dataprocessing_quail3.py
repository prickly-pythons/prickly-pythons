#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 13 16:15:00 2018

@author: Emily
"""

"""
Program purpose: to take areas representing amount of nutrient (e.g. carotenoids), 
process them, and store them in a way that will be easily retrievable with all
associated data.

"""
import csv



class BIRD:
    """
    A class which represents an individual subject (in this case birds)
    
    The class will be used to create a list of objects with properties
    associated with individual birds in an experiment (e.g. id, sex, treatment,
    tissues, etc.).
    """
    def __init__(self, i="", s="", tr="", ti={}):
        self.__idbird = i
        self.__sex = s
        self.__treatment = tr
        self.__tissues = ti
    
    
    @property
    def tissues(self):
        """
        tissues (ti) represents a dictionary of tissues where the keyword is
        the name of the tissue type (e.g. liver) and the value is a dictionary
        of nutrients in that tissue
        """
        return self.__tissues
    
    
    @tissues.setter
    def tissues(self, value):
        self.__tissues = value
    
    
    def __str__(self):
        return "Bird ID = {}, Sex = {}, Treatment = {}, Tissues = {}"\
                .format(self.__idbird, self.__sex, self.__treatment, self.__tissues)



class TISSUE:
    """
    A class which represents a tissue (e.g. liver, spleen)
    
    The class will be used to create a list of objects with properties
    associated with tissues (e.g. name/type, mass of the sample analyzed, total
    mass of the tissue, nutrients, and the bird the tissue came from)
    """
    def __init__(self, n="", ms=None, mt=None, nutri={}, b=None):
        self.__name = n
        self.__mass_sample = ms
        self.__mass_total = mt
        self.__nutrients = nutri
        self.__bird = b
    
    
    def __str__(self):
        return "Name = {}, Sample Mass = {}, Total Mass = {}, Bird = {}, Nutrients = {}"\
                .format(self.__name, self.__mass_sample, self.__mass_total, self.__bird, self.__nutrients)
                




#could add property "calculate" to class tissue; if name is "liver", calculate
#= [insert function here, e.g. liver_calc]

#proportion calculations; build into tissue and bird classes

#eventually make it so that I have to give column numbers associated with 
#certain as input to make the code more generalizable to different numbers of 
#data columns

def getInput():
    """
    Get input on file name from user
    
    :returns: str of file name. Input file name must include .csv designation
    #include try-except loop for whether there was a .csv at the end of the file name
    """
    infile_name = input("Enter name of input file: ")
    return infile_name


def readData(infile_name):
    """
    Get columns of data from infile (using infile_name)
    
    :parameter infile_name: name of .csv file containing columns of data
    :returns: tuple of two dictionries (columns, indexToName). columns dictionary
    has keys that are headings in the infile_name, and values are a list of all
    the entries in that column. indexToName dictionary maps column index to names
    that are used as keys in the columns dictionary. The names are the same as the
    headings used in the infile_name.
    """  
    with open(infile_name, "r") as csvfile:
        data = list(csv.reader(csvfile))
        columns = {}
        indexToName = {}
        for rownum, row in enumerate(data):
            if rownum == 0:
                i = 0
                for heading in row:
                    heading = heading.strip()
                    columns[heading] = []
                    indexToName[i] = heading
                    i += 1
            else:
                i = 0
                for cell in row:
                    cell = cell.strip()
                    columns[indexToName[i]].append(cell)
                    i += 1
        return columns, indexToName         


def invokeBIRD(columns, indexToName, ti_list):
    #dictionary of keyword=birdid and value=dictionary of tissues
    bird_tissue_dicts = {}
    i = 0
    for b in columns[indexToName[0]]:
        if b in bird_tissue_dicts:
            tissue_type = columns[indexToName[3]][i]
            tissue_obj = ti_list[i]
            bird_tissue_dicts[b][tissue_type] = tissue_obj
            i += 1
        else:
            tissues = {}
            tissue_type = columns[indexToName[3]][i]
            tissue_obj = ti_list[i]
            tissues[tissue_type] = tissue_obj
            bird_tissue_dicts[b] = tissues
            i += 1
    bird = {}
    i = 0
    for b in columns[indexToName[0]]:
        if b in bird:
            i += 1
        else:
            sex = columns[indexToName[2]][i] 
            treatment = columns[indexToName[1]][i]
            tissues = bird_tissue_dicts[b]
            bird[b] = BIRD(i=b, s=sex, tr=treatment, ti=tissues)
            i += 1
    return bird


def invokeTISSUE(columns, indexToName, nutri_list):
    #list of tissues in row order
    ti_list = []
    i = 0
    for b in columns[indexToName[0]]:
        bird_id = columns[indexToName[0]][i]
        tissue_type = columns[indexToName[3]][i]
        mass_sample = columns[indexToName[8]][i]
        mass_total = columns[indexToName[9]][i]
        nutri = nutri_list[i]
        tissue_obj = TISSUE(n=tissue_type, ms=mass_sample, mt=mass_total, b=bird_id, nutri=nutri)
        ti_list.append(tissue_obj)
        i += 1
    return ti_list
        

def getNutrients(columns, indexToName):
    #list of nutrient dictionaries in row order
    nutri_list = []
    i = 0
    #to generalize this part, will have to make this a while loop
    for b in columns[indexToName[0]]:
        nutrients = {}
        nutrients[indexToName[4]] = columns[indexToName[4]][i]
        nutrients[indexToName[5]] = columns[indexToName[5]][i]
        nutrients[indexToName[6]] = columns[indexToName[6]][i]
        nutrients[indexToName[7]] = columns[indexToName[7]][i]
        nutri_list.append(nutrients)
        i += 1
    return nutri_list


def main():
   infile_name = getInput()
   columns, indexToName = readData(infile_name)
   nutri_list = getNutrients(columns, indexToName)
   ti_list = invokeTISSUE(columns, indexToName, nutri_list)
   bird = invokeBIRD(columns, indexToName, ti_list)
   print(bird["41W"]) #test to make sure it works - it does!


if __name__ == "__main__":
    main()






