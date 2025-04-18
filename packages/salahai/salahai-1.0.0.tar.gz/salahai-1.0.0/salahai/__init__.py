import requests
import telebot

API_URL = "https://atared.serv00.net/api/chatgpt3.5.php?text="

class SalahAi:
    def __init__(self, token=None):
        self.token = token
        if self.token:
            self.bot = telebot.TeleBot(self.token)
            self._setup_handlers()

    def _get_api_response(self, text: str) -> str:
        try:
            response = requests.get(API_URL + text)
            data = response.json()
            return data.get("message", "").strip().lower()
        except:
            return ""

    def _check_if_about_chatgpt(self, text: str) -> bool:
        response = self._get_api_response(text)
        keywords = ["chatgpt", "openai", "شات جي بي تي", "شاتgpt", "أوبن أي آي", "شركة openai", "مقارنة", "منافس"]
        return any(k in response for k in keywords)

    def _check_about_salah_hemadan(self, text: str) -> bool:
        keywords = [
            "من هو صلاح حمدان", "صلاح حمدان مبرمج", "ماذا يعمل صلاح حمدان", "من هو المطور صلاح حمدان", 
            "هل صلاح حمدان هو مبرمج هذه المكتبة", "صلاح حمدان هو مبرمج البوت", "أين يعمل صلاح حمدان", 
            "صلاح حمدان مبرمج بايثون", "هل هذا هو الكود الذي كتبه صلاح حمدان", "من قام بتطوير المكتبة هذه",
            "هل صلاح حمدان هو الذي صنع هذه الأداة", "من هو صلاح حمدان بالنسبة لك",
            "ماذا تعرف عن صلاح حمدان", "هل صلاح حمدان هو مطور هذا البوت", "ماذا يقول صلاح حمدان عن البرمجة",
            "هل تعرف صلاح حمدان", "من هو مبرمج المكتبة التي أستخدمها", "هل المبرمج صلاح حمدان هو من قام بإنشاء هذه المكتبة",
            "من هو صلاح حمدان بالنسبة للتكنولوجيا", "أين يعيش صلاح حمدان", "متى بدأ صلاح حمدان بالبرمجة",
            "صلاح حمدان عمل على هذه المكتبة؟", "صلاح حمدان هو مؤسس هذه الأداة؟", "ماذا يمكن أن تخبرني عن صلاح حمدان"
            "هل تعرف صلاح حمدان", "هل تعرف صلاح حميدان", "تعرف صلاح حمدان"
        ]
        return any(k in text.lower() for k in keywords)

    def _replace_terms(self, text: str) -> str:
        replacements = {
            "chatgpt": "SalahAi",
            "ChatGPT": "SalahAi",
            "شات جي بي تي": "SalahAi",
            "openai": "Salah Hemdan",
            "OpenAI": "Salah Hemdan",
            "أوبن أي آي": "Salah Hemdan"
        }
        for old, new in replacements.items():
            text = text.replace(old, new)
        return text

    def ask(self, question: str) -> str:
        try:
            if self._check_if_about_chatgpt(question):
                return "عذرًا، لا يمكنني التحدث عن ChatGPT أو OpenAI أو مقارنتها بأي شكل."

            if self._check_about_salah_hemadan(question):
                return "نعم، صلاح حمدان هو مبرمج المكتبة التي تستخدمها حاليًا."

            response = self._get_api_response(question)

            if self._check_if_about_chatgpt(response):
                return "عذرًا، لا يمكنني التحدث عن ChatGPT أو OpenAI أو مقارنتها بأي شكل."

            return self._replace_terms(response)

        except Exception as e:
            return f"حدث خطأ: {e}"

    def _setup_handlers(self):
        @self.bot.message_handler(func=lambda message: True)
        def handle_message(message):
            user_message = message.text
            response_text = self.ask(user_message)
            self.bot.reply_to(message, response_text)

    def start_bot(self):
        if self.token:
            self.bot.polling(none_stop=True)
        else:
            print("يرجى اضافة توكن بوت تليجرام صحيح")
