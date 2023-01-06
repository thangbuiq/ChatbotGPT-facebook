import json
import aiohttp
import openai
import time
from os import environ
from aiohttp import web
# Set the API - OpenAI
openai.api_key = "HIDDEN"
# token
_PAGE_ACCESS_TOKEN = 'HIDDEN'
_VERIFY_TOKEN = 'HIDDEN'
# Choose the ChatGPT model
_model_engine = "text-davinci-002" #large ver or davinci-002
"""
text-davinci-002: A medium-sized version of ChatGPT with a capacity of around 1.5 billion parameters.
text-curie-001: A small version of ChatGPT with a capacity of around 500 million parameters.
text-babbage-001: A large version of ChatGPT with a capacity of around 3 billion parameters.
"""
def openaiGPT_request(question:str):
    response = openai.Completion.create(engine=_model_engine, prompt=question + ". trả lời ngắn gọn.", max_tokens=1024, n=1,stop=None,temperature=0.5)
    answer:str = "Câu trả lời chính thức của mình: \n" + response.choices[0].text
    return answer

class BotControl(web.View):
    async def get(self):
        query = self.request.rel_url.query
        if(query.get('hub.mode') == "subscribe" and query.get("hub.challenge")):
            if not query.get("hub.verify_token") == _VERIFY_TOKEN:
                return web.Response(text='Verification token mismatch', status=403)
            return web.Response(text=query.get("hub.challenge"))
        return web.Response(text='Forbidden', status=403)
    async def post(self):
        data = await self.request.json()
        if data.get("object") == "page":
            await self.send_greeting("Helu pé 🐄 Mình là bot trim non ụm pòa tạo bởi pa Théng nhí")
            for entry in data.get("entry"):
                for messaging_event in entry.get("messaging"):
                    if messaging_event.get("message"):
                        sender_id = messaging_event["sender"]["id"]
                        message_text = messaging_event["message"]["text"]
                        #max_money:int = 200000
                        #current_money:int = 0
                        if any(["chào" in message_text.lower(), "hello" in message_text.lower(), "nhô" in message_text.lower()]):
                            await self.send_message(sender_id, "chào pé iu cũa tớ 🐄")
                        elif any(["tên" in message_text.lower(),"name" in message_text.lower()]):
                            await self.send_message(sender_id, "mình tên là bot trimnon kute xicule xữa hột gè nha")
                        elif any(["eh" in message_text.lower(), "lô" in message_text.lower()]):
                            await self.send_message(sender_id, "kiu j đóa pò iu cũa pé")
                        else:
                            await self.send_message(sender_id, "cái nì trim hok bíc bạn đợi trim chút để trim nghiên cứu nhé!")
                            await self.send_message(sender_id, "đừng vội nhắn tin nhắn mới hãy đợi chút nhé")
                            await self.send_message(sender_id,"...")
                            await self.send_message(sender_id, openaiGPT_request(message_text))
                            await self.send_message(sender_id, "hy vọng bạn hài lòng với câu trả lời trên 🐮")
        return web.Response(text='ok', status=200)

    async def send_greeting(self, message_text):
        params = {
            "access_token": _PAGE_ACCESS_TOKEN
        }
        headers = {
            "Content-Type": "application/json"
        }
        data = json.dumps({
            "setting_type": "greeting",
            "greeting": {
                "text": message_text
            }
        })
        async with aiohttp.ClientSession() as session:
            await session.post("https://graph.facebook.com/v3.0/me/thread_settings", params=params, headers=headers, data=data)

    async def send_message(self, sender_id, message_text):

        params = {
            "access_token": _PAGE_ACCESS_TOKEN
        }
        headers = {
            "Content-Type": "application/json"
        }
        data = json.dumps({
            "recipient": {
                "id": sender_id
            },
            "message": {
                "text": message_text
            }
        })

        async with aiohttp.ClientSession() as session:
            await session.post("https://graph.facebook.com/v3.0/me/messages", params=params, headers=headers, data=data)



routes = [
    web.get('/', BotControl, name='verify'),
    web.post('/', BotControl, name='webhook'),
]

app = web.Application()
app.add_routes(routes)
#hi
#if __name__ == '__main__':
#   web.run_app(app, host='0.0.0.0', port=environ.get("PORT", 9090))
