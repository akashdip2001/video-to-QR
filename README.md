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

![Screenshot (665)](https://github.com/user-attachments/assets/69783636-fd28-4831-8e31-b98a8bb5e126)
![Screenshot (664)](https://github.com/user-attachments/assets/5600f15a-db53-400e-be57-f37403c30533)
![Screenshot (667)](https://github.com/user-attachments/assets/ad353b4b-65bb-4ccc-b614-48da0fc6972c)

---

## 📚 **Conclusion**

**QRVideoSlicer** is a unique, practical tool built for modern-day versioning and distribution challenges involving large video files. Its focus on interactivity, automation, and data preservation makes it ideal for learning purposes and real-world utility.
