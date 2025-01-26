# WebGPTVoiceAssistant
WebGPTVoiceAssistant is a voice-activated assistant that leverages real-time data from the Google Custom Search Engine. Powered by OpenAI's GPT and Whisper APIs, this project is designed to run seamlessly on both a Raspberry Pi 4 and macOS.

## Virtual Environoment (Optional)
To ensure a clean and isolated environment, it is recommended to set up a virtual environment for Python. Use the following commands in the terminal:
```bash
pip install virtualenv
python3 -m venv myvenv
```

## Installation
Before running the assistant, you need to install `portaudio19-dev`, `mpg123` and `flac`. Activate the virtual environment and install the required libraries from `requirements.txt` using the following commands:
```bash
sudo apt install portaudio19-dev
sudo apt install mpg123
sudo apt install flac

source myvenv/bin/activate
pip install -r requirements.txt
```

## Usage
To use WebGPTVoiceAssistant, set the required API keys as environment variables in the terminal. Obtain your API keys from the following sources:
- [OpenAI API Key](https://platform.openai.com/account/api-keys)
- [Google CSE API Key](https://programmablesearchengine.google.com/controlpanel/all)
- [Google CSE Id](https://developers.google.com/custom-search/v1/introduction)

Once you have your API keys, export them as environment variables using the following commands in the terminal:
```bash
export OPENAI_API_KEY='[your-key]'
export GOOGLE_CSE_API_KEY='[your-key]'
export GOOGLE_CSE_ID='[your-key]'
```

After setting up the environment variables, run the assistant in the terminal with the following command:
```bash
python3 main.py
```

## Done !
Enjoy the seamless integration of voice commands and real-time Google Custom Search Engine data retrieval with WebGPTVoiceAssistant on your Raspberry Pi 4 or macOS device.

## Any Questions or Issues?
Feel free to ask any questions at [my website](https://haavishbonala.github.io/) or report issues in the Issues section. I appreciate your feedback and contributions to make WebGPTVoiceAssistant even better!
