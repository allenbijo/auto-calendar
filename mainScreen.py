import pickle
import google_api as gapi, taskScheduler as taskS


def main():
    print("Enter 1 to update one day's calendar")
    print("Enter 2 to update next 7 days' calendar")
    print("Enter 3 to manage preferences")
    print("Enter 4 to exit")
    choice = int(input(">> "))
    print()
    if choice == 1:
        ch = int(input('''Enter day difference from today 
[0 > today, 1 > tomorrow]
>> '''))
        update(ch)
        print('Calendar updated')
    elif choice == 2:
        for i in range(1, 8):
            update(i)
        print('Calendar updated')
    elif choice == 3:
        x = pref_manager()
    elif choice == 4:
        return 'break'


def update(x):
    gapi.slotter(gapi.get_events(x))
    taskS.scheduler(x)
    gapi.unslotter(x)


def pref_manager():
    print('Your preferences are:')
    print(['Name', 'Start time', 'End time', 'Duration', 'Days', 'Preference'])
    try:
        with open('preferences.dat', 'rb') as file:
            lst = (pickle.load(file))
    except:
        with open('preferences.dat', 'wb') as file:
            pickle.dump([], file)
        lst = []
    lst.sort(key=lambda lst: lst[1])
    for i in lst:
        print(lst.index(i)+1, '. ', i)
    print()
    print("Enter 1 to ADD a preferences")
    print("Enter 2 to EDIT a preference")
    print("Enter 3 to DELETE a preference")
    print("Enter 4 to EXIT")
    choice = int(input(">> "))

    if choice == 1:
        h = int(input("How many tasks do you want to enter: "))
        for i in range(h):
            a = input("Enter Task Name: ")
            b = input("Enter Start Time (in HH:MM format): ")
            c = input("Enter End Time (in HH:MM format): ")
            d = input("Enter Duration (in HH:MM format): ")
            e = input("Enter Days (in format MTWTFSS w/ 1&0): ")
            p = int(input("Enter preference number: "))
            s = [a, b, c, d, e, p]
            lst.append(s)
            print('Task added successfully')
            print(s)
        with open("preferences.dat", 'wb') as k:
            pickle.dump(lst, k)

    elif choice == 2:
        ch = int(input('Enter serial number of preference to edit: '))
        print('You are editing ', lst[ch-1])
        a = input("Enter new Task Name: ")
        b = input("Enter new Start Time (in HH:MM format): ")
        c = input("Enter new End Time (in HH:MM format): ")
        d = input("Enter new Duration (in HH:MM format): ")
        e = input("Enter new Days (in format MTWTFSS w/ 1&0): ")
        p = int(input("Enter new preference number: "))
        s = [a, b, c, d, e, p]
        lst[ch-1] = s
        with open("preferences.dat", 'wb') as k:
            pickle.dump(lst, k)


    elif choice == 3:
        ch = int(input('Enter serial number of preference to delete: '))
        print('You have deleted ', lst[ch-1])
        lst.pop(ch-1)
        with open("preferences.dat", 'wb') as k:
            pickle.dump(lst, k)

    elif choice == 4:
        return 'break'


print('Welcome to the main console!')
gapi.get_calendar()
while True:
    x = main()
    print()
    if x == 'break':
        break
