import piexif
from PIL import Image
import argparse
import os

def inject_exif(image_path, output_path, payload):
    if not os.path.exists(image_path):
        print(f"[!] File not found: {image_path}")
        return

    print(f"📥 Loading image: {image_path}")
    img = Image.open(image_path)

    # If no EXIF, create empty dict
    if "exif" in img.info:
        exif_dict = piexif.load(img.info["exif"])
    else:
        exif_dict = {"0th": {}, "Exif": {}, "GPS": {}, "1st": {}, "thumbnail": None}

    payload_bytes = payload.encode("utf-8")

    # Inject payload into standard EXIF fields
    exif_dict["0th"][piexif.ImageIFD.ImageDescription] = payload_bytes
    exif_dict["Exif"][piexif.ExifIFD.UserComment] = b"ASCII\x00\x00\x00" + payload_bytes

    exif_bytes = piexif.dump(exif_dict)
    img.save(output_path, "jpeg", exif=exif_bytes)
    print(f"💾 Saved modified image to: {output_path}")

def view_exif(image_path):
    if not os.path.exists(image_path):
        print(f"[!] File not found: {image_path}")
        return

    print(f"📂 Viewing EXIF for: {image_path}")
    img = Image.open(image_path)
    if "exif" not in img.info:
        print("[-] No EXIF metadata found.")
        return

    exif_data = piexif.load(img.info["exif"])
    print("🔍 EXIF Metadata:")
    for ifd_name in exif_data:
        if ifd_name == "thumbnail":
            continue
        for tag in exif_data[ifd_name]:
            tag_name = piexif.TAGS[ifd_name][tag]["name"]
            value = exif_data[ifd_name][tag]
            if isinstance(value, bytes):
                try:
                    value = value.decode("utf-8", errors="ignore")
                except:
                    value = value
            print(f" • {tag_name}: {value}")

def main():
    parser = argparse.ArgumentParser(description="📷 EXIF Metadata Injector")
    parser.add_argument("image", help="Input JPEG image path")
    parser.add_argument("output", nargs="?", help="Output image path (for injection)")
    parser.add_argument("--payload", help="Payload/message to inject")
    parser.add_argument("--view", action="store_true", help="Only view existing EXIF metadata")
    args = parser.parse_args()

    if args.view:
        view_exif(args.image)
    elif args.payload and args.output:
        inject_exif(args.image, args.output, args.payload)
    else:
        print("[!] Invalid arguments. Use --help for usage info.")

if __name__ == "__main__":
    main()
