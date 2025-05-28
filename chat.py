from tools.perplexity import ask_perplexity
from tools.crt_sh import crt_sh_lookup

import signal
import os

from elevenlabs.client import ElevenLabs
from elevenlabs.conversational_ai.conversation import Conversation, ClientTools
from elevenlabs.conversational_ai.default_audio_interface import DefaultAudioInterface


# I don't believe in .get() when it comes to env vars.
# They should be there. Program needs to crash if they're not.
ELEVENLABS_API_KEY = os.environ["ELEVENLABS_API_KEY"]
# Provisionally agent_01jwc8eak8e0pb3d7wx6w0smjw but this should be a conscious
# choice just set the env var :p
AGENT_ID = os.environ["AGENT_ID"]

# Tool registration
client_tools = ClientTools()
client_tools.register("askPerplexity", ask_perplexity, is_async=True)
client_tools.register("crtShLookup", crt_sh_lookup, is_async=True)

conversation = Conversation(
    ElevenLabs(api_key=ELEVENLABS_API_KEY),
    AGENT_ID,
    requires_auth=bool(ELEVENLABS_API_KEY),
    audio_interface=DefaultAudioInterface(),
    client_tools=client_tools,
    callback_agent_response=lambda response: print(f"Agent: {response}"),
    callback_agent_response_correction=lambda original, corrected: print(f"Agent: {original} -> {corrected}"),
    callback_user_transcript=lambda transcript: print(f"User: {transcript}")
)

print("Starting conversation. Press Ctrl+C to exit.")
conversation.start_session()
# Kill chat on Ctrl+C
signal.signal(signal.SIGINT, lambda sig, frame: conversation.end_session())
conversation_id = conversation.wait_for_session_end()
print(f"Conversation ID: {conversation_id}")
