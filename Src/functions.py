import subprocess
from config import config
import os
from pathlib import Path
from time import sleep
import tmux

BASE_URL = Path(__file__).resolve().parent

def is_power_of_two(n):
    # Check if the number is greater than 0 and has only one bit set
    return n > 0 and (n & (n - 1)) == 0

def devide_keyspace(n, keyspace):
    devided = []
    keyspace_0, keyspace_1 = int(keyspace[0],16), int(keyspace[1],16)
    delta = (keyspace_1+1) - keyspace_0
    step = delta // n
    for i in range(n):
        devided.append((hex(keyspace_0+(i*step)), hex(keyspace_0+((i+1)*step) -1)))
    return devided

def check_inputs():
    if not(is_power_of_two(config['main_batch'])):
        raise Exception("The main_batch is not power of two")
    if not(is_power_of_two(config['sub_batch'])):
        raise Exception("The sub_batch is not power of two")

def run_BitCrack_in_window(session_name, window_name, address, keyspace, device_id=0, blocks=1920, threads=256, points=32, share="1/1"):
    command = " ".join([
    str(BASE_URL.joinpath("BitCrack/bin/cuBitCrack").resolve()),
    "-d", str(device_id),
    "--keyspace", keyspace,
    "-b", str(blocks),
    "-t", str(threads),
    "-p", str(points),
    "--share", share,
    "-o", str(BASE_URL.parent/'results'/f'{window_name}.txt'),
    address
    ])

    tmux.run_command(command, session_name, window_name)
    return True


def run_sub_batch(id, keyspace, sub_batch):
    tmux.create_window(config["session_name"], config["window_name"]+str(id))
    run_BitCrack_in_window(config['session_name'],
                            config['window_name']+str(id),
                            config['address'],
                            f"{keyspace[0]}:{keyspace[1]}",
                            config['devices'][0]['device_id'],
                            config['devices'][0]['blocks']/config['main_batch'],
                            config['devices'][0]['threads'],
                            config['devices'][0]['points'],
                            share="1/1")


def run_main_batch(keyspace, main_batch, sub_batch):
    tmux.create_session(config['session_name'])
    sub_keyspaces = devide_keyspace(main_batch, keyspace)
    for i in range(main_batch):
        run_sub_batch(i+1, sub_keyspaces[i], sub_batch)

run_main_batch(config['keyspace'], config['main_batch'], config['sub_batch'])

# print(BASE_URL.parent)