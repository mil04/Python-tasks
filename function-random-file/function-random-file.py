import random
import os
import os.path

def remove_file_from_disk(file_name):
    if os.path.exists(file_name):
        os.remove(file_name)

def number_to_letter(number):
    return chr(number + ord('a'))

def join_letter(base, letter):
    return base + letter

def parse_line(line, separator=" "):
    line_items = line.split(separator)
    if len(line_items) != 3:
        return None
    return int(line_items[0]), line_items[1], line_items[2]

def get_file_name(file_id):
    """Zwraca nazwę pliku na podstawie identyfikatora pliku"""
    return f"file{file_id}.txt"

def print_files_state(files_count=3):
    """Wypisuje stan plików"""
    for file_id in range(files_count):
        file_name = get_file_name(file_id)
        if not os.path.exists(file_name):
            continue
        content = ''
        with open(file_name, "r") as read_file:
            print(f'-- {file_name} --: ')
            content = read_file.read()

        if content.strip() !='':
            print(content.strip())

def get_line_starting_from_index(content, start_index=0):
    """Funkcja zwraca linię startując od start_index bądź -1 jeśli nie ma"""
    if not content:
        return -1, None
    
    end_index = content.find('\n', start_index)
    if end_index == -1:
        return -1, None
    line = content[start_index:end_index]
    return end_index, line

def generate_row():
    row_id, counter = 0, 0
    while counter < 5:
        digit = random.randint(0, 9)
        if counter == 0 and digit == 0:
            continue
        row_id = row_id * 10 + digit
        counter += 1
    login=''
    last=last_last=-1
    while len(login)<5:
        ind=random.randint(0, 25)
        if ind==last_last:
            continue
        login=join_letter(login, number_to_letter(ind))
        last_last, last = last, ind
    probability=random.random()
    if probability<0.20:
        scale='unsatisfactory'
    elif probability<0.50:
        scale= 'poor'
    elif probability<0.80:
        scale='satisfactory'
    elif probability<0.95:
        scale='good'
    else:
        scale='very_good'
    return row_id, login, scale

def get_file_for_row(row_id, file0_exists, file1_exists, file2_exists):
    hash=row_id%360
    file_code=None
    if file1_exists and 0<hash<=120:
        file_code=1
    elif file2_exists and hash<=240:
        file_code=2
    elif file0_exists and (hash==0 or hash<360):
        file_code=0
    if file_code is not None:
        return file_code
    if file1_exists:
        return 2
    elif file2_exists:
        return 1
    raise ValueError("Plików nie ma!")

def find_row(searched_row_id, file0_exists, file1_exists, file2_exists):
    id=get_file_for_row(searched_row_id, file0_exists, file1_exists, file2_exists)
    with open(get_file_name(id), "r") as searched_file:
        for line in searched_file:
            row_id, login, scale=parse_line(line)
            if(row_id==searched_row_id):
                return row_id, login, scale
    return None

def can_add_file(file_id, file0_exists, file1_exists, file2_exists):
    if file_id==0 and not file0_exists:
        return True
    elif file_id==1 and not file1_exists:
        return True
    elif file_id==2 and not file2_exists:
        return True
    return False

def get_next_file_id(file_id, file0_exists, file1_exists, file2_exists):
    if file_id == 0:
        if file2_exists:
            return 2
        return 1
    elif file_id == 1:
        if file0_exists:
            return 0
        return 2
    elif file_id == 2:
        if file1_exists:
            return 1
        return 0
    raise ValueError("Plików nie ma!")

def add_file(file_id, file0_exists, file1_exists, file2_exists):
    file=get_next_file_id(file_id, file0_exists, file1_exists, file2_exists)
    content=None
    file_name=get_file_name(file)
    with open(file_name, "r") as file_:
        content=file_.read()
    remove_file_from_disk(file_name)
    end_index, line=get_line_starting_from_index(content, 0)
    while end_index!=-1:
        row_id, login, scale=parse_line(line)
        file_new=get_file_for_row(row_id, file0_exists, file1_exists, file2_exists)
        with open(get_file_name(file_new), "a") as file_:
            print(line, file=file_)
        end_index, line = get_line_starting_from_index(content, end_index+1)

def main():
    random.seed(2000)
    file2_exists=True
    file0_exists=file1_exists=False
    print(f'Możliwe akcje to: \n1 - Wygeneruj wiersz danych\n2 - Wyszukaj zapisany wiersz po row_id\n'
          f'3 - Dodaj plik o podanym id (0-2)\n4 - Wyjdź z programu')
    while True:
        opt=int(input("Podaj jaką akcję chcesz wykonać: "))
        if opt==1:
            row_id, login, scale=generate_row()
            print(f"Wygenerowano wiersz: row_id:{row_id}, login:{login}, scale:{scale}")
        elif opt==2:
            row=int(input("Podaj id wiersza do odszukania: "))
            found=find_row(row, file0_exists, file1_exists, file2_exists)
            if found is None:
                print(f'Nie znaleziono wiersza o podanym row_id: {row}')
            else:
                print('row_id:{result[0]}, login:{result[1]}, scale:{result[2]}')
        elif opt==3:
            add_file_=int(input("Podaj id pliku do dodania: "))
            add_b= can_add_file(add_file_, file0_exists, file1_exists, file2_exists)
            if not add_b:
                print(f'Nie można dodać pliku o id: {add_file_}')
                continue
            if add_file_==0:
                file0_exists=True
            elif add_file_==1:
                file1_exists=True
            elif add_file_==2:
                file2_exists=True
            add_file(add_file_, file0_exists, file1_exists, file2_exists)
            print(f"Dodano plik o id: {add_file_}")
            print_files_state()
        elif opt==4:
            break
        else:
            print("Nieprawidłowy numer akcji")
            print(f'Możliwe akcje to: \n1 - Wygeneruj wiersz danych\n2 - Wyszukaj zapisany wiersz po row_id\n'
                  f'3 - Dodaj plik o podanym id (0-2)\n4 - Wyjdź z programu')

if __name__ == "__main__":
    main()