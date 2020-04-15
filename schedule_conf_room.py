import os
import sys

#NOTE: Here i have used mainly dictionaries, list and tuples to solve this program

#Comparing two time (hr:min) and return value will be minutes
def time_compare(t1, t2):
  #print t1, t2
  s = t1.split(":")
  e = t2.split(":")
  x = int(s[0]) - int(e[0])
  if x != 0:
    return x
  return int(s[1]) - int(e[1])

#Returning time difference
def time_diff(t1, t2):
  #print t1, t2
  s = t1.split(":")
  e = t2.split(":")
  t = (int(e[0]) - int(s[0])) * 60
  return (t + int(e[1]) - int(s[1]))

#get_room_info - will return rooms which are available
#parsing the i/p file and storing it in dictionary 
#Key is floor.member
#first value is room capacity
#second value is time slots
def get_room_info():
  f = open("room.txt", "r")
  meeting = {}
  for line in f.readlines():
    if not line:
      continue
    line = line.strip()
    room = line.split(",")
    print(room)
    if room[0] not in meeting:
      meeting[room[0]] = {}
    time = []
    for i in range(2, len(room), 2):
      time.append((room[i], room[i+1], time_diff(room[i], room[i+1])))
    meeting[room[0]] = (room[1], time)
  f.close()
  return meeting


#find_rooms - will return matching dictionary
#for my time, availability of room
def find_rooms(floor, num, t1, t2, meeting):
  time = (t1, t2, time_diff(t1, t2))
  res = {}
  start = time[0]
  end = time[1]
  for room, val in meeting.items():
    if int(val[0]) >= int(num):
      slot_list = []
      for (s,e,d) in val[1]:
        #print s,e,d, start, end, time_compare(s, start), time_compare(end, e)
        if time_compare(s, start) <= 0 and time_compare(end, e) <= 0:
          slot_list.append((s,e,d))
      if not slot_list:
        continue
      res[room] = (val[0], slot_list)
  return res

#find_best_room - searching for the room which is avilable on the same floor or near to the floor(as input given)
def find_best_room(floor, num, t1, t2, res):
  best  = 0
  diff_floor_min = 0
  diff_mem_min = 0
  for room, val in res.items():
    f, _ = room.split(".")
    diff_floor = abs(int(f) - int(floor))
    diff_mem = int(val[0]) - int(num)
    if best == 0:
      best = room
      diff_floor_min = diff_floor
      diff_mem_min = diff_mem
      continue
    if diff_floor > diff_floor_min:
      continue
    if diff_floor < diff_floor_min:
      best = room
      diff_floor_min = diff_floor
      diff_mem_min = diff_mem
      continue
    if diff_floor == diff_floor_min:
      if diff_mem < diff_mem_min:
        diff_mem_min = diff_mem
        best = room
  return best

floor, num, t1, t2 = input("Please enter Floor number, Member count, Start time[hr:min] and End time[hr:min]. Each separated by a space : ").split()
print ("Team Floor : %s Num %s Start time %s End time %s" % (floor, num, t1, t2))

meeting = get_room_info()
print ("======================")
print ("Meeting room available :")
print ("----------------------")
for room in meeting:
  print ("%s : %s" % (room, meeting[room]))
print ("----------------------")
print ("Meeting room short listed :")
print ("----------------------")
res = find_rooms(floor, num, t1, t2, meeting)
for room in res:
  print ("%s : %s" % (room, res[room]))
print ("----------------------")
print ("Meeting room selected:")
print ("----------------------")
found = find_best_room(floor, num, t1, t2, res)
if found:
  print ("Room: %s Time: %s" % (found, res[found]))
else:
  print ("No Room found")
print ("======================")
