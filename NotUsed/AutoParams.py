import inspect

def autoParams(function, context, isMethod=False):
    if isMethod:
        params = inspect.getfullargspec(function)[0][1:]
    else:
        params = inspect.getfullargspec(function)[0]
    return {k:context[k] for k in params}

#def function(a,c,e):
    #print("works", a,c,e)
#context = {k:v for k,v in zip("abcdef",[1,2,3,4,5,6])}
#function(**(autoParams(function,context)))