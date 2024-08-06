import asyncio
import board
import digitalio
import neopixel
import adafruit_rfm69
from collections import deque

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
    digitalio.DigitalInOut(board.D13),
    digitalio.DigitalInOut(board.D12),
    digitalio.DigitalInOut(board.D11),
    digitalio.DigitalInOut(board.D10)
]

for r in relays:
    r.direction = digitalio.Direction.OUTPUT

KEYMAP = {
    0: "UP",
    1: "LEFT",
    2: "DOWN",
    3: "RIGHT"
}

relay_queue = deque([], 3)


async def pulse_relay(relay, interval):
    if relays[relay].value == False:
        print(f"relay {relay} pulse started")
        relays[relay].value = True
        await asyncio.sleep(interval)
        relays[relay].value = False
        print(f"relay {relay} pulse ended")


def consume(queue):
    while True:
        if len(queue) > 0:
            r = queue.popleft()
            await pulse_relay(r, FLAME_ON_DURATION)
        await asyncio.sleep_ms(1)


async def reciever(radio, queue):
    while True:
        packet = rfm69.receive(timeout=0.05)
        if packet is not None:
            print(f"Recieved bytes: {packet}")
            # add to queue
            queue.append(int(packet))
        await asyncio.sleep_ms(1)


async def main():
    radio_task = asyncio.create_task(reciever(rfm69, relay_queue))
    pulse_task1 = asyncio.create_task(consume(relay_queue))
    pulse_task2 = asyncio.create_task(consume(relay_queue))
    pulse_task3 = asyncio.create_task(consume(relay_queue))
    pulse_task4 = asyncio.create_task(consume(relay_queue))
    await asyncio.gather(radio_task, pulse_task1, pulse_task2, pulse_task3, pulse_task4)

asyncio.run(main())
