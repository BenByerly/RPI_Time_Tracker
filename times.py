# times.py


# =================
#     Time list
# =================
times = [
    # first column
    "7:30",  "7:45",
    "8:00", "8:15", "8:30", "8:45",
    "9:00", "9:15", "9:30", "9:45",
    "10:00", "10:15","10:30", "10:45",
    "11:00", "11:15", "11:30",


    # second column
    "11:45",
    "12:00", "12:15", "12:30", "12:45",
    "1:00", "1:15", "1:30", "1:45",
    "2:00", "2:15", "2:30", "2:45",
    "3:00", "3:15", "3:30", "3:45",

    
]

strike_fourpm = False

# colum assignment
mid = len(times) // 2
col_1 = times[:mid]
col_2 = times[mid:]

# crossed out state
crossed = [False] * len(times)

# pointer init to next item cross
ptr = 0
