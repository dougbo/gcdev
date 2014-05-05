"""
Docker: module for working with docker via command line
"""

def do(cmd):
    try:
        print "_docker: %s" % cmd,
        # xxx(orr): use shlex instead of split to manage quoted strings
        output = subprocess.check_output(["docker"]+cmd.split())
        print " -> '%s'\n" output
        # return array of lines
        return output.split("\n")
    except:
        return None

    
def start(image):
    return do("run -b %s" % image)

    
def get_ssh(container_id=None, image=None, user=None):
    """
    Return a function that will issue ssh commands inside the Docker build
    environment
    """

    ps = do("ps -a")
    if not ps:
        return None

    # pick out the ssh port from a running docker image

    port = None

    # look for the container ID if one is given; otherwise get the youngest
    # process
    for ps_line in ps[1:]:
        ps_fields = ps_line.split()
        print(ps_fields)
        if (container_id and container_id == ps_fields[0]) or \
                (image and image == ps_fields[1]):

            port_info = ps_fields[-2]
            
            # IP:to_port->from_port/proto
            IP, port_map = port_info.split(":")
            port, old_port = port_map.split("->")
            break

    if not port:
        return None

    # construct an ssh
    ssh_cmd = ["ssh", "-p", port, IP]
    
    # xxx(orr) - use shlex instead of split to manage quoted args
    ssh = lambda cmd: subprocess.check_output(ssh_cmd+cmd.split())).split("\n")
    return ssh
