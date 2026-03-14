# 🚀 Area Sensing YOLOv8n

A real-time **AI area monitoring system** built using **YOLOv8n, Python, and OpenCV**.  
The system allows users to **draw custom monitoring areas using the mouse**, and **object detection works only inside the selected region**.

This project demonstrates how AI-based object detection can be combined with **interactive area selection** for smart monitoring systems.

Possible applications:

🏫 Smart classroom monitoring  
🏭 Industrial safety zones  
🚧 Restricted area detection  
🚗 Parking monitoring  
🛒 Smart surveillance systems  

---

# 📂 Project Structure

```
area-sensing-yolov8n
│
├── LICENSE
├── README.md
├── area sensing yolov8n.py
└── yolov8n.pt
```

| File | Description |
|-----|-------------|
| area sensing yolov8n.py | Main Python program |
| yolov8n.pt | YOLOv8n pretrained detection model |
| README.md | Project documentation |
| LICENSE | Project license |

---

# ⚙️ Installation

## 1️⃣ Clone the Repository

```
git clone https://github.com/rsamwilson2323-cloud/area-sensing-yolov8n.git
cd area-sensing-yolov8n
```

---

## 2️⃣ Install Python

Make sure **Python 3.8 or higher** is installed.

Check version:

```
python --version
```

---

## 3️⃣ Install Required Libraries

```
pip install ultralytics opencv-python numpy torch torchvision
```

---

# 📦 Requirements

```
ultralytics
opencv-python
numpy
torch
torchvision
```

| Library | Purpose |
|------|------|
| ultralytics | YOLOv8 object detection |
| opencv-python | camera processing and mouse interaction |
| numpy | coordinate calculations |
| torch | deep learning framework |
| torchvision | model support |

---

# ▶️ Running The Program

Run the main file:

```
python "area sensing yolov8n.py"
```

After running:

📷 Camera window will open  
🖱 You can draw the sensing area using the mouse  

---

# 🖱 Creating The Monitoring Area

The system allows users to create different **area shapes**.

Supported area types:

✏ Free Line Area  
⭕ Circle Area  
⬛ Rectangle / Square Area  

Object detection will **only work inside the selected area**.

---

# ✏ Free Line Area

Used to draw **custom irregular monitoring regions**.

### Steps

1️⃣ Click the **Left Mouse Button** to place points.  
2️⃣ Each click creates a **line segment connecting the previous point**.  
3️⃣ Continue clicking to form the desired boundary.  
4️⃣ Once the shape forms a loop, **Right Click above the line to finish the area**.

This creates a **closed custom region** that will be used as the sensing zone.

Examples:

• irregular restricted areas  
• classroom sections  
• custom surveillance boundaries  

---

# ⭕ Circle Area

Used to create a **circular sensing region**.

### Steps

1️⃣ Click the center position  
2️⃣ Drag outward to define the radius  
3️⃣ Release the mouse to create the circle

Useful for:

• machine safety radius  
• round monitoring areas  
• focus zones

---

# ⬛ Rectangle / Square Area

Used to create **rectangular monitoring zones**.

### Steps

1️⃣ Click the first corner  
2️⃣ Drag the mouse diagonally  
3️⃣ Release to finalize the rectangle

Common uses:

• door monitoring  
• entrance detection  
• parking detection

---

# ↩️ Undo Drawing

If a mistake happens:

```
Press Z
```

The **last drawn shape will be removed**.

---

# ↪️ Redo Drawing

If undo was accidental:

```
Press Y
```

The removed shape will **appear again**.

---

# 🎯 Detection Inside Selected Area

The program uses **YOLOv8n object detection**.

Detection process:

1️⃣ YOLO detects objects in the camera frame.

2️⃣ The center of each detected bounding box is calculated.

```
center_x = x + width/2
center_y = y + height/2
```

3️⃣ The program checks if the **center point lies inside the selected area**.

4️⃣ If inside the region:

```
Object is detected and displayed
```

5️⃣ If outside the region:

```
Object is ignored
```

This ensures detection occurs **only within the selected monitoring zone**.

---

# 🧠 YOLOv8n Model

The project uses:

```
yolov8n.pt
```

YOLOv8n is the **Nano version of YOLOv8**, designed for:

⚡ Fast inference  
🪶 Lightweight performance  
💻 CPU-friendly execution  
📷 Real-time detection  

---

# 🖥 Output

The system displays:

📷 Live camera feed  
🟩 Selected monitoring region  
📦 Detected objects inside the region  
🏷 Object labels and bounding boxes  

Objects **outside the sensing region are ignored**.

---

# ❌ Ending The Program

To safely exit the program:

```
Press ENTER
```

The camera window will close and the program will terminate.

---

# 🧩 Technologies Used

| Technology | Purpose |
|------|------|
| Python | main programming language |
| YOLOv8n | object detection |
| OpenCV | camera processing and drawing |
| PyTorch | deep learning backend |
| NumPy | coordinate calculations |

---

# ⭐ Features

✅ Custom area detection  
✅ Multiple drawing tools  
✅ Mouse-based interface  
✅ Undo and Redo drawing  
✅ Real-time YOLOv8 detection  
✅ Detection limited to selected region  

---

# 👨‍💻 Author

**Sam Wilson**

📧 Email: rsamwilson2323@gmail.com  
🌐 GitHub: https://github.com/rsamwilson2323-cloud  
💼 LinkedIn: https://www.linkedin.com/in/sam-wilson-14b554385

---

# 📜 License

This project is licensed under the terms provided in the **LICENSE** file.

---
