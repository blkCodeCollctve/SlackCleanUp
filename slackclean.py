import yaml
from slackclient import SlackClient
from datetime import  datetime, timedelta

def get_config(config_file):
    with open(config_file, 'r') as infile:
        config = yaml.load(infile)

    return config

def get_old_files(token, days):
    # Making slack client
    sc = SlackClient(token)

    # Calculate
    to_time = datetime.now() - timedelta(days=days)
    to_time_stamp = int(to_time.timestamp())

    print('Getting files to {} ({} days)'.format(to_time.strftime('%m/%d/%Y %H:%M:%S'), days))
    # List of all files
    file_list = []

    # Making initial call

    resp = sc.api_call('files.list',ts_to=to_time_stamp)
    pages = resp['paging']['pages']
    print('Getting Page: 1/{}'.format(pages))
    file_list += resp['files']

    if pages > 1:
        # Paging through API calls to get all objects
        for page in range(2, pages+1):
            print('Getting Page: {}/{}'.format(page, pages))
            # Getting next page
            resp = sc.api_call('files.list', page=page, ts_to=to_time_stamp)
            # Adding new files to list to be returned
            file_list += resp['files']

    return file_list


def main():
    config = get_config('config.yml')
    slack_token = config['slack_creds']['token']

    old_file_list = get_old_files(slack_token, 90)

    total_size = 0
    for file in old_file_list:
       total_size += file['size']

    print('{} MB to be deleted'.format(total_size/(1024*1024)))


if __name__ == '__main__':
    main()