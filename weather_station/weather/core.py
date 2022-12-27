import os, subprocess, unicodedata, requests, re

def detect_undervoltage() -> bool:
    process = subprocess.Popen(['vcgencmd', 'get_throttled'], stdout=subprocess.PIPE)
    response: str = process.communicate()[0].decode().replace('throttled=', '').strip()
    if response == '0x0':
        return False
    if '5' in response:
        # throttled, under-voltage
        return True
    if '4' in response:
        # under-voltage
        return True
    raise ValueError(f'Unknown status for `vcgencmd get_throttled`: {response}')

def send_slack(msg):
        """
        Send message to a slack webhook
        :param msg:
        :return:
        """
        if 'SLACK_HOOK' not in os.environ:
            print(f'SLACK_WEBHOOK is absent! Cannot send message {msg}')
            return
        # sanitise.
        msg = unicodedata.normalize('NFKD', msg).encode('ascii', 'ignore').decode('ascii')
        msg = re.sub('[^\w\s\-.,;?!@#()\[\]]', '', msg)

        r = requests.post(url=os.environ['SLACK_HOOK'].strip(),
                          headers={'Content-type': 'application/json'},
                          data=f"{{'text': '{msg}'}}")
        if r.status_code == 200 and r.content == b'ok':
            return True
        else:
            print(f'{msg} failed to send (code: {r.status_code}, {r.content}).')
            return False
