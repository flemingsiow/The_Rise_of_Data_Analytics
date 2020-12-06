
# define the countdown func. 
def countdown(t): 

    # import the time module 
    import time 

    while t: 
        mins, secs = divmod(t, 60) 
        timer = '{:02d}:{:02d}'.format(mins, secs) 
        #print(timer, end="\r") 
        print(timer)
        time.sleep(1) 
        t -= 1