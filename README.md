## ElevenLabs Investigation Agent

![Discussing a predatory affiliate site](elevenlabs-chat.png)

Thrown together in an evening. Run the `chat.py` script to get an interactive terminal where you can talk to an ElevenLabs agent.

### Quickstart

```
python3 -m venv elevenlabs_agent_venv
```
```
source elevenlabs_agent_venv/bin/activate
```
```
pip install requirements.txt
```
```
python chat.py
```

### Tools

Via natural language conversation you have an agent that can do agentic web search with Perplexity and Certificate Transparency lookups via `crt.sh`. I would have done VirusTotal as well but it's time for bed.

A few things to note. Won't necessarily work immediately out the box. You'll need API keys for ElevenLabs, and if you want to use the Perplexity API tool you'll need one for that as well. Need to be set as env vars in the env you run

### Agent Configuration

You also need to set an env var for the agent ID. There's a code comment to guide you to the one I made, however consider whether you want to use it, that was made under my account in ElevenLabs, and you won't be able to edit it which may be irritating. If you want to make your own by all means! It's not difficult, only complexity to be aware of is that you need to make sure when you're defining an ElevenLabs ConversationalAI agent you add all of the tool you'd like it to be able to use, and by extension all the tools you register in the code, as _Client_ tools in the ElevenLabs web UI (I spent a while scratching my head wondering why my webhooks weren't working lol).