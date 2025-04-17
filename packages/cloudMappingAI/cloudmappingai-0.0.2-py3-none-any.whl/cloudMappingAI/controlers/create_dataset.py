from roboflow import Roboflow
from datasets import Dataset, DatasetDict, Image
import os
# dwonload dataset


class combin_dataset:
    def __init__(self, path_train, path_valid, path_test):
        self.path_train = path_train
        self.path_valid = path_valid
        self.path_test = path_test

    def sortingIndexImage(self, filename):
        """
        deskripsi : fungsi untuk mengurutkan index gambar

        Args:
            filename (_string_): berisi path gambar

        Returns:
            _string_: index gambar unix
        """
        return filename.split('.rf.')[-1].split('.')[0]

    def combine(self):
        """
        deskripsi : fungsi untuk menggabungkan dataset

        Returns:
            _dict_: berisi dataset train, validasi, dan test
        """
        path_dataset_train = self.path_train
        path_dataset_validasi = self.path_valid
        path_dataset_test = self.path_test

        dataset_train = os.listdir(path_dataset_train)
        dataset_validasi = os.listdir(path_dataset_validasi)
        dataset_test = os.listdir(path_dataset_test)

        # train
        dataset_train_image = [os.path.join(
            path_dataset_train, i) for i in dataset_train if "mask" not in i and "_classes" not in i]
        dataset_train_mask = [os.path.join(
            path_dataset_train, i) for i in dataset_train if "mask" in i and "_classes" not in i]
        dataset_train_image = sorted(
            dataset_train_image, key=self.sortingIndexImage)
        dataset_train_mask = sorted(
            dataset_train_mask, key=self.sortingIndexImage)

        # validasi
        dataset_validasi_image = [os.path.join(
            path_dataset_validasi, i) for i in dataset_validasi if "mask" not in i and "_classes" not in i]
        dataset_validasi_mask = [os.path.join(
            path_dataset_validasi, i) for i in dataset_validasi if "mask" in i and "_classes" not in i]
        dataset_validasi_image = sorted(
            dataset_validasi_image, key=self.sortingIndexImage)
        dataset_validasi_mask = sorted(
            dataset_validasi_mask, key=self.sortingIndexImage)

        # test
        dataset_test_image = [os.path.join(
            path_dataset_test, i) for i in dataset_test if "mask" not in i and "_classes" not in i]
        dataset_test_mask = [os.path.join(
            path_dataset_test, i) for i in dataset_test if "mask" in i and "_classes" not in i]
        dataset_test_image = sorted(
            dataset_test_image, key=self.sortingIndexImage)
        dataset_test_mask = sorted(
            dataset_test_mask, key=self.sortingIndexImage)

        return {
            "train_image": [dataset_train_image, dataset_train_mask],
            "validasi_image": [dataset_validasi_image, dataset_validasi_mask],
            "test_image": [dataset_test_image, dataset_test_mask]
        }


class create_dataset_to_model:
    def __init__(self, combine):
        self.combine = combine

    def create_dataset(self, image_paths, label_paths):
        """
        deskripsi : fungsi untuk membuat dataset untuk model

        Args:
            image_paths (_string_): berisi path gambar
            label_paths (_string_): berisi path label atau segmentasi gambar

        Returns:
            _dict_: berisi dataset
        """
        dataset = Dataset.from_dict({
            'image': image_paths,
            'label': label_paths
        })
        dataset = dataset.cast_column('image', Image())
        dataset = dataset.cast_column('label', Image())
        return dataset

    def combine_dataset_model(self):
        """
        descrption : fungsi untuk menggabungkan dataset untuk model

        Args:
            combine (_dict_): berisi dictionary dataset train, validasi, dan test

        Returns:
            _datasetDict_: berisi dataset train, validasi, dan test
        """
        train_dataset = self.create_dataset(
            self.combine['train_image'][0], self.combine['train_image'][1])
        validasi_dataset = self.create_dataset(
            self.combine['validasi_image'][0], self.combine['validasi_image'][1])
        test_dataset = self.create_dataset(
            self.combine['test_image'][0], self.combine['test_image'][1])

        return DatasetDict({
            'train': train_dataset,
            'validasi': validasi_dataset,
            'test': test_dataset
        })


def roboflow_dwonload(api_key, name_workspace, name_project, vers, name_version):
    """
    deskripsi : fungsi untuk download dataset menggunakan roboflow

    Args:
        api_key (_string_): digunakan untuk mengakses api roboflow
        name_workspace (_string_): digunakan untuk memilih workspace
        name_project (_string_): digunakan untuk memilih project
        vers (_int_): digunakan untuk memilih versi
        name_version (_string_): digunakan untuk memilih jenis dataset

    returns:
        None

    contoh penggunaan :
        roboflow_dwonload(api_key, name_workspace, name_project, vers, name_version)
    """
    rf = Roboflow(api_key=api_key)
    project = rf.workspace(name_workspace).project(name_project)
    version = project.version(vers)
    dataset = version.download(name_version)
    print(dataset)
