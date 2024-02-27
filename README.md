# Image-Generator
The primary objective of this project is to develop a system that can analyze images based on textual prompts, providing detailed insights and answers to questions asked about the image content. This integration will enhance the capabilities of AI systems in understanding and interpreting visual data through natural language interactions.

**Requirements:**
Python 3.12.0
pip 23.3.1
pip install replicate

Note: Replicate account and API Token need and added to enivronment variable if its in windows flow this link for guidance: https://replicate.com/docs/get-started/python 

carry out additional installations as directed.


**Methodology:**

Text-to-Image Generation with SDXL(Stability AI/Stable Diffusion XL)

Multimodal Analysis with LLaVA(Large Language and Vision Assistant) and added audio using GTTS(Google Text To Speech)

Integration and Deployment

**Text-to-Image Generation with SDXL:**

Stable Diffusion XL, developed by Stability AI, is a cutting-edge text-to-image generative AI model, succeeding Stable Diffusion. It excels in creating visually stunning images from textual descriptions.
Ensemble of Experts: SDXL employs a mixture-of-experts pipeline where the base model initiates the generation process, followed by a refining model for detailed denoising. This approach yields detailed images with fewer steps, enhancing efficiency. Handover point default is at 0.8 (80%).

Two-Stage Pipeline:

In the first stage, the base model generates latent representations.

The second stage involves a specialized high-resolution model utilizing SD Edit (img2img) technique(arXiv:2108.01073) to refine generated latents, resulting in higher-resolution outputs.

![image](https://github.com/SrinivasVamshiM/Image-Generator/assets/98442269/246129ef-bb9e-4a35-a5b3-d691ecd72f79)

While slightly slower, this method ensures greater fidelity in image generation.

**Multimodal Analysis with LLaVA:**

LLaVA (Large Language-and-Vision Assistant) represents a breakthrough in multimodal analysis, combining language understanding with visual comprehension. 
LLaVA is an open-source chatbot, developed by fine-tuning LlamA/Vicuna on GPT-generated multimodal instruction-following data.
It operates as an auto-regressive language model based on the transformer architecture, specialized for multimodal tasks.

Enhancements and Achievements:

Fully-Connected Vision-Language Cross-Modal Connector: LLaVA leverages a powerful and data-efficient connector, enabling robust multimodal analysis.

Model Modifications: Simple adjustments, such as using CLIP-ViT-L-336px with MLP projection and incorporating academic-task-oriented VQA data, have strengthened LLaVA's performance.

State-of-the-Art Results: LLaVA achieves state-of-the-art performance across 11 benchmarks, demonstrating its efficacy in various multimodal tasks.


**Integration and Deployment:**



**First view:**


<img width="817" alt="image" src="https://github.com/SrinivasVamshiM/Image-Generator/assets/98442269/f6297a50-cfe8-4a9b-9ed7-1d5e2388d628">



**Application Working:**


<img width="781" alt="image" src="https://github.com/SrinivasVamshiM/Image-Generator/assets/98442269/087072fb-12d2-4e46-8ae6-48f3d85996c4"><img width="775" alt="image" src="https://github.com/SrinivasVamshiM/Image-Generator/assets/98442269/cebfeca8-da06-4763-ba19-52d803d8067f">







