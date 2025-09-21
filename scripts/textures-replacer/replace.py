import json
import os
import sys

def build_face_map(elements, face_map):
    """Recursively collect element faces by name into a dictionary."""
    for elem in elements:
        name = elem.get("name")
        if name and "faces" in elem:
            face_map[name] = elem["faces"]
        if "children" in elem:
            build_face_map(elem["children"], face_map)

def apply_faces(elements, face_map):
    """Recursively apply faces from face_map to matching elements by name."""
    for elem in elements:
        name = elem.get("name")
        if name in face_map:
            elem["faces"] = face_map[name]
        if "children" in elem:
            apply_faces(elem["children"], face_map)

def transfer_faces_to_file(source_face_map, target_file, output_file):
    try:
        with open(target_file, "r", encoding="utf-8") as f:
            target = json.load(f)
    except Exception as e:
        print(f"Skipping {os.path.basename(target_file)}: {e}")
        return

    apply_faces(target.get("elements", []), source_face_map)

    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(target, f, indent=4, ensure_ascii=False)

def transfer_faces(source_file, target_folder, output_folder):
    # Load source file and build face map once
    with open(source_file, "r", encoding="utf-8") as f:
        source = json.load(f)

    source_face_map = {}
    build_face_map(source.get("elements", []), source_face_map)

    # Apply to all target files
    for filename in os.listdir(target_folder):
        if filename.lower().endswith(".json"):
            target_file = os.path.join(target_folder, filename)
            output_file = os.path.join(output_folder, filename)

            transfer_faces_to_file(source_face_map, target_file, output_file)
            print(f"Processed: {filename}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python transfer_faces.py <source_model.json> <target_folder> <output_folder>")
    else:
        transfer_faces(sys.argv[1], sys.argv[2], sys.argv[3])
