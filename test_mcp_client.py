#!/usr/bin/env python3
"""Simple MCP client to test the server."""

import json
import subprocess
import sys
import time


def test_mcp_server(container_name: str = "ephemeris-mcp:latest"):
    """Test MCP server by sending tool call request."""

    # Start container with MCP server
    print("🚀 Starting MCP server container...")
    proc = subprocess.Popen(
        ["docker", "run", "--rm", "-i", container_name],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
    )

    try:
        # Send initialize request
        init_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "test-client", "version": "1.0.0"},
            },
        }
        print("📞 Initializing MCP session...")
        proc.stdin.write(json.dumps(init_request) + "\n")
        proc.stdin.flush()

        # Read initialization response
        response = proc.stdout.readline()
        if response:
            init_data = json.loads(response)
            if "result" in init_data:
                print("✅ Server initialized")
            else:
                print(f"⚠️  Unexpected init response: {init_data}")

        # Send tool call request
        tool_request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {
                "name": "get_planetary_positions",
                "arguments": {"iso_time": "2025-12-16T15:28:00Z", "latitude": 40.7128, "longitude": -74.0060},
            },
        }
        print("📍 Calling get_planetary_positions(2025-12-16T15:28:00Z, NYC)...")
        proc.stdin.write(json.dumps(tool_request) + "\n")
        proc.stdin.flush()

        # Read tool response
        response = proc.stdout.readline()
        if response:
            data = json.loads(response)
            if "result" in data:
                result = data["result"]
                print("\n✅ MCP server responded!\n")

                # Handle if result is wrapped in content array (MCP protocol format)
                if isinstance(result.get("content"), list) and len(result["content"]) > 0:
                    content_text = result["content"][0].get("text", "")
                    if content_text:
                        # Parse the JSON response
                        chart_data = json.loads(content_text)

                        print("🌟 BODIES:")
                        for name, body_data in chart_data.get("bodies", {}).items():
                            line = (
                                f"  {name:18} {body_data['sign']:10} "
                                f"{body_data['sign_degrees']:6.2f}° ({body_data['motion']})"
                            )
                            print(line)

                        print("\n🏠 HOUSES:")
                        for name, house_data in chart_data.get("houses", {}).items():
                            print(f"  {name:18} {house_data['sign']:10} {house_data['sign_degrees']:6.2f}°")

                        print("\n✅ MCP interface test passed!")
                        return 0

                # Handle direct bodies/houses structure (fallback)
                bodies = result.get("bodies", {})
                houses = result.get("houses", {})

                if isinstance(bodies, dict) and bodies:
                    print("🌟 BODIES:")
                    for name, body_data in bodies.items():
                        line = (
                            f"  {name:18} {body_data['sign']:10} "
                            f"{body_data['sign_degrees']:6.2f}° ({body_data['motion']})"
                        )
                        print(line)

                if isinstance(houses, dict) and houses:
                    print("\n🏠 HOUSES:")
                    for name, house_data in houses.items():
                        print(f"  {name:18} {house_data['sign']:10} {house_data['sign_degrees']:6.2f}°")

                print("\n✅ MCP interface test passed!")
                return 0
            elif "error" in data:
                print(f"❌ Error from server: {data['error']}")
                return 1
            else:
                print(f"⚠️  Unexpected response: {json.dumps(data, indent=2)}")
                return 1
        else:
            print("❌ No response from server")
            return 1

    finally:
        # Close stdin to signal we're done
        proc.stdin.close()
        # Give it a moment to finish
        time.sleep(0.5)
        # Terminate if still running
        if proc.poll() is None:
            proc.terminate()
            try:
                proc.wait(timeout=2)
            except subprocess.TimeoutExpired:
                proc.kill()


if __name__ == "__main__":
    sys.exit(test_mcp_server())
