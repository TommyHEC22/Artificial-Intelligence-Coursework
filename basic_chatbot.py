import re
import json
import os
import random

MEMORY_FILE = "memory.json"

VOCAB = {
    "what","is","ai","artificial","intelligence","will","take","my","job",
    "intelligent","agent","agents","how","used","world","hello","hi","hey",
    "help","explain","name","thanks","bye","goodbye","examples","code",
    "takeover","scared","worried","fear","sad","angry","happy"
}

KB = {
    "what_is_ai": [
        "AI is software that can learn patterns from data and uses it to make predictions or decisions. It isnt some which craft and is not magic — just maths and training on data.",
        "AI is systems that can recognise patterns, reason, or make choices based on data that has been fed into it for it to learn from. Think of it like giving a computer the ability to notice patterns."
    ],
    "will_ai_take_my_job": [
        "Alot of tasks can get automated, but most jobs change rather than disappear completely. People who learn to use AI usually become more valuable to the companies they work for.",
        "AI replaces repetitive and monotanous tasks, not entire people. Your creativity and judgement still matter massively and it will only be jobs you dont want to do because theyre too boring that it can take over."
    ],
    "intelligent_agents": [
        "An intelligent agent observes and sees the world, makes a decision, and acts. Virtual assistants and robots are classic examples.",
        "They follow a loop: sense → think → act. Very similar to how we would approach tackling a task."
    ],
    "ai_takeover_claim": [
        "Nah, AI isn't close to that level. It's powerful but not anywhere near clever enough (yet!). It can't form intentions or goals on its own wothout someone setting them.",
        "Most 'AI takeover' stuff is sci-fi. Real systems are specialised and depend fully on human direction. Alot have systems in place to prevent these things from happening"
    ],
}

EMOTIONS = {
    "happy": ["happy","glad","great","excited","pleased"],
    "sad": ["sad","down","unhappy","depressed"],
    "angry": ["angry","furious","annoyed","frustrated"],
    "fear": ["scared","afraid","worried","anxious","concerned"],
    "neutral": []
}

QUIZ = [
    {
        "q": "What does 'AI' stand for?",
        "opts": ["a) Automated Internet", "b) Artificial Intelligence", "c) Active Interface"],
        "ans": "b"
    },
    {
        "q": "What does LLM stand for in AI?",
        "opts": ["a) Large Languagey Modem", "b) Lazy Language Model", "c) Large Language Model"],
        "ans": "c"
    },
    {
        "q": "Levenshtein edit distance measures:",
        "opts": ["a) The length of a text", "b) Minimum character edits between strings", "c) Computational Cost of an algorithm"],
        "ans": "b"
    }
]

def play_quiz():

    print("\nAlright, quick 3-question quiz. Answer with a, b or c. Or you can just say quit if you dont want to bother")
    score = 0

    for i, item in enumerate(QUIZ, start=1):
        print(f"\nQuestion {i}: {item['q']}")

        for o in item["opts"]:
            print("   ", o)

        while True:
            answer = input("You: ").strip().lower()

            if answer == "quit":
                print("Quiz stopped. Your score:", score, "out of 3")
                return
            
            if answer[0] in ("a","b","c"):

                if answer[0] == item["ans"]:
                    print("Nice — that's correct.")
                    score = score + 1

                else:
                    print(f"Not quite. The correct answer was '{item['ans']}'.")
                break

            else:
                print("Please answer with a, b or c (or 'quit').")

    print("\nDone. Your final score:", score, "out of 3")

    return

GREETINGS = ["Hi", "Hello", "Hey"]
FALLBACKS = [
    "chat like that just doesnt tickle my brain. Ask me a question about AI, i'm fascinated by AI right now so ask me about that",
    "forget all that, you want to do a quiz about AI? If you do just say quiz or play quix or something like that",
    "dude, just ask me about ai or say quiz to play a game."
]


def load_memory():
    if os.path.exists(MEMORY_FILE): 
        try:                 
            return json.load(open(MEMORY_FILE, "r", encoding="utf-8")) 
        except: 
            return {} 
    return {}

def save_memory(mem):
    json.dump(mem, open(MEMORY_FILE, "w", encoding="utf-8"), indent=2)


def normalize(text):
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9'\s]", " ", text)
    return re.sub(r"\s+", " ", text)


def tokenize(text):
    return normalize(text).split()


def edit_distance(a, b):

    la, lb = len(a), len(b)
    if a == b: 
        return 0
    if la == 0: 
        return lb
    if lb == 0: 
        return la

    dp = [[0]*(lb+1) for _ in range(la+1)]
    for i in range(la+1): dp[i][0] = i
    for j in range(lb+1): dp[0][j] = j

    for i in range(1, la+1):
        for j in range(1, lb+1):
            cost = 0 if a[i-1] == b[j-1] else 1
            dp[i][j] = min(dp[i-1][j] + 1, dp[i][j-1] + 1, dp[i-1][j-1] + cost)

    return dp[la][lb]


def correct_token(token, vocab=VOCAB, thresh=2):
    if token in vocab:
        return token
    
    best = token
    best_dist = 999

    for v in vocab:
        d = edit_distance(token, v)
        if d < best_dist:
            best_dist = d
            best = v

    return best if best_dist <= thresh else token


def preprocess(text):

    tokens = tokenize(text)
    corrected = [correct_token(t) for t in tokens]
    return " ".join(corrected)


def detect_intents(text):
    t = text.lower()
    intents = []
    if "what is ai" in t or "what ai" in t:
        intents.append("what_is_ai")
    if "take my job" in t or "will ai take" in t:
        intents.append("will_ai_take_my_job")
    if "intelligent agent" in t or "intelligent agents" in t:
        intents.append("intelligent_agents")
    if "take over the world" in t or "ai takeover" in t:
        intents.append("ai_takeover_claim")
    if any(g in t for g in ["hello","hi","hey"]):
        intents.append("greeting")

    if "quiz" in t or "play quiz" in t or "play a quiz" in t:
        intents.append("play_quiz")
    return intents


def detect_emotion(text):
    t = normalize(text)
    counts = {k: 0 for k in EMOTIONS}
    for emo, words in EMOTIONS.items():
        for w in words:
            if re.search(r"\b" + w + r"\b", t):
                counts[emo] += 1
    top = max(counts.items(), key=lambda x: x[1])
    return top[0] if top[1] > 0 else "neutral"


def reply_prefix(memory):
    name = memory.get("name")
    if name:
        return f"{name}, "
    return ""


def generate_response(user_text, memory):

    clean = preprocess(user_text)
    intents = detect_intents(clean)
    emotion = detect_emotion(user_text)

    if emotion != "neutral":

        memory["last_emotion"] = emotion

    if not memory.get("name"):
        name_match = None
        
        patterns = [
            r"\bmy name is ([a-z]{2,})\b",
            r"\bmy name's ([a-z]{2,})\b",
            r"\bcall me ([a-z]{2,})\b",
            r"\bi am ([a-z]{2,})\b",
            r"\bi'm ([a-z]{2,})\b"
        ]
        
        for pat in patterns:
            m = re.search(pat, clean)
            if m:
                name_match = m.group(1)
                break
        if name_match:
            memory["name"] = name_match.capitalize()

    prefix = reply_prefix(memory)

    if "play_quiz" in intents:
        return "__PLAY_QUIZ__", memory

    if "greeting" in intents:
        return f"{prefix}{random.choice(GREETINGS)} — what's on your mind?", memory

    for intent in intents:
        if intent in KB:
            resp = random.choice(KB[intent])
            if emotion == "fear":
                resp += " And don't worry — none of this is as scary as headlines make it look."
            return prefix + resp, memory

    if emotion != "neutral":
        return prefix + f"I can't fully answer that, but you sound a bit {emotion}. Want to tell me more?", memory

    return prefix + random.choice(FALLBACKS), memory


def main():
    memory = load_memory()

    if memory.get("name"):
        print(f"Hey {memory['name']}, what's up?")
    else:
        print("Hey — what's your name?")

    while True:
        user = input("\nYou: ").strip()
        if user.lower() in ["bye","exit","quit"]:
            print("Alright, take care.")
            save_memory(memory)
            break

        response, memory = generate_response(user, memory)
        save_memory(memory)

        if response == "__PLAY_QUIZ__":
            play_quiz()
            continue

        print(response)


main()
