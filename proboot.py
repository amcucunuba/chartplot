from openai import OpenAI
#mail: mfaliar.nutricion@gmail.com

client = OpenAI(
  api_key="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"
)

answ = client.chat.completions.create(
  model="gpt-4o-mini",
  max_tokens=100,
  messages=[
    {"role": "system", "content": "You are a 4ht grade teacher"},
    {"role": "user", "content": "Please explain the immigration in the world to a young student in three sentences"}
  ],
  temperature=0.7,
)

print('----------------')
print(f'Whole requet: {answ}')
print('----------------')
print(answ.choices[0].message.content)