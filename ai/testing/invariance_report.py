import os
import re
import cv2
import numpy as np
import matplotlib.pyplot as plt


RESULT_DIR = r"D:\SIH26166\Result\invariance"
REPORT_DIR = os.path.join(RESULT_DIR, "combined")

os.makedirs(REPORT_DIR, exist_ok=True)


# RESULTS FROM OUR TESTS


scale_results = {
    "0.5x": 0.887,
    "0.75x": 0.969,
    "1.5x": 0.976,
    "2.0x": 0.975
}

rotation_results = {
    "-90°": 0.979,
    "-45°": 0.953,
    "-30°": 0.974,
    "-15°": 0.969,
    "15°": 0.967,
    "30°": 0.953,
    "45°": 0.969,
    "90°": 0.982
}

illumination_results = {
    "Very Dark": 0.550,
    "Dark": 0.854,
    "Slightly Dark": 0.971,
    "Bright": 0.990,
    "Very Bright": 0.988
}



# PRINT SUMMARY


print("=" * 65)
print("          SIH26166 INVARIANCE PERFORMANCE REPORT")
print("=" * 65)


print("\nSCALE INVARIANCE")
print("-" * 40)

for condition, ratio in scale_results.items():
    print(
        f"{condition:15s} : {ratio * 100:.1f}%"
    )


print("\nROTATION INVARIANCE")
print("-" * 40)

for condition, ratio in rotation_results.items():
    print(
        f"{condition:15s} : {ratio * 100:.1f}%"
    )


print("\nILLUMINATION INVARIANCE")
print("-" * 40)

for condition, ratio in illumination_results.items():
    print(
        f"{condition:15s} : {ratio * 100:.1f}%"
    )



# AVERAGES


scale_average = np.mean(
    list(scale_results.values())
)

rotation_average = np.mean(
    list(rotation_results.values())
)

illumination_average = np.mean(
    list(illumination_results.values())
)


print("\nAVERAGE PERFORMANCE")
print("-" * 40)

print(
    "Scale Average       :",
    f"{scale_average * 100:.2f}%"
)

print(
    "Rotation Average    :",
    f"{rotation_average * 100:.2f}%"
)

print(
    "Illumination Average:",
    f"{illumination_average * 100:.2f}%"
)



# SAVE TEXT REPORT


report_path = os.path.join(
    REPORT_DIR,
    "invariance_report.txt"
)

with open(
    report_path,
    "w",
    encoding="utf-8"
) as file:

    file.write(
        "SIH26166 INVARIANCE PERFORMANCE REPORT\n"
    )

    file.write("=" * 65 + "\n\n")

    file.write("SCALE INVARIANCE\n")
    file.write("-" * 40 + "\n")

    for condition, ratio in scale_results.items():

        file.write(
            f"{condition:15s} : "
            f"{ratio * 100:.1f}%\n"
        )

    file.write("\nROTATION INVARIANCE\n")
    file.write("-" * 40 + "\n")

    for condition, ratio in rotation_results.items():

        file.write(
            f"{condition:15s} : "
            f"{ratio * 100:.1f}%\n"
        )

    file.write("\nILLUMINATION INVARIANCE\n")
    file.write("-" * 40 + "\n")

    for condition, ratio in illumination_results.items():

        file.write(
            f"{condition:15s} : "
            f"{ratio * 100:.1f}%\n"
        )

    file.write("\nAVERAGE PERFORMANCE\n")
    file.write("-" * 40 + "\n")

    file.write(
        f"Scale Average: "
        f"{scale_average * 100:.2f}%\n"
    )

    file.write(
        f"Rotation Average: "
        f"{rotation_average * 100:.2f}%\n"
    )

    file.write(
        f"Illumination Average: "
        f"{illumination_average * 100:.2f}%\n"
    )



# CREATE GRAPH 1 — SCALE


plt.figure(figsize=(8, 5))

plt.plot(
    list(scale_results.keys()),
    [x * 100 for x in scale_results.values()],
    marker="o"
)

plt.xlabel("Scale")
plt.ylabel("Inlier Ratio (%)")
plt.title("SIFT Scale Invariance")

plt.ylim(0, 105)
plt.grid(True)

scale_graph = os.path.join(
    REPORT_DIR,
    "scale_invariance.png"
)

plt.savefig(
    scale_graph,
    dpi=200,
    bbox_inches="tight"
)

plt.close()



# CREATE GRAPH 2 — ROTATION


plt.figure(figsize=(9, 5))

plt.plot(
    list(rotation_results.keys()),
    [x * 100 for x in rotation_results.values()],
    marker="o"
)

plt.xlabel("Rotation Angle")
plt.ylabel("Inlier Ratio (%)")
plt.title("SIFT Rotation Invariance")

plt.ylim(0, 105)
plt.grid(True)

rotation_graph = os.path.join(
    REPORT_DIR,
    "rotation_invariance.png"
)

plt.savefig(
    rotation_graph,
    dpi=200,
    bbox_inches="tight"
)

plt.close()



# CREATE GRAPH 3 — ILLUMINATION


plt.figure(figsize=(9, 5))

plt.plot(
    list(illumination_results.keys()),
    [x * 100 for x in illumination_results.values()],
    marker="o"
)

plt.xlabel("Illumination Condition")
plt.ylabel("Inlier Ratio (%)")
plt.title("SIFT Illumination Invariance")

plt.ylim(0, 105)
plt.grid(True)

illumination_graph = os.path.join(
    REPORT_DIR,
    "illumination_invariance.png"
)

plt.savefig(
    illumination_graph,
    dpi=200,
    bbox_inches="tight"
)

plt.close()



# FINAL


print("\n" + "=" * 65)
print("REPORT GENERATED SUCCESSFULLY")
print("=" * 65)

print("\nText report:")
print(report_path)

print("\nGraphs:")

print(scale_graph)
print(rotation_graph)
print(illumination_graph)