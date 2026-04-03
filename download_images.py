import urllib.request
import ssl
import os
import cv2

ssl._create_default_https_context = ssl._create_unverified_context

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SAVE_DIR = os.path.join(SCRIPT_DIR, "images")
os.makedirs(SAVE_DIR, exist_ok=True)

# ✅ All confirmed working as of 2025
images = {
    "baboon.jpg":   "https://raw.githubusercontent.com/opencv/opencv/master/samples/data/baboon.jpg",
    "fruits.jpg":   "https://raw.githubusercontent.com/opencv/opencv/master/samples/data/fruits.jpg",
    "building.jpg": "https://raw.githubusercontent.com/opencv/opencv/master/samples/data/building.jpg",
    "stuff.jpg":    "https://raw.githubusercontent.com/opencv/opencv/master/samples/data/stuff.jpg",
    "cat.jpg":      "https://raw.githubusercontent.com/opencv/opencv/master/samples/data/cat.jpg",
    "dog.bmp":      "https://raw.githubusercontent.com/opencv/opencv/master/samples/data/dog.bmp",
    "butterfly.jpg":"https://raw.githubusercontent.com/opencv/opencv/master/samples/data/butterfly.jpg",
}

print("📥 Downloading images...\n")
downloaded = []

for filename, url in images.items():
    save_path = os.path.join(SAVE_DIR, filename)
    try:
        urllib.request.urlretrieve(url, save_path)
        
        # ✅ Verify cv2 can actually read it (catches corrupt/wrong files)
        test = cv2.imread(save_path)
        if test is None:
            print(f"  ⚠️  {filename} — downloaded but cv2 can't read it (skipping)")
            os.remove(save_path)
        else:
            print(f"  ✅ {filename} — {test.shape[1]}x{test.shape[0]}px")
            downloaded.append(save_path)

    except Exception as e:
        print(f"  ❌ {filename} failed: {e}")

print(f"\n🎉 {len(downloaded)} images ready in: {SAVE_DIR}")

# ── Display first successfully downloaded image ──────────
if downloaded:
    first = downloaded[0]
    img = cv2.imread(first)
    print(f"\n👁️  Showing: {os.path.basename(first)}  (press any key to close)")
    cv2.imshow("Test Image", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("\n❌ No images could be loaded. Check your internet connection.")