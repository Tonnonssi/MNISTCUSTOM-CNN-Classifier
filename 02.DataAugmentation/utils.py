
def find_url_by_fname(fname:str)-> bool:
    if 'unimproved' in fname:
        if 'incorrect' in fname:
            improved, correct = False, False
        else:
            improved, correct = False, True
    else:
        if 'incorrect' in fname:
            improved, correct = True, False
        else:
            improved, correct = True, True
    return improved, correct

def improved_or_correct_url(improved=True, correct=True):
    '''
    :param improved:
    :param correct:
    :return:
    '''
    if improved == True:
        if correct == True:
            return 'improved_correct/'
        else:
            return 'improved_incorrect/'
    else:
        if correct == True:
            return 'unimproved_correct/'
        else:
            return 'unimproved_incorrect/'

