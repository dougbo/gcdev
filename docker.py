"""
Docker: module for working with docker via command line
"""

import subprocess
import re

def do(cmd_vec):
    """
    do: convenience function that executes a docker command and returns an array
    of output lines on success.
    """
    try:
        docker_cmd = ["docker"]+cmd_vec
        output = subprocess.check_output(docker_cmd)
        # return array of lines
        return output.split("\n")
    except subprocess.CalledProcessError:
        return None

    
def ps():
    """
    ps: return info about existing docker processes, structured as a list of dict's
    keys for the dicts are (lower case'd) column names. 
    """
	ps_out = do(["ps"])

	# ps output is column-aligned. Use the column headers to pull 
        # out the column data which we return in a list of dicts 

        # (it's super annoying they include a space in a col name, btw)
        _COLS_RE = [
            "container id +",
            "image +",
            "command +",
            "created +",
            "status +",
            "ports +",
            "names +"
            ]

        # get the column names including the space padding from the actual ps output
	all_cols = ps_out[0].lower()
	cols = re.findall("|".join(_COLS_RE), all_cols)

        # pick through each line of output and create a dict with the column 
        # contents, keyed by the column name. shift the processed part 
        # of the line off and repeat
        ps = []
        for line in ps_out[1:]:
            if line.strip() == '':
                continue

            d = {}
            for col in cols:
                # use the space padding to determine column contents; remove space 
                # padding in column name and contents when putting in the dict
                cname = col.strip()

                d[cname] = line[:len(col)].strip()
                line = line[len(col):]
            ps.append(d)

        # return the array of dict's (in ps order, which corresponds to creation time)
        return ps


def kill(container_id):
    """
    kill: kill the given docker container
    """
    do(["kill", container_id])
    

def start(image, env={}):
    """
    start: start a new instance of a docker image; propagate environment
    variables.
    """
    cmd_vec = ["run", "-t", "-d", "-P"]
    for key in env.keys():
        cmd_vec.append("-e")
        cmd_vec.append("%s=%s" % (key, env[key]))
    cmd_vec.append(image)
    return do(cmd_vec)



def ifconfig():
    """
    ifconfig: return parsed output from the ifconfig process for the current 
    docker network.

    xxx(orr): ASSUMING one docker net per host
    """
    def _ifconfig_parse(c):
        _KW_ARG = [
            "Link encap:",
            "HWaddr",
            "inet addr:",  
            "Bcast:",  
            "Mask:",
            "MTU:",
            "Metric:",
            "errors:", 
            "dropped:", 
            "overruns:", 
            "frame:",
            "carrier:",
            "collisions:", 
            "txqueuelen:",
            "RX bytes:",
            "TX bytes:",
            ]
        _KW = [
            "TX packets:",
            "RX packets:",
            "UP", 
            "DOWN",
            "BROADCAST",
            "RUNNING",
            "MULTICAST"
            ]

        # ifconfig parsing --

        # find the next keyword; if the keyword has an arg, look ahead to the 
        # next keyword and pull off what's in between the first kw as its arg; 
        # we're ignoring the non-arg _KW's except to stop parsing args...
        # that could be improved. Also, since some, but not all kw's 
        # are _not_ separated from their args by colons, we include the colon as 
        # part of the kw... not awesome but easier to undo than
        # the other more rigid things we'd need to do with the argument parsing otherwise.

        c = str.replace(c, '\n', ' ')
        kwarg_pat = "|".join(_KW_ARG)
        kw_pat = "|".join(_KW)
        allkw_pat = "%s|%s" % (kwarg_pat, kw_pat)
        matches = re.findall("(%s)(.+?)(?=%s)" % (kwarg_pat, allkw_pat), c)

        ifconfig = {}
        for kw, value in matches:
            if kw[len(kw)-1] == ':':
                kw = kw[0:len(kw)-1]
            ifconfig[kw] = value.strip()
            
        return ifconfig

    all_config = subprocess.check_output("/sbin/ifconfig").split("\n\n")
    for c in all_config:
        if c[0:len("docker")] == "docker":

            # xxx(orr): we only work properly with one docker network
            docker_ifconfig = c[len("docker0"):]
            return _ifconfig_parse(docker_ifconfig)

    return None



def get_ip():
    """
    Return the host's IP address of the current Docker instance
    """

    ifconfig_info = ifconfig()
    if not ifconfig_info or not ifconfig_info['inet addr']:
        return None

    return ifconfig_info['inet addr']

    
    
def get_ssh(container_id=None, image=None, user=None):
    """
    Return a function that will issue ssh commands inside the Docker container
    """

    ps_info = ps()
    # pick through and find either the container ID or first matching image
    rec = None

    for i in ps_info:

        if not rec and (not container_id or (i['image'] == image and i['ports'])):
            # record the first record that matches our image and has a port spec
            rec = i

        if i['container id'] == container_id:
            # exact match trumps
            rec = i
            break
        

    if not rec or not rec['ports']:
        return None

    # pick out the ssh port from a running docker image

    # IP:to_port->from_port/proto
    IP, port_map = rec['ports'].split(":")
    port, old_port = port_map.split("->")

    if not port:
        return None

    docker_ip = get_ip()

    # construct an ssh
    ssh_cmd = ["ssh", "-o", "StrictHostKeyChecking=no","-p", port, docker_ip]

    
    ssh = lambda *args: subprocess.check_call(ssh_cmd+list(args))
    return ssh

if __name__ == '__main__':
    print ps()
    print ifconfig()

    ssh = get_ssh()

    if ssh:
        ssh("hostname")
    else:
        print "get_ssh failed"
