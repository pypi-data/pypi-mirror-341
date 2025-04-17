# CloudMappingAI

## Intisari

Library yang bertujuan untuk membantu para peneliti untuk membangun dan menggunakan model pemetaan awan dalam penelitian Geografis. librayr ini terdiri dari 3 tahapan dalam penggunaannya:

1. **_pra-pemrosesan dataset_**

   Bagian ini merupakan tahapan awal dari pengolahan dataset yang berbentuk gambar dalam pemetaan awan. Isi dari _pra-pemrosesan dataset_ ini adalah mengubah format gambar secara default ke _.png_ dan meningkatkan resolusi gambar menggunakan model ESRGAN

2. **_pemrosesan dataset_**

   Bagian ini merupakan tahapan kedua dari pengolahan dataset yang siap untuk nantinya di training di dalam model _segmentation image_

3. **CloudMappingAI**

   Bagian ini merupakan tempat untuk pelatihan model, penyimpanan model, evaluasi model, penggunaan model kembali dalam melakukan pemetaan awan.

## Model

Model yang digunakan iyalah berbasi _transfer learning transformer_ dengan nama **_[nvidia/mti-b0 :Segformer](https://huggingface.co/nvidia/mit-b0)_** adapun gambaran arsitektur dari model ini sebagai berikut,

![Screenshot 2024-11-06 103907](https://github.com/user-attachments/assets/00f96926-c197-4d45-aff9-79aba04908f3)

## Cara Penggunaan

### Mengenal Beberapa Fungsi Dari Library

| Fungsi/method                                         | Deskripsi                                                                                                                                                                                                                                                                                                                     |
| ----------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| change_image_format_to_png_directory_dataset          | metod dari class pra_pemrosesanDataset (cla-ss) yang disimpan di variabel pra_pemrosesan_data yaitu change_image_format_to_png_directory_dataset (method) yang akan mengubah gambar ke format png pada sekalah gambar folder.                                                                                                 |
| change_image_format_to_png_for_on_image_dataset       | berfungsi untuk mengubah format gambar secara satu per satu, dengan memasukan path file lokasi gambar dan path folder yang menampung hasil dari perubahan format gambar ke png.                                                                                                                                               |
| list_change_image_format_to_png_directory_dataset     | bertujuan untuk meletakan hasil dari path Lokasi gambar yang sudah diubah format nya ke dalam sebuah array.                                                                                                                                                                                                                   |
| ESRGAN_resolusi_dataset                               | penggunaan untuk melakukan resolusi gambar dengan model ESRGAN dengan method yang dipanggil ESRGAN\_ resolusi_dataset (method) , method ini merupakan pengubah resolusi gambar sekala folder dan menghasilkan type data dictionary yang terdiri dari list image serta image_hasil yang sudah di resolusi dengan model ESRGAN. |
| ESRGAN_resolusi_on_image dan plot_image_result_esrgan | bertujuan untuk meningkatkan resolusi gambar satu per satu dengan memasukan Lokasi path gam-bar di parameter method terse-but, dan menggunakan me-thod dari plot_image_result (method) yang bertujuan untuk menampilkan gambar hasil resolusi dari esrgan.                                                                    |
| dwonload_dataset_roboflow                             | bertujuan untuk menginisialisasi untuk meng-gunakan method pemrosesan gambar yang akan siap di masukan ke dalam training model. Penggunaan metohd yang dipanggil iyalah dwonload_dataset_roboflow (method) bertujuan untuk mendwonlod data dari hasil pemrosesan di aplikasi pihak ke-3 yaitu roboflow.                       |
| combine_dataset_pra_pemrosesan                        | bertujuan untuk mengkelompokkan dataset berdasarkan jenis data seperti training, validasi, dan testing.                                                                                                                                                                                                                       |
| combine_dataset_to_model                              | bertujuan untuk menjadikan di tiap kelompok gambar untuk di jadikan format PIL agar dapat mudah di tampilkan dan dibentuk ke dataset pelatihan model yang terparti menjadi “image” dan “label”.                                                                                                                               |
| dataset_transform_area_model                          | bertujuan untuk mengubah struktur gambar menjadi array pixel_velues agar dapat mudah melakukan training model serta labelnya diubah ke dalam array yang berisi nilai 0 dan 1.                                                                                                                                                 |
| train                                                 | bertujuan untuk melatih model.                                                                                                                                                                                                                                                                                                |
| history_model_evaluate                                | bertujuan untuk mendwon-load dan menampilkan data history hasil evaluasi training model                                                                                                                                                                                                                                       |
| model_save                                            | bertujuan untuk menyimpan model yang sudah di training sebelumnya.                                                                                                                                                                                                                                                            |
| testing_model                                         | betujuan untuk melakukan prediksi pada satu gambar dengan memasukan gambar dari data_tes yang sudah di proses sebelumnya menjadi format PIL image dan model yang sudah kita latih dari path lokasinya kedalam method.                                                                                                         |
| predict_all_image_model                               | bertujuan untuk melakukan sekaligus pada semua gambar dari data_tes yang sudah di olah. Gambar yang ada di data_tes ada 6 gambar dan di prediksi secara sekaligus.                                                                                                                                                            |
| show_image_model_prediction                           | bertujuan untuk menampilkan sampel gambar yang sudah di prediksi berserta target yang sudah memenuhi.                                                                                                                                                                                                                         |

### Implementasi

Penggunaan library ini dapat diterapkan dengan penggunaan code serta parameter yang di ikutsertakan pada saat pengeksekusian code berlangsung, berikut implementasi dalam code yang dijalankan.

#### **Penginstalan Library**

```shell
pip install cloudmappingai
```

#### **Import Library**

Dalam mengimport library di **_cloudMappingAI_** ada dua cara penggunaan :

1. Import untuk semuanya

   ```python
   from cloudMappingAI import *
   ```

   tanda (\*) merupakan tanda untuk memanggil segala bentuk method yang ada di library cloudMappingAI.

2. Import untuk satu per satu method atau class nya
   ```python
   from cloudMappingAI.cloud_mapping_ai import pra_pemrosesanDataset
   from cloudMappingAI.cloud_mapping_ai import pemrosesanDataset
   from cloudMappingAI.cloud_mapping_ai import CloudMappingAI
   ```
   Dalam code di atas ada 3 jenis class utama yang akan di panggil yaitu tahapan pra-pemrosesan dataset, pemrosesan datasetm, dan CloudMappingAI sebagai class training model.

#### **_Pra-pemrosesan datasets_**

Ada beberapa class dan method yang digunakan pada libraray cloudmappingai ini di tahapan _pra-pemrosesan dataset_,

1. Inisialisasi tahapan pra-pemrosesan dataset

   ```python
   pra_pemrosesan_data = pra_pemrosesanDataset(
      path_directory_input=...,
      path_directory_output=...,
      path_directory_output_result_esrgan=...
   )
   ```

   Inisialisasi _pra_pemrosesanDataset_ melibatkan pemasukan beberapa parameter terdiri dari:

   | parameter                             | deskripsi                                                                                                                                                                                    |
   | ------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
   | _path_directory_input_                | Sebagai parameter yang bernilai _(string)_ yang menyimpan _string_ berupa lokasi dari gambar directory atau penyimpanan inputan                                                              |
   | _path_directory_output_               | Sebagai parameter yang bernilai _(string)_ yang menyimpan _string_ berupa lokasi dari gambar directory atau penyimpanan outputan                                                             |
   | _path_directory_output_result_esrgan_ | Sebagai parameter yang bernilai _(string)_ yang menyimpan _string_ berupa lokasi dari gambar yang sudah di ubah format nya menjadi _.png_ yang nantinya akan siap di tingkatkan resolusinya. |

2. Penggunaan method ubah format gambar sekala directory atau folder.

   ```python
   pra_pemrosesan_data.change_image_format_to_png_directory_dataset()
   ```

   output:
   ![Screenshot 2024-12-11 111114](https://github.com/user-attachments/assets/b04b39ae-9059-468e-85cb-05130bb4aa16)

   Penggunaan method ini bertujuan untuk mengubah gambar dari yang semulanya adalah format mentahan dari citra setelit yaitu _.tif_ diubah ke format _.png_ secara keseluruhan dalam sekala directory.

3. Penggunaan method ubah format gambar dalam satu per satu gambar.

   ```python
   pra_pemrosesan_data.change_image_format_to_png_for_on_image_dataset
   (
      path_image=....,
      path_output_image=...,
   )
   ```

   Output :
   ![image](https://github.com/user-attachments/assets/44178dee-1f5e-4af7-83e5-b06d271a60a8)

   Penggunaan method ini bertujuan untuk mengubah format gambar dengan menginputkan satu gambar, yang mana meletakan path atau lokasi dari satu gambar berformat _.tif_ dan akan disimpan ke dalam alokasi path outputnya yang berisi format _.png_. Berikut parameter yang ada di dalam method tersebut:
   | parameter | deskripsi|
   |-----|-----|
   |_path_image_|Parameter yang menyimpan nilai (_string_) yaitu berupa lokasi path image yang berformat _.tif_|
   |_path_output_|Paramater yang menyimpan nilai (_string_) yaitu berupa lokasi path directory untuk output hasil pengubahan gambar ke _.png_|

4. Penggunaan method ubah format gambar secara keseluruhan dari satu folder dan menyimpan lokasi path gambar ke dalam sebuah array

   ```python
   data_gambar = pra_pemrosesan_data.list_change_image_format_to_png_directory_dataset()
   ```

   Output:
   ![Screenshot 2024-12-11 165018](https://github.com/user-attachments/assets/821ec836-7665-449c-af15-162f9cf9cb9b)

5. Resolusi ESRGAN gambar secara banyak dalam satu folder.

   ```python
   pra_pemrosesan_data.ESRGAN_resolusi_dataset()
   ```

   Output:
   ![Screenshot 2024-12-11 165505](https://github.com/user-attachments/assets/593cd432-21ce-4af5-8209-9ef3dadb832e)

   Method ini berfungsi untuk meresolusikan gambar menggunakan model ESRGAN, dengan sekali banyak gambar dalam satu directory yang akan diresolusikan dengan ESRGAN ini dan mengembalikan nilai _dictionary_ yang berisi "_image_", "_image_hasil_".

6. Resolusi ESRGAN gambar secara satu per satu

   ```python
   fake_tes_gambar = pra_pemrosesan_data.ESRGAN_resolusi_on_image(
      path_image=...
   )
   ```

   | Parameter    | Deskripsi                                                                               |
   | ------------ | --------------------------------------------------------------------------------------- |
   | _path_image_ | parameter yang berisi nilai (_string_) yaitu lokasi path image yang akan diresolusikan. |

7. Menampilkan plot gambar hasil resolusi

   ```python
   pra_pemrosesan_data.plot_image_result_esrgan(
      image=...,
      title=...
   )
   ```

   Output :
   ![Screenshot 2024-12-11 170841](https://github.com/user-attachments/assets/54dad74b-3976-46da-a4d8-94095cb5cb25)

   | Prameter | Deskripsi                                                                                      |
   | -------- | ---------------------------------------------------------------------------------------------- |
   | _image_  | parameter yang berisi nilai tensor berdimensi 3D yang terdiri dari panjang, lebar, dan tinggi. |
   | _title_  | parameter yang berisi nilai string untuk memberikan judul di plot.                             |

   Method ini berfungsi untuk menampilkan resolusi gambar dengan menggunakan plot matplotlib.

#### **_Pemrosesan dataset_**

Ada beberapa class dan method yang digunakan pada libraray cloudmappingai ini di tahapan _pemrosesan dataset_

1. Inisialisasi Pemrosesan dataset

   ```python
   pemrosesan_data = pemrosesanDataset(
      path_train=...,
      path_valid=...,
      path_test=...
      )
   ```

   | parameter    | deskripsi                                                                                                         |
   | ------------ | ----------------------------------------------------------------------------------------------------------------- |
   | _path_train_ | Parameter yang menyimpan nilai (_string_) yaitu path lokasi data train saat sudah mendwonload data dari roboflow. |
   | _path_valid_ | Parameter yang menyimpan nilai (_string_) yaitu path lokasi data valid saat sudah mendwonload data dari roboflow. |
   | _path_test_  | Parameter yang menyimpan nilai (_string_) yaitu path lokasi data test saat sudah mendwonload data dari roboflow.  |

   Method ini merupakan inisialisais untuk penggunaan class dan method di bagian pemrosesan dataset yang mengimputkan 3 parameter yaitu data train, validasi, dan testing.

2. Dwonload dataset

   ```python
   dataset.dwonload_dataset_roboflow(
      api_key=...,
      name_workspace=...,
      name_project=...,
      vers=...,
      name_version=...
   )
   ```

   Output:
   ![image](https://github.com/user-attachments/assets/7a2348f7-6f22-4a3a-81af-2b17a0c5e6dc)

   | parameter        | deskripsi                                                                     |
   | ---------------- | ----------------------------------------------------------------------------- |
   | _api_key_        | parameter yang menyimpan nilai _string_ yaitu api key dari roboflow.          |
   | _name_workspace_ | parameter yang menyimpan nilai _string_ yaitu workspace dari roboflow.        |
   | _name_project_   | parameter yang menyimpan nilai _string_ yaitu nama projek di roboflow.        |
   | _vers_           | parameter yang menyimpan nilai _string_ yaitu versi dataset di roboflow.      |
   | _name_version_   | parameter yang menyimpan nilai _string_ yaitu nama versi dataset di roboflow. |

   method ini berfungsi untuk mendwonload dataset di roboflow dengan mengakses data di roboflow untuk di dwonload datasetnya.

3. Mengklompokan dan menyesuaikan gambar sesuai dengan jenis training, validasi, dan testing

   ```python
   datas = pemrosesan_data.combine_dataset_pra_pemrosesan()
   ```

   Output:
   ![image](https://github.com/user-attachments/assets/1f035542-a6a2-46c4-8ea4-f9447afe44cd)

   method tersebut bertujuan untuk mengelompokan data serta mengurutkan data sesuai dengan mask atau semantic tiap gambar sesuai dengan index unik, kemudian mengembalikan nilai \_dictionary yang terdiri dari train_image, validasi_image, dan testing image.

4. Combinasi dataset untuk model

   ```python
   datas = pemrosesan_data.combine_dataset_to_model(combine_ds=...)
   ```

   Output :

   ![image](https://github.com/user-attachments/assets/7d6ce4d0-a5d2-4f2b-a9cd-0e25e94d1e95)

   | parameter    | deskripsi                                                                                        |
   | ------------ | ------------------------------------------------------------------------------------------------ |
   | _combine_ds_ | parameter ini berisi data _dictionary_ dengan key 'train_image', 'validasi_image', 'test_image'. |

   Pada method ini dataset yang sudah di kelompokan dari dictionary akan dijadikan menjadi datasetDict yang menampung nilai dari semua gambar yang di ubah ke bentuk format PIL image.

#### **_Model CloudMappingAI_**

Pada bagian ini bertujuan untuk menjalankan area pengembangan model, evaluasi model, serta menyimpan model untuk melakukan testing dan penerapan model untuk pemetaan awan, berikut beberapa class dan method yang ada di bagian ini:

1. Inisialisasi class

   ```python
   ModelCloudMappingAI = CloudMappingAI(
      id2label=...,
      label2id=...,
      checkpoint_train='...'
   )
   ```

   Output:
   ![image](https://github.com/user-attachments/assets/1ada95d4-ebff-4428-a4f7-00450b15a66b)

   | parameter          | deskripsi                                                                                                           |
   | ------------------ | ------------------------------------------------------------------------------------------------------------------- |
   | _id2label_         | parameter ini menyimpan nilai dictionary class dengan key nya adalah index class objek itu sendiri.                 |
   | _label2id_         | parameter ini menyimpan nilai dictionary class dengan key nya adalah name class objek itu sendiri.                  |
   | _checkpoint_train_ | parameter yang menyimpan nilai string dari model yang diimputkan di hugging face dengan prinsip _transfer learning_ |

   Bagian inisialisasi ini adalah awalan untuk menggunakan method platihan model yang ada di library.

2. Transfrom dataset

   ```python
   dataset_to_model = ModelCloudMappingAI.dataset_transform_area_model(datas)
   ```

   Output:

   ![image](https://github.com/user-attachments/assets/624fb1d9-8455-487c-86f7-71da9fc227a0)

   | parameter | deskripsi                                                                                                                                |
   | --------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
   | _dataset_ | parameter ini berisi type datasetDict untuk di ubah format gambarnya menjadi vektor array agar sesuai dan dapat ditraining dengan model. |

3. Training model

   ```python
   model_baru = ModelCloudMappingAI.train(
      train_ds=...,
      validation_ds=...,
      learning_rate=...,
      num_train_epochs=...,
      per_device_train_batch_size=...,
      per_device_eval_batch_size=...,
      output_dir=...
   )
   ```

   Output:

   ![image](https://github.com/user-attachments/assets/4069a4ec-5932-446a-84b7-2c32a68a4895)

   | parameter                     | deskripsi                                                                                                                                                  |
   | ----------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
   | _train_ds_                    | parameter yang berisi nilai array gambar untuk dataset train yang sudah di normalisasai dari method "_dataset_transform_area_model_".                      |
   | _validation_ds_               | parameter yang berisi nilai array gambar untuk dataset validation yang sudah di normalisasi dari method "_dataset_transform_area_model_".                  |
   | _learning_rate_               | parameter yang berisi nilai float untuk mengatur seberapa besar atau batasan perubahan bobot dalam model setiap langkah platihan model.                    |
   | _num_train_epochs_            | parameter yang berisi nilai integer untuk menentukan berapa banyak jumlah iterasi pelatihan yang akan dilakukan pada model yang kita latih dengan dataset. |
   | _per_device_train_batch_size_ | parameter yang berisi nilai integer untuk sebagai penentu jumlah sampel data yang akan diproses secara bersamaan dalam satu langkah pelatihan.             |
   | _per_device_eval_batch_size_  | parameter yang berisis nilai integer yang fungsi nya sama dengan parameter "_per_device_train_batch_size_" tapi di bagian data validasi.                   |
   | _output_dir_                  | parameter yang berisi lokasi tempat menyimpan hasil atau data chece dari berjalannya pelatihan model.                                                      |

   method yang digunakan tersebut bertjuan untuk melakukan training pada model dengan menginputkan dataset yang sudah di normalisasikan agar sesuai dengan model yang dilatih serta pengaturan parameter platihan seperti bacth size dan iterasi platihan (_epoch_)

4. History model

   ```python
   history = ModelCloudMappingAI.history_model_evaluate()
   ```

   Output:
   ![image](https://github.com/user-attachments/assets/e34a833a-5cc5-4985-a680-e50c1740d255)

   method _history_model_evaluate_ bertujuan untuk mendwonload dan melihat history dari evaluasi selama pelatihan pada tiap becth nya dengan mendwonload data hasil evaluasi nya ke dalam bentuk CSV.

5. Save model

   ```python
   ModelCloudMappingAI.model_save(
      path_output_dir=...
   )
   ```

   Output:

   ![image](https://github.com/user-attachments/assets/f5188efe-5ec7-4094-9e0d-dfc29a0af2e4)

   | parameter         | deskripsi                                                                                                    |
   | ----------------- | ------------------------------------------------------------------------------------------------------------ |
   | _path_output_dir_ | parameter ini berisi nilai string yang berupa lokasi folder output untuk menyimpan model yang sudah dilatih. |

   method _model_save_ ini bertujuan untuk menyimpan model apabila model sudah melakukan pelatihan dan memiliki evaluasi yang bagus dengan performa model yang baik.

6. Testing Model

   ```python
   predic_gambar = ModelCloudMappingAI.testing_model(
      image_test_area=...,
      checkpoint_test=...
   )
   ```

   Output:

   ![image](https://github.com/user-attachments/assets/684ec949-8368-4e65-a0b8-141ccc2ca051)

   | parameter         | diskripsi                                                                                                               |
   | ----------------- | ----------------------------------------------------------------------------------------------------------------------- |
   | _image_test_area_ | parameter yang berisi gambar berforma PIL image                                                                         |
   | _checkpoint_test_ | paraemter yang berisi path model yang sudah dilatih untuk digunakan pada data testing untuk implementasi dan pengujian. |

7. Prediksi banyak gambar

   ```python
   predic_all_image = ModelCloudMappingAI.predict_all_image_model(data_tes, "/content/best_model")
   ```

   Output :

   ![image](https://github.com/user-attachments/assets/500c865b-38a9-4c72-a380-16f2c9df51c4)

   | parameter         | diskripsi                                                                                                               |
   | ----------------- | ----------------------------------------------------------------------------------------------------------------------- |
   | _test_ds_         | parameter yang berisi array gambar berforma PIL image yang siap untuk di uji coba                                       |
   | _checkpoint_test_ | paraemter yang berisi path model yang sudah dilatih untuk digunakan pada data testing untuk implementasi dan pengujian. |

8. Menampilkan gambar sampel testing

   ```python
   model_testing.show_image_model_prediction(predic_all_image)
   ```

   output:
   ![image](https://github.com/user-attachments/assets/ac7a36b9-9206-4464-b072-f993b4e5f9db)

9. Melakukan penghapusan awan di gambar asli

```python
hasil_gambar_hasil_hapus_awan = ModelCloudMappingAI.remove_cloudh_with_transparansy(
   original_image="",
   segmentation_image="",
   cloud_label=""
)
```

Paramater yang digunakan :

| parameter            | penjelasan                                                                                        |
| -------------------- | ------------------------------------------------------------------------------------------------- |
| _original_image_     | Sebagai parameter yang menampung variabel gambar yang asli atau inputan gambar berbentuk vector   |
| _segmentation_image_ | Sebagai parameter yang menampung variabel gamba hasil prediksi model berbentuk vector             |
| _cloud_label_        | sebagai parameter yang menampung nilai interger label yang mendeskripsikan awan contoh 1,2,3,.... |

cara penggunaannya:

![Image](https://github.com/user-attachments/assets/fff208a9-1991-4530-ba8f-d5bfc86ccc8e)

Hasil :

![Image](https://github.com/user-attachments/assets/8053af39-7b0c-4d23-ab60-8d541f2151c1)
