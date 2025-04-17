import requests

class EitaaBot:
    def __init__(self, token):
        self.token = token
        self.base_url = f'https://eitaayar.ir/api/{self.token}'
  
    def send_message(self, chat_id, message):
        url = f'{self.base_url}/sendMessage'
        data = {'chat_id': chat_id, 'text': message}
        response = requests.post(url, data=data)
        return response.json()
  
    def send_photo(self, chat_id, photo_path, caption=None, date=None):
        url = f'{self.base_url}/sendPhoto'
        data = {'chat_id': chat_id}
        if caption:
            data['caption'] = caption
        if date:
            data['date'] = date
        with open(photo_path, 'rb') as photo_file:
            response = requests.post(url, data=data, files={'photo': photo_file})
        return response.json()
   
    def send_file(self, chat_id, file_path, title=None, caption=None, date=None):
        url = f'{self.base_url}/sendFile'
        data = {'chat_id': chat_id}
        files = {'file': open(file_path, 'rb')}
        if title:
            data['title'] = title
        if caption:
            data['caption'] = caption
        if date:
            data['date'] = date
        response = requests.post(url, data=data, files=files)
        return response.json()
    
    def send_document(self, chat_id, document_path, caption=None, date=None):
        url = f'{self.base_url}/sendDocument'
        data = {'chat_id': chat_id}
        if caption:
            data['caption'] = caption
        if date:
            data['date'] = date
        with open(document_path, 'rb') as document_file:
            response = requests.post(url, data=data, files={'document': document_file})
        return response.json()
   
    
    def get_bot_info(self):
        url = f'{self.base_url}/getMe'
        response = requests.get(url)
        return response.json()
   
    
    