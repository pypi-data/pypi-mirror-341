import requests

class Digikala:
    def __init__(self, token):
        self.token = token
        self.api_url = "https://abas-server.ir/diji.php"
        self.token_verify_url = "https://token2.abas-server.ir/search_token.php?token="
    
    def verify_token(self):
        """توکن"""
        try:
            response = requests.get(f"{self.token_verify_url}{self.token}")
            data = response.json()
            return data.get('result') == 'ok'
        except Exception as e:
            print(f"خطا در بررسی توکن: {str(e)}")
            return False
    
    def search(self, query):
        """
    جستجوی محصول در دیجی‌کالا 
        
        پارامترها:
            query: عبارت جستجو
        """
        if not self.verify_token():
            print("توکن نامعتبر است یا خطایی رخ داده است!")
            return None
            
        try:
         
            response = requests.get(
                self.api_url,
                params={
                    "q": query,
                    "token": self.token
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "success":
                    result = data.get("result")
                    
                  
                    if result:
                        print("\nنتایج جستجو در دیجی‌کالا:")
                        print("="*40)
                        print(f"📦 نام محصول: {result.get('name', '---')}")
                        print(f"💶 قیمت: {result.get('price', 0):,} تومان")
                        print(f"📎 لینک: {result.get('url', '---')}")
                        print("="*40)
                        return result
                    
            print("نتیجه‌ای یافت نشد")
            return None
            
        except Exception as e:
            print(f"خطا در جستجو: {str(e)}")
            return None

