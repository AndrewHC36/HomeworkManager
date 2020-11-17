from datetime import date
import json
import time
import sys
import random
import dataclasses

"""
Mini Changelog (Documented Revision):

Revision 1:
	Note: Please do check HELP due to a lot of command renaming
	- Printing: skips the delay when printing whitespaces
	- Status: added an assessment status to denote an test/quiz/etc. an event
	- Status: removed unstatic and replaced it with status clear to clear *all* the statuses
	- Discard: added discard command to discard an assignment (a.k.a documented deletion)
	- Text Output: updated some of the text formats and content
	- Commands: updated some command names due to possible confusions UNDO; added subject-remove command; removed edit subject-name and edit hw assignment name
"""

"""
Assignment Datatype and Ordering

[Static, Assessment]

1. Static
2. Assessment
3. Assignment <- the default status, so it does not shows under the status column

Static: A status to set the assignment as some sort of a routine or a long-term assignment that won't be finished soon
Assessment: A status for quizzes/exam/tests/essay, basically assignments that counts towards majority of your grade
Assignment: A generic task or assignment
"""

E00_SYNTAX = "Syntax Error"
E01_INV_CMD = "Invalid/Unkown Command"


print(
	"*****************************\n"
	"|         The Super         |\n"
	"|  Homework and Assigments  |\n"
	"|          Manager          |\n"
	"*****************************\n"
)

sbj = []    # subject list
todo = []   # todo list
compl = []  # completed list
dscrd = []  # discarded list
dscrd_date = []  # time of deletion of that hw assignment

HW_ID = 0
cur_sbj = None
loaded_fname = None


def stat_name(dt):
	if dt[0]:   return " STATIC     "
	elif dt[1]: return " ASSESSMENT "
	else:       return "            "


while True:
	try:
		inp = input("\n#>>")
	except KeyboardInterrupt:
		print()
		break
	tkn = inp.split(" ")
	check = lambda ind: None if ind >= len(tkn) else tkn[ind].upper()
	sbj_max_len = lambda fallback_list: len(max(sbj, key=lambda s: len(s))) if len(sbj) > 0 else len(max(map(lambda i: i[2], fallback_list), key=lambda s: len(s)))
	
	if check(0) == "ADD":
		if check(1) == "SUBJECT":
			if check(2) != None:
				subject = " ".join(tkn[2:])
				sbj.append(subject)
			else:
				print("Empty Value")
		elif check(1) == "HW":
			if check(2) != None:
				if cur_sbj != None:
					if cur_sbj in sbj:
						homework = " ".join(tkn[2:])
						todo.append([str(date.today()), HW_ID, cur_sbj, homework, [False, False]])  # refer to Assignment Status Datatype
						HW_ID += 1
					else:
						print("Invalid Subject")
				else:
					print("Empty Subject")
			else:
				print("Empty Value")
		else:
			print(E01_INV_CMD)
	elif check(0) == "SUBJECT-REMV":  # removes the subject from the listing, but will still show in historical assignments
		if check(1) != None:
			if 0 < sbj.count(tkn[1]):
				sbj.remove(tkn[1])
				if cur_sbj == tkn[1]:
					cur_sbj = None
			else:
				print("Subject name not found")
		else:
			print("Missing subject name parameter")
	elif check(0) == "STAT":
		if check(1) == "STATIC":  # stat static <hw id>
			if check(2) != None:
				try:
					hw_id = int(check(2))
				except:
					print("This is not a valid homework id")
				else:
					ids = [i for i in map(lambda x: x[1], todo)]
					if ids.count(hw_id) > 0:
						ind = ids.index(hw_id)
						todo[ind][4] = [True, False]
					else:
						print("Homework ID not found.")
			else:
				print("Empty homework ID.")
		elif check(1) == "ASSESSMENT":  # stat assessment <hw id>
			if check(2) != None:
				try:
					hw_id = int(check(2))
				except:
					print("This is not a valid homework id")
				else:
					ids = [i for i in map(lambda x: x[1], todo)]
					if ids.count(hw_id) > 0:
						ind = ids.index(hw_id)
						todo[ind][4] = [False, True]
					else:
						print("Homework ID not found.")
			else:
				print("Empty homework ID.")
		elif check(1) == "CLEAR":  # stat clear <hw id>
			if check(2) != None:
				try:
					hw_id = int(check(2))
				except:
					print("This is not a valid homework id")
				else:
					ids = [i for i in map(lambda x: x[1], todo)]
					if ids.count(hw_id) > 0:
						ind = ids.index(hw_id)
						todo[ind][4] = [False, False]
					else:
						print("Homework ID not found.")
			else:
				print("Empty homework ID.")
		else:
			print(E01_INV_CMD)
	elif check(0) == "INTO":
		if check(1) != None:
			subject = " ".join(tkn[1:])
			if subject in sbj:
				cur_sbj = subject
			else:
				print("Subject Not Found")
		else:
			print("Empty Value")
	elif check(0) == "FINISH":
		if check(1) != None:
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
	elif check(0) == "DISCARD":  # once it is discarded, it stays discarded forever
		if check(1) != None:
			if check(1).isdigit():
				id_no = int(check(1))
				ids = [i for i in map(lambda x: x[1], todo)]
				if ids.count(id_no) > 0:
					ind = ids.index(id_no)
					dscrd.append(todo[ind])
					dscrd_date.append((todo[ind][1], str(date.today())))
					del todo[ind]
				else:
					print("Homework ID not found")
			else:
				print("Homework ID must be in whole numbers")
		else:
			print("Empty Value")
	elif check(0) == "REENACT":
		if check(1) != None:
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
		disp_data = ""
		print("Active TODO Assignments:")
		print("|  Date  |  ID  | Status |  Subject  |  Homework")
		
		# 1. Static
		# 2. Assessment
		# 3. Assignments

		for hw_date, hw_id, subj, name, stat in todo:
			if stat[0]:
				disp_data += f"{hw_date}{' '*(13-len(hw_date))}{hw_id}{' '*(4-len(str(hw_id)))}{stat_name(stat)}{subj}{' '*(2+sbj_max_len(todo)-len(subj))}{name}\n"
		for hw_date, hw_id, subj, name, stat in todo:
			if stat[1]:
				disp_data += f"{hw_date}{' '*(13-len(hw_date))}{hw_id}{' '*(4-len(str(hw_id)))}{stat_name(stat)}{subj}{' '*(2+sbj_max_len(todo)-len(subj))}{name}\n"
		for hw_date, hw_id, subj, name, stat in todo:
			if stat == [False, False]:
				disp_data += f"{hw_date}{' '*(13-len(hw_date))}{hw_id}{' '*(4-len(str(hw_id)))}{stat_name(stat)}{subj}{' '*(2+sbj_max_len(todo)-len(subj))}{name}\n"
		for c in disp_data:
			if c not in [" ", "\t"]:
				time.sleep(0.01)
			print(c, end="")
			sys.stdout.flush()
	elif check(0) == "FINISHED":
		disp_data = ""
		print("Finished Assignments:")
		print("|  Date  |  ID  | Status |  Subject  |  Homework")

		for hw_date, hw_id, subj, name, stat in compl:
			disp_data += f"{hw_date}{' '*(13-len(hw_date))}{hw_id}{' '*(4-len(str(hw_id)))}{stat_name(stat)}{subj}{' '*(2+sbj_max_len(compl)-len(subj))}{name}\n"
		for c in disp_data:
			if c not in [" ", "\t"]:
				# just used for slowing down a little bit to emulate computer slowly loading text for cassette
				d = [random.randint(0,1000) for i in range(1000)]
				d_res = random.randint(0,1000) in d
			sys.stdout.write(c)
			sys.stdout.flush()
	elif check(0) == "DISCARDED":
		disp_data = ""
		print("Discarded Assignments:")
		print("|  Date  | Del. Date | ID | Status |  Subject  |  Homework")

		for hw_date, hw_id, subj, name, stat in dscrd:
			deletion_date = None
			for del_id, del_date in dscrd_date:
				if del_id == hw_id:
					deletion_date = del_date
			if deletion_date is not None:
				disp_data += f"{hw_date} {deletion_date}{' '*(13-len(hw_date))}{hw_id}{' '*(4-len(str(hw_id)))}{stat_name(stat)}{subj}{' '*(2+sbj_max_len(dscrd)-len(subj))}{name}\n"
			else:
				print(f"Deletion date for homework <{hw_id}> was not found!")
		for c in disp_data:
			if c not in [" ", "\t"]:
				# just used for slowing down a little bit to emulate computer slowly loading text for cassette
				d = [random.randint(0, 1000) for i in range(1000)]
				d_res = random.randint(0, 1000) in d
			sys.stdout.write(c)
			sys.stdout.flush()
	elif check(0) == "SAVE":
		if check(1) != None:
			"""
			Data Serialization (Save File) Version IDs
			0 - Original one
			1 - Added static state for homework
			2 - Changed the static bool to a tuples of bool (static, assessment)
				Added discard list and discard deletion list
			"""
			data = {
				"version": 2,
				"subjects": sbj,
				"todo": todo,
				"completed": compl,
				"hw-id": HW_ID,
				"discard": dscrd,
				"discard-date": dscrd_date,
			}
			with open(tkn[1], 'w') as fbj:
				json.dump(data, fbj)
			loaded_fname = tkn[1]
		else:
			print("Empty Value")
	elif check(0) == "RESAVE":
		if loaded_fname != None:
			"""
			Data Serialization (Save File) Version IDs:
			(Look for the same titled comment under SAVE command)
			"""
			data = {
				"version": 2,
				"subjects": sbj,
				"todo": todo,
				"completed": compl,
				"hw-id": HW_ID,
				"discard": dscrd,
				"discard-date": dscrd_date,
			}
			with open(loaded_fname, 'w') as fbj:
				json.dump(data, fbj)
		else:
			print("Cannot find the cached file name")
	elif check(0) == "LOAD":  # loading from a file resets all the previous states, so be sure to save before loading a new save
		if check(1) != None:
			data = {}
			with open(tkn[1], 'r') as fbj:
				data = json.load(fbj)
			loaded_fname = tkn[1]
			
			if data["version"] == 0:  # version 0 does not support static, so it defaults to False
				sbj = data["subjects"]
				todo = [i for i in map(lambda x: [x[0], x[1], x[2], x[3], (False, False)], data["todo"])]
				compl = [i for i in map(lambda x: [x[0], x[1], x[2], x[3], (False, False)], data["completed"])]
				HW_ID = data["hw-id"]
				dscrd = []
				dscrd_date = []
			elif data["version"] == 1:  # version 1 does not have multiple statuses, so we convert it to a tuple and added the new status as False
				sbj = data["subjects"]
				todo = [i for i in map(lambda x: [x[0], x[1], x[2], x[3], (x[4], False)], data["todo"])]
				compl = [i for i in map(lambda x: [x[0], x[1], x[2], x[3], (x[4], False)], data["completed"])]
				HW_ID = data["hw-id"]
				dscrd = []
				dscrd_date = []
			elif data["version"] == 2:
				sbj = data["subjects"]
				todo = data["todo"]
				compl = data["completed"]
				HW_ID = data["hw-id"]
				dscrd = data["discard"]
				dscrd_date = data["discard-date"]
			else:
				print(f"ERROR: file '{tkn[1]}' has an incompatible version")
		else:
			print("Empty Value")
	elif check(0) == "QUIT":
		break
	elif check(0) == "INTERNAL":
		print(f"Subjects: {sbj}")
		print(f"TODO: {todo}")
		print(f"FINISHED: {compl}")
		print(f"HW ID: {HW_ID}")
		print(f"Current Subj: {'<Null>' if cur_sbj == None else cur_sbj}")
		print(f"DISCARDED: {dscrd}")
		print(f"DISCARDED DATE: {dscrd_date}")
	elif check(0) == "HELP":
		print(
			"""
 ******** Help Commands ********

 ADD SUBJECT ..... To add new subjects
 ADD HW ---------- To add new assignments under the currently specified subject
 SUBJECT-REMV .... To remove the subject from a list of registered subjects
 STAT STATIC ----- Sets the homework status to static
 STAT ASSESSMENT . Sets the homework status to assessment
 STAT CLEAR ------ Clears the status of the assignment of that specified ID
 INTO ............ Switches the currently specified subject to a new subject from a list of registered subjects
 FINISH ---------- Moves the assignment from TODO list to the finished lists
 DISCARD ......... Moves the assignment from TODO list to the discard lists (permanent)
 REENACT --------- Moves the assignment from finished lists back to the TODO list
 TODO ............ Displays the TODO list
 FINISHED -------- Displays the finished list
 DISCARDED ....... Displays the discarded list
 SAVE ------------ Saves the current state to a specified file name [JSON]
 RESAVE .......... Saves the current state to the same file name (JSON) if there is a name to use from the most recent SAVE and LOAD command
 LOAD ------------ Loads the save using the specified file name of that save [JSON]
 QUIT ............ Quits the program (Warning: the current state of program will not be saved if not saved)
 INTERNAL -------- Displays the internal datatype information for debugging purposes
 HELP ............ Displays the information of each commands used in this program (or help page)

 _______________________________
	"""
		)
	else:
		print(E00_SYNTAX)
	


"""
Command ideas

Porbably need a string?
"""
