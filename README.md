# Video Frame Interpolation Through Adaptive Separable Convolution

# Authors
Deval Jayesh Pandya (djpandya@asu.edu)
Hunter Olson (hmolson4@asu.edu)
Kinghei Ma (kingheim@asu.edu)
Ti-Han Wu (tihanwu@asu.edu)

# Problem Statement
Traditional video frame interpolation techniques rely on optical flow estimation between frames, which often involves separate estimation and synthesis steps. Recent advancements have combined these steps using 2D convolutional kernels for improved efficiency. However, the large kernel size needed to handle significant motion demands substantial memory, posing a challenge for practical implementations.

To address this, we implemented the method proposed in [1], which reduces memory usage by estimating 1D kernels through a convolutional neural network (CNN) rather than employing 2D kernels. This approach achieves high-quality interpolation with a smaller memory footprint, enabling practical and efficient video processing.

# Solution
We developed a fully convolutional neural network (Figure 1) to generate four 1-dimensional kernels for performing horizontal and vertical convolutions on two input frames, producing an interpolated frame. Our solution workflow includes the following:

Dataset Creation:

Source: Publicly available YouTube videos (.mp4 format).
Frame extraction: Generate consecutive frames and detect jump cuts using OpenCV's optical flow methods.
Patching: Randomly extract 150x150 patches from frames.
Format: Store patches in .tfrecord files.
Augmentation: Apply rotation, shear, zoom, and shift to 150x150 patches to fit the CNN input size of 128x128.
Model Training:

Optimizer: Adamax with a learning rate of 0.001.
Loss Function: Custom loss combining:
L1 loss.
Perceptual loss from the block4_conv4 layer of VGG19.
Structural Similarity Index (SSIM).
Performance:
L1 loss provides quantitative accuracy.
Custom loss produces visually sharper and higher-quality interpolations (Figure 5).
Challenges:

Large motion between frames results in blocky artifacts.
Fixed input size (128x128) limits performance on high-resolution videos.
Minimal improvements observed with stop-motion animation videos.
Results:

Effective for real-life videos with small motion differences.
Notable improvements visible when videos are slowed down.
Interpolation Results
For consistency in naming conventions:

Original frames: Odd-numbered (e.g., frame 1, frame 3, etc.).
Synthesized frames: Even-numbered (e.g., frame 2).
Sample Outputs
The synthesized frames bridge temporal gaps between input frames, providing smoother playback. For optimal comparison, view the provided interpolated videos below.

Figures
Figure 1: Model Architecture ([1])
Figure 2: Block Diagram
Figure 3: Custom Loss Function Analysis
![image](https://github.com/user-attachments/assets/2b7f6a5b-c5e5-449f-956c-ec5e120834ee)

![image](https://github.com/user-attachments/assets/df9119c1-4574-4f4d-8a5e-8a6fe29eed91)

Figure 5: Visual Comparison of Interpolation Quality
References
[Paper Title and Authors] - Methodology reference for adaptive separable convolution.
Optical Flow Estimation - Techniques from OpenCV for preprocessing.
Structural Similarity Index (SSIM) - Evaluation metric for perceptual quality.

# How to Use
Dataset Preparation:

Use scripts to extract frames and create .tfrecord files.
Ensure augmentation settings align with the model's input requirements.
Model Training:

Train the model using the provided dataset and custom loss function.
Adjust hyperparameters to fine-tune performance.
Evaluation:

Evaluate on real-life videos with small motions for best results.
Generate interpolated videos and analyze quality visually.
