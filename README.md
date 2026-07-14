# AI-Powered Movie Compressor

A highly optimized, hardware-accelerated Flask web application that compresses large movie and video files efficiently while preserving maximum visual quality. Designed specifically to leverage NVIDIA GPUs (NVENC) for blazing-fast compression speeds.

## ✨ Features
- **Hardware Accelerated**: Uses NVIDIA's `hevc_nvenc` (H.265) encoder to crunch massive files in minutes rather than hours.
- **Smart Bitrate Capping**: Analyzes original video metadata to mathematically guarantee the output file is significantly reduced, avoiding accidental file inflation.
- **Beautiful Interface**: Modern, responsive, glassmorphism-inspired UI with real-time compression progress polling.
- **Compression History**: Built-in SQLite database that tracks all past compressions, total space saved, and provides instant download links.

## 🛠️ Prerequisites
- **Python 3.8+**
- **FFmpeg**: Must be installed and accessible in your system's PATH.
- **NVIDIA GPU**: Highly recommended (e.g., RTX 3050 or better) to take full advantage of the blazing-fast NVENC hardware acceleration.

## 🚀 Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/movie-compressor.git
   cd movie-compressor
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**
   ```bash
   python app.py
   ```

4. **Access the Web App**
   Open your web browser and navigate to:
   ```text
   http://127.0.0.1:5000
   ```

## 🎥 Usage
1. Upload a video file (supports MP4, MKV, AVI, MOV, etc.).
2. Select a compression mode:
   - **High Quality**: Maximum quality, moderate size reduction (targets 75% of original bitrate).
   - **Balanced**: The perfect sweet spot between quality and size (targets 50% of original bitrate).
   - **Max Compression**: Aggressive size reduction for archiving (targets 30% of original bitrate).
   - **Custom**: Manually select the codec (H.264/H.265) and CQ/CRF levels.
3. The application will leverage FFmpeg and your NVIDIA GPU to rapidly compress the video in the background.
4. Download your optimized video directly from the Results page!
