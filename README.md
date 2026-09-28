<div align="center">

# 🎥 AI-Powered Movie & Video Compressor

**A high-throughput, hardware-accelerated Flask application leveraging NVIDIA NVENC GPU computing for rapid video compression with zero perceptible quality degradation.**

[![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![FFmpeg](https://img.shields.io/badge/FFmpeg-007808?style=for-the-badge&logo=ffmpeg&logoColor=white)](https://ffmpeg.org/)
[![NVIDIA NVENC](https://img.shields.io/badge/NVIDIA-NVENC_Accelerated-76B900?style=for-the-badge&logo=nvidia&logoColor=white)](https://developer.nvidia.com/nvidia-video-codec-sdk)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

<p align="center">
  <a href="https://omkar-portfolio-live.vercel.app"><img src="https://img.shields.io/badge/🌐_Portfolio-Live_Site-0A66C2?style=for-the-badge&logo=vercel&logoColor=white" /></a>
  <a href="https://github.com/omkar333333"><img src="https://img.shields.io/badge/Status-Open_to_Internships_&_Roles-brightgreen?style=for-the-badge" /></a>
  <a href="mailto:your-email@example.com"><img src="https://img.shields.io/badge/Email-Direct_Contact-blue?style=for-the-badge&logo=gmail&logoColor=white" /></a>
</p>

<p align="center">
  <a href="#-recruiter--hiring-manager-quick-summary-tldr">📌 Recruiter Summary</a> •
  <a href="#-features">✨ Features</a> •
  <a href="#-architecture--pipeline">🏗️ Architecture</a> •
  <a href="#-prerequisites">🛠️ Prerequisites</a> •
  <a href="#-installation--setup">🚀 Setup</a>
</p>

</div>

---

> [!TIP]
> ### 📌 Recruiter & Hiring Manager Quick Summary (TL;DR)
> - **Developer**: **Omkar Mote** — *B.E. in Artificial Intelligence & Data Science* (Pune, India)
> - **Core Stack**: Python, Flask, FFmpeg, FFprobe, NVIDIA NVENC (`hevc_nvenc`), SQLite, HTML5/CSS3/JavaScript.
> - **Problem Solved**: Overcomes the storage bottlenecks of 4K/1080p raw media files by accelerating H.265/HEVC encoding via dedicated GPU silicon, reducing file sizes by up to 70% with negligible loss.
> - **Key Engineering Highlights**:
>   - ⚡ **GPU Hardware Acceleration**: Offloads transcoding from CPU to NVIDIA NVENC ASICs for 5x–10x speedups.
>   - 🧠 **Dynamic Bitrate Capping**: Probes source streams using `ffprobe` and calculates mathematical CRF/bitrate upper-bounds to avoid accidental file bloating.
>   - 📊 **Telemetry Logging**: SQLite database logging execution runtimes, compression ratios, and megabytes conserved.
> - **Direct Links**: [GitHub Profile](https://github.com/omkar333333) • [Live Portfolio Website](https://omkar-portfolio-live.vercel.app)

---

## ✨ Features

- ⚡ **Hardware Accelerated**: Uses NVIDIA's `hevc_nvenc` (H.265 / HEVC) encoder to crunch massive video files in minutes rather than hours.
- 🎯 **Smart Bitrate Capping**: Analyzes source video metadata to mathematically guarantee significant file size reduction without accidental bitrate inflation.
- 🎨 **Modern Glassmorphic UI**: Responsive, sleek dark-mode web dashboard with real-time compression progress polling.
- 📊 **Compression History & Analytics**: SQLite database logging all past compressions, computation times, and total megabytes saved, complete with direct download buttons.
- 🛡️ **Safety Fallbacks**: Automatically degrades gracefully to CPU encoding (`libx265` / `libx264`) if hardware acceleration is unavailable.

---

## 🏗️ Architecture & Pipeline

```text
[User Upload (MP4/MKV)]
         │
         ▼
[Metadata Extractor (ffprobe)] ──► Bitrate & Resolution Analysis
         │
         ▼
[Smart Parameter Calculator] ──► Optimal CRF / Target Bitrate
         │
         ▼
[NVENC Hardware Encoding] ──► H.265 Compression via GPU
         │
         ▼
[SQLite History Logger] ──► Space Saved & Download Link
```

---

## 🛠️ Prerequisites

- **Python 3.8+**
- **FFmpeg**: Must be installed and accessible in your system's `PATH`.
- **NVIDIA GPU** *(Recommended)*: RTX 20/30/40 series or GTX 16 series to leverage NVENC hardware encoding.

---

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/omkar333333/AI-Powered_Video_Compression_Platform.git
cd AI-Powered_Video_Compression_Platform
```

### 2. Create a Virtual Environment
```bash
python -m venv venv

# Windows (PowerShell)
.\venv\Scripts\Activate.ps1

# Linux / macOS
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Verify FFmpeg & GPU Support
```bash
# Verify FFmpeg is accessible
ffmpeg -version

# Check if NVIDIA NVENC is available
ffmpeg -encoders | grep nvenc
```

### 5. Launch the Application
```bash
python app.py
```
Open your browser and navigate to: `http://localhost:5000`

---

## 👨‍💻 Author

**Omkar Mote**  
- 🎓 *B.E. in Artificial Intelligence & Data Science*  
- 🌐 [Live Portfolio Website](https://omkar-portfolio-live.vercel.app)  
- 💻 [GitHub Profile](https://github.com/omkar333333)
