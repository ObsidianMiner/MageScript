import json
import pyaudio
import speech_recognition as sr
from vosk import Model, KaldiRecognizer, SetLogLevel
from difflib import get_close_matches
from keywordGen import get_keywords, get_phrases


END_PHRASES = [
	"so it is written",
	"the spell is complete",
	"thus concludes the incantation",
	"let it be done"
]

MAGESCRIPT_PHRASES = get_phrases()

def boost_phrase_match(text, phrases, threshold=0.8):
	
	try:
		"""
		Attempt to auto-correct or boost low-confidence phrases
		using fuzzy matching from the phrase list.
		"""
		if not text:
			print("Could not get any text")
		words = text.split()
		corrected = []

		for i in range(len(words)):
			# Try 3-word phrases
			for span in range(3, 0, -1):
				chunk = " ".join(words[i:i+span])
				matches = get_close_matches(chunk, phrases, n=1, cutoff=threshold)
				if matches:
					corrected.append(matches[0])
					i += span - 1  # Skip matched words
					break
			else:
				corrected.append(words[i])
		
		return " ".join(corrected)
	except Exception as e:
		print(e)
		print("There was an error trying to fix up voice recognition problems...\ncontinuing without it")
	return text


lines = []
def setup_vos():
	MODEL_PATH = "vosk-model-en-us-0.22"
	SetLogLevel(0)
	model = Model(MODEL_PATH)

	grammar = f'["{" ".join(MAGESCRIPT_PHRASES)}", "[unk]"]'
	recognizer = KaldiRecognizer(model, 16000.0, grammar)
	p = pyaudio.PyAudio()
	stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
	stream.start_stream()
	return recognizer, stream

def listen_for_spell_vos():
	recognizer, stream = setup_vos()

	print("🎙️ Begin speaking your spell. Say 'retry' to re-enter the last line.")
	while True:
		data = stream.read(4000, exception_on_overflow=False)
		if recognizer.AcceptWaveform(data):
			res = json.loads(recognizer.Result())
			text = res.get("text", "").strip().lower()
			if not text:
				continue
			if text == "retry":
				if lines:
					print("↩ Line discarded. Please re-speak that line.")
					lines.pop()
				else:
					print("⇅ Nothing to retry yet.")
				continue
			
			text = boost_phrase_match(text, MAGESCRIPT_PHRASES)
			print("🗣️ You said:", text)
			lines.append(text)
			if any(ep in text for ep in END_PHRASES):
				print("🔮 Spell completed. Running the spell…")
				break
		else:
			partial = json.loads(recognizer.PartialResult()).get("partial", "")
			if partial:
				print("\r… " + partial, end="")
	return "\n".join(lines)

#region fallback recog
def listen_for_spell_reg():
	recognizer = sr.Recognizer()
	mic = sr.Microphone()
	
	recognizer.dynamic_energy_threshold = True
	recognizer.energy_threshold = 200

	with mic as source:
		print("🎙️ Adjusting to ambient noise...")
		recognizer.adjust_for_ambient_noise(source)
		print("🎙️ Listening for your incantation...")
		while(len(lines) == 0 or not any(phrase in lines for phrase in END_PHRASES)):
			line = listen_for_line_reg(recognizer, source)
			if line != None:
				lines.append(line)

	return None
def listen_for_line_reg(recognizer, source):
	#print("🎙️ Listening for line...")
	audio = recognizer.listen(source)
	try:
		text = recognizer.recognize_google(audio, language="en-US")
		print("🗣️ You said:", text)
		return text.lower()
	except sr.UnknownValueError:
		print("⚠️ The aether heard nothing intelligible.")
	except sr.RequestError:
		print("❌ Connection to the ether (Google) failed.")
#endregion

def speak_spell(assistedWithSpell: str = None):
	if assistedWithSpell:
		pass
	listen()
	spellFileName = "speached.spell"
	with open(spellFileName, "w") as f:
		f.write("\n".join(lines))

def listen():
	try:
		listen_for_spell_vos()
	except Exception as e:
		try:
			print(e)
			print("❌ Could not find vosk, or it had an error, switching to fallback reconizer...")
			listen_for_spell_reg()
		except:
			print("Neither speach recognizers work :(")

if __name__ == "__main__":
	print("runing...")
	speak_spell()