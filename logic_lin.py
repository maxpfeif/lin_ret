#	Authored: Max Pfeiffer - 2018
#
#	Converts the .csv output generated from Saleae Logic Lin Analyzer to a more legible 
# 	and data-processing friendly format. 
#
#	Usage: 	python gls_ecu_filt.py "gls_info_cabana_logfile.csv" "0xAA" "0xBB" ...
#		"gls_info_cabana_logfile.csv" = the file to decode 
#		"0xAA" = first id to filter 
#		"0xBB" = second id to filter 
# 		etc.. 
#
#	Output: "lin_ + filename.csv" in format; "Time, ID, Data"
#
#
#!/usr/bin/python
import sys
import csv
import ctypes

filename = sys.argv[1]

input_file = open(sys.argv[1])
og_data = csv.reader(input_file, delimiter = ",")

output_data = open("lin_"+ sys.argv[1], "w+")							
output_writer = csv.writer(output_data, delimiter = ",")
output_writer.writerow(["Time", "ID", "Data"]) 

time = 0
pid = -1
data = ""
header = 1
chk_flag = 0 



# takes in the first character of a log data line 
# returns true if this is the beginning of a checksum line  
def is_checksum(first_char): 
	print first_char + " = " + str(ord(first_char))

	# return ord(test_list.pop(0)) == 67


# takes in the first character of a log data line 
# returns true if this is the beginning of a PID line 
def is_pid(first_char):
	return ord(first_char) == 80 


# returns boolean of passed row as a Protected ID
# preserves the state of test_list by putting the 
# popped value back 
#def is_pid(test_list):
#	cur_char = ord(test_list.pop(0))
#	if cur_char == 80:
#		return 1 
#	else: 
#		return 0 


# takes in the first character of a log data line 
# returns true if this is the beginning of a Data line 
def is_data(first_char):
	return ord(first_char) == 97


# returns classification if test list is LIN data
#def is_data(test_list):
#	cur_char = ord(test_list.pop(0))
#	if cur_char == 97:
#		return 1 
#	else:
#		return 0 


# checks the data to see if the last byte is a checksum byte
# returns the data string without the checksum byte if present 
# def is_checksum(test_list):
	# need to determine whether we are using the classic checksum, where the sum is based only on 
	# the data, or the enhanced checksum, where the PID is added into the checksum.
	# also need to make sure we're apropriately handling the carry bit during the sum, as this could 
	# be a problem. 
	# handle the carry bit by using a uint16 to store the checksum 


	# get the list in string form
	# [0 1 2 3 4 5]
	# take the first two, concatenate them and add them to the beginning of the list 
	# list.insert(0, str(list.pop(0) + list.pop(0)))
	# [01 2 3 4 5]
	# list.insert(1, srt(list.pop(1) + list.pop(1)))
	# [01 23 4 5]
	# list.insert(2, str(list.pop(2) + list.pop(2)))
	# [01 23 45]
	# this evaluates to..
	#for i in range(0,len(test_list)/2):
	#	test_list.insert(i, (str(test_list.pop(i)) + str(test_list.pop(i))))
	#print "test list = " + str(test_list)

	# look over the whole list 
	#chk = 0 
	#data_bytes = ""
	#for i in range(0, len(test_list) - 1):
	#	byte = test_list.pop(0)
	#	data_bytes = data_bytes + str(byte)
	#	chk += int(byte, 16)

	# check to see if we got something reasonable.. 
	#print "chk = " + str(chk)
	#print "last byte is " + str(test_list)
	#print "data bytes is " + str(data_bytes)

	# calculate the checksum for the first n-1 items 
	# you chould try using an XOR.. or you could try doing some math..
	# chk = -chk - 1 

	#print "checksum = " + str(chk)

	# compare this with the last entry 
	#last_byte = test_list.pop(0)
	#if chk != last_byte: 
	#	data_bytes = data_bytes + str(last_byte) 
	#print "data_bytes after check is " + str(data_bytes)
	#return data_bytes


	# remove the last entry if it matches the checksum calc 	

# returns the hex data portion of the passed list as a list 
def extract_hex(test_list):


	# find the first open paren 
	cur_char = ord(test_list.pop(0))
	while (cur_char != 40):
		cur_char = ord(test_list.pop(0))

	# extract the hex contents until the close paren 
	new_list = []
	next_element = test_list.pop(0)
	while (cur_char != 41):
		new_list.append(next_element)
		next_element = test_list.pop(0)
		cur_char = ord(next_element)

	# return the result in string form 
	result = ""
	while(len(new_list)):
		result = result + str(new_list.pop(0)) 

	return result


# saves the present message content 
# resets the message content variables
def save_message(content): 
	output_writer.writerow(content)
	time = 0 



for row in og_data:
	if header:
		header = 0
	else: 
		row_data = list(row.pop(2))				
		first_char = row_data.pop(0)
		row_data.insert(0,first_char) 		# preserve the row data..? 

		is_checksum(first_char)
		
		if(is_pid(row_data)):
			if(pid > -1): #once past the initial edge case, save the message previously. 
				# check for the checksum 
				save_message([time,pid,data])
				data = ""
			pid = extract_hex(row_data)
			pid = list(pid)
			pid.pop(0)
			pid.pop(0)
			string_id=""
			while(len(pid)):
				string_id = string_id + pid.pop(0)
			pid = int(string_id, 16)	
			time = row.pop(0)

		elif(is_data(row_data)):
			hex_data = list(extract_hex(row_data))
			data = data + hex_data.pop(2)
			data = data + hex_data.pop(2)
			


# for the last frame, lets just save it once we exit the for loop
save_message([time, pid, data])


