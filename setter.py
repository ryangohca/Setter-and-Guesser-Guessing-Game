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
mina = 1
maxa = 100
minb = 1
maxb = 100
display.scroll("  Select A:", delay=100)
curr_a = getNumber(mina, maxa)
display.scroll("  Select B:", delay=100)
curr_b = getNumber(minb, maxb)
prev_a, prev_b = curr_a, curr_b
radio.send(' '.join(["Actual", str(curr_a), str(curr_b)]))
while True:
    msg = radio.receive()
    if msg is None:
        display.show(Image.NO)
    elif msg.startswith("Guess"):
        display.clear()
        dummy, guess_a, verdict_a, guess_b, verdict_b = msg.split(' ')
        if verdict_a == '>':
            maxa = min(maxa, int(guess_a) - 1)
        else:
            mina = max(mina, int(guess_a))
        if verdict_b == '>':
            maxb = min(maxb, int(guess_b) - 1)
        else:
            minb = max(minb, int(guess_b))
        display.scroll("  Opponent guessed (A: %s, B: %s)" % (guess_a, guess_b), delay=100)
        display.scroll("Select A:", delay=100)
        curr_a = getNumber(mina, maxa, default=prev_a)
        display.scroll("  Select B:", delay=100)
        curr_b = getNumber(minb, maxb, default=prev_b)
        preva, prevb = curr_a, curr_b
        radio.send(' '.join(["Actual", str(curr_a), str(curr_b)]))
    elif msg.startswith("Done"):
        display.clear()
        dummy, guesses = msg.split(' ')
        display.scroll("  Opponent guessed both numbers correctly.", delay=100)
        display.scroll("Number of guesses (bigger better): " + guesses, delay=100)
        break