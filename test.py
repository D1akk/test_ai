import g4f

def test(prompt:str)->str:
    response = g4f.ChatCompletion.create(
        model=g4f.models.gpt_35_turbo,
        messages=[{
            "role":"user",
            "content": prompt,
        }]
    )

    return response

print(test("Расскажи анекдот про якута"))