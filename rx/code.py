import asyncio
import board
import digitalio
import neopixel
import adafruit_rfm69
from collections import deque

# Time to hold gas solenoids open
FLAME_ON_DURATION = 0.5

## Radio parts
ENCKEY = bytearray("asdfghjklasdfghj", 'utf-8')
RADIO_FREQ_MHZ = 915.0
# Define Chip Select and Reset pins for the radio module.
CS = digitalio.DigitalInOut(board.RFM_CS)
RESET = digitalio.DigitalInOut(board.RFM_RST)

# Initialise RFM69 radio
rfm69 = adafruit_rfm69.RFM69(board.SPI(), CS, RESET, RADIO_FREQ_MHZ, encryption_key=ENCKEY)

relays = [
    digitalio.DigitalInOut(board.D6),   # UP
    digitalio.DigitalInOut(board.D9),   # LEFT
    digitalio.DigitalInOut(board.D10),  # DOWN
    digitalio.DigitalInOut(board.D11)   # RIGHT
]

for r in relays:
    r.direction = digitalio.Direction.OUTPUT

KEYMAP = {
    0: "UP",
    1: "LEFT",
    2: "DOWN",
    3: "RIGHT",
    4: "BIGBUTTON"
}

relay_queue = deque([], 4)
pulse_all_running = False


async def pulse_relay(relay, interval):
    global pulse_all_running  # ugh
    if pulse_all_running:
        print("ALREADY RUNNING PULSE ALL")
        return
    if relays[relay].value == False:
        print(f"relay {relay} pulse started")
        relays[relay].value = True
        await asyncio.sleep(interval)
        relays[relay].value = False
        print(f"relay {relay} pulse ended")
    else:
        print(f"relay {relay} already high")

async def pulse_all(interval):
    '''
    When you give up on making pulse_relay clever... :(
    '''
    global pulse_all_running  # ugh
    if pulse_all_running:
        print("ALREADY RUNNING PULSE ALL")
        return
    pulse_all_running = True
    print("PULSE ALL")
    for r in range(4):
        relays[r].value = True
    await asyncio.sleep(interval)
    for r in range(4):
        relays[r].value = False
    print("PULSE ALL OFF")
    pulse_all_running = False


def consume(queue):
    while True:
        if len(queue) > 0:
            r = queue.popleft()
            if r < 4:
                await pulse_relay(r, FLAME_ON_DURATION)
            elif r == 4:
                await pulse_all(FLAME_ON_DURATION)
            else:
                print("relay out of range")
        await asyncio.sleep_ms(0)


async def reciever(radio, queue):
    while True:
        packet = rfm69.receive(timeout=0.05)
        if packet is not None:
            print(f"Recieved bytes: {packet}")
            r = int(packet)
            # add to queue
            queue.append(r)
        await asyncio.sleep_ms(0)


async def main():
    radio_task = asyncio.create_task(reciever(rfm69, relay_queue))
    pulse_task1 = asyncio.create_task(consume(relay_queue))
    pulse_task2 = asyncio.create_task(consume(relay_queue))
    pulse_task3 = asyncio.create_task(consume(relay_queue))
    pulse_task4 = asyncio.create_task(consume(relay_queue))
    await asyncio.gather(radio_task, pulse_task1, pulse_task2, pulse_task3, pulse_task4)

asyncio.run(main())
