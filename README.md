# video-colorization-pipeline
AI video colorization using DeOldify and Google Colab




# AI Video Colorization Pipeline

This project demonstrates an end-to-end **AI video colorization pipeline** built using **Google Colab**, **PyTorch**, **FFmpeg**, and **DeOldify**.  
The goal was to take a **black-and-white video** as input and generate a **colorized output video** using a pretrained deep learning model.

---

## Project Purpose

Old black-and-white videos often lose visual detail and emotional impact compared to modern color footage.  
The purpose of this project was to build a simple but effective pipeline that can:

- accept a grayscale video as input,
- process it using an AI-based colorization model,
- and generate a final colorized video output.

This project focuses on **applying an existing pretrained model in a complete workflow**, rather than training a new model from scratch.

---

## Objective

The main objective of this project was to understand how a real AI-based video processing workflow is built and executed, including:

- setting up a GPU environment,
- handling video input,
- loading a pretrained model,
- running inference on video data,
- and exporting the final output.

---

## Tools and Technologies Used

### 1. Google Colab
**Why we used it:**  
Video colorization is computationally expensive, especially for deep learning models. Google Colab provides access to a **GPU environment**, which makes processing much faster than running on a normal CPU.

**How we used it:**  
We used a **Tesla T4 GPU runtime** in Colab to run the notebook, install dependencies, load the model, and process the video.

---

### 2. Python
**Why we used it:**  
Python is widely used in AI, machine learning, and computer vision workflows.

**How we used it:**  
Python was used to write the notebook logic, manage the workflow, load the model, and call the video colorization functions.

---

### 3. PyTorch
**Why we used it:**  
DeOldify is built on top of PyTorch, which is a deep learning framework used to load and run pretrained neural network models.

**How we used it:**  
PyTorch was used indirectly through DeOldify to load the pretrained video colorization model and perform inference on the video.

---

### 4. DeOldify
**Why we used it:**  
DeOldify is a well-known open-source project for image and video colorization. It provides pretrained models that can colorize black-and-white media without requiring us to train a model ourselves.

**How we used it:**  
We cloned the DeOldify repository, installed its dependencies, downloaded the pretrained video model weights, and used its `VideoColorizer` pipeline to process the input video.

---

### 5. FFmpeg
**Why we used it:**  
FFmpeg is a powerful multimedia tool used for video and audio processing.

**How we used it:**  
FFmpeg was installed as part of the environment setup because DeOldify relies on it internally for handling video processing tasks such as reading the source video and generating the final processed output.

---

## Methodology

The project was completed in the following steps:

### Step 1: Set up the environment
A Google Colab notebook was created with GPU acceleration enabled.  
Required system tools such as `ffmpeg` and `git` were installed.

### Step 2: Clone the DeOldify repository
The DeOldify GitHub repository was cloned into the Colab environment so the project code could be used.

### Step 3: Install dependencies
The required Python packages for DeOldify were installed using its Colab requirements file.

### Step 4: Download pretrained model weights
The pretrained **video colorization model** (`ColorizeVideo_gen.pth`) was downloaded and stored in the model directory.

### Step 5: Upload the input video
The black-and-white input video was uploaded into the Colab environment.

### Step 6: Load the model
The DeOldify video colorizer was initialized using GPU mode so that inference could run efficiently.

### Step 7: Run video colorization
The uploaded video was passed into the DeOldify colorization pipeline.  
The model processed the frames and generated a final colorized video.

### Step 8: Export and download the result
The output video was saved in the result directory and then downloaded from Colab.

---

## Why a Pretrained Model Was Used

Training a video colorization model from scratch requires:

- a large labeled dataset,
- long training time,
- high GPU resources,
- and advanced model tuning.

Instead of training a new model, this project used a **pretrained DeOldify model**.  
This allowed the focus to stay on:

- understanding the workflow,
- integrating the model into a working pipeline,
- and successfully generating output.

So, in this project:

- **the model was not trained from scratch**
- **the pipeline was built and executed using a pretrained model**

---

## Input

The input to the system was:

- a black-and-white video file (`.mp4`)

Example input:
- grayscale or old footage
- short video clip uploaded into Colab

---

## Output

The final output of the project was:

- a **colorized video** generated from the original black-and-white input

Output file location in Colab:
```bash
/content/DeOldify/video/result/test.mp4
