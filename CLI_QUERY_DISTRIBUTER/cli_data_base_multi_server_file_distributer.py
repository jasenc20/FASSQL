
from dotenv import load_dotenv
import os
import paramiko



load_dotenv()

ssh = paramiko.SSHClient()
ssh.load_system_host_keys()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # accepts unknown host keys



#List of Server IP
server_ips = [
    {    
    'ip': os.getenv("SSH_HOST_IP"),
    'username': os.getenv("SSH_USERNAME"),
    'password': os.getenv("SSH_PASSWORD")}    
]

# Distribute Files from the master server to the child servers
def multi_server_file_distributer():

    ssh.connect(
        hostname=server_ips[0]['ip'],
        port=22,
        username=server_ips[0]['username'],
        password=server_ips[0]['password']
    )

    local_folder = f"{os.getenv("BASE_FILE_PATH")}/OUTPUT_TABLES"
    remote_folder = f"{os.getenv("SSH_KEY_PATH")}/OUTPUT_TABLES"
    
    with ssh.open_sftp() as sftp:
    
        # make sure the remote folder exists
        try:
            sftp.stat(remote_folder)
        except FileNotFoundError:
            sftp.mkdir(remote_folder)

        
        for filename in os.listdir(local_folder):
            local_path = os.path.join(local_folder, filename)

            if os.path.isfile(local_path):  # skip subfolders
                remote_path = f"{remote_folder}/{filename}"
                sftp.put(local_path, remote_path)
                print(f"Copied {filename} -> {remote_path}")

    ssh.close()
    return "File copied"