#this is what i've found in gpt
import locale
locale.setlocale(locale.LC_ALL, 'en_US')
a = 200
#z = float(a)
b = float(300)
formatted_amount = locale.currency(a, grouping=True)
#I'm learning python basics syntax in www.w3schools.com
y = 5
z = 2
a ="Hello world"
if y > z:
    print("Test code " + a)
    print("test1")
    #comment
    """Multi line comment
    Add another comment
    and Add another comment"""

    x = 5
    # I want to change the value and data type of my x
    # So I'll recreate x value
    x = "Hello world"
    print(x)


    # I want to see what are the data types of my variables that i've declared

print(type(a) ,"\n")
print(type(x), type(z))




#decimaltwoas = "{:.2f}".format(a)
decimaltwobs = "{:.3f}".format(b)
print(formatted_amount)
