import facebook
import json
from datetime import datetime
from collections import defaultdict

import pandas as pd

class FacebookCollector():
    def __init__(self, access_token):
        try:
            self.access_token = access_token
            self.graph = facebook.GraphAPI(access_token)
        except Exception as e:
            print(f"Loi khoi tao: {e}")
    
    def check_token_validity(self):
        try:
            me = self.graph.get_object('me', fields='id,name')
            print('Token hop le')
            return True
        except Exception:
            print("Token khong hop le")
            return False
        
    def collect_data(self, limit=5):
        try:
            # Khai bao fields
            fields = (
                'id'
                ',message'
                ',created_time'
                ',comments.limit(100).summary(true)'
                '{created_time,from{id,name},message,reactions}'
                ',reactions.limit(100).summary(true)'
                '{id,type,name}'
                ',shares'
                ',type'
            )
            # Lay bai viet
            posts = self.graph.get_object('me/feed')

            # Debug bai post dau tien
            for post in posts.get('data', []):
                print("-------------------------")
                print(post.get('message'))
                print("-------------------------")

            return posts

        except Exception:
            pass
        
    def to_excel(self, data, excel_file=None):
        posts = []
        for post in data.get('data', []):
            post_data = {
                'id': post.get('id', ''),
                'create_time': post.get('created_time', ''),
                'message': post.get('message', '')
            }
            posts.append(post_data)

        # Chuyen thanh DataFrame
        df = pd.DataFrame(posts)

        # Chuyen doi created_time sang dinh dang datetime
        df['created_time'] = pd.to_datetime(df['created_time'])

        # Format cho de doc
        df['created_time'] = df['created_time'].dt.strftime('%Y-%m-%d %H:%M:%S')

        # Tao ten file excel neu khong duoc cung cap
        if not excel_file:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            excel_file = f"facebook_posts_{timestamp}.xlsx"

        df.to_excel(excel_file, index=False)

        return excel_file
def main():
    ACCESS_TOKEN = 'EAAP4N1WbyZCkBO7ZB7wMHvfMySwhWH55bVK6uuBzS1xZAaWJAjzXHvmUc2Uc3LzLhoA6kkY3W9t5kl9hi8dmyAVzDOVYBcVZA1FJifGCmDFI6HjBEefZAR0mkcclbfIYNJN0kEFvtofSYP5BGu3eyYZBG0WVvuI58024EGckVZBZAZAh2HjPq5NFpWBI6FUV2V9ZCx8p6w70nr2aLcJeVsEMYauvzVp4X56LeTvAZDZD'
    collector = FacebookCollector(ACCESS_TOKEN)

    if collector.check_token_validity():
        data = collector.collect_data(limit=2)
        collector.to_excel(data)

if __name__== "__main__":
    main()