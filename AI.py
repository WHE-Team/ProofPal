
import os
from openai import OpenAI


os.environ['OPENAI_API_KEY'] = ''

client = OpenAI(
    api_key="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",
)

def analyze_homework(content, goal):
    prompts = "This goal is:" + goal + "Has this homework alined with the goal? Say yes or no. Only say a single yes or no."

    response = client.chat.completions.create(
        messages=[{"role": "system", "content": prompts},
                    {"role": "user", "content": content}],
        model="gpt-3.5-turbo",
        temperature=0,
    )
    resp = response.choices[0].message.content.lower()
    if "yes" in resp:
        return True
    elif "no" in resp:
        return False
    else:
        print("SMTH HAPPENED:", resp)
        return False
    

content = "Elimina quickly adapts to the harsh realities of the academy, despite the difficulties she faced due to her upbringing. As Elimina was nurtured and nourished by modern ideals, she experienced great emotional distress being incorporated into the gutter system, namely denial and depression, both classic stages of grief. As Elimina is led through the academy, she retorts “I don’t belong here. You’re all … I’m not … I’m not a Gutter Child”, and later in her room “‘I don’t want to be here’ I say, crying into my arms to muffle the sound” (Richerson, Gutter Child 8, 44). Denying the reality, Elimina tells both herself and others that she doesn't belong in the academy; when she finally realizes the inevitable, the weight of it crushes her, sending her into a depressive state. However, she is determined to survive and gain back the freedom she so desperately wants back. In fact, she establishes this at the very start of the book, stating “happiness isn’t something a kid like me can afford to hold out for” and later on, “‘It will take time,’ she says. ‘And if you want to make it happen, you’re going to have to suffer a little. But I never knew anything good that didn’t come without a bit of hurt.’ ‘I’m ready,’ I say” (4, 60). As one can see, Elimina is indirectly showing her resolve to survive here in the first quote, then in the second actively choosing her freedom and survival as her priority, as well as readying herself for the future. The fruits of Elimina’s effects would later ripen, giving way to her success, as some would call it. After leashing a child, Elimina observes: “I find Louis watching me, smiling and nodding his approval, as though I’ve finally earned his respect”. Moreover, Mabel Freeman promises her a position at the hill: “you’re going to hire me? I say, and when she nods….” (87, 113). With both a place in the academy and a job secure, Elimina is elevated to an extremely favorable position under her extremely unfavorable situation; Elimina, faced with hardships and grief, carried through with determination, even thrives by relinquishing her morals as a necessity to survive and gain freedom; though she would later abandon this objective for another."
goal = " reach 200 words"
print(analyze_homework(content, goal))