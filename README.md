# AI Scientific Figure Generator

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

🎨 **Generate publication-quality scientific figures using AI models**

This tool uses a sophisticated two-step workflow to create NeurIPS/ICLR-style scientific figures from your research text:
1. **GPT-5** analyzes your scientific text and generates a structured MODULE LIST
2. **Gemini-2.5-flash-image** (nano banana) creates a professional figure based on the MODULE LIST

## ✨ Features

- 🤖 **Integrated AI Workflow**: GPT-5 analysis guides nano banana for optimal results
- 📊 **Publication-Ready**: Generates clean, NeurIPS-style scientific figures
- 🎯 **Structured Approach**: Two-step process ensures logical, accurate visualizations
- 🔧 **Easy Configuration**: Simple `.env` file setup
- 💾 **Automatic Saving**: Saves both MODULE LIST and generated figures
- 🖥️ **CLI Interface**: User-friendly command-line tool

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
git clone git@github.com:hengzzzhou/FigForge.git
cd FigForge

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

Create a `.env` file from the template:

```bash
cp .env.example .env
```

Edit `.env` and add your API credentials:

**Option 1: OpenAI-Compatible API** (default, for relay endpoints)
```env
API_TYPE=openai
OPENAI_BASE_URL=
OPENAI_API_KEY=
ANALYSIS_MODEL=gpt-5
IMAGE_MODEL=gemini-2.5-flash-image
OUTPUT_DIR=outputs
```

**Option 2: Native Google Gemini API**
```env
API_TYPE=gemini
GEMINI_API_KEY=
OPENAI_BASE_URL=
OPENAI_API_KEY=
ANALYSIS_MODEL=gpt-5
IMAGE_MODEL=gemini-2.5-flash-image
OUTPUT_DIR=outputs
```

> **Note**: When using `API_TYPE=gemini`, the MODULE LIST generation still uses the OpenAI-compatible API, but image generation uses the native Google Gemini API.

### 3. Usage

**Generate from a file:**
```bash
python scientific_plotter.py -i examples/sample_input.txt
```

**Generate from text directly:**
```bash
python scientific_plotter.py -t "Your scientific text describing your model architecture..."
```

**Specify output location:**
```bash
python scientific_plotter.py -i input.txt -o my_awesome_figure.png
```

**Generate MODULE LIST only:**
```bash
python scientific_plotter.py -i input.txt --module-list-only
```

## 📸 Examples

Here are some scientific figures generated using FigForge:

### Sample Input - Neural Architecture

![sample_input_1.png](output_case/sample_input_1.png)

### [LiveSearchBench](https://arxiv.org/abs/2511.01409)

![livesearchbench.png](output_case/livesearchbench.png)

### [ReSo](https://arxiv.org/abs/2503.02390)

![reso.png](output_case/reso.png)

### [VIKI-R](https://arxiv.org/abs/2506.09049)

![viki-r.png](output_case/viki-r.png)

> All figures are generated with clean conference-style design, featuring flat aesthetics, consistent line weights, and professional color palettes.

---

## 📖 How It Works

### Step 1: MODULE LIST Generation (GPT-5)

The GPT-5 model analyzes your scientific text and creates a structured MODULE LIST that breaks down your architecture into:

1. **Input(s)**: Data sources and preprocessing
2. **Preprocessing/Encoding/Embedding**: Feature extraction layers
3. **Core Architecture/Stages/Blocks**: Main model components in sequence
4. **Special Mechanisms**: Attention, memory, routing, etc.
5. **Output Head**: Final prediction layers

### Step 2: Figure Generation (Gemini-2.5-flash-image)

Using the MODULE LIST as a guide, nano banana generates a clean, professional figure following these design principles:

- ✅ Flat, clean conference style (no gradients, shadows)
- ✅ Consistent thin line weights
- ✅ Professional pastel color palette
- ✅ Rounded rectangles for module blocks
- ✅ Clear arrows indicating data flow
- ✅ Concise labels (no long sentences)
- ✅ Pure white background with clean spacing

## 📁 Project Structure

```
NBP/
├── scientific_plotter.py      # Main application script
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variable template
├── .gitignore                 # Git ignore patterns
├── prompts/
│   ├── step1_module_generation.txt    # Prompt for MODULE LIST
│   └── step2_figure_generation.txt    # Prompt for figure generation
├── examples/
│   └── sample_input.txt       # Sample scientific text
├── outputs/                   # Generated figures (auto-created)
└── README.md                  # This file
```

## 🎯 Example Workflow

```bash
$ python scientific_plotter.py -i examples/sample_input.txt

================================================================================
🚀 Starting Scientific Figure Generation Workflow
================================================================================

📊 Step 1: Generating MODULE LIST using gpt-5...
✅ MODULE LIST generated successfully!

================================================================================
MODULE LIST:
================================================================================
[Structured breakdown of your architecture...]
================================================================================

📝 MODULE LIST saved to: outputs/sample_input_module_list_20231125_143022.txt

🎨 Step 2: Generating figure using gemini-2.5-flash-image...
💾 Downloading image from: [URL]
✅ Figure saved to: outputs/sample_input_20231125_143022.png

================================================================================
🎉 Workflow completed successfully!
================================================================================
📄 MODULE LIST: outputs/sample_input_module_list_20231125_143022.txt
🖼️  Figure: outputs/sample_input_20231125_143022.png
================================================================================
```

## ⚙️ Configuration Options

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `API_TYPE` | API type for image generation: `openai` or `gemini` | `openai` |
| `OPENAI_BASE_URL` | OpenAI-compatible API endpoint URL | Required |
| `OPENAI_API_KEY` | API key for OpenAI-compatible endpoint | Required |
| `GEMINI_API_KEY` | Google Gemini API key (required when `API_TYPE=gemini`) | - |
| `ANALYSIS_MODEL` | Model for MODULE LIST generation | `gpt-5` |
| `IMAGE_MODEL` | Model for figure generation | `gemini-2.5-flash-image` |
| `OUTPUT_DIR` | Directory for output files | `outputs` |

### Command-Line Options

| Option | Short | Description |
|--------|-------|-------------|
| `--input FILE` | `-i` | Path to input text file |
| `--text TEXT` | `-t` | Scientific text as string |
| `--output FILE` | `-o` | Custom output path |
| `--module-list-only` | | Generate MODULE LIST only |
| `--help` | | Show help message |

## 🔍 Tips for Best Results

1. **Provide Clear Text**: The more detailed and structured your input text, the better the MODULE LIST
2. **Describe Flow**: Explicitly mention data flow and connections between components
3. **Specify Components**: Name specific layers, blocks, or mechanisms in your architecture
4. **Review MODULE LIST**: Check the generated MODULE LIST before proceeding to figure generation
5. **Iterate**: You can regenerate figures with modified MODULE LIST for fine-tuning

## 🐛 Troubleshooting

**Problem**: `Error initializing plotter`
- **Solution**: Make sure `.env` file exists and contains valid API credentials

**Problem**: `FileNotFoundError: Prompt template not found`
- **Solution**: Ensure `prompts/` directory exists with both template files

**Problem**: API connection errors
- **Solution**: Verify your `OPENAI_BASE_URL` and `OPENAI_API_KEY` are correct

**Problem**: Image generation fails
- **Solution**: Check that `gemini-2.5-flash-image` model is available on your API endpoint

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- Prompt templates based on NeurIPS/ICLR figure design principles
- Powered by OpenAI-compatible API endpoints
- Uses GPT-5 for analysis and Gemini-2.5-flash-image (nano banana) for generation

---

**Happy Scientific Plotting! 🎨✨**

For questions or issues, please open an issue on GitHub.
