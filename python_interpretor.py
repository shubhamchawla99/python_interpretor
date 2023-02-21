# checks if x is a constant(integer or bool)
def is_constant(x):
    try:
        x = eval(x)
        if isinstance(x, (int, bool)):
            return True
        return False
    except:
        return False

# checks if x is assignment operator('=')
def is_assignment(x):
    if x == '=':
        return True
    return False

# checks if 'x' is a variable(sequence of one or more letters)
def is_variable(x):
    if x.isalpha():
        if x in ['False', 'True', 'and', 'or', 'not']:
            return False
        return True
    return False

# returns index of given constant 'x' or index of value assigned to variable 'x' ( returns none if they are not present in the list)
def find(x, data, type):
    for idx, element in enumerate(data):
        if type == 'constant':
            if element == x:
                return idx
        else:
            if element[0] == x:
                return idx
    return None

# checks if 'x'(len = 1) is a valid term
def is_term_valid(x):
    if is_constant(x) or is_variable(x):
        return True
    else :
        return False

# checks if expression(len = 2) is valid for unary operation
def is_unary_expression_valid(x):
    if (x[0] == '-' or x[0] == 'not') and (is_term_valid(x[1])):
        return True
    else:
        return False

# defining binary operators
def is_binary_operator(x):
    if x in ['+', '-', '*', '//', '/', ">", "<", ">=", "<=", "==", "!=", "and", "or"]:
        return True
    return False

# checks if expression(len = 3) is valid for unary operation
def is_binary_expression_valid(x):
    if is_term_valid(x[0]) and is_binary_operator(x[1]) and is_term_valid(x[2]) :
        return True
    return False

# checks if the expression is following constraints provided in assignment and is computable
def is_valid_expression(x):
    if len(x) == 1:
        return is_term_valid(x[0])
    elif len(x) == 2:
        return is_unary_expression_valid(x)
    elif len(x) == 3:
        return is_binary_expression_valid(x)
    else:
        return False

# defining computation of single term operation on x which can be a constant or a variable
# returns =>index of constant x or =>index of values assigned to variable x(if variable x is pre-defined)
def term_operation(x, data):
    if is_variable(x):
        idx = find(x, data, 'variable')
        if idx is None:
            print("Variable '{}' is not defined".format(x))  # {} k andar x ki value aa jaegi
            return None, None
        val = data[data[idx][1]]
        idx = find(val, data, 'constant')
    elif is_constant(x):
        idx = find(x, data, 'constant')
        if idx is None:
            data.append(x)
            return x, len(data) - 1
        val = x
    return val, idx

# computation of unary expression
def unary_operation(x, data):
    val, idx = term_operation(x[1], data)
    if idx is None:
        return None, None
    computed_val = eval(x[0] + ' ' + val)
    val, idx = term_operation(str(computed_val), data)
    return val, idx

def binary_operation(x, data):
    val1, idx1 = term_operation(x[0], data)
    if idx1 is None:
        return None, None
    val2, idx2 = term_operation(x[2], data)
    if idx2 is None:
        return None, None
    try:
        if x[1] == '/':
            del(x[1])
            x.insert(1,'//')
        computed_val = eval(val1 + ' ' + x[1] + ' ' + val2)
        val, idx = term_operation(str(computed_val), data)
        return val, idx
    except:
        if x[1] == '//' and val2 == '0' :
            print ("error: division by 0 is not possible")
        return None, None

# returns type of expression
def get_expression_type(x):
    if x[0] in ['BLE', 'BE', 'BLT', 'branch']:
        return 'LOOP'
    return 'STATEMENT'

def is_valid_expression_loop(x):
    if x[0] == 'branch':
        return True
    if x[0] in ['BLE', 'BLT', 'BE']:
        return is_term_valid(x[1]) and is_term_valid(x[2])

def compute_loop_statement(x, data):
    val_1, idx_1 = term_operation(x[1], data)
    val_2, idx_2 = term_operation(x[2], data)
    if val_1 is None:
        print ('{} is not defined'.format(x[1]))
        return None
    if val_2 is None:
        print ('{} is not defined'.format(x[2]))
        return None
    if x[0] == 'BLE':
        if val_1 <= val_2:
            return True
        else:
            return False
    if x[0] == 'BLT':
        if val_1 < val_2:
            return True
        else:
            return False
    if x[0] == 'BE':
        if val_1 == val_2:
            return True
        else :
            return False

# main function that does all the operation and there-by returns the required data list
def interpret(x, data, i):
    x = x.split(' ')
    type_expression = get_expression_type(x)
    if type_expression == 'STATEMENT' and len(x) >= 3:
        if is_variable(x[0]) and is_assignment(x[1]) and is_valid_expression(x[2:]):
            if len(x[2:]) == 1:  # expression is a term
                val, idx = term_operation(x[2], data)
            elif len(x[2:]) == 2:  # expression contains unary operator
                val, idx = unary_operation(x[2:], data)
            elif len(x[2:]) == 3:  # expression contains binary operator
                val, idx = binary_operation(x[2:], data)

            if idx is None or val is None:
                return False

            var_idx = find(x[0], data, 'variable')
            if var_idx is None:
                data.append((x[0], idx))
            else:
                data[var_idx] = (x[0], idx)
            return i+1
        else:
            print('invalid syntax')
            return False
    elif type_expression == 'LOOP':
        if is_valid_expression_loop(x):
            if x[0] == 'branch':
                return int(x[1])
            else :
                val = compute_loop_statement(x, data)
                if val == None:
                    return False
                elif val == True :
                    return int(x[-1])
                else :
                    return i+1
    else:
        print('input is invalid')
        return False

# returns garbage values of given data list
def gar(data):
    not_gar = []
    garbage = []
    for i in range(0, len(data)):
        if isinstance(data[i], tuple):
            not_gar.append(i)
            not_gar.append(data[i][1])
    for i in range(0, len(data)):
        idx = find(i, not_gar, 'constant')
        if idx == None:
            garbage.append(data[i])
    return garbage

def contains_while(line):
    line_s = line.split(' ')
    if line_s[0] == 'while':
        if line_s[2] == '==':
            return 'BE {} {}'.format(line_s[1], line_s[3][:-1]), True
        elif line_s[2] == '>':
            return 'BLE {} {}'.format(line_s[1], line_s[3][:-1]), True
        elif line_s[2] == '>=':
            return 'BLT {} {}'.format(line_s[1], line_s[3]), True
        elif line_s[2] == '<':
            return 'BLE {} {}'.format(line_s[3][:-1], line_s[1]), True
        elif line_s[2] == '<=':
            return 'BLT {} {}'.format(line_s[3][:-1], line_s[1]), True
        else :
            return 'INVALID', True
    else :
        return line, False

instruction_list = []
loop_list = []
data = []
current_tabs = 0
with open('D:/IITD/col_100/Ass5/input_file_1.txt') as f:
    lines = f.readlines()
    for line in lines:
        number_of_tabs = len(line)-len(line.lstrip())
        if number_of_tabs % 4 != 0:
            print ('indentation is wrong at {} line'.format(line))
            break
        number_of_tabs = number_of_tabs//4
        if (number_of_tabs == current_tabs) or (len(loop_list) > 0 and number_of_tabs <= current_tabs - 1):
            statement, found = contains_while(line.strip())
            if statement == 'INVALID':
                print ('error at line {}'.format(line))
                break
            if found and number_of_tabs >= current_tabs:
                instruction_list.append(statement)
                loop_list.append((current_tabs, len(instruction_list) - 1))
                current_tabs += 1
            elif found and number_of_tabs < current_tabs:
                while current_tabs > number_of_tabs and len(loop_list) > 0:
                    last_id = len(loop_list) - 1
                    instruction_list.append('branch {}'.format(loop_list[last_id][1]))
                    instruction_list[loop_list[last_id][1]] = instruction_list[loop_list[last_id][1]] + ' ' + str(len(instruction_list))
                    current_tabs = loop_list[last_id][0]
                    loop_list.pop(last_id)
                instruction_list.append(statement)
                loop_list.append((current_tabs, len(instruction_list) - 1))
                current_tabs += 1
            else:
                if not found and number_of_tabs < current_tabs:
                    last_idx = len(loop_list) - 1
                    instruction_list.append('branch {}'.format(loop_list[last_idx][1]))
                    instruction_list[loop_list[last_idx][1]] = instruction_list[loop_list[last_idx][1]] + ' ' + str(len(instruction_list))
                    current_tabs = loop_list[last_idx][0]
                    loop_list.pop(last_idx)
                    while current_tabs > number_of_tabs and len(loop_list) > 0:
                        last_id = len(loop_list) - 1
                        instruction_list.append('branch {}'.format(loop_list[last_id][1]))
                        instruction_list[loop_list[last_id][1]] = instruction_list[loop_list[last_id][1]] + ' ' + str(len(instruction_list))
                        current_tabs = loop_list[last_id][0]
                        loop_list.pop(last_id)
                    instruction_list.append(statement)
                else :
                    instruction_list.append(statement)
        else :
            print ('indentation is wrong at {} line'.format(line))
    print (instruction_list)
    i = 0
    while True:
        i = interpret(instruction_list[i], data, i)
        if i == False or i == len(instruction_list):
            break
    print(data)
    for i in range(0, len(data)):
        if isinstance(data[i], tuple):
            val = data[data[i][1]]
            print(data[i][0], '=', val)
    print("garbage: {}".format(gar(data)))