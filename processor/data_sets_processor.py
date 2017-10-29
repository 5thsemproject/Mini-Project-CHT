#--------------------------------------------------------------------------
#
#                           * DATA SETS - PROCESSING *
#                            
#
#--------------------------------------------------------------------------

# Required import statements
import sys
import os
import re
import shutil
import glob

data_set_dict = {}


def file_list():
    # List all the files present in the data sets
    path = "./data-sets"
    dirs = os.listdir( path )

    f = open("./processor/file_listing.txt", "w+")
    for file in dirs:
        f.write(file+"\n")
    f.close()

    

def set_dimension(value):
    #remove - symbol if found any
    value = value.replace("-", "")

    if value.find("Plate") >= 0:
        value = value.replace("Plate","")
        
    if value.find("W") >= 0:
        value = value.replace("W","")

    if value.find("\"") >= 0:
        value = value.replace("\"","")

    if value.find("fullplate") >= 0:
        value = value.replace("fullplate","")

    if value.find(",") >=0:
        values = value.split(',')
        values[0] = values[0].replace("cm","")
        float_value = float(values[0])
        float_value = float_value * 0.01
        value = str(float_value)
        return value
    
    if value.find("meters") >= 0:
        value = value.replace("meters","")
        return value

    if value.find("meter") >= 0:
        value = value.replace("meter","")
        return value

    if value.find("mm") >= 0:
        value = value.replace("mm","")
        float_value = float(value)
        float_value = float_value / 1000
        value = str(float_value)
        return value

    if value.find("inches") >= 0:
        value = value.replace("inches","")
        float_value = float(value)
        float_value = float_value * 0.0254
        value = str(float_value)
        return value

    if value.find("inch") >= 0:
        value = value.replace("inch","")
        float_value = float(value)
        float_value = float_value * 0.0254
        value = str(float_value)
        return value

    if value.find("cm") >= 0:
        value = value.replace("cm","")
        float_value = float(value)
        float_value = float_value * 0.01
        value = str(float_value)
        return value


def set_weight(value):
    #remove - if found any
    value = value.replace("-", "")

    if value.find("(persingleShoe)Weightoftheproductmayvarydependingonsize.") >=0:
        value = value.replace("(persingleShoe)Weightoftheproductmayvarydependingonsize." , "")

    if value.find(",") >=0:
        values = value.split(',')
        values[0] = values[0].replace("(WithBattery)","")
        values[0] = values[0].replace("g","")
        float_value = float(values[0])
        float_value = float_value / 1000
        value = str(float_value)
        return value

    if value.find("(WithoutBattery)") >=0:
        value = value.replace("(WithoutBattery)","")
        if value.find("gm") >= 0:
            value = value.replace("gm","")
        if value.find("g") >= 0:
            value = value.replace("g","")
        float_value = float(value)
        float_value = float_value / 1000
        value = str(float_value)
        return value

    if value.find("(WithBattery)") >=0:
        value = value.replace("(WithBattery)","")
        if value.find("gm") >= 0:
            value = value.replace("gm","")
        if value.find("g") >= 0:
            value = value.replace("g","")
        float_value = float(value)
        float_value = float_value / 1000
        value = str(float_value)
        return value

    if value.find("kgs") >= 0:
        value = value.replace("kgs","")
        return value
    
    if value.find("kg") >= 0:
        value = value.replace("kg","")
        return value

    if value.find("K") >= 0:
        value = value.replace("K","")
        return value

    if value.find("gram") >= 0:
        value = value.replace("gram","")
        float_value = float(value)
        float_value = float_value / 1000
        value = str(float_value)
        return value

    if value.find("gm") >= 0:
        value = value.replace("gm","")
        float_value = float(value)
        float_value = float_value / 1000
        value = str(float_value)
        return value
    
    if value.find("g") >=0:
        value = value.replace("g","")
        float_value = float(value)
        float_value = float_value / 1000
        value = str(float_value)
        return value


def process_and_generate_specs():
    global data_set_dict

    key_count = 0
     
    path = "./data-sets/"
    spec_list = set()


    # Get the running item id from the file
    fid = open("./commons/id-count.txt", "r")
    item_id = int(fid.read())
    fid.close()


    domain_list = []
    dfile = open("./processor/domains.txt", "r")
    for line in dfile:
        line = line.strip()
        domain_list.append(line)
    dfile.close()

    pd_file = open("./processor/product_domain.txt", "a")
    
    fp = open("./processor/file_listing.txt", "r")
    for file in fp:
        file= file.strip()

        data_set_dict = {}
        
        # Load the data from file to dictionary
        f = open(path + file, "r", encoding="utf8")
        #print(file)
        for line in f:
            line = line.strip("\r\n")

            # If there is only spec and no value, dont load it
            if len(line.split()) == 2:
                spec_val = line.split()
                if spec_val[0] and spec_val[1] is not None:
                    spec_val[0] = spec_val[0].lower()
                    data_set_dict[spec_val[0]] = spec_val[1]
        f.close()

        
        value_list = {}
        flag = 0
        domain_flag = 0

        # If hieght, width and depth are merged together
        for key, value in data_set_dict.items():
            if key == 'product-name':
                words = [d for d in domain_list if d in value]
                if len(words) != 0:
                    domain_flag = 1
                if "Zenfone" in value:
                    domain_flag = 2
                if "Lenovo" in value:
                    domain_flag = 2
                if "Canvas" in value:
                    domain_flag = 2
                if "Galaxy" in value:
                    domain_flag = 2
                if "Food" in value:
                    domain_flag = 4
                if "Dinner" in value:
                    domain_flag = 8
                if "iPhone" in value:
                    domain_flag = 2
                if "iphone" in value:
                    domain_flag = 2
                if "IPhone" in value:
                    domain_flag = 2
                if "Notice" in value:
                    domain_flag = 9
                if "Bird" in value:
                    domain_flag = 10
                if "Weighing" in value:
                    domain_flag = 11
                if "Washing" in value:
                    domain_flag = 12
                    
            
            if re.search("(width.*height.*depth.*)",key):
                if key.find("with-stand") >= 0:
                    continue
                else:
                    value_list = value.split("x")
                    if len(value_list) == 1:
                        if value_list[0].find("mm") >= 0:
                            flag = 1

                    if len(value_list) == 3:
                        if value_list[0].find("mm") == -1 and value_list[2].find("mm") >= 0:
                            flag = 1
                            if value_list[0].find("W") >= 0:
                                value_list[0].replace("W", "")
                            if value_list[1].find("W") >= 0:
                                value_list[1].replace("W", "")
                            if value_list[2].find("W") >= 0:
                                value_list[2].replace("W", "")
                                
                            value_list[0] = value_list[0] + "mm"
                            value_list[1] = value_list[0] + "mm"
                            value_list[2] = value_list[0] + "mm"
                                            
        if flag == 1:
            data_set_dict["width"] = value_list[0]
            data_set_dict["height"] = value_list[0]
            data_set_dict["depth"] = value_list[0]

        if domain_flag == 1:
            data_set_dict["domain"] = words[0]
        if domain_flag == 2:
            data_set_dict["domain"] = "Mobile"
        if domain_flag == 0:
            data_set_dict["domain"] = "NOT-ASSIGNED"
        if domain_flag == 4:
            data_set_dict["domain"] = "Food Processor"
        if domain_flag == 8:
            data_set_dict["domain"] = "Dinner Set"
        if domain_flag == 9:
            data_set_dict["domain"] = "Notice Board"
        if domain_flag == 10:
            data_set_dict["domain"] = "Bird House"
        if domain_flag == 11:
            data_set_dict["domain"] = "Weighing Scale"
        if domain_flag == 12:
            data_set_dict["domain"] = "Washing Machine"
        

        for key, value in data_set_dict.items():
            # All height will be in meters
            if key == "height":
                data_set_dict[key] = set_dimension(data_set_dict[key])

            # All width will be in meters
            if key == "width":
                data_set_dict[key] = set_dimension(data_set_dict[key])

            # All depth will be in meters
            if key == "depth":
                data_set_dict[key] = set_dimension(data_set_dict[key])

            # All weights in kilograms
            if key == "weight":
                data_set_dict[key] = set_weight(data_set_dict[key])

            spec_list.add(key)
                

        if len(data_set_dict) >= 3:
            data_set_dict['id'] = str(item_id)
            file = open("./suck-the-key-files/"+str(item_id)+".txt", "w+", encoding="utf8")
            for key, value in data_set_dict.items():
                if key and value is not None:
                    file.write(key+" "+value+"\n")
                    
            item_id = item_id + 1
            key_count = key_count + 1
            file.close()


        # File which keeps track of product and its domain
        pd_file.write(data_set_dict['product-name']+"\t"+data_set_dict['domain']+"\n")

        #
        #if data_set_dict["domain"] == "Mobile" or data_set_dict["domain"] == "Notebook" or data_set_dict["domain"] == "Refrigetor" or
        # data_set_dict["domain"] == "Speaker" or data_set_dict["domain"] == "TV" or data_set_dict["domain"] == "Amplifier" or data_set_dict["domain"] == "Camera":
        #    for key, value in data_set_dict.items():
        #        spec_list.add(key)
        #
        
    fp.close()
    pd_file.close()
    
    # Update the item id in file
    fid = open("./commons/id-count.txt", "w+")
    fid.write(str(item_id))
    fid.close()

    # Copy the files to processed data sets directory as a backup
    src = "./suck-the-key-files"
    dest = "./processed-data-sets"
    src_files = os.listdir(src)
    for file_name in src_files:
        full_file_name = os.path.join(src, file_name)
        if (os.path.isfile(full_file_name)):
            shutil.copy(full_file_name, dest)
    

    # Management of key_count and spec_count
    commons_path = "./commons/"
    
    # Updating the key_count
    fkey = open(commons_path + "key-count.txt", "r", encoding="utf8")
    current_key_count = int(fkey.read())
    fkey.close()

    # If already a count exists, then update the count
    if current_key_count != 0:
        key_count = key_count + current_key_count

    # Update the key count in file
    fkey = open(commons_path + "key-count.txt", "w+", encoding="utf8")
    fkey.write(str(key_count))
    fkey.close()


    # Update the spec_list
    # We have a new spec list created everytime new data sets are processed
    # Merge and Updated with the existing list
    spec_count = 0
    spec_count = len(spec_list)
    old_spec_count = spec_count
    
    if os.stat(commons_path + "specs.txt").st_size == 0:
        spec_list = sorted(spec_list)
        fspec = open(commons_path + "specs.txt", "w+")
        for spec in spec_list:
            fspec.write(spec+"\n")
        fspec.close()

        # Update the spec count in file
        fspec_count = open(commons_path + "spec-count.txt", "w+", encoding="utf8")
        fspec_count.write(str(spec_count))
        fspec_count.close()

        
    else:
        # Add the existing file contents to the set
        fspec = open(commons_path + "specs.txt", "r")
        for line in fspec:
            line = line.strip()
            spec_list.add(line)
        fspec.close()

        # Sort the set
        spec_list = sorted(spec_list)

        # Get the updated count
        spec_count = len(spec_list)

        # Set the spec dirty bit if the number of spec has increased
        if spec_count > old_spec_count:
            dirty_spec_f = open("./commons/dirty-spec.txt", "w+")
            dirty_spec_f.write("1")
            dirty_spec_f.close()

        # Write the updated set to the file
        if spec_count > old_spec_count:
            fspec = open(commons_path + "specs.txt", "w+")
            for spec in spec_list:
                fspec.write(spec+"\n")
            fspec.close()

            # Update the spec count in file
            fspec_count = open(commons_path + "spec-count.txt", "w+", encoding="utf8")
            fspec_count.write(str(spec_count))
            fspec_count.close()


    # Empty the data-sets directory
    pathd = "./data-sets"
    delete_files = glob.glob(pathd+"/*")
    for f in delete_files:
        os.remove(f)


if __name__ == "__main__":
    file_list()
    process_and_generate_specs()

