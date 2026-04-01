# 🧠 NeuroPath AI

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Framework: PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?logo=pytorch&logoColor=white)](https://pytorch.org/)

**NeuroPath AI** is a highly efficient, real-time framework designed for the automated classification, localization, and surgical-grade segmentation of brain tumors from T1-CE MRI scans. 

By utilizing a unique 3-stage "Funnel" architecture (ResNet-101 → YOLOv8 → ResUNet), the system bypasses the computationally expensive process of whole-image segmentation. It features an "Early Exit" triage for healthy scans and processes only localized tumor crops, achieving **99.7% classification accuracy** and an **85.2% Dice score** with an ultra-low inference latency of just **43ms**.

---

## 🚀 Key Features

* **Smart Triage (Early Exit):** Filters out healthy scans in Stage 1, saving up to 90% of GPU compute time.
* **Precision Localization:** Anchor-free detection that dynamically crops the MRI to the exact Region of Interest (ROI) with a 15-pixel peritumoral boundary.
* **Surgical-Grade Segmentation:** Extracts high-fidelity tumor boundaries exclusively from the localized ROI.
* **Clinical UI/UX:** A streamlined, multi-step web dashboard designed for radiologist and intraoperative workflows.

---

## 🏗️ System Architecture

The core innovation of NeuroPath AI is its sequential, narrowing "Funnel" pipeline. Rather than forcing a single model to understand the entire brain, the architecture divides the cognitive load across three specialized networks.

![Architecture](https://github.com/user-attachments/assets/ff89362d-fbdf-462c-b5f1-e088f92afaed)


1. **Stage 1 (Gatekeeper):** A ResNet-101 classifier analyzes the 640x640 scan. If healthy, the pipeline halts. If a tumor is present, it identifies the class and passes the scan forward.
2. **Stage 2 (Localizer):** A YOLOv8 object detection head finds the coordinates `(x, y, w, h)` of the lesion and applies a 15-pixel symmetric padding to create a cropped Region of Interest (ROI).
3. **Stage 3 (Segmenter):** A custom ResUNet with hybrid loss (BCE + Dice) processes the 128x128 cropped ROI to output a pixel-perfect binary mask.

---

## 🖥️ System Pipeline & Interface

The NeuroPath AI dashboard guides the user seamlessly from data ingestion to final probability analysis.

### 1. Data Ingestion
Users can upload standard T1-weighted Contrast-Enhanced (T1-CE) MRI scans directly via local files or PACS integration.
![Upload](https://github.com/user-attachments/assets/b589a186-1756-47d4-80e1-a031271385e5)


### 2. Stage 1: Classification & Triage (ResNet-101)
The model acts as a gatekeeper, categorizing the scan into Glioma, Meningioma, Pituitary, or Healthy. 
![Choose](https://github.com/user-attachments/assets/8c9b50c0-ece0-4b1c-962f-23c49f19461f)
![Classification](https://github.com/user-attachments/assets/25a43ba9-ed7c-4964-89fb-c547f2151d9a)


### 3. Stage 2: ROI Localization (YOLOv8)
For pathological scans, an anchor-free YOLOv8 head identifies the exact coordinates of the lesion. This creates a "Bounding Box Bridge" that crops the image.

![ROI](https://github.com/user-attachments/assets/67e81b62-e328-4734-b6b3-b82779b675a7)

### 4. Stage 3: Targeted Segmentation (ResUNet)
The cropped ROI is processed through a Residual U-Net. By processing a localized 128x128 tensor instead of the entire scan, the model captures fine-grained boundary details without background noise interference.

![Segment](https://github.com/user-attachments/assets/f5eaa4da-ebfd-4a81-9612-7dbb3aae17cb)

---

## 📊 Analytical Insights & Visualizations

The platform provides deep analytical tools for clinical validation, including qualitative overlays and pixel-wise probability mapping.

### Final Pipeline Visualization
A side-by-side comparison proving pipeline efficacy: YOLO ROI → Ground Truth Mask → ResUNet Prediction → Final MRI Overlay.
![Final](https://github.com/user-attachments/assets/185931f2-9421-499e-9cd7-87ab34cb4a47)


### Probability Heatmap
Continuous probability mapping visualizes model certainty, showing high confidence (red) at the tumor core and dynamic probability at the irregular tissue boundaries.

![Heatmap](https://github.com/user-attachments/assets/f145c3a1-0481-46f9-a430-19ebbc975983)

---

## 📈 Model Performance Metrics

Evaluated on a rigorous 787-image testing set, the multi-stage architecture significantly outperforms standard single-stage U-Net variants in both speed and accuracy.

### Classification Triage (ResNet-101)

| Metric | Stage 1 (Classification) | Stage 3 (Segmentation) |
| :--- | :--- | :--- |
| **Accuracy** | 99.7% | - |
| **Dice Coefficient** | - | 85.2% |
| **Precision** | 99.6% | 87.4% |
| **Inference Latency**| 12 ms | 31 ms |
| **Total Pipeline Time**| **-** | **43 ms** |



---

## ⚙️ Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/yourusername/NeuroPath-AI.git](https://github.com/yourusername/NeuroPath-AI.git)
   cd NeuroPath-AI
