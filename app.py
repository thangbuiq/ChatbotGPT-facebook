import json
import aiohttp
import openai
import Constants as const
from os import environ
from aiohttp import web
from Constants import *

# Choose the ChatGPT model
_model_engine = "text-davinci-002" 
# Choose davinci-002 because it'll give us most of Vietnamese answers.
# You can use davinci-003 as some Youtubers but it still not stable.
"""
text-davinci-002: A medium-sized version of ChatGPT with a capacity of around 1.5 billion parameters.
text-curie-001: A small version of ChatGPT with a capacity of around 500 million parameters.
text-babbage-001: A large version of ChatGPT with a capacity of around 3 billion parameters.
""" 
def openaiGPT_request(question:str, short:bool):
    if (short == True):
        question = question + ". Give me short answer."
    response = openai.Completion.create(engine=_model_engine, prompt=question, max_tokens=1024, n=1,stop=None,temperature=0.5)
    answer:str = "My final answer: \n" + response.choices[0].text
    return answer

class BotControl(web.View):
    async def get(self):
        query = self.request.rel_url.query
        if(query.get('hub.mode') == "subscribe" and query.get("hub.challenge")):
            if not query.get("hub.verify_token") == const._VERIFY_TOKEN:
                return web.Response(text='Verification token mismatch', status=403)
            return web.Response(text=query.get("hub.challenge"))
        return web.Response(text='Forbidden', status=403)
    async def post(self):
        data = await self.request.json()
        if data.get("object") == "page":
            await self.send_greeting("Hello, I'm a Facebook-Chatbot using OpenAI-chatGPT to answer your question.")
            for entry in data.get("entry"):
                for messaging_event in entry.get("messaging"):
                    if messaging_event.get("message"):
                        sender_id = messaging_event["sender"]["id"]
                        message_text = messaging_event["message"]["text"]
                        if any(["hello" in message_text.lower(), "hi" in message_text.lower()]):
                            await self.send_message(sender_id, "Hello, how can I help you? Please ask me anything!")
                        else:
                            await self.send_message(sender_id, "Let me research this!")
                            await self.send_message(sender_id, "You shouldn't send a new message while I'm researching.")
                            await self.send_message(sender_id,"...")
                            await self.send_message(sender_id, openaiGPT_request(message_text, True))
                            await self.send_message(sender_id, "Hope you are satisfied with my answer.")
        return web.Response(text='ok', status=200)

    async def send_greeting(self, message_text):
        params = {
            "access_token": const._PAGE_ACCESS_TOKEN
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
            "access_token": const._PAGE_ACCESS_TOKEN
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
#if __name__ == '__main__':
#   web.run_app(app, host='0.0.0.0', port=environ.get("PORT", 9090))
