import requests


class Rubino:
    def __init__(self, token):
        self.token = token
        self.base_url = "https://abas-server.ir/rubino.php?user="
        self.token_verify_url = "https://token2.abas-server.ir/search_token.php?token="
    
    def verify_token(self):
        """توکن شما"""
        try:
            response = requests.get(f"{self.token_verify_url}{self.token}")
            data = response.json()
            return data.get('result') == 'ok'
        except Exception as e:
            print(f"خطا در بررسی توکن: {str(e)}")
            return False
    
    def get_user(self, username):
        """پارامتر ها :
        
        username: آبدی روبینو بدن @
        """
        if not self.verify_token():
            print(".توکن نامعتبر است!")
            return None
        
        try:
            response = requests.get(f"{self.base_url}{username}")
            data = response.json()
            
            if 'result' in data:
                result = data['result']
                print("="*40)
                print(f"نام: {result.get('name', '---')}")
                print(f"بیوگرافی: {result.get('bio', '---')}")
                print(f"تعداد دنبال‌کنندگان: {result.get('followers', 0)}")
                if 'profile_pic' in result:
                    print(f"\nلینک آواتار: {result['profile_pic']}")
                print("="*40)
                return result
            else:
                print("هیچ اطلاعاتی برای این کاربر یافت نشد")
                return None
        except Exception as e:
            print(f"خطا در دریافت اطلاعات: {str(e)}")
            return None
