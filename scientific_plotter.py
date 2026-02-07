#!/usr/bin/env python3
"""
Scientific Figure Generator using AI Models

This script generates publication-quality scientific figures using a two-step workflow:
1. GPT-5 analyzes scientific text and generates a structured MODULE LIST
2. Gemini-2.5-flash-image (nano banana) creates the figure based on the MODULE LIST
"""

import os
import sys
from pathlib import Path
from typing import Optional
import click
from openai import OpenAI
from dotenv import load_dotenv
import base64
import requests
from datetime import datetime

# Google Gemini imports (optional, used when API_TYPE=gemini)
try:
    from google import genai
    from google.genai import types
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False


class ScientificPlotter:
    """Main class for generating scientific figures"""
    
    def __init__(self):
        """Initialize the plotter with API configuration"""
        load_dotenv()
        
        # Determine API type
        self.api_type = os.getenv("API_TYPE", "openai").lower()
        
        # Initialize OpenAI client (used for both analysis and image generation in openai mode)
        self.openai_client = OpenAI(
            base_url=os.getenv("OPENAI_BASE_URL"),
            api_key=os.getenv("OPENAI_API_KEY")
        )
        
        # Initialize Google Gemini client if needed
        self.gemini_client = None
        if self.api_type == "gemini":
            if not GEMINI_AVAILABLE:
                raise ImportError(
                    "google-genai package is not installed. " 
                    "Please install it with: pip install google-genai"
                )
            gemini_api_key = os.getenv("GEMINI_API_KEY")
            if not gemini_api_key:
                raise ValueError("GEMINI_API_KEY is required when API_TYPE=gemini")
            self.gemini_client = genai.Client(api_key=gemini_api_key)
        
        self.analysis_model = os.getenv("ANALYSIS_MODEL", "gpt-5")
        self.image_model = os.getenv("IMAGE_MODEL", "gemini-2.5-flash-image")
        self.output_dir = Path(os.getenv("OUTPUT_DIR", "outputs"))
        
        # Create output directory if it doesn't exist
        self.output_dir.mkdir(exist_ok=True)
        
        # Load prompt templates
        self.prompts_dir = Path(__file__).parent / "prompts"
        self.step1_template = self._load_template("step1_module_generation.txt")
        self.step2_template = self._load_template("step2_figure_generation.txt")
    
    def _load_template(self, filename: str) -> str:
        """Load a prompt template from the prompts directory"""
        template_path = self.prompts_dir / filename
        if not template_path.exists():
            raise FileNotFoundError(f"Prompt template not found: {template_path}")
        return template_path.read_text(encoding="utf-8")
    
    def generate_module_list(self, scientific_text: str) -> str:
        """
        Step 1: Use GPT-5 to analyze scientific text and generate MODULE LIST
        
        Args:
            scientific_text: The scientific text to analyze
            
        Returns:
            The generated MODULE LIST as a string
        """
        print(f"📊 Step 1: Generating MODULE LIST using {self.analysis_model}...")
        
        prompt = self.step1_template.format(scientific_text=scientific_text)
        
        try:
            response = self.openai_client.chat.completions.create(
                model=self.analysis_model,
                messages=[
                    {"role": "system", "content": "You are an expert scientific illustrator."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=8000  # Increased for reasoning models like GPT-5
            )
            
            module_list = response.choices[0].message.content
            print("✅ MODULE LIST generated successfully!")
            print("\n" + "="*80)
            print("MODULE LIST:")
            print("="*80)
            print(module_list)
            print("="*80 + "\n")
            
            return module_list
            
        except Exception as e:
            print(f"❌ Error generating MODULE LIST: {e}")
            raise
    
    def generate_figure(self, module_list: str, output_path: Optional[Path] = None, input_filename: Optional[str] = None) -> Path:
        """
        Step 2: Use Gemini to generate the scientific figure
        
        Args:
            module_list: The MODULE LIST from step 1
            output_path: Optional custom output path for the figure
            input_filename: Optional input filename to use in output naming
            
        Returns:
            Path to the generated figure
        """
        print(f"🎨 Step 2: Generating figure using {self.image_model} (API: {self.api_type})...")
        
        prompt = self.step2_template.format(module_list=module_list)
        
        if self.api_type == "gemini":
            return self._generate_figure_gemini(prompt, output_path, input_filename)
        else:
            return self._generate_figure_openai(prompt, output_path, input_filename)
    
    def _generate_figure_gemini(self, prompt: str, output_path: Optional[Path] = None, input_filename: Optional[str] = None) -> Path:
        """
        Generate figure using native Google Gemini API
        
        Args:
            prompt: The prompt for image generation
            output_path: Optional custom output path for the figure
            input_filename: Optional input filename to use in output naming
            
        Returns:
            Path to the generated figure
        """
        try:
            # Create chat session with Gemini
            chat = self.gemini_client.chats.create(
                model=self.image_model,
                config=types.GenerateContentConfig(
                    response_modalities=['TEXT', 'IMAGE'],
                    temperature=0.7
                )
            )
            
            # Send message to generate image
            response = chat.send_message(prompt)
            
            # Process response parts
            image_saved = False
            if output_path is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                if input_filename:
                    base_name = Path(input_filename).stem
                    output_path = self.output_dir / f"{base_name}_{timestamp}.png"
                else:
                    output_path = self.output_dir / f"scientific_figure_{timestamp}.png"
            
            for part in response.parts:
                if part.text is not None:
                    print(f"📝 Model response: {part.text[:200]}...")
                elif image := part.as_image():
                    image.save(str(output_path))
                    print(f"✅ Figure saved to: {output_path}")
                    image_saved = True
                    break
            
            if not image_saved:
                raise ValueError("No image was generated in the response")
            
            return output_path
            
        except Exception as e:
            print(f"❌ Error generating figure with Gemini API: {e}")
            raise
    
    def _generate_figure_openai(self, prompt: str, output_path: Optional[Path] = None, input_filename: Optional[str] = None) -> Path:
        """
        Generate figure using OpenAI-compatible API (base64 decoding)
        
        Args:
            prompt: The prompt for image generation
            output_path: Optional custom output path for the figure
            input_filename: Optional input filename to use in output naming
            
        Returns:
            Path to the generated figure
        """
        try:
            # Use chat completions for image generation models
            response = self.openai_client.chat.completions.create(
                model=self.image_model,
                messages=[
                    {"role": "system", "content": "You are an expert scientific illustrator for generating NeurIPS-style figures."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=4000
            )
            
            # The response contains base64 encoded image data in markdown format
            response_content = response.choices[0].message.content
            print(f"📥 Received response from model")
            
            # Extract base64 data from markdown format
            # Format: ![image](data:image/png;base64,<base64_data>)
            import re
            
            # Try to extract base64 from markdown data URI
            base64_pattern = r'data:image/png;base64,([A-Za-z0-9+/=]+)'
            match = re.search(base64_pattern, response_content)
            
            if match:
                base64_data = match.group(1)
                print(f"✅ Extracted base64 data from markdown format")
            else:
                # Fallback: assume the whole content is base64
                base64_data = response_content
                print(f"⚠️  No markdown format detected, trying direct decode")
            
            # Decode base64 image data
            try:
                image_data = base64.b64decode(base64_data)
                print(f"✅ Successfully decoded base64 image data ({len(image_data)} bytes)")
                
                # Check for PNG header and clean if needed
                png_header = b'\x89PNG\r\n\x1a\n'
                if not image_data.startswith(png_header):
                    # Find PNG header position
                    png_pos = image_data.find(png_header)
                    if png_pos > 0:
                        print(f"⚠️  Found PNG header at position {png_pos}, removing {png_pos} bytes of prefix")
                        image_data = image_data[png_pos:]
                    elif png_pos == -1:
                        print(f"❌ No valid PNG header found in decoded data")
                        raise ValueError("Invalid PNG data: no PNG header found")
                
                print(f"✅ Valid PNG data confirmed ({len(image_data)} bytes)")
                
                # Save the image
                if output_path is None:
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    if input_filename:
                        base_name = Path(input_filename).stem
                        output_path = self.output_dir / f"{base_name}_{timestamp}.png"
                    else:
                        output_path = self.output_dir / f"scientific_figure_{timestamp}.png"
                
                output_path.write_bytes(image_data)
                print(f"✅ Figure saved to: {output_path}")
                
                return output_path
                
            except Exception as decode_error:
                # If decoding fails, save the response for debugging
                print(f"⚠️ Failed to decode base64 data: {decode_error}")
                print(f"Response content preview: {response_content[:500]}...")
                
                if output_path is None:
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    output_path = self.output_dir / f"response_{timestamp}.txt"
                
                output_path.write_text(response_content, encoding="utf-8")
                print(f"📝 Response saved to: {output_path}")
                raise ValueError(f"Failed to decode image data: {decode_error}. The response has been saved for review.")
            
        except Exception as e:
            print(f"❌ Error generating figure with OpenAI API: {e}")
            raise
    
    def generate_from_text(self, scientific_text: str, output_path: Optional[Path] = None, input_filename: Optional[str] = None) -> Path:
        """
        Complete workflow: Generate MODULE LIST and then the figure
        
        Args:
            scientific_text: The scientific text to visualize
            output_path: Optional custom output path for the figure
            input_filename: Optional input filename to use in output naming
            
        Returns:
            Path to the generated figure
        """
        print("\n" + "="*80)
        print("🚀 Starting Scientific Figure Generation Workflow")
        print("="*80 + "\n")
        
        # Step 1: Generate MODULE LIST
        module_list = self.generate_module_list(scientific_text)
        
        # Save MODULE LIST for reference
        if output_path:
            module_list_path = output_path.with_suffix('.txt')
        else:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            if input_filename:
                base_name = Path(input_filename).stem
                module_list_path = self.output_dir / f"{base_name}_module_list_{timestamp}.txt"
            else:
                module_list_path = self.output_dir / f"module_list_{timestamp}.txt"
        
        module_list_path.write_text(module_list, encoding="utf-8")
        print(f"📝 MODULE LIST saved to: {module_list_path}\n")
        
        # Step 2: Generate figure
        figure_path = self.generate_figure(module_list, output_path, input_filename)
        
        print("\n" + "="*80)
        print("🎉 Workflow completed successfully!")
        print("="*80)
        print(f"📄 MODULE LIST: {module_list_path}")
        print(f"🖼️  Figure: {figure_path}")
        print("="*80 + "\n")
        
        return figure_path


@click.command()
@click.option(
    '--input', '-i',
    type=click.Path(exists=True, path_type=Path),
    help='Path to input file containing scientific text'
)
@click.option(
    '--text', '-t',
    type=str,
    help='Scientific text as a string (alternative to --input)'
)
@click.option(
    '--output', '-o',
    type=click.Path(path_type=Path),
    help='Output path for the generated figure (default: outputs/scientific_figure_TIMESTAMP.png)'
)
@click.option(
    '--module-list-only',
    is_flag=True,
    help='Only generate MODULE LIST without creating the figure'
)
def main(input: Optional[Path], text: Optional[str], output: Optional[Path], module_list_only: bool):
    """
    Generate publication-quality scientific figures using AI models.
    
    This tool uses a two-step workflow:
    1. GPT-5 analyzes your scientific text and creates a structured MODULE LIST
    2. Gemini-2.5-flash-image generates a NeurIPS-style figure from the MODULE LIST
    
    Examples:
    
        # Generate from file
        python scientific_plotter.py -i examples/sample_input.txt
        
        # Generate from text
        python scientific_plotter.py -t "Your scientific text here..."
        
        # Specify output path
        python scientific_plotter.py -i input.txt -o my_figure.png
        
        # Only generate MODULE LIST
        python scientific_plotter.py -i input.txt --module-list-only
    """
    
    # Validate input
    if not input and not text:
        click.echo("❌ Error: Please provide either --input or --text", err=True)
        click.echo("Use --help for usage information", err=True)
        sys.exit(1)
    
    if input and text:
        click.echo("⚠️  Warning: Both --input and --text provided. Using --input file.", err=True)
    
    # Read scientific text
    input_filename = None
    if input:
        scientific_text = input.read_text(encoding="utf-8")
        input_filename = str(input)
        click.echo(f"📖 Reading from: {input}")
    else:
        scientific_text = text
        click.echo("📖 Using provided text")
    
    # Initialize plotter
    try:
        plotter = ScientificPlotter()
    except Exception as e:
        click.echo(f"❌ Error initializing plotter: {e}", err=True)
        click.echo("\n💡 Make sure you have created a .env file with your API credentials.", err=True)
        click.echo("   Copy .env.example to .env and fill in your details.", err=True)
        sys.exit(1)
    
    # Generate
    try:
        if module_list_only:
            module_list = plotter.generate_module_list(scientific_text)
            
            # Save MODULE LIST
            if output:
                output_path = output
            else:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_path = plotter.output_dir / f"module_list_{timestamp}.txt"
            
            output_path.write_text(module_list, encoding="utf-8")
            click.echo(f"\n✅ MODULE LIST saved to: {output_path}")
        else:
            plotter.generate_from_text(scientific_text, output, input_filename)
            
    except Exception as e:
        click.echo(f"\n❌ Error during generation: {e}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
