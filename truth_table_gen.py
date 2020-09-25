import numpy as np
import pandas as pd

def _or_(a, b, t_table, var, col):
	print("or function invoked")
	# in_a = t_table[0].index(a)
	# in_b = t_table[0].index(b)
	# t_table.append([a + " or " + b])
	# for i in range(1, pow(2, len(var))+1):
	# 	bool_res = (t_table[i][in_a] or t_table[i][in_b])
	# 	t_table.append([bool_res])
	bool_res = []
	# print(t_table[a][0])
	for i in range(pow(2, len(var))):
		bool_res.append((t_table[a][i] == "True") or (t_table[b][i] == "True"))
	t_table[col] = bool_res



def _and_(a, b, t_table, var, col):
	print("and function invoked")
	bool_res = []
	# print(t_table[a][0])
	for i in range(pow(2, len(var))):
		bool_res.append((t_table[a][i] == "True") and (t_table[b][i] == "True"))
	t_table[col] = bool_res



def imp(a, b, t_table, var, col):
	print("imp function invoked")
	bool_res = []
	# print(t_table[a][0])
	for i in range(pow(2, len(var))):
		bool_res.append(False == ((t_table[a][i] == "True") and (t_table[b][i] == "False")))
		# print((t_table[a][i] and (t_table[b][i] == False)), t_table[a][i], t_table[b][i])
	t_table[col] = bool_res



def iff(a, b, t_table, var, col):
	print("iff function invoked")
	in_a = t_table[0].index(a)
	in_b = t_table[0].index(b)
	t_table.append([a + " iff " + b])
	for i in range(1, pow(2, len(var))+1):
		bool_res = (t_table[i][in_a] and t_table[i][in_b]) or ((not t_table[i][in_a]) and (not t_table[i][in_b]))
		t_table.append([bool_res])



def neg(a, t_table):
	print("neg function invoked")



def create_var_seq(var):
	table = [var]
	t_table = {}
	for k in range(pow(2, len(var))):
		temp = ["0"]*len(var)
		k_bin = bin(k).replace("0b","")
		for i in range(len(k_bin)-1, -1, -1):
			temp[len(var)-len(k_bin)+i] = k_bin[i]
		for i in range(len(temp)):
			if temp[i] == "0":
				temp[i] = True
			else:
				temp[i] = False
		table.append(temp)

	table = np.array(table)
	for i in range(len(var)):
		t_table[table[0, i]] = table[1::1, i]
	return pd.DataFrame(t_table)



def create_action_order_list(action_order_list, arr, open_per_index = [0]):
	# temp = []
	# start_temp = []
	pair = 0
	start_index = -1
	# count = 0
	open_pair = False
	while True:
		# print(arr)
		for i in range(len(arr)):
			# if arr[i] == "(":
			# 	start_temp.append(True)
			# elif arr[i] == ")":
			# 	temp.append(arr[i])
			# 	start_temp.pop()
			# 	action_order_list.append(temp[1:])
			# if sum(start_temp) != 0:
			# 	temp.append(arr[i])
			if arr[i] == "(":
				pair +=1
				open_pair = True
				# print(start_index, i, "A")
				if start_index == -1:
					start_index = i
			elif arr[i] == ")":
				pair -=1
			if pair == 0 and open_pair == True:
				action_order_list.append(arr[start_index:i+1])
				# print(start_index, i, "B")
				arr.pop(i)
				arr.pop(start_index)
				start_index = -1
				open_pair = False
				break
		if "(" not in arr:
			break
	action_order_list.reverse()




def valid_per(arr):
	pair = 0
	for i in arr:
		if i == "(":
			pair+=1
		elif i == ")":
			pair-=1
		if pair < 0:
			return False
	return pair == 0

	
operations = {
	"or" : _or_,
	"and" : _and_,
	"imp" : imp,
	"iff" : iff,
	"~" : neg
}


input_str = input("Enter expression: ")
# arr = ["("] + input_str.split(" ") + [")"]
arr = input_str.split(" ")
var = []

for i in range(len(arr)):
	if arr[i] != "(" and arr[i] != ")" and (arr[i] not in operations):
		var.append(arr[i])

if len(var) > 0:
	t_table = create_var_seq(var)
else:
	print("********* ERROR. No values were inputted. *********")
	exit()

# for i in range(len(arr)):
# 	if arr[i] == "imp":
		
# 	elif arr[i] == "iff":

formated_input = input_str.replace("~", "not")
t_table[input_str] = [True] * pow(2, len(var))

for r in range(pow(2, len(var))):
	formated_input_temp = formated_input
	for v in var:
		formated_input_temp = formated_input_temp.replace(v, t_table[v][r])
		# print(v, t_table[v][r])
	# print(formated_input_temp)
	# print(t_table)
	t_table.loc[r,input_str] = eval(formated_input_temp)


# if valid_per(arr):
# 	action_order_list = []
# 	create_action_order_list(action_order_list, arr)
# 	# print(action_order_list)
# else:
# 	print("********* ERROR. Wrong perentesis set up. *********")
# 	exit()

# for i in action_order_list:
# 	t_table[" ".join(i)] = [True]*pow(2, len(var))
# 	for k in range(len(i)):
# 		if i[k] in operations:
# 			operations[i[k]](i[k-1], i[k+1], t_table, var, " ".join(i))
	# curr_action = " ".join(i)
	

pd.set_option("display.max_rows", None, "display.max_columns", None)
print(t_table.to_string())






