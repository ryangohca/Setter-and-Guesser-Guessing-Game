from microbit import *
import radio
radio.on()
radio.config(channel=2)
def getNumber(minnum=1, maxnum=100, default=None):
    if default is None or default > maxnum or default < minnum:
        default = minnum
    curr_num = default
    while True:
        curr_num += button_a.get_presses()
        if curr_num > maxnum:
            if minnum == maxnum:
                curr_num = minnum
            else:
                curr_num = minnum + (curr_num - minnum - 1) % (maxnum - minnum)
        display.scroll(curr_num)
        if button_b.was_pressed():
            display.show(Image.YES)
            sleep(1000)
            display.clear()
            return curr_num
num_guesses = 0
preva = 1
prevb = 1
while True:
    msg = radio.receive()
    if msg is None:
        display.show(Image.NO)
    elif msg.startswith("Actual"):
        display.clear()
        dummy, a, b = msg.split(" ")
        a = int(a)
        b = int(b)
        display.scroll("Opponent is done. Your turn to guess.", delay=100)
        display.scroll("  Select A:", delay=100)
        a_guess = getNumber(default=preva)
        display.scroll("  Select B:", delay=100)
        b_guess = getNumber(default=prevb)
        num_guesses += 1
        if a == a_guess and b == b_guess:
            radio.send("Done " + str(num_guesses))
            display.scroll("  Congrats, you are right!", delay=100)
            display.scroll("  Number of guesses (smaller better): %d" % num_guesses, delay=100)
            break
        else:
            verdict_a = '<='
            if a_guess > a:
                verdict_a = '>'
            verdict_b = '<='
            if b_guess > b:
                verdict_b = '>'
            display.scroll(' '.join(["  A", '<' if verdict_a == '>' else '>=', str(a_guess) + ',']), delay=100)
            display.scroll(' '.join(["  B", '<' if verdict_b == '>' else '>=', str(b_guess)]), delay=100)
            preva, prevb = a_guess, b_guess
            radio.send(' '.join(["Guess", str(a_guess), verdict_a, str(b_guess), verdict_b]))
    