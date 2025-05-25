import openai

class LMStudioClient:
    """LM Studio APIクライアント"""

    def __init__(self, base_url, model_name):
        self.base_url = base_url
        self.model_name = model_name
        try:
            self.client = openai.OpenAI(base_url=self.base_url)
        except Exception as e:
            print(f"API接続エラー: {e}")
            raise
    
    def get_response(self, text: str):
        """APIを使って応答文を生成"""
        print(f"質問: {text}")
        try:
            messages = []        
            messages.append({"role": "user", "content": text})

            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages
            )
            response_text = response.choices[0].message.content
            messages.append({"role": "assistant", "content": response_text})
            print(response_text)
            return response_text
        except Exception as e:
            print(f"テキスト生成エラー: {e}")
            raise  # エラーを再発生させる
