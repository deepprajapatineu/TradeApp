import subprocess
import time

def run_server():
    print("Starting the server...")
    server_process = subprocess.Popen(
        ["python", "src/server.py"], 
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE, 
        text=True
    )
    return server_process

def run_client():
    print("Starting the client...")
    client_process = subprocess.Popen(
        ["python", "src/client.py"], 
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE, 
        text=True
    )
    return client_process

def wait_for_server_ready(server_process):
    while True:
        output = server_process.stdout.readline()
        if "Session created" in output:
            print("Server is ready.")
            break
        if server_process.poll() is not None:
            print("Server process ended unexpectedly.")
            raise Exception("Server failed to start.")
        time.sleep(1)

def main():
    server_process = run_server()

    try:
        wait_for_server_ready(server_process)
        client_process = run_client()

        # Wait for the client to finish (or you can implement your own logic)
        client_process.wait()

    finally:
        # Cleanup: Terminate the server if still running
        if server_process.poll() is None:
            server_process.terminate()
            print("Server terminated.")

if __name__ == "__main__":
    main()
