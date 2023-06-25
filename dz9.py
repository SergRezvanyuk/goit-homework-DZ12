

def input_error(func):
    def inner(x):
        result = func(x)
        global err
        if err == 0:
            print(1,x)
            return result
        elif err == 1:
            print(2,x)
            return 'Wrong command',True
        elif err == 2:
            print(3,x)
            return 'Error. There should be a command, name, phone number separated by a space', True
        elif err == 3:
            return 'Error. The number must consist of numbers, brackets and a sign "-"', True
        elif err == 4:
            return 'Subscriber not found', True
    
    return inner




def hello(str):
    return 'How can I help you?', True

@input_error
def add(str):
    text = str.split()
    global err, book
    try:
        if len(text) >1:
            pattern = r'^[\(\)\-\d]+$'
            if re.match(pattern, text[-1]):
                book.update({str[:len(str)-len(text[-1])]: text[-1]})
                return 'Added ' + str, True
            else:
                err = 3
                return
                        
        else:
            err = 2
            return
    except :
        err = 2

        
    
    


@input_error
def change(str):
    global book, err
    text = str.split()
    if len(text) < 2:
        err = 2
        return
    t = book.get(str[:-len(text[-1])])
    if t:
        pattern = r'^[\(\)\-\d]+$'
        if re.match(pattern, text[-1]):
            book.update({str[:len(str)-len(text[-1])]: text[-1]})
            return 'Changed ' + str, True
        else:
                err = 3
                return
    else:
        err = 4
        return 

    return 'Changed ' + str, True

@input_error
def phone(str):
    text = str.split()[0]
    global book, err
    t = book.get(text+' ')
    if not t:
        err = 4
        return 

    return str + ' :' + t, True

def show_all(str):
    global book
    str = ''
    for k, v in book.items():
        str = str + k +': ' + v + '\n'

    return str, True

def good_bye(str):
    return str, False

def close(str):
    return str, False

def exit(str):
    return str, False

    



def func_distrib(input_C, commands):
    global err
    if input_C.strip(): 
        input_0 = (input_C.lower()).split()[0]
        if input_0 in commands:
            c = input_0 + '(input_C[len(input_0) + 1:],'')'
            answer = eval(c)
            # answer = add(input_C)
            return answer
        input_0 = (input_C).split()
        if isinstance(input_0,list):
            input_1 = (input_C.lower()).split()[0] + ' ' + (input_C.lower()).split()[1]        
            if input_1 in commands:
                c = (input_C.lower()).split()[0] + '_' + (input_C.lower()).split()[1]
                c = c + '(input_C[len(c)+1:])'
                answer = eval(c)
                return answer
    return f'Wrong command {input_C}', True


 
import re 
book = {}
err = 0



def main():
    global err
    commands = ('hello','add','change','phone','show all','good bye','close','exit')
    l = True
    while l:
        text = input(' Go -->')
        err = 0
        f = func_distrib(text, commands)
        l = f[1]
        print(f[0])



if __name__ == '__main__':

    main()

