from .controlers.create_dataset import roboflow_dwonload, combin_dataset, create_dataset_to_model
from .controlers.model import Model
from .controlers.preprosesing_esrgan import *
from .controlers.preprosesing import change_image_format_to_png_directory, change_image_format_to_png_for_on_image, list_change_image_format_to_png_directory
import os


class pra_pemrosesanDataset:
    def __init__(self, path_directory_input,
                 path_directory_output,
                 path_directory_output_result_esrgan,
                 path_model_ESRGAN="https://tfhub.dev/captain-pool/esrgan-tf2/1",
                 image_format_before=".tif",
                 image_format_after=".png"):
        self.path_directory_input = path_directory_input
        self.path_directory_output = path_directory_output
        self.path_directory_output_result_esrgan = path_directory_output_result_esrgan
        self.image_format_before = image_format_before
        self.image_format_after = image_format_after
        self.model_ESRGAN = ModelESRGAN(path_model_ESRGAN)

    def change_image_format_to_png_directory_dataset(self):
        change_image_format_to_png_directory(self.path_directory_input,
                                             self.path_directory_output,
                                             self.image_format_before,
                                             self.image_format_after)

    def change_image_format_to_png_for_on_image_dataset(self, path_image, path_output_image):
        change_image_format_to_png_for_on_image(path_image, path_output_image)

    def list_change_image_format_to_png_directory_dataset(self):
        return list_change_image_format_to_png_directory(self.path_directory_input,
                                                         self.path_directory_output,
                                                         self.image_format_before,
                                                         self.image_format_after)

    def ESRGAN_resolusi_dataset(self):
        list_image = os.listdir(self.path_directory_output)
        list_path_image = [os.path.join(self.path_directory_output, image)
                           for image in list_image if f"{self.image_format_after}" in image]
        list_image_hasil = []
        for list_gambar in list_path_image:
            hr_image = preprocess_image(list_gambar)
            fake_image = self.model_ESRGAN(hr_image)
            fake_image = decode_gambar(fake_image)
            list_image_hasil.append(fake_image)
            save_image(fake_image,
                       list_gambar.split("/")[-1].split(".")[0],
                       self.path_directory_output_result_esrgan)
        print(f"{len(list_path_image)} gambar berhasil di konversi ke png")
        return {
            "image": list_path_image,
            "image_hasil": list_image_hasil
        }

    def ESRGAN_resolusi_on_image(self, path_image):
        hr_image = preprocess_image(path_image)
        fake_image = self.model_ESRGAN(hr_image)
        fake_image = decode_gambar(fake_image)
        return fake_image

    def plot_image_result_esrgan(self, image, title=""):
        plot_image(image, title)


class pemrosesanDataset:
    def __init__(self, path_train="", path_valid="", path_test=""):
        self.combine_ds = combin_dataset(path_train, path_valid, path_test)

    def dwonload_dataset_roboflow(self, api_key, name_workspace, name_project, vers, name_version):
        roboflow_dwonload(api_key, name_workspace,
                          name_project, vers, name_version)

    def combine_dataset_pra_pemrosesan(self):
        return self.combine_ds.combine()

    def combine_dataset_to_model(self, combine_ds):
        combine = create_dataset_to_model(combine_ds)
        return combine.combine_dataset_model()


class CloudMappingAI:
    def __init__(self, id2label, label2id, checkpoint_train="nvidia/mit-b0", name_evaluate="mean_iou"):
        self.model_semantic = Model(
            id2label, label2id, checkpoint_train, name_evaluate)

    def dataset_transform_area_model(self, dataset):
        return self.model_semantic.dataset_transform_area(dataset)

    def train(self, train_ds,
              validation_ds,
              learning_rate,
              num_train_epochs,
              per_device_train_batch_size,
              per_device_eval_batch_size,
              output_dir,):
        return self.model_semantic.train_model(train_ds,
                                               validation_ds,
                                               learning_rate,
                                               num_train_epochs,
                                               per_device_train_batch_size,
                                               per_device_eval_batch_size,
                                               output_dir,)

    def history_model_evaluate(self):
        return self.model_semantic.display_evaluation_tabel()

    def model_save(self, path_output_dir):
        self.model_semantic.save_model(path_output_dir)

    def testing_model(self, image_tes_area, checkpoint_test=""):
        return self.model_semantic.model_testing(image_tes_area, checkpoint_test)

    def predict_all_image_model(self, test_ds, checkpoint_test=""):
        return self.model_semantic.predict_all_images(test_ds, checkpoint_test)

    def show_image_model_prediction(self, prediction):
        self.model_semantic.show_all_three_sample_testing_images(prediction)

    def remove_cloudh_with_transparansy(self, original_image, segmentation_image, cloud_label):
        return self.model_semantic.remove_clouds_with_transparency(
            original_image, segmentation_image, cloud_label)

    def show_image_remove_clouds_with_transparency(self, test_dataset, mask_prdict, cloud_label, index_image, fungsi_remove_clouds_with_transparency):
        CLOUD_LABEL = cloud_label
        index = index_image
        original_image = test_dataset['image'][index]
        segmentation_image = mask_prdict[index]

        self.model_semantic.show_image_remove_clouds_with_transparency(
            original_image, segmentation_image, CLOUD_LABEL, fungsi_remove_clouds_with_transparency)
