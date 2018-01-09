# Tiny Stopwatch in Python

import simplegui

# define global variables
time_decisecs = 0
stops = 0
success = 0

def score():
    return str(success) + "/" + str(stops)

def calc_score():
    global stops, success
    stops += 1
    if((time_decisecs%10) == 0):
        success +=1
        

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(time):
    deciseconds = time % 10
    seconds = (time/10) % 60
    minutes = (time/10) / 60
    
    minutes = str(minutes)
    
    if seconds < 10:
        seconds = "0" + str(seconds)
    else:
        seconds = str(seconds)
        
    deciseconds = str(deciseconds)
    
    formated_time = minutes + ":" + seconds + "." + deciseconds
    return formated_time
    
# define event handlers for buttons; "Start", "Stop", "Reset"
def start():
    timer.start()
    
def stop():
    timer.stop()
    calc_score()

def reset():
    timer.stop()
    global time_decisecs, stops, success
    time_decisecs = stops = success = 0

# define event handler for timer with 0.1 sec interval
def counter():
    global time_decisecs
    time_decisecs += 1

# define draw handler
def draw(canvas):
    canvas.draw_text(format(time_decisecs), (25, 50), 20, "Red")
    canvas.draw_text(score(), (70, 20), 20, "Green")
    
# create frame
frame = simplegui.create_frame("Stop Watch", 100, 150)
frame.set_draw_handler(draw)
start_button = frame.add_button("Start", start)
frame.add_label("")
stop_button = frame.add_button("Stop", stop)
frame.add_label("")
reset_button = frame.add_button("Reset", reset)
frame.add_label("")

# register event handlers
timer = simplegui.create_timer(100, counter)

# start frame
frame.start()

# Please remember to review the grading rubric
