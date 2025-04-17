from transformers import AutoImageProcessor, AutoModelForSemanticSegmentation, TrainingArguments, Trainer
from sklearn.metrics import precision_score, recall_score, f1_score
import numpy as np
import pandas as pd
import torch
from torch import nn
import evaluate
import matplotlib.pyplot as plt


class Model:
    def __init__(self, id2label, label2id,
                 checkpoint_train="nvidia/mit-b0",
                 name_evaluate="mean_iou"):
        self.id2label = id2label
        self.label2id = label2id
        self.lenLabel = len(id2label)
        self.chackpoint_train = checkpoint_train
        self.processor = AutoImageProcessor.from_pretrained(checkpoint_train)
        self.model = AutoModelForSemanticSegmentation.from_pretrained(
            checkpoint_train, id2label=id2label, label2id=label2id)
        self.metric = evaluate.load(name_evaluate)
        self.history_evaluasi = []

    def transform_area(self, example_batch):
        """
        deskripsi : fungsi untuk transformasi area

        Args:
            example_batch (_dict_): berisi dataset

        Returns:
            _dict_: berisi dataset yang terdiri dari pixel_values dan label
        """
        images = [x for x in example_batch['image']]
        labels = [x for x in example_batch['label']]
        inputs = self.processor(images, labels)
        return inputs

    def dataset_transform_area(self, dataset):
        """
        deskripsi : fungsi untuk transformasi dataset

        Args:
            dataset (_dict_): berisi dataset

        Returns:
            _dict_: berisi dataset yang terdiri dari train dan validasi
        """
        train_ds = dataset['train']
        validasi_ds = dataset['validasi']

        train_ds.set_transform(self.transform_area)
        validasi_ds.set_transform(self.transform_area)

        return {
            'train': train_ds,
            'validasi': validasi_ds
        }

    # di peruntukan untuk penggunaan training model
    def compute_metrics(self, eval_pred):
        """
        descripsi : fungsi untuk menghitung metric

        Args:
            eval_pred (_tuple_): terdiri dari logits dan label yang akan dihitung

        Returns:
            _dict_: berisi metric untuk evaluasi training
        """
        with torch.no_grad():
            logits, labels = eval_pred
            logits_tensor = torch.from_numpy(logits)
            logits_tensor = nn.functional.interpolate(
                logits_tensor,
                size=labels.shape[-2:],
                mode="bilinear",
                align_corners=False,
            ).argmax(dim=1)

            pred_labels = logits_tensor.detach().cpu().numpy()
            mean_iou = self.metric.compute(
                predictions=pred_labels,
                references=labels,
                num_labels=self.lenLabel,
                ignore_index=255,
                reduce_labels=False,
            )
            # Menghitung precision, recall, dan F1 score
            labels_flat = labels.flatten()
            pred_labels_flat = pred_labels.flatten()

            # Mengabaikan nilai dengan label ignore_index
            mask = labels_flat != 255
            labels_flat = labels_flat[mask]
            pred_labels_flat = pred_labels_flat[mask]

            # inisialisasi precision, recall f1
            precision = precision_score(
                labels_flat, pred_labels_flat, average="weighted")
            recall = recall_score(
                labels_flat, pred_labels_flat, average="weighted")
            f1 = f1_score(labels_flat, pred_labels_flat, average="weighted")

            for key, value in mean_iou.items():
                if isinstance(value, np.ndarray):
                    mean_iou[key] = value.tolist()

            mean_iou['precision'] = precision
            mean_iou['recall'] = recall
            mean_iou['f1'] = f1
            self.history_evaluasi.append(mean_iou)
            return mean_iou

    def train_model(self, train_ds,
                    validation_ds,
                    learning_rate,
                    num_train_epochs,
                    per_device_train_batch_size,
                    per_device_eval_batch_size,
                    output_dir):
        """
        deskripsi : fungsi untuk training model

        Args:
            train_ds (_dict_): dataset training model terdiri pixel_values dan label
            validation_ds (_dict_): dataset validasi model terdiri pixel_values dan label
            learning_rate (_float_): batas pembelajaran
            num_train_epochs (_int_): jumlah epoch
            per_device_train_batch_size (_int_): jumlah batch training
            per_device_eval_batch_size (_int_): jumlah batch validasi
            output_dir (_str_): output directory model

        Returns:
            _object_: model
        """
        training_args = TrainingArguments(
            output_dir=output_dir,
            learning_rate=learning_rate,
            num_train_epochs=num_train_epochs,
            per_device_train_batch_size=per_device_train_batch_size,
            per_device_eval_batch_size=per_device_eval_batch_size,
            save_total_limit=3,
            eval_strategy="steps",
            save_strategy="steps",
            save_steps=20,
            eval_steps=20,
            logging_steps=1,
            eval_accumulation_steps=5,
            remove_unused_columns=False,
            push_to_hub=False,
        )
        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=train_ds,
            eval_dataset=validation_ds,
            compute_metrics=self.compute_metrics,
        )

        trainer.train()

        return self.model

    def display_evaluation_tabel(self):
        """
        deskripsi : fungsi untuk menampilkan tabel evaluasi

        Returns:
            _pd.DataFrame_: tabel evaluasi
        """
        history = pd.DataFrame(self.history_evaluasi)
        history.to_csv("history_evaluasi.csv", index=False)
        return history

    def save_model(self, path_output_dir):
        """
        deskripsi : fungsi untuk menyimpan model

        Args:
            path_output_dir (_string_): berisi path output model
        """
        self.model.save_pretrained(path_output_dir)
        print("model berhasil disimpan di %s" % path_output_dir)

    def model_testing(self, image_tes_area, checkpoint_test=""):
        """
        deskripsi : fungsi untuk model testing

        Args:
            image_tes_area (_PIL.Image_): gambar tes

        Returns:
            _tensor_: hasil prediksi
        """
        # use GPU if available, otherwise use a CPU
        model_load = AutoModelForSemanticSegmentation.from_pretrained(
            checkpoint_test)
        # device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        device = torch.device("cpu")
        encoding = self.processor(image_tes_area, return_tensors="pt")
        pixel_values = encoding.pixel_values.to(device)
        outputs = model_load(pixel_values=pixel_values)
        logits = outputs.logits.cpu()
        upsampled_logits = nn.functional.interpolate(
            logits,
            size=image_tes_area.size[::-1],
            mode="bilinear",
            align_corners=False,
        )
        pred_seg = upsampled_logits.argmax(dim=1)[0]
        return pred_seg

    def predict_all_images(self, test_ds, checkpoint_test=""):
        """
        deskripsi : fungsi untuk prediksi semua gambar

        Args:
            test_ds (_dict_): dataset test

        Returns:
            _dict_: berisi gambar, label, dan prediksi
        """
        print(f"Memprediksi gambar sebanyak {len(test_ds['image'])} gambar")
        return {
            "image": test_ds["image"],
            "label": test_ds["label"],
            "prediction": [self.model_testing(image, checkpoint_test) for image in test_ds['image']]
        }

    def show_all_three_sample_testing_images(self, predictions):
        """
        deskripsi : fungsi untuk menampilkan tiga gambar sample

        Args:
            predictions (_dict_): gambar, label, dan prediksi
        """
        plt.figure(figsize=(10, 10))
        plt.subplot(3, 3, 1)
        plt.imshow(predictions['image'][0])
        plt.title("Input")
        plt.axis('off')
        plt.subplot(3, 3, 2)
        plt.imshow(predictions['label'][0])
        plt.axis('off')
        plt.title("Target")
        plt.subplot(3, 3, 3)
        plt.imshow(predictions['prediction'][0])
        plt.axis('off')
        plt.title("Prediction")
        plt.subplot(3, 3, 4)
        plt.imshow(predictions['image'][1])
        plt.axis('off')
        plt.subplot(3, 3, 5)
        plt.imshow(predictions['label'][1])
        plt.axis('off')
        plt.subplot(3, 3, 6)
        plt.imshow(predictions['prediction'][1])
        plt.axis('off')
        plt.subplot(3, 3, 7)
        plt.imshow(predictions['image'][2])
        plt.axis('off')
        plt.subplot(3, 3, 8)
        plt.imshow(predictions['label'][2])
        plt.axis('off')
        plt.subplot(3, 3, 9)
        plt.imshow(predictions['prediction'][2])
        plt.axis('off')
        plt.show()

    def remove_clouds_with_transparency(self, original_image, segmentation_mask, cloud_label):
        # Convert original image to numpy array (H,W,3)
        if not isinstance(original_image, np.ndarray):
            original_image = np.array(original_image)

        # Convert mask to numpy and ensure it's 2D (H,W)
        if isinstance(segmentation_mask, torch.Tensor):
            segmentation_mask = segmentation_mask.cpu().numpy()
        segmentation_mask = np.squeeze(segmentation_mask)

        # Create alpha channel (255 = opaque, 0 = transparent)
        alpha = np.where(segmentation_mask == cloud_label,
                         0, 255).astype(np.uint8)

        # Combine RGB + Alpha
        rgba = np.dstack((original_image, alpha))  # (H,W,4)

        return rgba

    def show_image_remove_clouds_with_transparency(self, original_image, segmentation_mask, CLOUD_LABEL, fungsi_remove_clouds_with_transparency):
        # Process image
        transparent_result = fungsi_remove_clouds_with_transparency(
            original_image, segmentation_mask, CLOUD_LABEL)

        # Display
        plt.figure(figsize=(15, 10))
        # Matplotlib otomatis handle transparansi
        plt.imshow(transparent_result)
        plt.title("Image with Transparent Clouds")
        plt.show()
