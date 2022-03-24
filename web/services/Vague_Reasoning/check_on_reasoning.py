#file content: function for controls in reasoning mode
from ctypes import ArgumentError

#control on proprieties and objects name
def par_control(property, objects, row, col):
  for i in range(col):
    property[i]=property[i].replace(' ', '')
    if property[i]=='': #error if property name is empty
      raise KeyError
    elif property[i].isalnum(): #error if property name contains the power symbol
      if 'P' in property[i]:
        raise PermissionError
    else: #error if property name is a number or contains other symbols
      raise NameError

  #as before
  for i in range(row): 
    string=objects[i].replace(' ', '')
    if string=='':
      raise KeyError
    elif string.isalnum():
      if 'P' in string:
        raise PermissionError
    else:
      raise NameError


#control on the query (it can't contein different properties)
def query_control(property, query):
    count=0
    name_list=[]

    query=query.replace('(', '')
    query=query.replace(')', '')
    query=query.replace('-', '')

    #get all properties in the query 
    start=0
    for i in range(len(query)):

        if not(query[i].isdecimal()) and not(query[i].isalpha()):
            string=query[start:i]
            start=i+1
            if string not in name_list:
              name_list.append(string)
        
        elif i==len(query)-1:
            string=query[start:]
            if string not in name_list:
                name_list.append(string)

    #real control
    for j in range(len(property)):
      if property[j] in name_list:
        count+=1
        name_list.remove(property[j])

    #at least one property has to be in the query
    #all properties in the query have to be in the table  
    if count==0 or len(name_list)!=0:
      raise ArgumentError







