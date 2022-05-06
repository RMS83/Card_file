
documents = [
        {"type": "passport", "number": "2207 876234", "name": "Василий Гупкин"},
        {"type": "invoice", "number": "11-2", "name": "Геннадий Покемонов"},
        {"type": "insurance", "number": "10006", "name": "Аристарх Павлов"}
      ]

directories = {
    '1': ['2207 876234', '11-2', '5455 028765'],
    '2': ['10006'],
    '3': [],
}

HELP = '''
* h – help –        вызов справки по командам;
* p – people –      команда, которая спросит номер документа и выведет имя человека, которому он принадлежит;
* s – shelf –       команда, которая спросит номер документа и выведет номер полки, на которой он находится;
* l – list –        команда, которая выведет список всех документов в формате passport "2207 876234" "Василий Гупкин";
* a – add –         команда, которая добавит новый документ в каталог и в перечень полок, спросив его номер, тип, 
                    имя владельца и номер полки, на котором он будет храниться.
* d – delete –      команда, которая спросит номер документа и удалит его из каталога и из перечня полок.
* m – move –        команда, которая спросит номер документа и целевую полку и переместит его с текущей полки на целевую.
* as – add_shelf –  команда, которая спросит номер новой полки и добавит ее в перечень.          
* e - exit -        прекращение работы программы.
'''

def help():
    return HELP

def people_(db):
    num_ = str(input('Введите номер документа: '))
    rez = None
    count_ = 0
    for param in db:
        if num_ == param['number']:
            rez = f"ФИО гр.: {param['name']}"
        else:
            count_ += 1
            if count_ > len(db) - 1:
                rez = 'Нет такого номера документа'
    return rez + '\n'

def shelf_(db2):
    num_ = str(input('Введите номер документа: '))
    rez = None
    count_ = 0
    for param in db2:
        if num_ in db2[param]:
            rez = f'Документ расположен на полке № {param}'
        else:
            count_ += 1
            if count_ > len(db2) - 1:
                rez = 'Нет такого номера документа'
    return rez + '\n'

def list_(db):
    rez = f'Список данных по гр.: \n'
    for param in db:
        rez += f'''{param['type']} "{param['number']}" "{param['name']}" \n'''
    return rez

def add_(db, db2):
    rez = ''
    type_ = str(input('Введите тип документа латиницей: ')).lower()
    num_doc = str(input(f'Введите номер {type_}: '))
    count_ = 0
    for param in db:
        if num_doc == param['number']:
            rez = 'Такой документ уже есть в базе данных'
            break
        else:
            count_ += 1
            if count_ > len(db) - 1:
                name_ = str(input('Введите ФИО: ')).title()
                num_dir = str(input('Введите номер полки для размещения: '))
                dict_ = {}
                dict_['type'] = type_
                dict_['number'] = num_doc
                dict_['name'] = name_
                db.append(dict_)
                count_ = 0
                for param in db2:
                    if num_dir == param:
                        db2[param] += [num_doc]
                        rez = f'Данные по гр. {name_} успешно внесены'
                        break
                    else:
                        count_ += 1
                        if count_ > len(db2) - 1:
                            answer = str(input(f'Такой полки нет, хотите создать полку {num_dir} '
                                                        f'и внести в нее {type_} с номером {num_doc} (y/n): ')).lower()
                            if answer == 'y':
                                db2[num_dir] = [num_doc]
                                rez = f'Данные по гр. {name_} успешно внесены'
                                break
                            else:
                                db.remove(dict_)
                                rez = f'Хорошо, занесение гр. {name_} в базу данных отменено'
                break
    return rez + '\n'

def delete_(db, db2):
    num_ = str(input('Введите номер документа для удаления из базы данных: '))
    rez = ''
    count_ = 0
    for id, param in enumerate(db):
        if num_ == param['number']:
            del db[id]
            rez = f'Документ с номером {num_} удален из базы данных'
        else:
            count_ += 1
            if count_ > len(db) - 1:
                rez = f'Документа с номером {num_} нет в базе данных'
    for param in db2:
        if num_ in db2[param]:
            db2[param].remove(num_)
    return rez + '\n'

def move_(db2):
    num_doc = str(input('Введите номер документа который хотите переместить: '))
    count_ = 0
    rez = None
    for param in db2:
        if num_doc not in db2[param]:
            count_ += 1
            if count_ > len(db2) - 1:
                rez = f'Документа {num_doc} нет в базе данных.'
        else:
            num_dir = str(input(f'Введите новый номер полки для документа {num_doc}: '))
            if num_dir:
                db2[param].remove(num_doc)
                if num_dir in db2.keys():
                    db2[num_dir] += [num_doc]
                    rez = f'Документ перемещен на полку № {num_dir}'
                    break
                else:
                    num_dir_ = str(input(f'Полки с номером {num_dir} не существует, создать ее (y/n): '))
                    # if num_dir_:
                    if 'y' == num_dir_:
                        db2[num_dir] = [num_doc]
                        rez = 'Полка создана документ перемещен'
                        break
                    else:
                        db2[param].append(num_doc)
                        rez = f'Ок, не создаем полку, возвращаем документ {num_doc} на полку № {param}'
                        break
            else:
                rez = f'Полка не может быть без номера, документ остается на полке № {param}'
                break
    return rez + '\n'

def add_shelf(db2):
    num_dir = str(input(f'Полку с каким номером вы хотели бы создать: '))
    count_ = 0
    rez = None
    if num_dir in db2.keys():
         rez = f'Полка c № {num_dir} уже существует'
    else:
        db2[num_dir] = []
        rez = f'Полка c № {num_dir} создана'
    return rez + '\n'

while True:
    command = input('Введите команду: ')
    if (command == 'h') or (command == 'help'):
        print(help())
    elif (command == 'e') or (command == 'exit'):
        print('Спасибо что пользовались нашей программой!')
        break
    elif (command == 'l') or (command == 'list'):
        print(list_(documents))
    elif (command == 'p') or (command == 'people'):
        print(people_(documents))
    elif (command == 's') or (command == 'shelf'):
        print(shelf_(directories))
    elif (command == 'a') or (command == 'add'):
        print(add_(documents, directories))
    elif (command == 'd') or (command == 'delete'):
        print(delete_(documents, directories))
    elif (command == 'm') or (command == 'move'):
        print(move_(directories))
    elif (command == 'as') or (command == 'add_shelf'):
        print(add_shelf(directories))
    else:
        print("Нет такой команды!")
        print((help()))
print("Hello World")