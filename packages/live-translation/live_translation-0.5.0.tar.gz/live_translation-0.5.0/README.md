# Real-time Speech-to-Text Translation

This project provides a real-time speech-to-text translation system built on a modular server–client architecture.

- The **client** streams microphone audio to the server and receives structured results in real time over a full-duplex WebSocket.
- The **server** performs transcription using **Whisper** and optional translation using **Opus-MT**, with **Silero VAD** for voice activity detection.
- Transcription and translation results are returned to the client in real time.
- The server can optionally log results to stdout or a **JSONL** file.

The program can be used both as a **command-line tool** or as a **Python API** in other applications, with full support for non-blocking and asynchronous workflows.

#### 🖥️🌍 Server-Client Demo

<a href="https://github.com/AbdullahHendy/live-translation/blob/main/doc/demo.gif?raw=true" target="_blank">
  <img src="https://github.com/AbdullahHendy/live-translation/blob/main/doc/demo.gif?raw=true" alt="Server-Client Demo" />
</a>

## Architecture Overview
<img src="https://github.com/AbdullahHendy/live-translation/blob/main/doc/live-translation-pipeline.png?raw=true" alt="Architecture Diagram" />


## Features

- Real-time speech capture using **PyAudio**
- Voice Activity Detection (VAD) using **Silero** for more efficient processing
- Speech-to-text transcription using OpenAI's **Whisper**
- Translation of transcriptions using Helsinki-NLP's **OpusMT**
- **Full-duplex WebSocket streaming** between client and server
- Multithreaded design for parallelized processing
- Optional server logging:
  - Print to **stdout**
  - Save transcription/translation logs to a structured **.jsonl** file
- Designed for both:
  - Simple **CLI** usage (***live-translate-server***, ***live-translate-client***)
  - **Python API** usage (***LiveTranslationServer***, ***LiveTranslationClient***) with Asynchronous support for embedding in larger systems
## Prerequisites

Before running the project, you need to install the following system dependencies:

- **PortAudio** (for audio input handling)
- **FFmpeg** (for audio and video processing)
    - On Ubuntu/Debian-based systems, you can install it with:
      ```bash
      sudo apt-get install portaudio19-dev ffmpeg
      ```

## Installation

**(RECOMMENDED)**: install this package inside a virtual environment to avoid dependency conflicts.
```bash
python -m venv .venv
source .venv/bin/activate
```

**Install** the [PyPI package](https://pypi.org/project/live-translation/):
```bash
pip install live-translation
```

**Verify** the installation:
```bash
python -c "import live_translation; print(f'live-translation installed successfully\n{live_translation.__version__}')"
```

## Usage

> **NOTE**: One can safely ignore similar warnings that might appear on **Linux** systems when running the client as it tries to open the mic:
>
> ALSA lib pcm_dsnoop.c:567:(snd_pcm_dsnoop_open) unable to open slave
> ALSA lib pcm_dmix.c:1000:(snd_pcm_dmix_open) unable to open slave
> ALSA lib pcm.c:2722:(snd_pcm_open_noupdate) Unknown PCM cards.pcm.rear
> ALSA lib pcm.c:2722:(snd_pcm_open_noupdate) Unknown PCM cards.pcm.center_lfe
> ALSA lib pcm.c:2722:(snd_pcm_open_noupdate) Unknown PCM cards.pcm.side
> ALSA lib pcm_dmix.c:1000:(snd_pcm_dmix_open) unable to open slave
> Cannot connect to server socket err = No such file or directory
> Cannot connect to server request channel
> jack server is not running or cannot be started
> JackShmReadWritePtr::~JackShmReadWritePtr - Init not done for -1, skipping unlock
> JackShmReadWritePtr::~JackShmReadWritePtr - Init not done for -1, skipping unlock
>

### CLI 
* **server** can be run directly from the command line:
  ```bash
  live-translate-server [OPTIONS]
  ```

  **[OPTIONS]**
  ```bash
  usage: live-translate-server [-h] [--silence_threshold SILENCE_THRESHOLD] [--vad_aggressiveness {0,1,2,3,4,5,6,7,8,9}] [--max_buffer_duration {5,6,7,8,9,10}] [--device {cpu,cuda}]
                              [--whisper_model {tiny,base,small,medium,large,large-v2,large-v3,large-v3-turbo}] [--trans_model {Helsinki-NLP/opus-mt,Helsinki-NLP/opus-mt-tc-big}]
                              [--src_lang SRC_LANG] [--tgt_lang TGT_LANG] [--log {print,file}] [--ws_port WS_PORT] [--transcribe_only] [--version]

  Live Translation Server - Configure runtime settings.

  options:
    -h, --help            show this help message and exit
    --silence_threshold SILENCE_THRESHOLD
                          Number of consecutive 32ms silent chunks to detect SILENCE.
                          SILENCE clears the audio buffer for transcription/translation.
                          NOTE: Minimum value is 16.
                          Default is 65 (~ 2s).
    --vad_aggressiveness {0,1,2,3,4,5,6,7,8,9}
                          Voice Activity Detection (VAD) aggressiveness level (0-9).
                          Higher values mean VAD has to be more confident to detect speech vs silence.
                          Default is 8.
    --max_buffer_duration {5,6,7,8,9,10}
                          Max audio buffer duration in seconds before trimming it.
                          Default is 7 seconds.
    --device {cpu,cuda}   Device for processing ('cpu', 'cuda').
                          Default is 'cpu'.
    --whisper_model {tiny,base,small,medium,large,large-v2,large-v3,large-v3-turbo}
                          Whisper model size ('tiny', 'base', 'small', 'medium', 'large', 'large-v2', 'large-v3', 'large-v3-turbo). 
                          NOTE: Running large models like 'large-v3', or 'large-v3-turbo' might require a decent GPU with CUDA support for reasonable performance. 
                          NOTE: large-v3-turbo has great accuracy while being significantly faster than the original large-v3 model. see: https://github.com/openai/whisper/discussions/2363 
                          Default is 'base'.
    --trans_model {Helsinki-NLP/opus-mt,Helsinki-NLP/opus-mt-tc-big}
                          Translation model ('Helsinki-NLP/opus-mt', 'Helsinki-NLP/opus-mt-tc-big'). 
                          NOTE: Don't include source and target languages here.
                          Default is 'Helsinki-NLP/opus-mt'.
    --src_lang SRC_LANG   Source/Input language for transcription (e.g., 'en', 'fr').
                          Default is 'en'.
    --tgt_lang TGT_LANG   Target language for translation (e.g., 'es', 'de').
                          Default is 'es'.
    --log {print,file}    Optional logging mode for saving transcription output.
                            - 'file': Save each result to a structured .jsonl file in ./transcripts/transcript_{TIMESTAMP}.jsonl.
                            - 'print': Print each result to stdout.
                          Default is None (no logging).
    --ws_port WS_PORT     WebSocket port the of the server.
                          Used to listen for client audio and publishe output (e.g., 8765).
    --transcribe_only     Transcribe only mode. No translations are performed.
    --version             Print version and exit.
  ```

* **client** can be run directly from the command line:
  ```bash
  live-translate-client [OPTIONS]
  ```

  **[OPTIONS]**
  ```bash
  usage: live-translate-client [-h] [--server SERVER] [--version]

  Live Translation Client - Stream audio to the server.

  options:
    -h, --help       show this help message and exit
    --server SERVER  WebSocket URI of the server (e.g., ws://localhost:8765)
    --version        Print version and exit.
  ```

### API
You can also import and use ***live_translation*** directly in your Python code.
The following is ***simple*** examples of running ***live_translation***'s server and client in a **blocking** fashion.
For more detailed examples showing **non-blocking** and **asynchronous** workflows, see [examples/](/examples/).

> **NOTE**: The examples below assumes the ***live_translation*** package has been installed as shown in the [Installation](#installation).
>
> **NOTE**: One can run a provided example in [examples/](./examples/) as **`python -m examples.<example_name>`**. For example: **`python -m examples.magic_word`** 
> Running the example this way from inside the repository assume a development environment has been set up, see [## Development & Contribution](#development--contribution) in the next section.
>

- **Server**
  ```python
  from live_translation import LiveTranslationServer, ServerConfig

  def main():
      config = ServerConfig(
          device="cpu",
          ws_port=8765,
          log="print",
          transcribe_only=False,
      )

      server = LiveTranslationServer(config)
      server.run(blocking=True)

  # Main guard is CRITICAL for systems that uses spawn method to create new processes
  # This is the case for Windows and MacOS
  if __name__ == "__main__":
      main()

  ```

- **Client**
  ```python
  from live_translation import LiveTranslationClient, ClientConfig

  def parser_callback(entry, *args, **kwargs):
      """Callback function to parse the output from the server.

      Args:
          entry (dict): The message from the server.
          *args: Optional positional args passed from the client.
          **kwargs: Optional keyword args passed from the client.
      """
      print(f"📝 {entry['transcription']}")
      print(f"🌍 {entry['translation']}")

      # Returning True signals the client to shutdown
      return False

  def main():
      config = ClientConfig(server_uri="ws://localhost:8765")

      client = LiveTranslationClient(config)
      client.run(
          callback=parser_callback,
          callback_args=(),  # Optional: positional args to pass
          callback_kwargs={},  # Optional: keyword args to pass
          blocking=True,
      )

  if __name__ == "__main__":
      main()

  ```

## Development & Contribution

To contribute or modify this project, these steps might be helpful:
> **NOTE**: This workflow below is developed with Linux-based systems with typical build tools installed e.g. ***Make*** in mind. One might need to install ***Make*** and possibly other tools on other systems. However, one can still do things manually without ***Make***, for example, run test manually using `python -m pytest -s tests/` instead of `make test`. 
> See **Makefile** for more details.


**Fork & Clone** the repository:
```bash
git clone git@github.com:<your-username>/live-translation.git
cd live-translation
```

**Ceate** a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate 
```

**Install** Dependencies:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Test** the package:
```bash
make test
```

**Build** the package:
```bash
make build
```
> **NOTE**: Building does ***lint*** and checks for ***formatting*** using [ruff](https://docs.astral.sh/ruff/). One can do that seprately using `make format` and `make lint`. For linting and formatting rules, see the [ruff config](/ruff.toml).

> **NOTE**: Building generates a ***.whl*** file that can be ***pip*** installed in a new environment for testing

**If needed**, run the server and the client within the virtual environment:
```bash
python -m live_translation.server.cli [OPTIONS]
python -m live_translation.client.cli [OPTIONS]
```
**For contribution**:
- Make your changes in a feature branch
- Ensure all tests pass
- Open a Pull Request (PR) with a clear description of your changes

## Tested Environment

This project was tested and developed on the following system configuration:

- **Architecture**: x86_64 (64-bit)
- **Operating System**: Ubuntu 24.10 (Oracular Oriole)
- **Kernel Version**: 6.11.0-18-generic
- **Python Version**: 3.12.7
- **Processor**: 13th Gen Intel(R) Core(TM) i9-13900HX
- **GPU**: GeForce RTX 4070 Max-Q / Mobile [^1]
- **NVIDIA Driver Version**: 560.35.03  
- **CUDA Toolkit Version**: 12.1  
- **cuDNN Version**: 9.7.1
- **RAM**: 32GB DDR5
- **Dependencies**: All required dependencies are listed in `requirements.txt` and [Prerequisites](#prerequisites)

[^1]: CUDA as the `DEVICE` is probably needed for heavier models like `large-v3-turbo` for Whisper. **Nvidia drivers**, **CUDA Toolkit**, **cuDNN** installation needed if option `"cuda"` was to be used.

## Improvements

- **ARM64 Support**: Ensure support for ARM64 based systems.
- **Concurrency Design Check**: Review and optimize the threading design to ensure thread safety and prevent issues like race conditions or deadlocks, etc., revisit the current design of ***WebSocketIO*** being a thread while ***AudioProcessor***, ***Transcriber***, and ***Translator*** being processes.
- **Logging**: Integrate detailed logging to track system activity, errors, and performance metrics using a more formal logging framework.
- **Translation Models**: Some of the models downloaded in ***Translator*** from [OpusMT's Hugging Face](https://huggingface.co/Helsinki-NLP) are not the best performing when compared with top models in [Opus-MT's Leaderboard](https://opus.nlpl.eu/dashboard/). Find a way to automatically download best performing models using the user's input of `src_lang` and `tgt_lang` as it's currently done. 
- **System Profiling & Resource Guidelines**: Benchmark and document CPU, memory, and GPU usage across all multiprocessing components. For example, "~35% CPU usage on 24-core **Intel i9-13900HX**", or "GPU load ~20% on **Nvidia RTX 4070** with `large-v3-turbo` Whisper model"). This will help with hardware requirements and deployment decisions.

## Citations
 ```bibtex
  @article{Whisper,
    title = {Robust Speech Recognition via Large-Scale Weak Supervision},
    url = {https://arxiv.org/abs/2212.04356},
    author = {Radford, Alec and Kim, Jong Wook and Xu, Tao and Brockman, Greg and McLeavey, Christine and Sutskever, Ilya},
    publisher = {arXiv},
    year = {2022}
  }

  @misc{Silero VAD,
    author = {Silero Team},
    title = {Silero VAD: pre-trained enterprise-grade Voice Activity Detector (VAD), Number Detector and Language Classifier},
    year = {2021},
    publisher = {GitHub},
    journal = {GitHub repository},
    howpublished = {\url{https://github.com/snakers4/silero-vad}},
    email = {hello@silero.ai}
  }

  @article{tiedemann2023democratizing,
    title={Democratizing neural machine translation with {OPUS-MT}},
    author={Tiedemann, J{\"o}rg and Aulamo, Mikko and Bakshandaeva, Daria and Boggia, Michele and Gr{\"o}nroos, Stig-Arne and Nieminen, Tommi and Raganato, Alessandro and Scherrer, Yves and Vazquez, Raul and Virpioja, Sami},
    journal={Language Resources and Evaluation},
    number={58},
    pages={713--755},
    year={2023},
    publisher={Springer Nature},
    issn={1574-0218},
    doi={10.1007/s10579-023-09704-w}
  }

  @InProceedings{TiedemannThottingal:EAMT2020,
    author = {J{\"o}rg Tiedemann and Santhosh Thottingal},
    title = {{OPUS-MT} — {B}uilding open translation services for the {W}orld},
    booktitle = {Proceedings of the 22nd Annual Conference of the European Association for Machine Translation (EAMT)},
    year = {2020},
    address = {Lisbon, Portugal}
  }
```