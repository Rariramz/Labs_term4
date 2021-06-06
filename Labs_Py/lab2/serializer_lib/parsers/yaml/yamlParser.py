import re

FLOAT_REGEX = "-?[\d]+\.[\d]+"
INT_REGEX = "^-?[\d]+$"


def dumps(obj):
    def dumps_complex(compl_obj, tabs=''):
        if len(compl_obj) == 0:
            return '{}\n'
        ans = str()
        for key, item in compl_obj.items():
            ans += tabs + key + ': '
            obj_type = type(item)
            if obj_type is dict:
                tabs += '\t'
                if len(item) != 0:
                    ans += '\n'
                ans += dumps_complex(item, tabs)
                tabs = tabs[:len(tabs)-1]
            elif obj_type is list or obj_type is tuple:
                ans += dumps_simple(item, tabs) + '\n'
            elif obj_type is str:
                if (' ' in item) or ('\t' in item) or ('\n' in item):
                    ans += '\'' + item + '\'' + '\n'
                else:
                    ans += item + '\n'
            elif obj_type is bool:
                if item:
                    ans += "true" + '\n'
                else:
                    ans += "false" + '\n'
            elif item is None:
                ans += "null" + '\n'
            else:
                ans += str(item) + '\n'
        return ans

    def dumps_simple(simp_obj, tabs=''):
        if len(simp_obj) == 0:
            return "[]"
        ans = str()
        for item in simp_obj:
            obj_type = type(item)
            if obj_type == str:
                ans += '\n' + tabs + '- '
                if (' ' in item) or ('\t' in item) or ('\n' in item):
                    ans += '\'' + item + '\''
                else:
                    ans += item
            elif obj_type == dict:
                ans += '\n' + tabs + '-' + '\n'
                tabs += '\t'
                ans += tabs + dumps_complex(item)
                tabs = tabs[:len(tabs)-1]
            elif obj_type == list or type(item) == tuple:
                ans += '\n' + tabs + '- ' + dumps_simple(item)
            elif obj_type == bool:
                if item:
                    ans += '\n' + tabs + '- ' + 'true'
                else:
                    ans += '\n' + tabs + '- ' + 'false'
            elif item is None:
                ans += '\n' + tabs + '- ' + 'null'
            else:
                ans += '\n' + tabs + '- ' + str(item)
        return ans

    return dumps_complex(obj)


def dump(obj, file):
    with open(file, 'w') as f:
        f.write(dumps(obj))


def loads(temp_str):
    def find_last_index(str_obj, i, tab_counter):
        flag = str()
        local_tabs_counter = 0
        temp_counter = i
        while True:
            while str_obj[temp_counter] == '\t':
                temp_counter += 1
                local_tabs_counter += 1
            if local_tabs_counter == tab_counter - 1 and str_obj[temp_counter] == '-':
                flag = 'list'
                local_tabs_counter = 0
                while True:
                    while str_obj[temp_counter] != '\n':
                        temp_counter += 1
                    temp_counter += 1
                    if temp_counter >= len(str_obj):
                        return len(str_obj), flag
                    while str_obj[temp_counter] == '\t':
                        temp_counter += 1
                        local_tabs_counter += 1
                    if local_tabs_counter == tab_counter - 1 and str_obj[temp_counter] == '-':
                        local_tabs_counter = 0
                        continue
                    else:
                        return (temp_counter - tab_counter), flag
            else:
                flag = 'dict'
                local_tabs_counter = 0
                while True:
                    while str_obj[temp_counter] != '\n':
                        if str_obj[temp_counter] == '\'':
                            temp_counter += 1
                            while str_obj[temp_counter] != '\'':
                                temp_counter += 1
                        temp_counter += 1
                    temp_counter += 1
                    if temp_counter >= len(str_obj):
                        return len(str_obj), flag
                    while str_obj[temp_counter] == '\t':
                        temp_counter += 1
                        local_tabs_counter += 1
                    if local_tabs_counter >= tab_counter:
                        local_tabs_counter = 0
                        continue
                    else:
                        return (temp_counter - tab_counter), flag

    def loads_obj(str_obj, prev_tab_counter=0):
        obj = dict()
        tab_counter = prev_tab_counter
        is_key = True
        definition = ""
        key = ""
        check = str()
        i = 0
        temp_i = 0
        while i < len(str_obj):
            if str_obj[i] == ' ' or str_obj[i] == '\t':
                i += 1
            elif str_obj[i] == ':' and is_key:
                i += 1
                is_key = False
            elif str_obj[i] == '[':
                if str_obj[i+1] != ']':
                    raise ValueError()
                obj[key] = list()
                i += 3
                is_key = True
                key = ''
                definition = ''
                tab_counter = prev_tab_counter
            elif str_obj[i] == '{':
                if str_obj[i+1] != '}':
                    raise ValueError()
                obj[key] = dict()
                i += 3
                is_key = True
                key = ''
                definition = ''
            elif str_obj[i] == '\'':
                i += 1
                temp_i = i
                while str_obj[temp_i] != '\'':
                    temp_i += 1
                    if temp_i > len(str_obj):
                        raise ValueError()
                obj[key] = str_obj[i:temp_i]
                i = temp_i + 2
                is_key = True
                key = ''
                definition = ''
                tab_counter = prev_tab_counter
            elif str_obj[i] == '\n':
                if definition != '':
                    if re.fullmatch(FLOAT_REGEX, definition):
                        obj[key] = float(definition)
                    elif definition == 'true':
                        obj[key] = True
                    elif definition == 'false':
                        obj[key] = False
                    elif definition == 'null':
                        obj[key] = None
                    elif re.fullmatch(INT_REGEX, definition):
                        obj[key] = int(definition)
                    else:
                        obj[key] = definition
                    is_key = True
                    key = ''
                    definition = ''
                    i += 1
                    tab_counter = prev_tab_counter
                else:
                    tab_counter += 1
                    i += 1
                    temp_i, check = find_last_index(str_obj, i, tab_counter)
                    if check == 'list':
                        obj[key] = loads_arr(str_obj[i: temp_i+1], tab_counter - 1)
                    else:
                        obj[key] = loads_obj(str_obj[i: temp_i+1], tab_counter)
                    i = temp_i + 1
                    key = ''
                    definition = ''
                    tab_counter -= 1
                    is_key = True
            else:
                if is_key:
                    key += str_obj[i]
                else:
                    definition += str_obj[i]
                i += 1
        return obj

    def loads_arr(str_obj, prev_tab_counter):
        obj = list()
        brackets = 0
        definition = ""
        tab_counter = 0
        i = 0
        pos_min = True
        temp_i = 0
        while i < len(str_obj):
            if str_obj[i] == '\t':
                tab_counter += 1
                i += 1
            elif str_obj[i] == ' ':
                i += 1
            elif str_obj[i] == '-' and pos_min:
                pos_min = False
                i += 1
            elif str_obj[i] == '\'':
                if pos_min:
                    raise ValueError()
                i += 1
                temp_i = i
                while str_obj[temp_i] != '\'':
                    temp_i += 1
                obj.append(str(str_obj[i:temp_i]))
                i = temp_i + 2
                pos_min = True
            elif str_obj[i] == '\n':
                if definition != '':
                    if re.fullmatch(FLOAT_REGEX, definition):
                        obj.append(float(definition))
                    elif definition == 'true':
                        obj.append(True)
                    elif definition == 'false':
                        obj.append(False)
                    elif definition == 'null':
                        obj.append(None)
                    elif re.fullmatch(INT_REGEX, definition):
                        obj.append(int(definition))
                    else:
                        obj.append(definition)
                    definition = ''
                    tab_counter = prev_tab_counter
                    pos_min = True
                else:
                    tab_counter += 1
                    i += 1
                    temp_i, check = find_last_index(str_obj, i, tab_counter)
                    if check == 'list':
                        obj.append(loads_arr(str_obj[i: temp_i+1], tab_counter - 1))
                    else:
                        obj.append(loads_obj(str_obj[i: temp_i+1], tab_counter))
                    i = temp_i + 1
                    definition = ''
                    tab_counter -= 1
                    pos_min = True
                i += 1
            else:
                definition += str_obj[i]
                i += 1
        return obj

    return loads_obj(temp_str)


def load(file):
    with open(file, 'r') as f:
        result = f.read()
        return loads(result)
