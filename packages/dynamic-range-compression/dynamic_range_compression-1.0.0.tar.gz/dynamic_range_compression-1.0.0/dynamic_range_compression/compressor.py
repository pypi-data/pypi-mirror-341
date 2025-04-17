import numpy as np
from pydub import AudioSegment
import os
import numba
from .compressorHelper import definitions as d
from .compressorHelper import envelope


# Value Ranges:
# Lookahead max: 1000 ms


class CompressorSettings:
    def __init__(
        self,
        thresholdDb,
        makeupGainDb,
        kneeWidthDb,
        compressionRatio,
        lookAheadMs,
        attackMs,
        releaseMs,
        sampleRate,
    ):
        self.thresholdDb = thresholdDb
        self.makeupGainDb = makeupGainDb
        self.kneeWidthDb = kneeWidthDb
        self.compressionRatio = compressionRatio
        self.lookAheadMs = lookAheadMs
        self.attackMs = attackMs
        self.releaseMs = releaseMs
        self.sampleRate = sampleRate

@numba.njit
def validate_settings(
    threshold,
    makeupGain,
    kneeWidth,
    compressionRatio,
    lookAhead,
    attack,
    release,
):
    # Example ranges -- adjust these as appropriate for your application:
    if not (-100 <= threshold <= 0):
        raise ValueError(f"Threshold ({threshold} dB) must be between -100 and 0 dB.")
    if not (-30 <= makeupGain <= 30):
        raise ValueError(
            f"Makeup gain ({makeupGain} dB) must be between -30 and 30 dB."
        )
    if not (0 <= kneeWidth <= 50):
        raise ValueError(f"Knee width ({kneeWidth} dB) must be between 0 and 50 dB.")
    if not (1 <= compressionRatio <= 100):
        raise ValueError(
            f"Compression ratio ({compressionRatio}) must be between 1 and 100."
        )
    if not (0 < lookAhead <= 1000):
        raise ValueError(
            f"LookAhead ({lookAhead} ms) must be greater than 0 and at most 1000 ms."
        )
    if not (0 < attack <= 200):
        raise ValueError(
            f"Attack ({attack} ms) must be greater than 0 and at most 200 ms."
        )
    if not (0 < release <= 1000):
        raise ValueError(
            f"Release ({release} ms) must be greater than 0 and at most 1000 ms."
        )

def write_audio_file(audio_np, sample_rate, destPath):
    """
    Writes a 2D NumPy array (channels x samples) of 16-bit audio samples to a file.
    The file format is determined by the extension of destPath.

    Parameters:
        audio_np (np.ndarray): 2D numpy array (channels x samples) with dtype=np.int16.
        sample_rate (int): The sample rate of the audio.
        destPath (str): Destination file path (e.g., "output.m4a", "output.wav").
    """
    # Determine the number of channels and samples
    channels, _ = audio_np.shape

    # Interleave channels: convert shape (channels, samples) to (samples, channels), then flatten.
    interleaved = audio_np.T.flatten()

    # Extract file extension (without the dot) and convert to lower case.
    _, ext = os.path.splitext(destPath)
    file_format = ext[1:].lower()
    if file_format == "m4a":
        file_format = "ipod"

    # Create an AudioSegment using the interleaved byte data.
    audio_segment = AudioSegment(
        data=interleaved.tobytes(),
        sample_width=2,  # 2 bytes per sample for int16
        frame_rate=sample_rate,
        channels=channels,
    )

    # Export the AudioSegment using the detected format.
    audio_segment.export(destPath, format=file_format)


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
    # Validate the settings.
    validate_settings(
        threshold=threshold,
        makeupGain=makeupGain,
        kneeWidth=kneeWidth,
        compressionRatio=compressionRatio,
        lookAhead=lookAhead,
        attack=attack,
        release=release,
    )

    # Load the audio file using pydub.
    audio = AudioSegment.from_file(filePath)

    # Get sample rate and number of channels.
    sample_rate = audio.frame_rate
    channels = audio.channels

    # Extract the raw interleaved samples.
    samples = audio.get_array_of_samples()

    # Convert the raw samples into a NumPy array of type int16.
    audio_np = np.array(samples, dtype=np.int16)

    # Reshape into a 2D numpy array (channels x samples).
    audio_np = audio_np.reshape((-1, channels)).T

    # Initialize settings class.
    settings = CompressorSettings(
        thresholdDb=threshold,
        makeupGainDb=makeupGain,
        kneeWidthDb=kneeWidth,
        compressionRatio=compressionRatio,
        lookAheadMs=lookAhead,
        attackMs=attack,
        releaseMs=release,
        sampleRate=sample_rate,
    )

    # Compress the audio using compressor function.
    compressed_audio = compress(audio_np, settings)

    # Write the compressed audio to the destination file.
    write_audio_file(compressed_audio, sample_rate, destPath)

    return None


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

    # Normalize the audio to the range [-1, 1) for processing.
    normalized_audio = audio.astype(np.float32) / 32768.0

    # Initialize variables.
    processed = 0
    audioLength = normalized_audio.shape[1]
    audioChannels = normalized_audio.shape[0]

    # Initialize compressor settings in the definitions module.
    d.setSettings(
        audioChannels,
        settings.thresholdDb,
        settings.makeupGainDb,
        settings.kneeWidthDb,
        settings.compressionRatio,
        settings.lookAheadMs,
        settings.attackMs,
        settings.releaseMs,
        settings.sampleRate,
    )

    # Main processing loop:
    # Process the audio in blocks of size d.mBlockSize until all frames are processed.
    while processed < audioLength:
        # Determine the number of frames to process in this iteration.
        toProcess = min(audioLength - processed, d.mBlockSize)

        # Update the compression envelope based on the current block of normalized audio.
        envelope.UpdateEnvelope(normalized_audio, processed, toProcess)

        # Update the delayed input:
        # For every channel, copy the current block (from processed to processed+toProcess)
        # to the delayed input buffer with an offset defined by d.delayInSamples.
        delay = d.lookAheadSettings.delayInSamples
        d.delayedInput[:, delay : delay + toProcess] = normalized_audio[
            :, processed : processed + toProcess
        ]

        # Apply the compression envelope to the current block of normalized audio.
        envelope.ApplyEnvelope(normalized_audio, d.mEnvelope, d.delayedInput, processed, toProcess, d.lookAheadSettings, d.compressionSettings)

        # Update the processed frame counter.
        processed += toProcess

    # Reconvert normalized audio back to 16-bit PCM.
    return (normalized_audio * 32767).astype(np.int16)
