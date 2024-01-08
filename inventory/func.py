from inventory.models import *

def create_attributes(data):
    try:
        for obj in data:
            for attr_name, attr_value in obj.items():
                print(attr_name, attr_value)
    except:
        return "Error"