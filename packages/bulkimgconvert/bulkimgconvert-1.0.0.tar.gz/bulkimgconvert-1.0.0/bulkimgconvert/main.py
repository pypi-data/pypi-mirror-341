import argparse
from bulkimgconvert.converter import convert_images


def main():
    parser = argparse.ArgumentParser(description="Bulk Image Converter")
    parser.add_argument('--input', type=str, required=True, help='Path to input folder')
    parser.add_argument('--output', type=str, required=True, help='Path to output folder')
    parser.add_argument('--format', type=str, required=True, choices=['JPEG', 'PNG', 'WEBP'], help='Output format')
    parser.add_argument('--resize', nargs=2, type=int, metavar=('width', 'height'), help='Resize dimensions (width height)')
    parser.add_argument('--quality', type=int, default=85, help='Compression quality (default: 85)')

    args = parser.parse_args()

    resize = tuple(args.resize) if args.resize else None

    convert_images(
        input_folder=args.input,
        output_folder=args.output,
        format=args.format,
        resize=resize,
        quality=args.quality
    )

if __name__ == "__main__":
    main()
