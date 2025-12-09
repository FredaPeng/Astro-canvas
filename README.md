# Stellar Lines: A Lucid Observatory 🌌

> "Start with a line, let the universe complete the picture."

**Stellar Lines** is an interactive web experiment that explores the relationship between human gesture and celestial geometry. Inspired by the [Land Lines](https://lines.chromeexperiments.com/) Chrome Experiment, this project transforms abstract data into a playful, tactile discovery of the cosmos.

[**✨ View Live Project**](https://fredapeng.github.io/Astro-canvas/)

## 🔭 Project Overview

Traditionally, learning astronomy feels academic and rigid. Stellar Lines removes the clutter of textbooks to focus on pure interaction.
- **Visual Style:** "Lucid Space" — A glassmorphic, ethereal UI that feels transparent and focuses on light and geometry.
- **Goal:** To bridge the gap between idle doodles and the ancient constellations defined by the IAU.

## 🚀 Features

### 1. Draw Mode (Gesture Recognition)
Draw any shape—a line, a curve, a hook—and the system uses a **geometric resampling engine** (based on the $1 Unistroke Recognizer algorithm) to analyze your input. It instantly "snaps" your drawing to the nearest matching constellation fragment from the database.
- **Multi-Stroke Support:** Lift your mouse to draw complex shapes like *Centaurus*.
- **Smart Data:** Matches link directly to [NOIRLab](https://noirlab.edu) for educational context.

### 2. Spectrum Mode (Color Discovery)
Explore the universe through the physics of light. Move your cursor to traverse the visible light spectrum (Redshift to Blueshift).
- **Interactive Gradient:** The background shifts from deep infrared-reds to ultraviolet-blues.
- **Telescope Lock:** Double-click a frequency to reveal deep-space photography (Hubble/Webb) corresponding to that chemical color palette.

## 🛠️ Tech Stack

* **Core:** HTML5 Canvas, Vanilla JavaScript (ES6+)
* **Styling:** CSS3 (Backdrop Filter, Glassmorphism)
* **Algorithms:** $1 Unistroke Recognizer (Geometric Matching), Euclidean Distance (Color Matching)
* **Data:** Custom JSON databases for IAU Constellations and NASA/Flickr Image Archives.

## 📦 Installation & Setup

To run this project locally:

1.  **Clone the repository**
    ```bash
    git clone [https://github.com/FredaPeng/Astro-canvas.git](https://github.com/FredaPeng/Astro-canvas.git)
    ```
2.  **Open the project**
    Navigate to the folder and open `index.html` in your browser.
    *Note: For the Fetch API to load JSON data correctly, you may need to run a local server (e.g., Live Server in VS Code).*

## 📚 Credits & Data Sources

* **Inspiration:** [Land Lines](https://lines.chromeexperiments.com/)
* **Constellation Data:** [IAU](https://www.iau.org/) & [NOIRLab](https://noirlab.edu/)
* **Imagery:** NASA, Hubble Heritage Project, James Webb Space Telescope (Flickr)
* **Algorithm:** $1 Unistroke Recognizer (Wobbrock, Wilson, Li)

---
*Created by **Freda Peng** for **IN250: Cosmic Vision/Fall25**
