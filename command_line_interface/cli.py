import os

from pathlib import Path


CWD = Path(os.getcwd())


phone_list_path = CWD / 'phone_list.txt'


phone_book = {}


start_commands = ['hello', 'start', 'hi']
add_commands = ['add']
change_commands = ['change']
get_phone_commands = ['phone']
get_all_commands = ['show all']
exit_commnads = ['good bye', 'close', 'exit']


# ----------File processing----------
def get_phone_list(phone_list_path: Path) -> None:
    with open(phone_list_path, 'r') as phone_list:
        for line in phone_list:
            phone_book.update({line.split(':')[0]: line.split(':')[1].strip()})

def write_phone_list(phone_list_path: Path) -> None:
    result = ''
    with open(phone_list_path, 'w') as phone_list:
        for k, v in phone_book.items():
            result += f'{k}: {v}\n'
        phone_list.write(result)


# ----------Handlers----------
def input_error(func) -> str:
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
        except IndexError:
            if func.__name__ == 'add_contact':
                return '\nGive me name and phone, please\n'
            if func.__name__ == 'change_contact':
                return '\nGive me name and phone, please\n'
            if func.__name__ == 'get_phone':
                return '\nGive me name, please\n'
        except KeyError:
            return f"\nI don't know this name(\n"
        else:
            return result
    return wrapper

@ input_error   
def add_contact(input_data: str) -> str:
    if len(input_data.split()[1]) > 16:
        return '\nName is too long. Must be less than 16 characters\n'
    elif not input_data.split()[-1].isdigit():
        return '\nPhone number must contain only numbers\n'
    elif len(input_data.split()[-1]) != 9:
        return '\nPhone number must contain 9 numbers\n'
    else:
        phone_book.update({input_data.split()[1]: input_data.split()[-1]})
        return f'\nPhone number [{input_data.split()[-1]}] with name "{input_data.split()[1]}" has been added!\nAnything else?\n'

@ input_error
def change_contact(input_data: str) -> str:
    if phone_book:
        if phone_book[input_data.split()[1]]:
            old_number = phone_book[input_data.split()[1]]
            if not input_data.split()[-1].isdigit():
                return '\nPhone number must contain only numbers\n'
            elif len(input_data.split()[-1]) != 9:
                return '\nPhone number must contain 9 numbers\n'
            else:
                phone_book[input_data.split()[1]] = input_data.split()[-1]
                return f'\nPhone number of "{input_data.split()[1]}" has been changed from [{old_number}] to [{input_data.split()[-1]}]\nAnything else?\n'
    else:
        return '\nPhone list is empty\nAnything else?\n'
    
@ input_error
def get_phone(input_data: str) -> str:
    if phone_book:
        return f'\n{input_data.split()[1]}: {phone_book[input_data.split()[1]]}\nAnything else?\n'
    else:
        return '\nPhone list is empty\nAnything else?\n'

@ input_error
def get_all() -> str:
    result = '\n{:^31}\n{:^31}\n'.format('PHONE BOOK', '-'*31)
    if phone_book:
        for k, v in phone_book.items():
            result += '|{:^17}|{:^11}|\n{:^31}\n'.format(k, v, ('-'*31))
    else:
        return '\nPhone list is empty\nAnything else?'
    
    return '{}\nAnything else?\n'.format(result)


# ----------Parser----------
@ input_error
def commands_search(input_data: list, commands: list) ->list:
    if input_data:
        for i in commands:
            if i == input_data[0:len(i)].lower():
                return True


# ----------Request-Respond----------
def main() -> None:
    if os.path.exists(phone_list_path):
        get_phone_list(phone_list_path)
    
    print(f'\nSupported functions:\n\n1. Add [Name] [Phone]\n2. Change [Name] [Phone]\n3. Phone [Name]\n4. Show all\n5. Exit\n')
    while True:
        
        user_input = input('Say hello to start!\n>>> ').strip()
        
        if user_input.lower() in start_commands:
            print('\nHow can I help you?')
            
            while True:
                
                user_input = input('>>> ').strip()
                
                if commands_search(user_input, add_commands):   
                    print(add_contact(user_input))
                    write_phone_list(phone_list_path)         
                elif commands_search(user_input, change_commands):          
                   print(change_contact(user_input))
                   write_phone_list(phone_list_path)            
                elif commands_search(user_input, get_phone_commands):                
                    print(get_phone(user_input))                  
                elif commands_search(user_input, get_all_commands):                 
                    print(get_all())
                elif user_input in exit_commnads:
                    print('\nGood bye!')                
                    return                  
                else:
                    print("I don't know this command(")

        elif user_input.lower() in exit_commnads:   
            print('\nGood bye!')
            return     
        else:
            print('\nBad beginning, try again\n')                


# ----------Entry point----------
if __name__ == '__main__':
    main()
