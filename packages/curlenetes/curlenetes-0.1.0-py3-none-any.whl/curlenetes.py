#!/usr/bin/python3
"""
This should run kubectl port-forward and live it running for consecutive runs.

How to run
KUBECONFIG=~/.kube/my-config.yaml curlenetes namespace.service_name:9180/any/path any curl argument
"""
import hashlib
import json
import os
import random
import socket
import subprocess
import sys
import time


def debug(*args):
    if os.environ.get("LOG_LEVEL", "").upper() == "DEBUG":
        print("DEBUG: ", *args, file=sys.stderr)


def get_context():
    context = (
        subprocess.check_output(["kubectl", "config", "current-context"])
        .decode("utf-8")
        .strip()
    )
    return context


def is_port_forward_running(pid_file):
    try:
        contents = json.load(open(pid_file))
    except FileNotFoundError:
        return False

    pid = contents["pid"]
    return is_pid_alive(pid)


def is_pid_alive(pid):
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    return True


def parse_host(host):
    try:
        ns, svc = host.split(".", 1)
    except ValueError:
        ns = 'default'
        svc = host
    svc, port = svc.split(":")
    port, *path = port.split("/", 1)
    path = path or ["/"]
    return ns, svc, port, "/" + path[0]


def start_port_forward(host, pid_file):
    ns, svc, port, path = parse_host(host)

    random_port = random.randint(30000, 60000)
    command = [
        "kubectl",
        "port-forward",
        "-n",
        ns,
        f"svc/{svc}",
        f"{random_port}:{port}",
    ]
    debug(f"Starting port-forward process with command: {' '.join(command)}")
    process = subprocess.Popen(command)
    debug(f"Started port-forward process with PID {process.pid}")
    with open(pid_file, "w") as f:
        json.dump({"pid": process.pid, "port": random_port}, f)


def get_local_port(pid_file):
    contents = json.load(open(pid_file))
    port = contents["port"]
    pid = contents["pid"]
    for retry in range(10):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect(("localhost", port))
        except ConnectionRefusedError as e:
            if not is_pid_alive(pid):
                raise Exception(f"Port-forward process with PID {pid} has exited")
            debug(f"ConnectionRefusedError: {e}")
            time.sleep(1)
            continue
        finally:
            sock.close()
        break
    else:
        raise Exception(f"Failed to connect to port {port}")

    return port


def main():
    try:
        host, *args = sys.argv[1:]
    except ValueError:
        print("Usage: curlenetes <namespace.service:port> [args]")
        sys.exit(1)
    context = get_context()
    pid_file = f"/tmp/{context}-{hashlib.sha256(host.encode()).hexdigest()}.pid"
    if not is_port_forward_running(pid_file):
        start_port_forward(host, pid_file)
    local_port = get_local_port(pid_file)
    path = parse_host(host)[-1]
    debug(f"Forwarding to {host}:{local_port}")
    command = ["curl", f"http://localhost:{local_port}{path}"] + list(args)
    debug(f"Executing command: {' '.join(command)}")
    subprocess.run(command)


if __name__ == "__main__":
    main()
