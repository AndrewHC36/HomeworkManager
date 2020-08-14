from datetime import date
import json

class Null:
	def __str__():
		return "<Null>"
	def __repr__():
		return "<Null>"


E00_SYNTAX = "Syntax Error"
E01_INV_CMD = "Invalid/Unkown Command"


print(
	"*****************************\n"
	"*         The Super         |\n"
	"*  Homework and Assigments  |\n"
	"*          Manager          |\n"
	"*****************************\n"
)

sbj = []
todo = []
compl = []

hw_id = 0
cur_sbj = Null


while True:
	inp = input("\n#>>")
	tkn = inp.split(" ")
	check = lambda ind: Null if ind >= len(tkn) else tkn[ind].upper()
	
	if check(0) == "ADD":
		if check(1) == "SUBJECT":
			if check(2) != Null:
				subject = " ".join(tkn[2:])
				sbj.append(subject)
			else:
				print("Empty Value")
		elif check(1) == "HW":
			if check(2) != Null:
				if cur_sbj != Null:
					if cur_sbj in sbj:
						homework = " ".join(tkn[2:])
						todo.append((str(date.today()), hw_id, cur_sbj, homework))
						hw_id += 1
					else:
						print("Invalid Subject")
				else:
					print("Empty Subject")
			else:
				print("Empty Value")
		else:
			print(E01_INV_CMD)
	elif check(0) == "INTO":
		if check(1) != Null:
			subject = " ".join(tkn[1:])
			if subject in sbj:
				cur_sbj = subject
			else:
				print("Subject Not Found")
		else:
			print("Empty Value")
	elif check(0) == "FINISHED":
		if check(1) != Null:
			if check(1).isdigit():
				id_no = int(check(1))
				ids = [i for i in map(lambda x: x[1], todo)]
				if ids.count(id_no) > 0:
					ind = ids.index(id_no)
					compl.append(todo[ind])
					del todo[ind]
				else:
					print("Homework ID not found")
			else:
				print("Homework ID must be in whole numbers")
		else:
			print("Empty Value")
	elif check(0) == "UNDO":
		if check(1) != Null:
			if check(1).isdigit():
				id_no = int(check(1))
				ids = [i for i in map(lambda x: x[1], compl)]
				if ids.count(id_no) > 0:
					ind = ids.index(id_no)
					todo.append(compl[ind])
					del compl[ind]
				else:
					print("Homework ID not found")
			else:
				print("Homework ID must be in whole numbers")
		else:
			print("Empty Value")
	elif check(0) == "TODO":
		print("Date | Homework ID | Subject | Homework")
		for i in todo:
			print(i)
	elif check(0) == "COMPLETED":
		print("Date | Homework ID | Subject | Homework")
		for i in compl:
			print(i)
	elif check(0) == "SAVE":
		if check(1) != Null:
			data = {
				"subjects": sbj,
				"todo": todo,
				"completed": compl,
				"hw-id": hw_id,
			}
			with open(tkn[1], 'w') as fbj:
				json.dump(data, fbj)
		else:
			print("Empty Value")
	elif check(0) == "LOAD":
		if check(1) != Null:
			data = {}
			with open(tkn[1], 'r') as fbj:
				data = json.load(fbj)
			sbj = data["subjects"]
			todo = data["todo"]
			compl = data["completed"]
			hw_id = data["hw-id"]
		else:
			print("Empty Value")
	elif check(0) == "INTERNAL":
		print(f"Subjects: {sbj}")
		print(f"TODO: {todo}")
		print(f"COMPLETED: {compl}")
		print(f"HW ID: {hw_id}")
		print(f"Current Subj: {'<Null>' if cur_sbj == Null else cur_sbj}")
	else:
		print(E00_SYNTAX)
	


"""
Command ideas


ADD SUBJECT English II
ADD SUBJECT Math

INTO Math
ADD HW Lesson 1: pg. 45-47
ADD HW About me

INTO English II
ADD HW Finish Essay

TODO
```
Date Added | Homework ID | Subject    | Homework
-----------------------------------------------------------
5/7/2020   | 0           | English II | Finish Essay
5/1/2020   | 1           | Math       | About me
12/2/2019  | 2           | Math       | Lesson 1: pg. 45-47
```

COMPLETE 1

TODO
```
Homework ID | Subject    | Homework
-------------------------------------------
0           | English II | Finish Essay
2           | Math       | Lesson 1: pg. 45-47
```

FINISHED
```
Homework ID | Subject    | Homework
-------------------------------------------
1           | Math       | About me
```

UNDO 1

FINISHED
```
Homework ID | Subject    | Homework
-------------------------------------------
```

SAVE homework.data

LOAD homework.data





DELETE <Homework ID>  # this fully deletes the Homework into the Deleted database

VIEW DELETE

"""

"""
Future implementations

Merge saves?
"""
