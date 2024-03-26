#
def get_selected_diagram(EARepos):
    selected_diagram = EARepos.GetCurrentDiagram()
    if selected_diagram is None:
        print("Please select a diagram")
    return selected_diagram
#
def trim_strings(name):
    return name.strip()
#
def is_tagged_value_exist(current_attribute, tag_name):
    for cur_tag in current_attribute.TaggedValues:
        if cur_tag.Name.lower() == tag_name.lower():
            return True
    return False
# Check attribute type and assign right DDL type to it
def define_db2_type(current_attribute, table_script):
    tag_val = None
    if convert_money_to_decimal(current_attribute, table_script) == False:
        val = -1
        type_lower = current_attribute.Type
        if type_lower:
            type_lower=type_lower.lower()
            if type_lower == "boolean":
                table_script += "SMALLINT"
            elif type_lower == "string" or type_lower == "enum":
                table_script += "VARCHAR("
                tag_name = "len"
                if is_tagged_value_exist(current_attribute, tag_name):
                    tag_val = current_attribute.TaggedValues.GetByName(tag_name)
                    table_script += trim_strings(tag_val.Value)
                else:
                    table_script += "NA"
                table_script += ")"
            elif type_lower == "date":
                table_script += "DATE"
            elif type_lower == "timestamp":
                table_script += "TIMESTAMP(NA)"
            elif type_lower == "long" or type_lower == "int" or type_lower == "integer":
                tag_name = "len"
                if is_tagged_value_exist(current_attribute, tag_name):
                    tag_val = current_attribute.TaggedValues.GetByName(tag_name)
                    str_val = trim_strings(tag_val.Value)
                    if not str_val.isdigit():
                        print("TaggedValue: length has a problem with it's value. Attribute: " + current_attribute.Name)
                        return
                    val = int(str_val)
                if val > 0 and val <= 4:
                    table_script += "SMALLINT"
                elif val > 4 and val <= 9:
                    table_script += "INTEGER"
                elif val > 9:
                    table_script += "BIGINT"
                else:
                    table_script += "LONG-ERROR"
            elif type_lower in ["bigdecimal", "number", "numeric", "money"]:
                table_script += type_lower.upper() + "("
                tag_name = "len"
                if is_tagged_value_exist(current_attribute, tag_name):
                    tag_val = current_attribute.TaggedValues.GetByName(tag_name)
                    table_script += trim_strings(tag_val.Value)
                else:
                    table_script += "NA"
                table_script += ")"
            else:
                if type_lower.startswith("enum"):
                    table_script += "VARCHAR("
                    tag_name = "len"
                    if is_tagged_value_exist(current_attribute, tag_name):
                        tag_val = current_attribute.TaggedValues.GetByName(tag_name)
                        table_script += trim_strings(tag_val.Value)
                    else:
                        table_script += "NA"
                    table_script += ")"
                elif type_lower.startswith("entity"):
                    table_script += "INTEGER("
                    tag_name = "len"
                    if is_tagged_value_exist(current_attribute, tag_name):
                        tag_val = current_attribute.TaggedValues.GetByName(tag_name)
                        table_script += tag_val.Value + ")"
                    else:
                        table_script += "10)"
                else:
                    table_script += current_attribute.Type.Name
    return table_script
#
def convert_money_to_decimal(current_attribute, table_script):
    tag_name = "len"
    if is_tagged_value_exist(current_attribute, tag_name):
        tag_val = current_attribute.TaggedValues.GetByName(tag_name)
        if tag_val.Value.strip().upper() == "MONEY":
            table_script += "DECIMAL(15,2) "
            return True
    return False
#
def check_multiplicity_type(multiplicity_type):
    symbol = ""
    if multiplicity_type == "*":
        symbol = "*"
    elif multiplicity_type in ["0", "0..*"]:
        symbol = "1"
    elif multiplicity_type in ["0..1", "1", "1..", "1..*"]:
        symbol = "*"
    return symbol
#
def create_upper_table_name(table_name):
    substr = ""
    if table_name == "":
        return "NO TABLE NAME"
    
    # Encode the table_name to bytes using UTF-8 encoding
    utf8_bytes = table_name.encode('utf-8')
    
    for ind in range(len(utf8_bytes)):
        if utf8_bytes[ind] >= 65 and utf8_bytes[ind] <= 90:
            if ind == 0:
                substr += chr(utf8_bytes[ind]).upper()
            elif ind != 0 and utf8_bytes[ind - 1] > 90:
                substr += "_" + chr(utf8_bytes[ind]).upper()
            elif ind != 0 and utf8_bytes[ind - 1] < 90:
                substr += chr(utf8_bytes[ind]).upper()
        else:
            substr += chr(utf8_bytes[ind]).upper()
        substr = substr.lstrip()
    
    substr += "_ID"
    return substr
# check if current package exists: return true;
def if_package_exist(rep, package_name, list_pac_guids, cur_package):
    if list_pac_guids:
        for cur_guid in list_pac_guids:
            cur_package = rep.GetPackageByGuid(cur_guid)
            if cur_package.Name == package_name:
                return True
    return False
#
def if_package_id_in_list(list_package_ids, package_id):
    return package_id in list_package_ids
#
def if_package_id_in_list(list_package_ids, package_id):
    for pack_l in list_package_ids:
        if pack_l.EaPackageID == package_id:
            return True
    return False
#
def if_package_element_in_list(list_packages, package_id):
    for cur_package in list_packages:
        if cur_package.PackageID == package_id:
            return True
    return False

# Returns a new list by adding strings from more_strings to array_strings
def add_string_to_array(array_strings, more_strings):
    return array_strings + more_strings

# Convert Hebrew text to UTF-8 encoding
def convert_utf8(hebrew_text):
    unicode_bytes = hebrew_text.encode('utf-16-le')
    bytes = unicode_bytes.decode('utf-16-le').encode('windows-1255')
    return bytes.decode('windows-1255')

# Capitalize the first letter of a string
def uppercase_first_letter(s):
    return s[0].upper() + s[1:]

# Helps to create formatted table in a plane txt file
def formatted_space(val, fixed_len):
    len_val = len(val)
    ret_val = val
    for cnt in range(fixed_len - len_val - 1):
        ret_val += " "
    return ret_val
