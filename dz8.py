from datetime import datetime, timedelta



def get_birthdays_per_week(d_user):
    list_w = []
    dn = datetime.now()
    pw = {}

    for _ in range(7):

        if dn.weekday() <= 4:
            list_w.append([dn.weekday(),dn.month,dn.day])
            if dn.weekday() == 0:
                pw.update({0:'Monday:'})
            elif dn.weekday() == 1:
                pw.update({1:'Tuesday:'})
            elif dn.weekday() == 2:
                pw.update({2:'Wednesday:'})
            elif dn.weekday() == 3:
                pw.update({3:'Thursday:'})
            elif dn.weekday() == 4: 
                pw.update({4:'Friday:'})
        else:
            list_w.append([0,dn.month,dn.day])
        dn = dn + timedelta(days = 1)
    for u in d_user:
        b = u['birthday']
        for i in list_w:
            if b.day == i[2] and b.month == i[1]:
                if pw[i[0]][-1] != ':':
                    pw[i[0]] = pw[i[0]]+','
                pw[i[0]] = pw[i[0]]+' '+u['name'] 


    for i in pw.values():
        print(i)


