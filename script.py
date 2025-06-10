import os
import base64
import json
import shutil
import subprocess
import sys
import time

CHUNK_SIZE = 2000
QR_VERSION = 40
QR_BOX_SIZE = 10

HEADER_FILENAME = "header.json"
OUTPUT_DIR = "output"
REQUIRED_MODULES = ["qrcode", "Pillow", "tqdm", "pyzbar", "opencv-python"]

MODULE_IMPORT_MAP = {
    "Pillow": "PIL"
}

def install_missing_modules():
    print("\nChecking and installing required Python modules...")
    for module in REQUIRED_MODULES:
        import_name = MODULE_IMPORT_MAP.get(module, module)
        try:
            __import__(import_name)
        except ImportError:
            print(f"Installing missing module: {module}")
            subprocess.check_call([sys.executable, "-m", "pip", "install", module])

def ensure_python():
    if shutil.which("python") is None:
        print("Python not found on system. Please install Python manually.")
        sys.exit(1)

def encode_video_to_qr(video_path):
    import qrcode
    from PIL import Image
    from tqdm import tqdm

    with open(video_path, 'rb') as f:
        video_data = f.read()

    b64_data = base64.b64encode(video_data).decode('utf-8')
    chunks = [b64_data[i:i+CHUNK_SIZE] for i in range(0, len(b64_data), CHUNK_SIZE)]
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    out_dir = os.path.join(os.getcwd(), video_name)
    os.makedirs(out_dir, exist_ok=True)

    print(f"\nEncoding video to QR in: {out_dir}")

    for i, chunk in enumerate(tqdm(chunks)):
        qr = qrcode.QRCode(version=QR_VERSION, box_size=QR_BOX_SIZE, border=2)
        qr.add_data(chunk)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(os.path.join(out_dir, f"chunk_{i:05d}.png"))

    header = {
        "video_name": os.path.basename(video_path),
        "num_chunks": len(chunks),
        "chunk_size": CHUNK_SIZE,
        "encoding": "base64"
    }

    with open(os.path.join(out_dir, HEADER_FILENAME), 'w') as f:
        json.dump(header, f)

    shutil.copy(__file__, os.path.join(out_dir, "export_here.py"))
    print("\nEncoding complete. Header and QR codes saved.")

    print("\nDo you want to delete the original video? (yes/no) [Default: no] (Respond within 3 seconds)")
    user_input = input_with_timeout(3, default='no')
    if user_input.lower() == 'yes':
        os.remove(video_path)
        print("Original video deleted.")
    else:
        print("Original video retained.")

def decode_qr_to_video(folder_path):
    from PIL import Image
    from tqdm import tqdm

    header_path = os.path.join(folder_path, HEADER_FILENAME)
    if not os.path.exists(header_path):
        print("Header file not found.")
        return

    with open(header_path, 'r') as f:
        header = json.load(f)

    chunks = []
    print("Reading QR code images...")
    for i in tqdm(range(header['num_chunks'])):
        img_path = os.path.join(folder_path, f"chunk_{i:05d}.png")
        if not os.path.exists(img_path):
            print(f"Missing chunk image: {img_path}")
            return
        img = Image.open(img_path)
        decoded = decode_qr_image(img)
        chunks.append(decoded)

    full_b64 = ''.join(chunks)
    video_bytes = base64.b64decode(full_b64)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    out_video_name = f"output_{header['video_name']}"
    out_video_path = os.path.join(OUTPUT_DIR, out_video_name)
    with open(out_video_path, 'wb') as f:
        f.write(video_bytes)

    print(f"\nVideo reconstructed at {out_video_path}")

    choice = input("Do you want to delete the image folder? (yes/no): ").strip().lower()
    if choice == 'yes':
        shutil.rmtree(folder_path)
        print("Folder deleted.")
    else:
        print("Folder retained.")

def decode_qr_image(image):
    from pyzbar.pyzbar import decode
    decoded = decode(image)
    if not decoded:
        raise ValueError("No QR code found in image.")
    return decoded[0].data.decode('utf-8')

def input_with_timeout(timeout, default):
    print(f"You have {timeout} seconds to respond...")
    start_time = time.time()
    user_input = ''
    while (time.time() - start_time) < timeout and not user_input:
        if os.name == 'nt':
            import msvcrt
            if msvcrt.kbhit():
                user_input = input()
                break
        else:
            import select
            if select.select([sys.stdin], [], [], timeout)[0]:
                user_input = input()
                break
        time.sleep(0.1)
    return user_input.strip() if user_input else default

def cleanup_dependencies():
    print("\nDo you want to remove installed dependencies? (yes/no) [Default: no] (Respond within 3 seconds)")
    user_input = input_with_timeout(3, default='no')
    if user_input.lower() == 'yes':
        for module in REQUIRED_MODULES:
            print(f"Uninstalling {module}...")
            subprocess.call([sys.executable, "-m", "pip", "uninstall", "-y", module])
        print("Dependencies removed.")
    else:
        print("Dependencies retained.")

def main():
    ensure_python()
    install_missing_modules()

    print("\n1. Convert video to QR code")
    print("2. Export video from QR code")
    choice = input("Select option [1/2]: ").strip()

    if choice == '1':
        files = [f for f in os.listdir('.') if f.lower().endswith(('.mp4', '.mkv', '.mov'))]
        if not files:
            print("No video files found in current directory.")
            return
        print("\nAvailable video files:")
        for i, f in enumerate(files):
            print(f"{i+1}. {f}")
        selected = int(input("Select video to convert: ")) - 1
        encode_video_to_qr(files[selected])

    elif choice == '2':
        folders = [f for f in os.listdir('.') if os.path.isdir(f) and HEADER_FILENAME in os.listdir(f)]
        if not folders:
            print("No valid QR folders found.")
            return
        print("\nAvailable QR code folders:")
        for i, f in enumerate(folders):
            print(f"{i+1}. {f}")
        selected = int(input("Select folder to decode: ")) - 1
        decode_qr_to_video(folders[selected])

    else:
        print("Invalid option.")

    cleanup_dependencies()

if __name__ == '__main__':
    main()
