from asyncio import Event
from logging import error, info
from helpers import ainput
from swarm import FtSwarm

swarm: FtSwarm = None

detect_repl_event = Event()

latest_commands = {
    "detect": ""
}

async def main(globalstate):
    global swarm

    swarm = globalstate["swarm"]

    while True:
        cmd = await ainput("")

        if cmd.startswith("sdc "):
            cmd = cmd.removeprefix("sdc ")

            swarm.ser.write(f"{cmd}\r\n".encode("utf-8"))
            await swarm.oninput.wait()
            info(f"Result: {swarm.line}")
            swarm.oninput.clear()
            continue
        
        if cmd.startswith("detect"):
            latest_commands["detect"] = cmd.removeprefix("detect").strip()
            detect_repl_event.set()
            continue
        
        error("Command not recognized")
        

    