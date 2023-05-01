import os

from pathlib import Path


CWD = Path(os.getcwd())


phone_list_path = CWD / 'phone_list.txt'


phone_book = {}

# ----------Comand lists----------
comands ={
    'hello_command': ['hello', 'start', 'hi'],
    'add_command': ['add'],
    'change_command': ['change'],
    'get_phone_command': ['phone'],
    'get_all_command': ['show all'],
    'exit_commnad': ['good bye', 'close', 'exit']
}


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


# ----------Messages----------
def start_message() ->str:
    return '\nSupported functions:\n\n1. Add [Name] [Phone]\n2. Change [Name] [Phone]\n3. Phone [Name]\n4. Show all\n5. Exit\n\nSay hello to start\n'

def hello_message() ->str:
    return '\nHow can I help you?'

def exit_message() ->str:
    return '\nGood bye!'

def unknown_command_message(command: str) ->str:
    return f"\nI don't know '{command}' command("


# ----------Data checking----------
def name_checking(name: str) ->bool:
    if len(name) < 16:
        return True
    
def phone_number_checking(phone_number: str) ->bool:
    if phone_number.isdigit() and len(phone_number) == 9:
        return True
    

# ----------Handlers----------
def input_error(func) -> str:
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
        except IndexError:
            return '\nSomething wrong, try again\n'
        except KeyError:
            return f"\nI don't know this name(\n"
        except TypeError:
            return '\nSomething wrong, try again\n'
        else:
            return result
    return wrapper

@ input_error   
def add_contact(name: str, phone_number: str) -> str:
    if name_checking(name):
        if phone_number_checking(phone_number):
            phone_book.update({name: phone_number})
            write_phone_list(phone_list_path)
            return f'\nPhone number [{phone_number}] with name "{name}" has been added!\nAnything else?\n'
        else:
            return f'\nPhone number must have only 9 digits\n'
    else:
        return f'\nName must be less than 16 characters\n'
        
@ input_error
def change_phone_number(name: str, new_phone_number: str) -> str:
    if phone_number_checking(new_phone_number):
        old_phone_number = phone_book[name]
        phone_book[name] = new_phone_number
        write_phone_list(phone_list_path)
        return f'\nPhone number of "{name}" has been changed from [{old_phone_number}] to [{new_phone_number}]\nAnything else?\n'
    else:
        return f'\nPhone number must have only 9 digits\n'
    
@ input_error
def get_phone_number(name: str) -> str:
    if phone_book:
        return f'\n{name}: {phone_book[name]}\nAnything else?\n'
    else:
        return '\nPhone book is empty\nAnything else?\n'

@ input_error
def get_all(_) -> str:
    result = '\n{:^31}\n{:^31}\n'.format('PHONE BOOK', '-'*31)
    if phone_book:
        for k, v in phone_book.items():
            result += '|{:^17}|{:^11}|\n{:^31}\n'.format(k, v, ('-'*31))
    else:
        return '\nPhone book is empty\nAnything else?'
    
    return '{}\nAnything else?\n'.format(result)


# ----------Parser----------
@ input_error
def commands_search(input_comand: str, commands: dict) ->list:
    for i in commands.keys():
        for j in commands[i]:
            if input_comand[0:len(j)].lower() == j:
                return i

commands_handler = {
    'hello_command': hello_message,
    'add_command': add_contact,
    'change_command': change_phone_number,
    'get_phone_command': get_phone_number,
    'get_all_command': get_all,
    'exit_commnad': exit_message
    }

# ----------Request-Respond----------
def main() -> None:
    if os.path.exists(phone_list_path):
        get_phone_list(phone_list_path)

    print(start_message())

    while True:
        
        user_input = input('>>> ').strip()
        
        command = commands_search(user_input, comands)
        if command:
            data = user_input.split(' ')[1:]        
            if command != 'exit_commnad':
                handler = commands_handler[command]
                result = handler(*data)
                print(result)
            else:
                handler = commands_handler[command]
                result = handler()
                print(result)
                return
        else:
            print(unknown_command_message(user_input.split(' ')[0]))


# ----------Entry point----------
if __name__ == '__main__':
    main()
    