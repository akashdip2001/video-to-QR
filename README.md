# 🧠 video-to-QR : **`QRVideoSlicer`**

---

## 📄 **Project Description**

**QRVideoSlicer** is a Python-based tool that allows users to **split large video files into QR code images**, making it possible to store and share videos within size-limited platforms (e.g., GitHub’s 25MB file limit). Each QR code contains a chunk of the encoded video, and a header file maps the order and metadata.

> The same tool can then be used to **reconstruct the original video** from these QR codes. This makes the system ideal for scenarios where videos need to be archived or transferred in limited environments.

![idea](https://github.com/user-attachments/assets/28f2a94a-73c5-4190-8f79-c21592bbe1ba)

---

## ✅ **Key Features**

* 🧩 **Split large videos** into compressed QR code chunks.
* 📁 **Folder-wise organization** of QR images for each video.
* 📜 **Header file** ensures correct reassembly of videos.
* ⚡ **Interactive script** with options: Convert or Reassemble.
* 🗑️ Prompts to delete original video or uninstall dependencies after use.
* 🧪 Auto-check and install dependencies.

---

## 📂 **Directory Structure**

```
project_root/
├── Video to QR.py         # Main interactive script
├── output/                # Reconstructed videos
├── MyVideo.mp4            # Input video file
├── MyVideo/               # Folder with QR images and header
│   ├── chunk_00000.png
│   ├── chunk_00001.png
│   ├── ...
│   ├── header.json
│   └── export_here.py     # Auto-reassemble script
```

---

## 🔄 **Workflow Diagram**

```text
          +------------------+
          |   Input Video    |
          +--------+---------+
                   |
                   v
         +---------------------+
         | QRVideoSlicer Tool  |
         | [1] Convert Video   |
         | [2] Export Video    |
         +---+-----------+----+
             |           |
   +---------+           +---------+
   |                             |
+--v--+                     +----v-----+
| QR  |                     | Rebuild  |
| Img |                     | Video    |
| Set |                     +----+-----+
+-----+                          |
                          +-----v------+
                          | output.mp4 |
                          +------------+
```

---

## 🧪 **Code Snippets and How They Work ??**

### 🔹 1. Splitting video into QR chunks

```python
with open("MyVideo.mp4", 'rb') as f:
    video_data = f.read()

# Encode video to base64
b64_data = base64.b64encode(video_data).decode('utf-8')

# Split into smaller chunks
chunks = [b64_data[i:i+CHUNK_SIZE] for i in range(0, len(b64_data), CHUNK_SIZE)]
```

> **What it does**: Reads the video file and splits it into chunks small enough to fit into individual QR codes.

---

### 🔹 2. Creating QR codes from chunks

```python
for i, chunk in enumerate(chunks):
    qr = qrcode.QRCode(version=40, box_size=10, border=2)
    qr.add_data(chunk)
    img = qr.make_image()
    img.save(f"chunk_{i:05d}.png")
```

> **What it does**: Each base64 chunk is converted into a high-capacity QR code image and saved.

---

### 🔹 3. Header file to store metadata

```python
header = {
    "video_name": "MyVideo.mp4",
    "num_chunks": len(chunks),
    "chunk_size": 2000,
    "encoding": "base64"
}
with open("header.json", 'w') as f:
    json.dump(header, f)
```

> **What it does**: Stores necessary info for reconstructing the video later, including number of QR codes and original filename.

---

### 🔹 4. Reconstructing video from QR codes

```python
# Load header metadata
with open("header.json") as f:
    meta = json.load(f)

# Read and decode all QR images
video_data = ''
for i in range(meta['num_chunks']):
    image = Image.open(f"chunk_{i:05d}.png")
    decoded = decode(image)[0].data.decode('utf-8')
    video_data += decoded

# Convert back to binary video
with open(f"output_{meta['video_name']}", 'wb') as f:
    f.write(base64.b64decode(video_data))
```

> **What it does**: Sequentially decodes all QR codes, concatenates their data, and writes the result as the reconstructed video.

---

## 💻 **How to Use**

1. **Place video file in script directory**

2. Run the script:

   ```bash
   python "Video to QR.py"
   ```

3. Choose:

   * `[1]` Convert to QR codes
   * `[2]` Export video from QR codes

4. Follow prompts to delete original video or clean up environment.

</br>
</br>
</br>
<div style="display: flex; align-items: center; gap: 10px;" align="center">
  
# ⭐ Video to QR ⭐
</div>

</br>
</br>

![Screenshot (665)](https://github.com/user-attachments/assets/69783636-fd28-4831-8e31-b98a8bb5e126)
![Screenshot (664)](https://github.com/user-attachments/assets/5600f15a-db53-400e-be57-f37403c30533)
![Screenshot (667)](https://github.com/user-attachments/assets/ad353b4b-65bb-4ccc-b614-48da0fc6972c)

---

</br>
</br>
<div style="display: flex; align-items: center; gap: 10px;" align="center">
  
# ⭐ QR to Video ⭐
</div>

</br>
</br>

https://github.com/user-attachments/assets/39cbb3f1-90d2-41ba-9308-02f75f32aade

</br>

> The warnings you're seeing — like:

```python
WARNING: zbar\decoder\databar.c:1250: <unknown>: Assertion "seg->finder >= 0" failed.
```

— are **coming from the `pyzbar` library**, which uses **ZBar**, a C-based QR/barcode scanner. These warnings typically occur when ZBar **fails to recognize a QR code** or **interprets image data as an invalid code**.

---

### ✅ The Script *Is Working* — ⚠️ But with Errors:

These warnings don't immediately crash the script, but they likely indicate that:

1. **Some QR code images aren't being decoded properly.**
2. **May end up with a corrupted output video**, or the script may fail later due to a missing or unreadable chunk.

---

### 🔍 Common Causes & Fixes:

#### 1. **QR Codes Are Too Dense or Large**

* You are using:

  ```python
  QR_VERSION = 40
  QR_BOX_SIZE = 10
  ```

  QR version 40 holds a lot of data — nearly **3KB per code** — and becomes **visually complex**, especially for `pyzbar` to decode correctly.

  ✅ **Fix**: **Reduce `QR_VERSION`** to something like 20–30, and increase `QR_BOX_SIZE` to 12–15 for better clarity.

#### 2. **Image Format or Compression**

* Saving in PNG is fine, but any post-processing or compression (e.g., if opened and resaved) may affect readability.

  ✅ **Fix**: Ensure the images remain untouched between encode and decode.

#### 3. **Switch to More Reliable QR Decoder**

* `pyzbar` is sometimes less accurate with large, complex QR codes.
* **Alternative**: Use `opencv-python` and `cv2.QRCodeDetector`, which can decode with more robustness.

---

### 🛠 Recommended Fixes (Code-Level)

Here’s how can **improve decoding**: (open source contributors)

#### 🔁 Update `decode_qr_image()` to Use OpenCV (Fallback or Primary)

```python
def decode_qr_image(image):
    import cv2
    import numpy as np
    from pyzbar.pyzbar import decode as pyzbar_decode

    try:
        # Try pyzbar first
        result = pyzbar_decode(image)
        if result:
            return result[0].data.decode('utf-8')
    except Exception:
        pass

    # Fallback to OpenCV QR detection
    img_array = np.array(image.convert('RGB'))
    detector = cv2.QRCodeDetector()
    data, _, _ = detector.detectAndDecode(img_array)
    if data:
        return data
    raise ValueError("QR decoding failed with both pyzbar and OpenCV.")
```

#### ⚙️ Tune QR Generation (Optional but Strongly Recommended)

In your `encode_video_to_qr()`:

```python
# Try reducing version and increasing box size for easier scanning
QR_VERSION = 30  # instead of 40
QR_BOX_SIZE = 12  # bigger boxes = easier decode
```

---

## 📚 **Conclusion**

**QRVideoSlicer** is a unique, practical tool built for modern-day versioning and distribution challenges involving large video files. Its focus on interactivity, automation, and data preservation makes it ideal for learning purposes and real-world utility.
