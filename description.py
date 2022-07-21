import xml.dom.minidom
import re
import itertools
import csv 

docs = xml.dom.minidom.parse("table.xml")

sensors = docs.getElementsByTagName("sensor_raw")

# List tat cac cac sensor
all_sensor = []
# Chen tat cac sensor vao 
for sensor in sensors:
    all_sensor.append(sensor.firstChild.data)

#print(all_sensor)
# Tim tat ca cac Interface
def find_Interface(sensors):
    Interfaces = []
    for sensor in sensors:
        interface = re.search("(Connection|Interface).*(input|output)",sensor).group()
        interface = re.sub("input|output","",interface).strip()
        interface = re.sub(" ","",interface)
        if interface:
        #print(interface)
            Interfaces.append(str(interface))
    return Interfaces

# Delete duplicate
def delete_duplicate(x):
    res = []
    for i in x:
        if i not in res:
            res.append(i)
    return res

def get_description_from_interface():
    description_list = []
    with open('name_description.csv', mode ='r') as file:
    # Doc  CSV file
        csvFile = csv.reader(file)
    # Lay tat ca cac description tu Interface, EVC tren thiet bi
        for lines in csvFile:
            type_interface = lines[0].split(':')[0]
            if type_interface == 'Connection':
                description_list.append([lines[0].split(':')[1],lines[1]])
            elif type_interface == 'Interface':
                re_desc = re.search("TO.*TY",lines[1]).group()
                description_list.append([lines[0].split(':')[1],re_desc])
    return description_list

# Dinh nghia cac ky tu dac biet
special_char = ['(',')','[',']','{','}','.',':','\n','\t']
# Rut ngan lai description cua sensor theo chuan
def short_description(description):
    for char in special_char:
        description = description.replace(char,"")
    short_description = re.sub("CBQoS|matchAny|Ethernet Virtual Connection|Interface|Main|Class Map","",description)
    short_description = short_description.strip()
    short_description = re.sub("   "," ",short_description)
    short_description = short_description.replace(" ","_")
    return short_description

# Chen description cua cong vao description cua sensor theo dung dinh hang
# Xuat file csv de luu description
def re_description_all_sensor(all_sensor):
    all_redescription = []
    description_from_interface = get_description_from_interface()
    for sensor in all_sensor:
        short_desc = short_description(sensor)
        for description in description_from_interface:
            desc_str = "_"+description[0]+"_"
            if desc_str in short_desc:
                short_desc = short_desc.replace(description[0],description[1])
                print(short_desc)
                all_redescription.append([sensor,short_desc])
    with open('description.csv', mode ='w') as file:    # Tao file csv
        csvFile = csv.writer(file)
        csvFile.writerows(all_redescription)

def main():
    allsensor = find_Interface(all_sensor)
    sensor_list = delete_duplicate(allsensor)
    for sensor in sensor_list:
        print(sensor)
    print(get_description_from_interface())
    re_description_all_sensor(all_sensor)

main()
