import sys
import re
from pathlib import Path
import shutil
if len(sys.argv) != 2:
    print("Введіть 2 параметра: назву скрипта і папку, яку потрібно розібрати")
    quit()
p = Path(sys.argv[1])
print(repr(p))
# p = Path("F:/")#"video/ttt/")


if not p.exists():
    print('Папку', p, 'не знайдено')
    # print (repr(p))
    sys.exit()
highest_dir = str(p) + '/' 
highest_len = len(highest_dir)
if highest_len <= 4:
    highest_len = 3
    pass
print(Path(highest_dir+'images'))

Path.mkdir(Path(highest_dir+'images'), exist_ok=True)
Path.mkdir(Path(highest_dir+'video'), exist_ok=True)
Path.mkdir(Path(highest_dir+'documents'), exist_ok=True)
Path.mkdir(Path(highest_dir+'audio'), exist_ok=True)
Path.mkdir(Path(highest_dir+'archives'), exist_ok=True)
Path.mkdir(Path(highest_dir+'unfamiliar'), exist_ok=True)

fi = []
fv = []
fd = []
fa = []
fr = []
fu = []
type_file = {'jpeg':1, 'jpg':1, 'png':1, 'svg':1,
             'avi':2, 'mp4':2, 'mov':2, 'mkv':2,
             'doc':3, 'docx':3, 'txt':3, 'pdf':3, 'xlsx':3, 'pptx':3,
             'mp3':4, 'ogg':4, 'wav':4, 'arm':4,
             'zip':5, 'gz':5, 'tar':5}
n_suffix = set()
u_suffix = set()

# Готуємо словник для транслітерації
CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")
TRANS = {}
TRANSLATIONC = tuple(CYRILLIC_SYMBOLS)

for c, l in zip(TRANSLATIONC, TRANSLATION):
    TRANS[ord(c)] = l
    TRANS[ord(c.upper())] = l.upper()


def normalize(name): #Транслітерація
  
    return name.translate(TRANS)


list_dir = []

def search_subdir(directory_path):#Створює список файлів в каталозі
    current_dir = Path(directory_path)
    for path in current_dir.glob('*'):
        if path.is_dir():
            search_subdir(path)
        else:
            list_dir.append(path)
    return list_dir


def refiles(fil):#
    for f in fil:
        sf = str(f)[highest_len:].split('\\')[0]
        if  sf == 'images' or sf == 'documents' or sf == 'video' or sf == 'audio' or \
        sf == 'archives' or sf == 'unfamiliar' : # Ігноруємо файли сортованих каталогів
            continue
        # if Path.is_dir(Path(f)):
        #     continue
        if len(f.suffix) == 0:
            s = f.name
        else:
            s = f.name[0: -len(f.suffix)]
        new_f =  re.sub(r'\W', '_', normalize(s))+f.suffix
        fget = type_file.get(f.suffix[1:])
        if fget == 1:
            fi.append(highest_dir + 'images/' + new_f)
            Path(f).replace(highest_dir + 'images/' + new_f)
        elif fget == 2:
            fv.append(highest_dir + 'video/' + new_f)
            Path(f).replace(highest_dir + 'video/' + new_f)
        elif fget == 3:
            fd.append(highest_dir + 'documents/' + new_f)
            Path(f).replace(highest_dir + 'documents/' + new_f)
        elif fget == 4:
            fa.append(highest_dir + 'audio/' + new_f)
            Path(f).replace(highest_dir + 'audio/' + new_f)
        elif fget == 5:
            try:
                Path.mkdir(Path(highest_dir+'archives/'+ re.sub(r'\W', '_', normalize(s))))
            except FileExistsError:
                pass
            nf = highest_dir+'archives/'+ re.sub(r'\W', '_', normalize(s))
            shutil.unpack_archive(f,Path(nf))
            Path.unlink(Path(f), missing_ok=False)
            fr.append(highest_dir + 'archives/' + re.sub(r'\W', '_', normalize(s)))
        else:
            fu.append(highest_dir + 'unfamiliar/' + new_f)
            Path(f).replace(highest_dir + 'unfamiliar/' + new_f)
        if fget == None or fget < 1 or fget > 5:
            u_suffix.add(f.suffix[1:])
        else:
            n_suffix.add(f.suffix[1:])


     
     

    

# Видалення пустих каталогів:
refiles(search_subdir(highest_dir))
dir_path = Path(highest_dir)
folders = [f for f in dir_path.glob('*/') if f.is_dir()]
sf = str
for p in folders:
    # sf = str(p).split('\\')[2]
    sf = str(p)[highest_len :].split('\\')[0]
    if not (sf == 'images' or sf == 'documents' or sf == 'video' or sf == 'audio' or \
        sf == 'archives' or sf == 'unfamiliar') :
        try:
            shutil.rmtree(str(p))
        except Exception:
            pass
with open(highest_dir+'/result.txt', 'w') as res:
    res.write('Список сортованих файлів:\n\n')
    res.write('images: \n')
    for i in fi:
        res.write('"' +str(i).split('/')[-1] + '" ')
    res.write('\nvideo: \n')
    for i in fv:
        res.write('"'+str(i).split('/')[-1] + '" ')
    res.write('\ndocuments:\n')
    for i in fd:
        res.write('"'+str(i).split('/')[-1] + '" ')
    res.write('\naudio: \n')
    for i in fa:
        res.write('"'+str(i).split('/')[-1] + '" ')
    res.write('\narchives: \n')
    for i in fr:
        res.write('"'+str(i).split('/')[-1] + '" ')
    res.write('\nunfamiliar: \n')
    for i in fu:
        res.write('"' +str(i).split('/')[-1] + '" ')
    res.write('\n\nРозширення, відомі скрипту: \n')
    for i in n_suffix:
        res.write(str(i) + ' ')
    res.write('\n\nРозширення, не відомі скрипту: \n')
    for i in u_suffix:
        res.write(str(i) + ' ')

    
    
    

print(n_suffix)
print(u_suffix)

#print(list_dir)




