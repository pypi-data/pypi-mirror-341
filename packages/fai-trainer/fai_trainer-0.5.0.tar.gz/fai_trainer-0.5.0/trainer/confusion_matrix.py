import numpy as np
import torch
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
from tqdm import tqdm
import warnings
import os

warnings.filterwarnings("ignore", category=UserWarning)


def get_predictions(model, data_loader, device):
    model.eval()
    all_preds = []
    all_labels = []
    with torch.no_grad():
        for data in tqdm(data_loader):
            inputs, labels = data
            inputs, labels = inputs.to(device), labels.to(device)
            outputs = model(inputs)
            _, preds = torch.max(outputs, 1)
            all_preds.extend(preds.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())
    return all_labels, all_preds


def calculate_scores(cm):
    correct_scores = [cm[i, i] / np.sum(cm[i]) for i in range(len(cm))]
    return correct_scores


def plot_confusion_matrix(actual, preds, class_labels, results_dir):
    cm = confusion_matrix(actual, preds)
    num_classes = len(class_labels)
    scores = calculate_scores(cm)

    fig, ax = plt.subplots(figsize=(12, 12))
    cmap = plt.cm.RdYlGn
    cax = ax.matshow(cm, cmap=cmap)

    for i in range(num_classes):
        for j in range(num_classes):
            color = "white" if i == j else "black"
            ax.text(j, i, str(cm[i, j]), va="center", ha="center", color=color)

    ax.set_xticks(np.arange(num_classes))
    ax.set_yticks(np.arange(num_classes))
    ax.set_xticklabels(class_labels)
    ax.set_yticklabels(class_labels)
    plt.xlabel("Predicted")
    plt.ylabel("Actual")

    def calculate_accuracy(cm):
        return np.trace(cm) / np.sum(cm)

    accuracy = calculate_accuracy(cm)
    str_title = f"Confusion Matrix\n{accuracy * 100:.2f}% accuracy."
    plt.title(str_title)

    legend_handles = [
        plt.Line2D(
            [0], [0], color=cmap(score), lw=4, label=f"{class_labels[i]}: {score:.2f}"
        )
        for i, score in enumerate(scores)
    ]

    legend_handles = sorted(
        legend_handles, key=lambda x: float(x.get_label().split(": ")[1]), reverse=True
    )
    legend = plt.legend(
        handles=legend_handles, loc="upper left", bbox_to_anchor=(1, 1), title="Legend"
    )
    plt.setp(legend.get_texts(), color="black")

    os.makedirs(results_dir, exist_ok=True)
    plt.savefig(f"{results_dir}/confusion_matrix.png", bbox_inches="tight")
    plt.close()

    return f"{results_dir}/confusion_matrix.png"
