import requests


def get_url_to_upload(group_id, access_token):
    url = 'https://api.vk.com/method/photos.getWallUploadServer'
    payload = {'group_id': group_id,
               'access_token': access_token,
               'v': '5.95'
               }
    response = requests.get(url, params=payload)
    return response.json()['response']


def upload_to_vk_server(upload_url, file_path):
    image_file_descriptor = open(file_path, 'rb')
    photo = {'photo': image_file_descriptor}
    response = requests.post(upload_url, files=photo)
    image_file_descriptor.close()
    return response.json()


def save_to_album(group_id, server, photo, vk_hash, access_token):
    url = 'https://api.vk.com/method/photos.saveWallPhoto'
    payload = {'group_id': group_id,
               'server': server,
               'photo': photo,
               'hash': vk_hash,
               'access_token': access_token,
               'v': '5.95'
               }
    response = requests.post(url, data=payload)
    return response.json()


def post_to_wall(group_id, owner_id, photo_id, message, access_token):
    url = 'https://api.vk.com/method/wall.post'
    attachment = f'photo{owner_id}_{photo_id}'
    payload = {'owner_id': -group_id,
               'from_group': 1,
               'attachments': attachment,
               'message': message,
               'access_token': access_token,
               'v': '5.95'
               }
    response = requests.post(url, data=payload)
    return response.json()


def vk_all_in_one(file_path, message, group_id, access_token):
    upload_url = get_url_to_upload(group_id, access_token)['upload_url']
    upload_response = upload_to_vk_server(upload_url, file_path)
    save_response = save_to_album(group_id,
                                  upload_response['server'],
                                  upload_response['photo'],
                                  upload_response['hash'],
                                  access_token
                                  )
    post_response = post_to_wall(group_id,
                                 save_response['response'][0]['owner_id'],
                                 save_response['response'][0]['id'],
                                 message,
                                 access_token
                                 )
    return post_response
