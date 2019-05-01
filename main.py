from os import getenv, remove
from dotenv import load_dotenv
from vk_processes import vk_all_in_one
from xkcd_processes import download_random_comics


if __name__ == '__main__':
    load_dotenv()
    access_token = getenv('ACCESS_TOKEN')
    group_id = getenv('GROUP_ID')
    directory = 'comics'

    file_path, message = download_random_comics(directory)
    json_response = vk_all_in_one(file_path, message, group_id, access_token)
    remove(file_path)
    print(json_response['response'])

