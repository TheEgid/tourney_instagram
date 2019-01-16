# tourney_instagram
'''
language_and_salary_list =[['kot', 9], ['krot', 99]]

final_language_and_salary_list = []
for language, salary in language_and_salary_list:
    salary = salary+1
    salary = str(salary*5) + ' ' + str(type(salary))
    final_language_and_salary_list.append([language, salary])
	
	
def pull(x):
    return x[0], cube(x[1])

def cube(x): 
    return x*50

language_and_salary_list = map(lambda x: [x[0], cube(x[1])], language_and_salary_list)

lst1, lst2 = zip(*language_and_salary_list)
lst2 = map(lambda x: cube(x), lst2)
language_and_salary_list = zip(lst1, lst2)

print (list(language_and_salary_list))
'''
