# Dynamic Range Compression in Python

Dynamic Range Compression in Python is a high-performance, multi-channel compressor that implements a translation of Audacity's dynamic range compressor (inspired by Daniel Rudrich’s algorithm). This package leverages Numba for JIT compilation to accelerate processing and supports any audio format that FFmpeg can handle (e.g., WAV, MP3, M4A, etc.).

## Features

- **Audacity-Inspired Compressor:**  
  Implements a dynamic range compression algorithm based on Audacity’s compressor (originally from Daniel Rudrich’s work).

- **Multi-Channel Support:**  
  Works with both mono and multi-channel audio.

- **Wide Audio Format Compatibility:**  
  Supports all FFmpeg-supported formats (WAV, MP3, M4A, etc.).

- **High Performance:**  
  Uses Numba to JIT compile critical processing routines for faster execution.

- **Flexible API:**  
  Two public API functions allow you to either process entire audio files or work directly with in-memory audio data.

## Public API

### `compress_audio(...)`

Loads an audio file from a specified path, converts it to an unnormalized 2D NumPy array of 16-bit samples, validates and initializes compressor settings, compresses the audio, and writes the compressed audio to a destination file.

**Function Signature:**

```python
def compress_audio(
    filePath,
    destPath,
    threshold,
    makeupGain,
    kneeWidth,
    compressionRatio,
    lookAhead,
    attack,
    release,
):
    """
    Loads an audio file from filePath, converts it to an unnormalized 2D NumPy array of 16-bit samples,
    validates and initializes compressor settings, compresses the audio, and writes the compressed audio to destPath.

    Parameters:
        filePath (str): Path to the input audio file.
        destPath (str): Path where the compressed audio file will be saved.
        threshold (float): Compression threshold in dB.
        makeupGain (float): Makeup gain in dB.
        kneeWidth (float): Knee width in dB.
        compressionRatio (float): Compression ratio.
        lookAhead (float): Lookahead time in milliseconds.
        attack (float): Attack time in milliseconds.
        release (float): Release time in milliseconds.

    Returns:
        None
    """
```

### `compress(audio, settings)`

This function applies dynamic range compression to an unnormalized 2D NumPy array of 16-bit audio samples. It first normalizes the audio to the range [-1, 1), then processes the audio in blocks by updating the compression envelope and the delayed input. Finally, it converts the processed audio back to 16-bit samples. This lower-level API provides granular control by allowing you to pass in audio data already loaded in memory along with a settings object.

```python
def compress(audio, settings):
    """
    Applies dynamic range compression to an unnormalized 2D NumPy array of 16-bit audio samples.

    The function first normalizes the input audio, then processes it in blocks by updating the 
    compression envelope, updating the delayed input, and finally applying the envelope.
    After processing all blocks, the audio is converted back to 16-bit samples.

    Parameters:
        audio (np.ndarray): A 2D NumPy array of shape (channels, samples) with dtype np.int16
                            containing the input audio samples.
        settings (CompressorSettings): An instance of a compressor settings class that contains the following attributes:
            - thresholdDb (float): Compression threshold in dB.
            - makeupGainDb (float): Makeup gain in dB.
            - kneeWidthDb (float): Knee width in dB.
            - compressionRatio (float): Compression ratio.
            - lookAheadMs (float): Lookahead time in milliseconds.
            - attackMs (float): Attack time in milliseconds.
            - releaseMs (float): Release time in milliseconds.
            - sampleRate (int): The sample rate of the audio.

            To use this function, create your own class (or object) with these attributes, instantiate it with
            your desired settings, and then pass that instance to this function.

    Returns:
        np.ndarray: A 2D NumPy array of shape (channels, samples) with dtype np.int16 containing the
                    compressed audio.
    """
```