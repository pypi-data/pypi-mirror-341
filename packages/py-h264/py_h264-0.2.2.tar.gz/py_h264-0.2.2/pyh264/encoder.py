# get the user's os type
import os
import platform
import subprocess
import logging
from typing import List
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class H264Encoder:
    """A universal H.264 video encoder that supports multiple operating systems.
    
    This class provides functionality to encode videos to H.264 format using system-specific
    encoders and images to videos converter. It supports Linux, macOS (Darwin) operating systems.
    """

    def __init__(self):
        self.os_type = platform.system().lower()
        
        # Validate OS support
        if self.os_type not in ["linux", "darwin"]:
            raise NotImplementedError(f"Operating system {self.os_type} is not supported.")
        
        logger.info(f"Initialized H264Encoder for {self.os_type}")

    def get_default_encoder_path(self) -> str:
        """Get the default encoder path based on the operating system.
        
        Returns:
            str: Path to the default encoder executable.
            
        Raises:
            FileNotFoundError: If the default encoder is not found.
        """
        base_dir = Path(__file__).parent
        encoder_path = base_dir / "__os__" / f"converter_{self.os_type}"
        
        if not encoder_path.exists():
            raise FileNotFoundError(
                f"Default encoder not found for {self.os_type} at {encoder_path}"
            )
        
        return str(encoder_path)

    def _build_command(self, video_path: str, output_path: str, is_image: bool = False, duration: int = 5) -> List[str]:
        """Build the command with current parameters.
        
        Args:
            video_path (str): Path to the input video file.
            output_path (str): Path to save the encoded video.
            is_image (bool): Whether the input is an image.
            duration (int): Duration of the video.
            
        Returns:
            List[str]: List of command arguments.
        """
        encoder = self.get_default_encoder_path()
        
        command = [
            encoder,
            video_path,
            output_path
        ]
        
        if is_image:
            # add --image to the command and duration to the command
            command.insert(1, '--image')
            command.append(duration)

        return command
            
    def encode(self, media_path: str, output_path: str, is_image: bool = False, duration: int = 5) -> bool:
        """Encode a video file to H.264 format or convert images to videos.
        
        Args:
            media_path (str): Path to the input media file.
            output_path (str): Path to save the encoded media.
            is_image (bool): Whether the input is an image.
            duration (int): Duration of the video.
            
        Returns:
            bool: True if encoding was successful, False otherwise.
            
        Raises:
            FileNotFoundError: If input video file doesn't exist.
            ValueError: If output path is invalid.
            subprocess.CalledProcessError: If encoding process fails.
        """
        # Validate input file
        if not os.path.exists(media_path):
            raise FileNotFoundError(f"Input media file not found: {media_path}")
            
        # Validate output directory
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        try:
            command = self._build_command(media_path, output_path, is_image, duration)
            logger.info(f"Starting encoding process with command: {' '.join(command)}")
            
            result = subprocess.run(
                command,
                check=True,
                capture_output=True,
                text=True
            )
            
            logger.info("Encoding completed successfully")
            return True
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Encoding failed: {e.stderr}")
            raise ValueError(f"Encoding failed: {e.stderr}")
        except Exception as e:
            logger.error(f"Unexpected error during encoding: {str(e)}")
            raise ValueError(f"Unexpected error during encoding: {str(e)}")
