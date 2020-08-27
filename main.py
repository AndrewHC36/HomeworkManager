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
	"|         The Super         |\n"
	"|  Homework and Assigments  |\n"
	"|          Manager          |\n"
	"*****************************\n"
)

sbj = []
todo = []
compl = []

HW_ID = 0
cur_sbj = Null


while True:
	try:
		inp = input("\n#>>")
	except KeyboardInterrupt:
		print()
		break
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
						todo.append((str(date.today()), HW_ID, cur_sbj, homework, False))
						HW_ID += 1
					else:
						print("Invalid Subject")
				else:
					print("Empty Subject")
			else:
				print("Empty Value")
		else:
			print(E01_INV_CMD)
	elif check(0) == "EDIT":
		if check(1) == "SUBJECT":  # edit subject <target name> <new name>
			if check(2) != Null:
				if sbj.count(check(2)) > 0:
					if check(3) != Null:
						sbj[sbj.index(check(2))] = check(3)
					else:
						print("Subject new name not found.")
				else:
					print("Subject not found.")
			else:
				print("Empty subject name")
		elif check(1) == "HW":  # edit hw <homework id> <new name>
			if check(2) != Null:
				try:
					hw_id = int(check(2))
				except:
					print("This is not a valid homework id")
				else:
					ids = [i for i in map(lambda x: x[1], todo)]
					if ids.count(hw_id) > 0:
						ind = ids.index(id_no)
						if check(3) != Null:
							todo[ind][3] = check(3)
						else:
							print("Empty new name for the homework")
					else:
						print("Homework ID not found.")
			else:
				print("Empty homework ID.")
		else:
			print(E01_INV_CMD)
	elif check(0) == "SET":
		if check(1) == "STATIC":  # set static <hw id>
			if check(2) != Null:
				try:
					hw_id = int(check(2))
				except:
					print("This is not a valid homework id")
				else:
					ids = [i for i in map(lambda x: x[1], todo)]
					if ids.count(hw_id) > 0:
						ind = ids.index(hw_id)
						todo[ind][4] = True
					else:
						print("Homework ID not found.")
			else:
				print("Empty homework ID.")
		elif check(1) == "UNSTATIC":  # set unstatic <hw id>
			if check(2) != Null:
				try:
					hw_id = int(check(2))
				except:
					print("This is not a valid homework id")
				else:
					ids = [i for i in map(lambda x: x[1], todo)]
					if ids.count(hw_id) > 0:
						ind = ids.index(hw_id)
						todo[ind][4] = False
					else:
						print("Homework ID not found.")
			else:
				print("Empty homework ID.")
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
	elif check(0) == "FINISH":
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
		print("Date | Homework ID | Status | Subject | Homework")
		# statics gets printed first regardless of date
		for hw_date, hw_id, subj, name, static in todo:
			if static:
				print(f"{hw_date}{' '*(13-len(hw_date))}{hw_id}{' '*(4-len(str(hw_id)))}{'STATIC'}{'  '}{subj}{' '*(2+len(max(sbj, key=lambda s: len(s)))-len(subj))}{name}")
		for hw_date, hw_id, subj, name, static in todo:
			if not static:
				print(f"{hw_date}{' '*(13-len(hw_date))}{hw_id}{' '*(4-len(str(hw_id)))}{'      '}{'  '}{subj}{' '*(2+len(max(sbj, key=lambda s: len(s)))-len(subj))}{name}")
	elif check(0) == "FINISHED":
		print("Date | Homework ID | Subject | Homework")
		for i in compl:
			print(i)
	elif check(0) == "SAVE":
		if check(1) != Null:
			"""
			Data Serialization (Save File) Version IDs
			0 - Original one
			1 - Added static state for homework
			"""
			data = {
				"version": 1,
				"subjects": sbj,
				"todo": todo,
				"completed": compl,
				"hw-id": HW_ID,
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
			if data["version"] == 0:  # version 0 does not support static, so it defaults to False
				sbj = data["subjects"]
				todo = [i for i in map(lambda x: [x[0], x[1], x[2], x[3], False], data["todo"])]
				compl = [i for i in map(lambda x: [x[0], x[1], x[2], x[3], False], data["completed"])]
				HW_ID = data["hw-id"]
			elif data["version"] == 1:
				sbj = data["subjects"]
				todo = data["todo"]
				compl = data["completed"]
				HW_ID = data["hw-id"]
			else:
				print("Incompatable version")
		else:
			print("Empty Value")
	elif check(0) == "QUIT":
		break
	elif check(0) == "INTERNAL":
		print(f"Subjects: {sbj}")
		print(f"TODO: {todo}")
		print(f"FINISHED: {compl}")
		print(f"HW ID: {HW_ID}")
		print(f"Current Subj: {'<Null>' if cur_sbj == Null else cur_sbj}")
	elif check(0) == "HELP":
		print(
			"""
	******** Help Commands ********
	
	ADD SUBJECT  - To add subjects
	ADD HW       - To add homeworks under the specified subject
	EDIT SUBJECT - Change the name of the subjects
	EDIT HW      - Change the assignment name of the homework
	SET STATIC   - Sets the homework status to static (the homework will be pinned and to signify for longterm/statuses/super long projects)
	SET UNSTATIC - Sets the homework status to not static
	INTO         - Switches the specicified subject to that subject from this command
	FINISH       - Using the Homework ID parameter to move that Homework into the finished lists from the TODO lists
	UNDO         - Using the Homework ID parameter to move back the Homework from the finished lists to TODO lists
	TODO         - Shows the todo lists
	FINISHED     - Shows the finished lists
	SAVE         - Saves the current state to a file (JSON)
	LOAD         - Loads the save file (JSON)
	QUIT         - Quits the program (WARNING: THE FILES WILL NOT SAVE)
	INTERNAL     - Displays the internal information for debugging purposes
	HELP         - Prints the information of a list of commands
	
	_______________________________
			"""
		)
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

FINISH 1

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

# This requires subject implied value too
ADD EVENT Events No2



"""

"""
Future implementations

Merge saves?
"""
