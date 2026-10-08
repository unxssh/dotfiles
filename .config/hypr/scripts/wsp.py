#!/usr/bin/env python3
"""
Hyprland Workspace Compactor
Automatically shifts workspaces to maintain contiguous numbering (1, 2, 3...)
whenever windows or workspaces are closed or moved.
"""
import glob
import json
import os
import socket
import subprocess
import time

def get_clients():
    try:
        out = subprocess.check_output(["hyprctl", "-j", "clients"], timeout=2)
        return json.loads(out)
    except Exception:
        return []

def get_active_workspace():
    try:
        out = subprocess.check_output(["hyprctl", "-j", "activeworkspace"], timeout=2)
        return json.loads(out).get("id", 1)
    except Exception:
        return 1

def compact_workspaces():
    clients = get_clients()
    # Positive IDs only (regular workspaces)
    occupied = sorted(list(set(c["workspace"]["id"] for c in clients if c["workspace"]["id"] > 0)))

    if not occupied:
        return

    # Check mapping
    mapping = {}
    for i, ws in enumerate(occupied):
        target = i + 1
        if ws != target:
            mapping[ws] = target

    if not mapping:
        return

    active_ws = get_active_workspace()
    new_active_ws = active_ws

    # Move windows in ascending order so target workspace is always vacant
    for ws in occupied:
        if ws in mapping:
            target = mapping[ws]
            ws_clients = [c for c in clients if c["workspace"]["id"] == ws]
            for c in ws_clients:
                addr = c.get("address")
                if addr:
                    subprocess.run(
                        ["hyprctl", "dispatch", "movetoworkspacesilent", f"{target},address:{addr}"],
                        check=False,
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL
                    )
            if active_ws == ws:
                new_active_ws = target

    # If the active workspace was shifted, follow it
    if new_active_ws != active_ws:
        subprocess.run(
            ["hyprctl", "dispatch", "workspace", str(new_active_ws)],
            check=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

def get_socket_path():
    runtime_dir = os.environ.get("XDG_RUNTIME_DIR", "/run/user/1000")
    sig = os.environ.get("HYPRLAND_INSTANCE_SIGNATURE")
    if sig:
        path = f"{runtime_dir}/hypr/{sig}/.socket2.sock"
        if os.path.exists(path):
            return path
    matches = glob.glob(f"{runtime_dir}/hypr/*/.socket2.sock")
    if matches:
        return matches[0]
    return None

def main():
    sock_path = get_socket_path()
    if not sock_path:
        time.sleep(2)
        sock_path = get_socket_path()
        if not sock_path:
            return

    # Initial check
    compact_workspaces()

    # Listen to Hyprland IPC events
    while True:
        try:
            s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            s.connect(sock_path)
            buffer = ""
            while True:
                data = s.recv(4096)
                if not data:
                    break
                buffer += data.decode("utf-8", errors="ignore")
                lines = buffer.split("\n")
                buffer = lines[-1]
                
                needs_compact = False
                for line in lines[:-1]:
                    event = line.split(">>")[0] if ">>" in line else line
                    if event in ("closewindow", "destroyworkspace", "movewindow", "changefloatingmode"):
                        needs_compact = True

                if needs_compact:
                    time.sleep(0.08)  # Debounce rapid actions
                    compact_workspaces()
        except Exception:
            time.sleep(1)

if __name__ == "__main__":
    main()
