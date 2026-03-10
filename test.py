input_file = "assets/king.obj"
output_file = "model_centered.obj"

vertices = []
lines = []

with open(input_file) as f:
    for line in f:
        lines.append(line)
        if line.startswith("v "):
            _, x, y, z = line.split()[:4]
            vertices.append((float(x), float(y), float(z)))

with open(output_file, "w") as out:
    for line in lines:
        if line.startswith("v "):
            parts = line.split()
            y = float(parts[2]) + 0.1
            out.write(f"v {x} {y} {z}\n")
        else:
            out.write(line)

print("Arquivo salvo:", output_file)