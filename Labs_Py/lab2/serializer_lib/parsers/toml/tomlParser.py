import re

FLOAT_REGEX = "-?[\d]+\.[\d]+"
INT_REGEX = "^-?[\d]+$"


def dumps(obj):
    def dumps_complex(compl_obj, primary_key=''):
        if len(compl_obj) == 0:
            return ''
        ans = str()
        for key, item in compl_obj.items():
            obj_type = type(item)
            if obj_type is dict:
                continue
            elif obj_type is list or obj_type is tuple:
                ans += key + ' = '
                ans += '[' + dumps_simple(item) + ']\n'
            elif obj_type is str:
                ans += key + ' = '
                ans += '\'' + item + '\'' + '\n'
            elif obj_type is bool:
                ans += key + ' = '
                if item:
                    ans += "true" + '\n'
                else:
                    ans += "false" + '\n'
            elif item is None:
                ans += key + ' = '
                ans += "null" + '\n'
            else:
                ans += key + ' = '
                ans += str(item) + '\n'
        for key, item in compl_obj.items():
            obj_type = type(item)
            if obj_type is dict:
                if primary_key != '':
                    primary_key += '.'
                primary_key += key
                ans += '\n[' + primary_key + ']\n'
                ans += dumps_complex(item, primary_key)
                primary_key = primary_key[:primary_key.rfind('.')]
        return ans

    def dumps_simple(simp_obj):
        if len(simp_obj) == 0:
            return ""
        ans = str()
        for item in simp_obj:
            obj_type = type(item)
            if obj_type == str:
                ans += '\'' + item + '\'' + ', '
            elif obj_type == dict:
                ans += dumps_complex(item) + ', '
            elif obj_type == list or type(item) == tuple:
                ans += '[' + dumps_simple(item) + ']' + ', '
            elif obj_type == bool:
                if item:
                    ans += "true" + ', '
                else:
                    ans += "false" + ', '
            elif item is None:
                ans += "null" + ', '
            else:
                ans += str(item) + ', '
        ans = ans[0:len(ans)-2]
        return ans

    return dumps_complex(obj)


def dump(obj, file):
    with open(file, 'w') as f:
        f.write(dumps(obj))


def loads(temp_str):
    def find_last_index(str_obj, i, key):
        temp_counter = i
        brackets = 0
        temp_key = str()
        while temp_counter < len(str_obj):
            while str_obj[temp_counter] != '[':
                temp_counter += 1
                if not (temp_counter < len(str_obj)):
                    return len(str_obj)
            if str_obj[temp_counter - 1] != '\n':
                temp_counter += 1
                continue
            temp_position = temp_counter
            while str_obj[temp_counter] != ']':
                temp_counter += 1
            temp_key = str_obj[temp_position+1:temp_counter]
            if not temp_key.startswith(key):
                return temp_position-1
            else:
                temp_counter += 1
                continue
        return len(str_obj)

    def loads_obj(str_obj, prev_key=''):
        obj = dict()
        brackets = 0
        quotes = 0
        is_key = True
        definition = ""
        key = ""
        i = 0
        temp_i = 0
        while i < len(str_obj):
            if str_obj[i] == ' ':
                i += 1
            elif str_obj[i] == '=':
                i += 1
                is_key = False
            elif str_obj[i] == '\'':
                i += 1
                temp_i = i
                while str_obj[temp_i] != '\'':
                    temp_i += 1
                    if temp_i >= len(str_obj):
                        raise ValueError()
                obj[key] = str_obj[i:temp_i]
                i = temp_i + 2
                is_key = True
                key = ''
                definition = ''
            elif str_obj[i] == '[':
                brackets = 1
                i += 1
                temp_i = i
                while brackets:
                    if str_obj[temp_i] == '[':
                        brackets += 1
                    elif str_obj[temp_i] == ']':
                        brackets -= 1
                    temp_i += 1
                    if temp_i > len(str_obj):
                        raise ValueError()
                obj[key] = loads_arr(str_obj[i:temp_i-1])
                i = temp_i + 1
                is_key = True
                key = ''
                definition = ''
            elif str_obj[i] == '\n':
                if str_obj[i-1] != '\n':
                    if is_key:
                        raise ValueError()
                    if definition == 'true':
                        obj[key] = True
                    elif definition == 'false':
                        obj[key] = False
                    elif definition == 'null':
                        obj[key] = None
                    elif re.fullmatch(FLOAT_REGEX, definition):
                        obj[key] = float(definition)
                    elif re.fullmatch(INT_REGEX, definition):
                        obj[key] = int(definition)
                    else:
                        raise ValueError()
                    is_key = True
                    key = ''
                    definition = ''
                    i += 1
                else:
                    i += 2
                    if i == len(str_obj):
                        break
                    if str_obj[i-1] != '[':
                        raise KeyError()
                    while str_obj[i] != ']':
                        if str_obj[i] == '[':
                            raise KeyError()
                        key += str_obj[i]
                        i += 1
                        if i > len(str_obj):
                            raise ValueError()
                    i += 1
                    temp_i = find_last_index(str_obj, i, key)
                    key = key[key.rfind('.')+1:]
                    obj[key] = loads_obj(str_obj[i+1: temp_i], key)
                    i = temp_i
                    key = ''
                    definition = ''
                    is_key = True
            else:
                if is_key:
                    key += str_obj[i]
                else:
                    definition += str_obj[i]
                i += 1
        return obj

    def loads_arr(str_obj):
        obj = list()
        brackets = 0
        definition = ""
        i = 0
        temp_i = 0
        while i < len(str_obj):
            if str_obj[i] != ' ':
                if str_obj[i] == '[':
                    brackets = 1
                    i += 1
                    temp_i = i
                    while brackets:
                        if str_obj[temp_i] == '[':
                            brackets += 1
                        elif str_obj[temp_i] == ']':
                            brackets -= 1
                        temp_i += 1
                        if temp_i > len(str_obj):
                            raise ValueError()
                    obj.append(loads_arr(str_obj[i:temp_i - 1]))
                    i = temp_i + 1
                    definition = ''
                elif str_obj[i] == '\'':
                    i += 1
                    temp_i = i
                    while str_obj[temp_i] != '\'':
                        temp_i += 1
                        if temp_i > len(str_obj):
                            raise ValueError()
                    obj.append(str(str_obj[i:temp_i]))
                    i = temp_i + 1
                elif str_obj[i] == ',':
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
                        raise ValueError()
                    definition = ''
                    i += 1
                else:
                    definition += str_obj[i]
                    i += 1
            else:
                i += 1
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
                raise ValueError()
        return obj

    return loads_obj(temp_str)


def load(file):
    with open(file, 'r') as f:
        result = f.read()
        return loads(result)
