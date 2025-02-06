from mail_room.email_moogent import work, test 
import yaml 

with open("mail_room/config.yaml") as f:
    config = yaml.safe_load(f)


if config['mode'] == 'work':
    work()
else:
    test()
