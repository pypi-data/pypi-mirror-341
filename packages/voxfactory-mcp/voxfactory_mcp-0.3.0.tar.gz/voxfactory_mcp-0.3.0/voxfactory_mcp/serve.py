import os
import base64
from pathlib import Path
from datetime import datetime
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Voxfactory TTS")
api_key = os.getenv('VoxFactory_API_KEY', '')

def get_output_path(output_dir, speaker, emotion):
    now_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    if not output_dir:
        output_dir = Path.home() / 'Desktop'
    elif not os.path.isabs(output_dir):
        output_dir = Path(os.path.expanduser(output_dir))
    output_dir.mkdir(parents=True, exist_ok=True)
        
    output_path = output_dir / f'{speaker}_{emotion}_{now_str}.wav'
    return str(output_path)

@mcp.tool()
async def tts(text:str, speaker:int=4, emotion:int=0, sr:int=44100, output_dir:str='') -> None:
    """
    Converts Korean text to natural speech using Text-to-Speech (TTS)
    
    This function specializes in generating Korean speech optimized for daily conversations
    and emotional expression. It supports various speaker types and emotion options to create
    appropriate voice outputs for different scenarios.

    It save the wav file at f"{output_dir}/{speaker}_{emotion}_{datetime}.wav".
    If output_dir is not given, the file is saved at Desktop.
    
    Parameters:
        text (str): Korean text to be converted to speech
        speaker (int, optional): Speaker type selection (default: 4)
            - 0: Female child
            - 1: Elderly woman
            - 2: Elderly man
            - 3: Adult male
            - 4: Adult female
        emotion (int, optional): Emotion type selection (default: 0)
            - 0: Daily conversation (neutral)
            - 1: Sadness
            - 2: Anger
        sr (int, optional): Audio sampling rate (default: 44100Hz)
        output_dir (int, optional): Directory where files should be saved. 
            Defaults to $HOME/Desktop
    
    Returns:
        None
        # str: Base64 encoded audio data
        
    Recommended usage:
        - Male daily conversation: speaker=3, emotion=0
        - Female daily conversation: speaker=4, emotion=0
    """
    # get output path
    output_path = get_output_path(output_dir, speaker, emotion)

    # get audio
    with open('/Users/guhyun/projects/mcp/test.wav', 'rb') as f:
        wav = f.read()
    encoded = base64.b64encode(wav).decode('utf-8')

    # save audio
    audio_byte = base64.b64decode(encoded)
    with open(output_path, 'wb') as f:
        f.write(audio_byte)

def main():
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main()