## Probe network

There are three ways to get the IPs of the Pis.

* check the router. Huff.
* make the Pis declare their IPs via Slack to you as soon as they boot up
* Brute force check

Each pi has a file `who_am_I.txt` which has "personal" details.

## Slack

See (setting_up.md)[../setting_up.md]

## Brute force

Roll call

    import requests
    
    def probe_network(penultimate='1'):
        """
        ``penultimate`` is to control the penultimate octet: 
        downstairs uses 192.168.0.x, while upstairs 192.168.1.x
        """
        valids = []
        for host_i in range(1, 256):
            try:
                url = f'http://192.168.{penultimate}.{host_i}:8888/'
                s = requests.Session()
                s.mount(url, requests.adapters.HTTPAdapter(max_retries=0))
                reply = s.get(url)
                if reply.status_code == 200:
                    print(f'VALID: {url}')
                    valids.append(url)
                else:
                    raise ConnectionError
            except Exception:
                print(f'INVALID: {url}')
        return valids
        
So `probe_network(penultimate='0')` will return the list of ips.
I started writing a way to type the password if needed, but it's overkill.
The idea was to see the `http://192.168.0.75:8888/view/who_am_I.txt` file

    def insert_password(sesh):
    rex = reply.text.search('name="_xsrf" value="(.*?)"\/\>')
    if rex:
        _xsrf = rex.group(1)
        password_input = '👾👾👾👾👾👾'
        reply = sesh.post('/login?next=%2Ftree', {'_xsrf': _xsrf, 'password_input': password_input})
        ...