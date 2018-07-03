# HAProxy L7 Load Balancer:
#
# Configure a daemon (a process that monitors backends change) 
# where the template file of HAProxy is rendered to a destination path, 
# and reloaded to be up-to-date.



while True:
	data = recv_message(lsnr)[0]
	changes = data.get("data", {})
	for change in changes:
		print(change)

def function():
	data = recv_message(lsnr)
	changes = data.get("data", {})
	for change in changes:
		print(change)


lsnr_path = "/var/lib/opensvc/lsnr/lsnr.sock"

lsnr = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
lsnr.connect(lsnr_path)
lsnr.sendall(msg_encode({"action": "events"}))
data = recv_message(lsnr)[0]
changes = data.get("data", {})
lsnr.close()


# functions to edit the haproxy configuration file :

def replace_line(file, line, char):
    with open(file, 'r') as f_r:
        lines = f_r.readlines()
        lines[line] = char
    with open(file, 'w') as f_w:
        f_w.writelines(lines)
        f_w.close()
 
def find_line(file_name, regex):

    lines_to_change = []
    with open(file_name, 'r') as f:
        for num, line in enumerate(f, 1):
            line = line.rstrip()
            for m in re.finditer(regex,line):
                lines_to_change.append(num)
    return lines_to_change
 

# test server (JS) 
var http = require('http');

function serve(ip, port)
{
        http.createServer(function (req, res) {
            res.writeHead(200, {'Content-Type': 'text/plain'});
            res.write(JSON.stringify(req.headers));
        }).listen(port, ip);
        console.log('Server running at http://'+ip+':'+port+'/');
}


CONFIG_FILE = '/etc/haproxy/haproxy.conf'

# HAProxy parameters


FRONTEND_PARAMETERS = [
    'bin',
    'bout',
    'comp_byp',
    'comp_in',
    'comp_out',
    'comp_rsp',
    'dreq',
    'dresp',
    'ereq',
    'hrsp_1xx',
    'hrsp_2xx',
    'hrsp_3xx',
    'hrsp_4xx',
    'hrsp_5xx',
    'hrsp_other',
    'rate',
    'rate_lim',
    'rate_max',
    'req_rate',
    'req_rate_max',
    'req_tot',
    'scur',
    'slim',
    'smax',
    'stot',
]




BACKEND_PARAMETERS = [
    'act',
    'bck',
    'bin',
    'bout',
    'chkdown',
    'cli_abrt',
    'comp_byp',
    'comp_in',
    'comp_out',
    'comp_rsp',
    'ctime',
    'downtime',
    'dreq',
    'dresp',
    'econ',
    'eresp',
    'hrsp_1xx',
    'hrsp_2xx',
    'hrsp_3xx',
    'hrsp_4xx',
    'hrsp_5xx',
    'hrsp_other',
    'lastchg',
    'lastsess',
    'lbtot',
    'qcur',
    'qmax',
    'qtime',
    'rate',
    'rate_max',
    'rtime',
    'scur',
    'slim',
    'smax',
    'srv_abrt',
    'stot',
    'ttime',
    'weight',
    'wredis',
    'wretr',
]


SERVER_PARAMETERS = [
    'qcur',
    'qmax',
    'scur',
    'smax',
    'stot',
    'bin',
    'bout',
    'dresp',
    'econ',
    'eresp',
    'wretr',
    'wredis',
    'weight',
    'act',
    'bck',
    'chkfail',
    'chkdown',
    'lastchg',
    'downtime',
    'qlimit',
    'throttle',
    'lbtot',
    'rate',
    'rate_max',
    'check_duration',
    'hrsp_1xx',
    'srvmaxtimeout',
    'hrsp_2xx',
    'hrsp_3xx',
    'hrsp_4xx',
    'hrsp_5xx',
    'hrsp_other',
    'cli_abrt',
    'srv_abrt',
    'lastsess',
    'qtime',
    'ctime',
    'rtime',
    'ttime',
]

# HAProxy changing URL :
# reqrep ^([^\ :]*)\ /\?pdf=(.*)(\ [^\ ]+)$  \1\ /newpdf?search=%22\2%22\3

def haproxy_status():
    # TODO: get haproxy status/pids

def reload_haproxy():
    reload = False
    if os.path.isfile("/etc/init/haproxy.conf"):
        reload = True
    if reload:
        print("we are reloading the haproxy conf")
        try:
            start = time.time()
            retry = start
            current_haproxy_status = harpoxy_status()
            # TODO: reload the config file / init haproxy
            new_haproxy_status = haproxy_status()
            # infinite loop until we reload
            while True:
                if len(current_haproxy_status - new_haproxy_status) >= 1:
                    print("reload succesful")
                    break
                ifretry = time.time() - retry
                if (ifretry > reload_frequency):
                    print("wait for new haproxy status")
                    time.sleep(1)
                    new_haproxy_status = haproxy_status()


class Template:
    def __init__(self, name, value):
        self.name = name
        self.value = value


class ConfigHaproxy(object):
    def __init__(self):
        self.template_haproxy = template_haproxy
        self.temp = dict()

      

    def append(self, template):
        self.temp[template.name] = template

    def generate_template(self):
        self.append(Template('main_config', 
            '''
            global
                log /dev/log local0
                log /dev/log local1 notice
                maxconn 50000
            defaults
                load-server-state-from-file global
                log   global
                backlog   10000
                maxconn   50000
                timeout connect 5000ms
                timeout client 50000ms
                timeout server 50000ms
                timeout http-keep-alive  1s
                timeout http-request     15s
            listen stats
                bind 0.0.0.0:1936
                balance
                mode http
                stats enable
            '''
            ))
        self.append(Template('frontend',
            '''
            frontend {frontend}
                bind {bind}
                mode http
            '''
            ))
        self.append(Template('backend',
            '''
            backend {backend}
                balance {balance}
                mode http
            '''
            ))

        # TODO:  add more template depending on whether it's required. 

    # override template from a template file. 
    def load_template(self):
        for template in self.temp:
            filen = self.template_haproxy
            with open(filen) as f:
                self.temp[template].value = f.read()
