import os
import cv2
import yaml
import shutil
import numpy as np
import matplotlib.pyplot as plt
from ultralytics import YOLO

# Function to list directory tree
def list_directory_tree_with_os_walk(starting_directory):
    for root, directories, files in os.walk(starting_directory):
        print(f"Directory: {root}")

# Function to preprocess bounding box data
def preprocess_bbox(bbox_data, img_height, img_width):
    bbox_data = bbox_data.strip('\n')
    # class, bbox center x, bbox center y, h, w
    _, x, y, w, h = map(float, bbox_data.split(" "))
    x1 = int((x - w / 2) * img_width)
    x2 = int((x + w / 2) * img_width)
    y1 = int((y - h / 2) * img_height)
    y2 = int((y + h / 2) * img_height)
    return [x1, y1, x2, y2]

# Function to plot labeled data
def plot_labeled_data(mode='train', img_data_path=None, label_data_path=None):
    if img_data_path is None or label_data_path is None:
        raise ValueError("img_data_path and label_data_path must be provided.")

    fig = plt.figure(figsize=(20, 20))
    rows = 4
    columns = 4

    imgs_list = os.listdir(img_data_path)
    labels_list = os.listdir(label_data_path)

    for i, img_name in enumerate(imgs_list[:16]):
        img = cv2.imread(os.path.join(img_data_path, img_name))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_h, img_w, _ = img.shape

        label_path = os.path.join(label_data_path, img_name[:-3] + 'txt')
        if os.path.exists(label_path):
            with open(label_path, 'r') as fl:
                data = fl.readlines()
                for d in data:
                    bbox = preprocess_bbox(d, img_h, img_w)
                    cv2.rectangle(img=img, pt1=(bbox[0], bbox[1]), pt2=(bbox[2], bbox[3]), color=(255, 0, 155), thickness=2)
            fig.add_subplot(rows, columns, i + 1)
            plt.imshow(img)
    plt.show()

# Function to plot predicted data
def plot_predicted_data(predicted):
    fig = plt.figure(figsize=(20, 20))
    rows = 4
    columns = 4

    for i, pred in enumerate(predicted[:16]):
        img_path = pred.path
        bboxes = pred.boxes.xyxy

        img = cv2.imread(img_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_h, img_w, _ = img.shape

        for bbox in bboxes:
            bbox = [int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])]
            cv2.rectangle(img=img, pt1=(bbox[0], bbox[1]), pt2=(bbox[2], bbox[3]), color=(255, 0, 155), thickness=2)
        fig.add_subplot(rows, columns, i + 1)
        plt.imshow(img)
    plt.show()

# Main function to run the license plate detection pipeline
def main():
    # Set dataset paths
    dataset_path = '/Users/zaphodschmidt/.cache/kagglehub/datasets/fareselmenshawii/large-license-plate-dataset/versions/1'
    working_dir = '/Users/zaphodschmidt/working_dataset'

    # Create working directory if it doesn't exist
    os.makedirs(working_dir, exist_ok=True)

    # Copy dataset to working directory
    shutil.copytree(f'{dataset_path}/images/train/', f'{working_dir}/train/images', dirs_exist_ok=True)
    shutil.copytree(f'{dataset_path}/labels/train/', f'{working_dir}/train/labels', dirs_exist_ok=True)
    shutil.copytree(f'{dataset_path}/images/val/', f'{working_dir}/validation/images', dirs_exist_ok=True)
    shutil.copytree(f'{dataset_path}/labels/val/', f'{working_dir}/validation/labels', dirs_exist_ok=True)
    shutil.copytree(f'{dataset_path}/images/test/', f'{working_dir}/test/images', dirs_exist_ok=True)
    shutil.copytree(f'{dataset_path}/labels/test/', f'{working_dir}/test/labels', dirs_exist_ok=True)

    # List directory tree
    list_directory_tree_with_os_walk(working_dir)

    # Create YAML configuration file
    training_config = {
        "path": working_dir,
        "train": "train/images",
        "val": "validation/images",
        "test": "test/images",
        "names": {0: "license_plate"}
    }
    with open('data.yaml', 'w') as yaml_file:
        yaml.dump(training_config, yaml_file, sort_keys=False)

    # Plot labeled data
    plot_labeled_data(mode='train', img_data_path=f'{working_dir}/train/images', label_data_path=f'{working_dir}/train/labels')
    plot_labeled_data(mode='test', img_data_path=f'{working_dir}/test/images', label_data_path=f'{working_dir}/test/labels')

    # Load YOLOv8 model
    model = YOLO("yolov8n.pt")

    # Train the model
    results = model.train(data="data.yaml", epochs=5, imgsz=640, patience=10)

    # Evaluate the model
    metrics = model.val(data='data.yaml', split='test', conf=0.15, iou=0.3)
    print(f"mAP50-95: {metrics.box.map}")
    print(f"mAP50: {metrics.box.map50}")

    # Make predictions
    predicted = model.predict(source=f'{working_dir}/test/images', conf=0.15, iou=0.3, classes=[0])

    # Plot predicted data
    plot_predicted_data(predicted)

    # Export the model
    model.export(format='onnx')  # Export to ONNX format
    model.save('best_model_NPT.pt')  # Save the PyTorch model

# Run the main function
if __name__ == "__main__":
    main()