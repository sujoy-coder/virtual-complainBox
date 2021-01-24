import re


def validationContent(source):
    recource = ['alert(','confirm(','<script>','</script>','.cookie']
    for itm in recource:
        if itm in source:
            # print("Denger !")
            return '<h5>Sorry, this user may be posted some harmful content. So due to some security purpose, we can not display that :( </h5>'
    # print('fine !')
    return source


def validateMail(email):
    emailPattren = '^[a-z0-9]+[\._]?[a-z0-9]+@aot.edu.in$'    
    if(re.search(emailPattren,email)):  
        # print("Valid Email")
        return True        
    else:  
        # print("Invalid Email") 
        return False