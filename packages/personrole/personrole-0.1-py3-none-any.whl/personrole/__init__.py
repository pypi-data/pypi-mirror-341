#Write a python program on based on age display as student/ employee / pensioner(Nested if else)


def role(age):
    if age < 0:
        print("Invalid age")

    else:
        if age <= 18:
            print("As a Student")

        elif age <= 60:
            print("As a Employee")

        else:
            print("As a Pensioner")
