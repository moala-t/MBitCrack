import subprocess

def kill_session(session_name):
    subprocess.check_output(f"tmux kill-session -t {session_name}".split(" ")).decode("utf-8")
    return True

def create_window(session_name, window_name):
    subprocess.check_output(f"tmux new-window -n {window_name} -d -t {session_name}".split(" ")).decode("utf-8")
    return True

def create_session(session_name):    
    subprocess.check_output(f"tmux new-session -d -s {session_name}".split(" "))
    session_list =  subprocess.check_output("tmux list-session".split(" ")).decode("utf-8")
    if session_name not in session_list:
        raise Exception("Couldn't Create a Tmux Session")
    return True

def get_stdout(session_name, window_name):
    return subprocess.check_output(f"tmux capture-pane -p -t {session_name}:{window_name}".split(" ")).decode("utf-8")

def run_command(command, session_name, window_name):
    tmux_command = [
    'tmux', 'send-keys',
    '-t', f'{session_name}:{window_name}',
    command, 'C-m'
    ]

    subprocess.check_output(tmux_command).decode("utf-8")
    return True

# run_command("ls -al", "MBitCrack", "sub1")