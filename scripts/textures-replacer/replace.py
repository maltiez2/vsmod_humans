import json
import sys

def build_face_map(elements, face_map):
    """Recursively collect element faces by name into a dictionary."""
    for elem in elements:
        name = elem.get("name")
        if name and "faces" in elem:
            face_map[name] = elem["faces"]
        # recurse into children
        if "children" in elem:
            build_face_map(elem["children"], face_map)

def apply_faces(elements, face_map):
    """Recursively apply faces from face_map to matching elements by name."""
    for elem in elements:
        name = elem.get("name")
        if name in face_map:
            elem["faces"] = face_map[name]
        # recurse into children
        if "children" in elem:
            apply_faces(elem["children"], face_map)

def transfer_faces(source_file, target_file, output_file):
    # Load source and target JSON files
    with open(source_file, "r", encoding="utf-8") as f:
        source = json.load(f)
    with open(target_file, "r", encoding="utf-8") as f:
        target = json.load(f)

    # Build mapping of element name -> faces
    face_map = {}
    build_face_map(source.get("elements", []), face_map)

    # Apply to target
    apply_faces(target.get("elements", []), face_map)

    # Save result
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(target, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python transfer_faces.py source.json target.json output.json")
    else:
        transfer_faces(sys.argv[1], sys.argv[2], sys.argv[3])
