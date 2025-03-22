from kokoro import KPipeline
import soundfile as sf

class TTSModel:
    # Mapping of voices to their details
    VOICE_DETAILS = {
        "af_heart": {
            "lang_code": "a",
            "traits": ["female", "❤️"],
            "target_quality": "",
            "training_duration": "",
            "overall_grade": "A"
        },
        "af_alloy": {
            "lang_code": "a",
            "traits": ["female"],
            "target_quality": "B",
            "training_duration": "MM minutes",
            "overall_grade": "C"
        },
        "af_aoede": {
            "lang_code": "a",
            "traits": ["female"],
            "target_quality": "B",
            "training_duration": "H hours",
            "overall_grade": "C+"
        },
        "af_bella": {
            "lang_code": "a",
            "traits": ["female", "🔥"],
            "target_quality": "A",
            "training_duration": "HH hours",
            "overall_grade": "A-"
        },
        "af_jessica": {
            "lang_code": "a",
            "traits": ["female"],
            "target_quality": "C",
            "training_duration": "MM minutes",
            "overall_grade": "D"
        },
        "af_kore": {
            "lang_code": "a",
            "traits": ["female"],
            "target_quality": "B",
            "training_duration": "H hours",
            "overall_grade": "C+"
        },
        "af_nicole": {
            "lang_code": "a",
            "traits": ["female", "🎧"],
            "target_quality": "B",
            "training_duration": "HH hours",
            "overall_grade": "B-"
        },
        "af_nova": {
            "lang_code": "a",
            "traits": ["female"],
            "target_quality": "B",
            "training_duration": "MM minutes",
            "overall_grade": "C"
        },
        "af_river": {
            "lang_code": "a",
            "traits": ["female"],
            "target_quality": "C",
            "training_duration": "MM minutes",
            "overall_grade": "D"
        },
        "af_sarah": {
            "lang_code": "a",
            "traits": ["female"],
            "target_quality": "B",
            "training_duration": "H hours",
            "overall_grade": "C+"
        },
        "af_sky": {
            "lang_code": "a",
            "traits": ["female"],
            "target_quality": "B",
            "training_duration": "M minutes 🤏",
            "overall_grade": "C-"
        },
        "am_adam": {
            "lang_code": "a",
            "traits": ["male"],
            "target_quality": "D",
            "training_duration": "H hours",
            "overall_grade": "F+"
        },
        "am_echo": {
            "lang_code": "a",
            "traits": ["male"],
            "target_quality": "C",
            "training_duration": "MM minutes",
            "overall_grade": "D"
        },
        "am_eric": {
            "lang_code": "a",
            "traits": ["male"],
            "target_quality": "C",
            "training_duration": "MM minutes",
            "overall_grade": "D"
        },
        "am_fenrir": {
            "lang_code": "a",
            "traits": ["male"],
            "target_quality": "B",
            "training_duration": "H hours",
            "overall_grade": "C+"
        },
        "am_liam": {
            "lang_code": "a",
            "traits": ["male"],
            "target_quality": "C",
            "training_duration": "MM minutes",
            "overall_grade": "D"
        },
        "am_michael": {
            "lang_code": "a",
            "traits": ["male"],
            "target_quality": "B",
            "training_duration": "H hours",
            "overall_grade": "C+"
        },
        "am_onyx": {
            "lang_code": "a",
            "traits": ["male"],
            "target_quality": "C",
            "training_duration": "MM minutes",
            "overall_grade": "D"
        },
        "am_puck": {
            "lang_code": "a",
            "traits": ["male"],
            "target_quality": "B",
            "training_duration": "H hours",
            "overall_grade": "C+"
        },
        "am_santa": {
            "lang_code": "a",
            "traits": ["male"],
            "target_quality": "C",
            "training_duration": "M minutes 🤏",
            "overall_grade": "D-"
        },
        'bf_alice': {
            'lang_code': 'b',  # British English
            'target_quality': 'C',
            'traits': ['female'],
            'training_duration': 'MM minutes',
            'overall_grade': 'D'
        },
        'bf_emma': {
            'lang_code': 'b',  # British English
            'target_quality': 'B',
            'traits': ['female'],
            'training_duration': 'HH hours',
            'overall_grade': 'B-'
        },
        'bf_isabella': {
            'lang_code': 'b',  # British English
            'target_quality': 'B',
            'traits': ['female'],
            'training_duration': 'MM minutes',
            'overall_grade': 'C'
        },
        'bf_lily': {
            'lang_code': 'b',  # British English
            'target_quality': 'C',
            'traits': ['female'],
            'training_duration': 'MM minutes',
            'overall_grade': 'D'
        },
        'bm_daniel': {
            'lang_code': 'b',  # British English
            'target_quality': 'C',
            'traits': ['male'],
            'training_duration': 'MM minutes',
            'overall_grade': 'D'
        },
        'bm_fable': {
            'lang_code': 'b',  # British English
            'target_quality': 'B',
            'traits': ['male'],
            'training_duration': 'MM minutes',
            'overall_grade': 'C'
        },
        'bm_george': {
            'lang_code': 'b',  # British English
            'target_quality': 'B',
            'traits': ['male'],
            'training_duration': 'MM minutes',
            'overall_grade': 'C'
        },
        'bm_lewis': {
            'lang_code': 'b',  # British English
            'target_quality': 'C',
            'traits': ['male'],
            'training_duration': 'H hours',
            'overall_grade': 'D+'
        },
        'jf_alpha': {
            'lang_code': 'j',  # Japanese
            'traits': ['female'],
            'target_quality': 'B',
            'training_duration': 'H hours',
            'overall_grade': 'C+'
        },
        'jf_gongitsune': {
            'lang_code': 'j',  # Japanese
            'traits': ['female'],
            'target_quality': 'B',
            'training_duration': 'MM minutes',
            'overall_grade': 'C'
        },
        'jf_nezumi': {
            'lang_code': 'j',  # Japanese
            'traits': ['female'],
            'target_quality': 'B',
            'training_duration': 'M minutes 🤏',
            'overall_grade': 'C-'
        },
        'jf_tebukuro': {
            'lang_code': 'j',  # Japanese
            'traits': ['female'],
            'target_quality': 'B',
            'training_duration': 'MM minutes',
            'overall_grade': 'C'
        },
        'jm_kumo': {
            'lang_code': 'j',  # Japanese
            'traits': ['male'],
            'target_quality': 'B',
            'training_duration': 'M minutes 🤏',
            'overall_grade': 'C-'
        },
        # Add more voices with their details here
    }

    def __init__(self, voice='af_heart'):
        if voice in self.VOICE_DETAILS:
            self.voice = voice
            self.lang_code = self.VOICE_DETAILS[voice]['lang_code']
            self.pipeline = KPipeline(lang_code=self.lang_code)
        else:
            raise ValueError(f"Unknown voice: {voice}")

    def set_voice(self, voice):
        """Set the voice and automatically update the language code."""
        if voice in self.VOICE_DETAILS:
            self.voice = voice
            self.lang_code = self.VOICE_DETAILS[voice]['lang_code']
            self.pipeline = KPipeline(lang_code=self.lang_code)
        else:
            raise ValueError(f"Unknown voice: {voice}")

    def get_voice_details(self, voice):
        """Return details of a specific voice."""
        if voice in self.VOICE_DETAILS:
            return self.VOICE_DETAILS[voice]
        else:
            raise ValueError(f"Unknown voice: {voice}")

    def get_all_voices(self):
        """Return a list of all known voices."""
        return list(self.VOICE_DETAILS.keys())

    def generate_audio(self, text, output_dir='./'):
        """
        Generate audio from the given text and save it as WAV files.

        :param text: The input text for TTS.
        :param output_dir: Directory where the WAV files will be saved (default is current directory).
        """
        generator = self.pipeline(text, voice=self.voice)
        for i, (gs, ps, audio) in enumerate(generator):
            print(f"Generating file {i} with GS: {gs}, PS: {ps}")
            output_path = f"{output_dir}/{i}.wav"
            sf.write(output_path, audio, 24000)
            print(f"Saved to {output_path}")

# Example usage (you can remove this part for the module itself)
if __name__ == "__main__":
    tts = TTSModel(voice='af_heart')
    text = "Hello, welcome to the Text-to-Speech system."
    tts.generate_audio(text, output_dir='./output')

    # Get all known voices
    print("Known Voices:", tts.get_all_voices())

    # Get details of a specific voice
    voice_details = tts.get_voice_details('bf_alice')
    print(f"Details for bf_alice: {voice_details}")

    # Change to another voice
    tts.set_voice('jf_alpha')
    text_jp = "こんにちは、テキストツーポーカーシステムへようこそ。"
    tts.generate_audio(text_jp, output_dir='./output')

    # Get details of the current voice
    current_voice_details = tts.get_voice_details(tts.voice)
    print(f"Details for current voice ({tts.voice}): {current_voice_details}")