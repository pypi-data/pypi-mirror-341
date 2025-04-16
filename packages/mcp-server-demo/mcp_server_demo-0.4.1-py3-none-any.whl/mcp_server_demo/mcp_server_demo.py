# server.py
from mcp.server.fastmcp import FastMCP
# import requests

# Create an MCP server
mcp = FastMCP("Demo")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b


# @mcp.tool()
# def run_docker_container(
#     access_token: str,
#     username: str,
#     token: str,
#     image_name: str,
#     container_name: str
# ) -> str:
#     url = "http://3.109.184.200:6001/docker-setup/run-docker-container"
#     headers = {
#         "Content-Type": "application/json",
#         "Access-Token": access_token
#     }
#     data = {
#         "username": username,
#         "token": token,
#         "image_name": image_name,
#         "container_name": container_name
#     }

#     try:
#         response = requests.post(url, headers=headers, json=data)
#         response.raise_for_status()
#         return response.text
#     except requests.exceptions.HTTPError as http_err:
#         return f"HTTP error occurred: {http_err} - {response.text}"
#     except requests.exceptions.ConnectionError as conn_err:
#         return f"Connection error occurred: {conn_err}"
#     except requests.exceptions.Timeout as timeout_err:
#         return f"Timeout error occurred: {timeout_err}"
#     except requests.exceptions.RequestException as req_err:
#         return f"An error occurred: {req_err}"


# @mcp.tool()
# def stop_docker_container(access_token: str, container_name: str) -> str:
#     url = "http://3.109.184.200:6001/docker-setup/stop-docker-container"
#     headers = {
#         "Content-Type": "application/json",
#         "Access-Token": access_token
#     }
#     data = {
#         "container_name": container_name
#     }

#     try:
#         response = requests.post(url, headers=headers, json=data)
#         response.raise_for_status()
#         return response.text
#     except requests.exceptions.HTTPError as http_err:
#         return f"HTTP error occurred: {http_err} - {response.text}"
#     except requests.exceptions.ConnectionError as conn_err:
#         return f"Connection error occurred: {conn_err}"
#     except requests.exceptions.Timeout as timeout_err:
#         return f"Timeout error occurred: {timeout_err}"
#     except requests.exceptions.RequestException as req_err:
#         return f"An error occurred: {req_err}"


# @mcp.tool()
# def remove_docker_container(access_token: str, container_name: str) -> str:
#     url = "http://3.109.184.200:6001/docker-setup/remove-docker-container"
#     headers = {
#         "Content-Type": "application/json",
#         "Access-Token": access_token
#     }
#     data = {
#         "container_name": container_name
#     }

#     try:
#         response = requests.post(url, headers=headers, json=data)
#         response.raise_for_status()
#         return response.text
#     except requests.exceptions.HTTPError as http_err:
#         return f"HTTP error occurred: {http_err} - {response.text}"
#     except requests.exceptions.ConnectionError as conn_err:
#         return f"Connection error occurred: {conn_err}"
#     except requests.exceptions.Timeout as timeout_err:
#         return f"Timeout error occurred: {timeout_err}"
#     except requests.exceptions.RequestException as req_err:
#         return f"An error occurred: {req_err}"


# @mcp.tool()
# def get_docker_container_status(access_token: str, container_name: str) -> str:
#     url = "http://3.109.184.200:6001/docker-setup/get-container-status"
#     headers = {
#         "Content-Type": "application/json",
#         "Access-Token": access_token
#     }
#     data = {
#         "container_name": container_name
#     }

#     try:
#         response = requests.post(url, headers=headers, json=data)
#         response.raise_for_status()
#         print("Status Code:", response.status_code)
#         print("Response Body:", response.text)
#         return response.text
#     except requests.exceptions.RequestException as e:
#         return f"Error occurred: {str(e)}"


# @mcp.tool()
# def start_stopped_container(access_token: str, container_name: str) -> str:
#     url = "http://3.109.184.200:6001/docker-setup/start-stopped-container"
#     headers = {
#         "Content-Type": "application/json",
#         "Access-Token": access_token
#     }
#     data = {
#         "container_name": container_name
#     }

#     try:
#         response = requests.post(url, headers=headers, json=data)
#         response.raise_for_status()
#         return response.text
#     except requests.exceptions.HTTPError as http_err:
#         return f"HTTP error occurred: {http_err} - {response.text}"
#     except requests.exceptions.ConnectionError as conn_err:
#         return f"Connection error occurred: {conn_err}"
#     except requests.exceptions.Timeout as timeout_err:
#         return f"Timeout error occurred: {timeout_err}"
#     except requests.exceptions.RequestException as req_err:
#         return f"An error occurred: {req_err}"
