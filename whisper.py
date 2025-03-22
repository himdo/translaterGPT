import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline

class SpeechRecognizer:
    def __init__(self, model_id="openai/whisper-large-v3-turbo"):
        self.device = "cuda:0" if torch.cuda.is_available() else "cpu"
        self.torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32
        self.model = AutoModelForSpeechSeq2Seq.from_pretrained(
            model_id, torch_dtype=self.torch_dtype, low_cpu_mem_usage=True, use_safetensors=True
        )
        self.processor = AutoProcessor.from_pretrained(model_id)
        self.pipe = pipeline(
            "automatic-speech-recognition",
            model=self.model,
            tokenizer=self.processor.tokenizer,
            feature_extractor=self.processor.feature_extractor,
            torch_dtype=self.torch_dtype,
            device=self.device,
        )

    def transcribe(self, audio_file_path):
        result = self.pipe(audio_file_path)
        return result["text"]

# Example usage
if __name__ == "__main__":
    recognizer = SpeechRecognizer()
    text = recognizer.transcribe("output.wav")
    print(text)