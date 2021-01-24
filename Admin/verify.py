
def tokenCheck(token):
    abnormalList = ['"',"'",'=','!']
    for item in abnormalList:
        if item in token:
            # print('Bad input')
            return False
    # print('Good input')
    return True


