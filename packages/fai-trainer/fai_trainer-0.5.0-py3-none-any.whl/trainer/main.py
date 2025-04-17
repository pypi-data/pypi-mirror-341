import argparse
from .data_preparation import prepare_data
from .model_training import train_model, test_model
import shutil
import time
import warnings

warnings.filterwarnings("ignore", category=UserWarning)


def clean_directories():
    print("Cleaning up.")
    for directory in ["./processed_data", "./results"]:
        try:
            shutil.rmtree(directory)
        except FileNotFoundError:
            pass

    while True:
        try:
            for directory in ["./processed_data", "./results"]:
                shutil.rmtree(directory)
        except FileNotFoundError:
            print("Cleaning finished.")
            break
        else:
            print("Waiting for cleaning to finish...")
            time.sleep(1)


def main():
    parser = argparse.ArgumentParser(
        description="Prepare data and train the model.",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    parser.add_argument("--clean", action="store_true", help="Clean run.")
    parser.add_argument("--full-model", action="store_true", help="Use full model.")
    parser.add_argument(
        "--prepare-data",
        action="store_true",
        help="Prepare the dataset for training and testing.",
    )
    parser.add_argument(
        "--train",
        action="store_true",
        help="Train the model with the specified parameters.",
    )
    parser.add_argument("--test", action="store_true", help="Test the trained model.")
    parser.add_argument(
        "--image-path", type=str, help="Path to an image for testing the model."
    )
    parser.add_argument(
        "--dataset-dir",
        type=str,
        default="datasets",
        help="Path to the dataset directory (default: 'datasets').",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=16,
        help="Batch size for training and testing (default: 16).",
    )
    parser.add_argument(
        "--epochs",
        type=int,
        default=5,
        help="Number of epochs for training (default: 5).",
    )
    parser.add_argument(
        "--image-size",
        type=int,
        nargs=2,
        default=(224, 224),
        help="Image dimensions (height, width) (default: (224, 224)).",
    )
    parser.add_argument(
        "--results-dir",
        type=str,
        default="results",
        help="Directory to save results and diagrams (default: 'results').",
    )
    parser.add_argument(
        "--learning-rate",
        type=float,
        default=0.001,
        help="Learning rate for training (default: 0.001).",
    )
    parser.add_argument(
        "--sampling-method",
        type=str,
        choices=["undersample", "oversample"],
        default="undersample",
        help="Sampling method to balance the dataset (default: undersample).",
    )

    args = parser.parse_args()

    if args.clean:
        clean_directories()

    if args.prepare_data:
        print(f"Preparing data in directory: {args.dataset_dir}")
        prepare_data(
            args.dataset_dir,
            image_size=tuple(args.image_size),
            processed_directory="./processed_data",
            sampling_method=args.sampling_method,
        )

    if args.train:
        print("Training model with dataset from: ./processed_data")
        train_model(
            batch_size=args.batch_size,
            epochs=args.epochs,
            image_size=tuple(args.image_size),
            dataset_dir="./processed_data",
            results_dir=args.results_dir,
            learning_rate=args.learning_rate,
        )

    if args.test:
        if args.image_path:
            print(f"Testing model with image: {args.image_path}")
        else:
            print("Testing model with validation dataset.")

        test_model(
            image_path=args.image_path,
            image_size=tuple(args.image_size),
            results_dir=args.results_dir,
            load_full_model=args.full_model,
        )


if __name__ == "__main__":
    main()
