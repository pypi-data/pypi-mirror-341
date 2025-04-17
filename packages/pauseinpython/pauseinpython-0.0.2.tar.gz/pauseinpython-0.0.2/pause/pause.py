def ex():
    print("Exit?")
    yn = input("y/n: ")
    if yn == "y":
        exit()
    elif yn == "n":
        pause()

try:
    def pause():
        anykey = input("Press any key to continue: ")
except KeyboardInterrupt:
    print("Exit?")
    yn = input("y/n: ")
    if yn == "y":
        exit()
    elif yn == "n":
        pause()
