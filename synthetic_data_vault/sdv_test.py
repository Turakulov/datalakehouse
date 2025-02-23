from sdv.datasets.demo import get_available_demos, download_demo
from sdv.multi_table import HMASynthesizer
import pickle
from faker import Faker

# fake = Faker(['en_US', 'en_PH'])
# print(fake.random_company_product())
# import random
# import string
#
# print(random.choice(string.ascii_letters).lower())

# data, metadata = download_demo(
#     modality='multi_table',
#     dataset_name= 'world_v1' #'SalesDB_v1'
# )
# print(data , type(data))
# print(metadata, type(metadata))

# with open('data.pickle', 'wb') as handle:
#     pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)
#
# with open('metadata.pickle', 'wb') as handle:
#     pickle.dump(metadata, handle, protocol=pickle.HIGHEST_PROTOCOL)

# with open('data.pickle', 'rb') as handle:
#     data = pickle.load(handle)
# data_dict  = metadata.tables.get('Customers').columns
# # Маппинг sdtype на PySpark типы
# sdtype_to_spark_type = {
#     'id': IntegerType(),
#     'categorical': StringType()
# }
#
# # Генерация StructType
# message_schema = StructType([
#     StructField(field_name, sdtype_to_spark_type[field_info['sdtype']], True)
#     for field_name, field_info in data_dict.items()
# ])
# print(metadata.tables.get('Customers').columns ,  type(metadata.tables.get('Customers').columns), type(dict(metadata.tables.get('Customers').columns)))

with open("metadata.pickle", "rb") as handle:
    metadata = pickle.load(handle)

# import json
# with open('metadata.json', 'r') as handle:
#     metadata = json.load(handle)

print(metadata)
# data_dict = metadata["tables"]["Customers"]["columns"]
# for field_name, field_info in data_dict.items():
#     print( field_name, field_info)


# synthesizer = HMASynthesizer(metadata)
# synthesizer.fit(data)
# synthetic_data = synthesizer.sample()

# Save the model to a file using Pickle
#
# with open('model_pickle', 'wb') as file:
#     pickle.dump(synthesizer, file)
#
#
# with open('model_pickle', 'rb') as file:
#     loaded_model = pickle.load(file)
# synthetic_data = loaded_model.sample()
# print(synthetic_data, type(synthetic_data))

# avs = get_available_demos(modality='multi_table')
# print(avs)


#              dataset_name  size_MB  num_tables
# 0            Accidents_v1   219.33           3
# 1      Atherosclerosis_v1     6.62           4
# 2   AustralianFootball_v1    31.18           4
# 3     Biodegradability_v1     0.57           5
# 4                 Bupa_v1     0.04           9
# 5                 CORA_v1     1.79           3
# 6       Carcinogenesis_v1     0.94           6
# 7                Chess_v1     0.25           2
# 8            Countries_v1     9.93           4
# 9                  DCG_v1     0.25           2
# 10               Dunur_v1     0.01          17
# 11                Elti_v1     0.05          11
# 12                FNHK_v1   120.00           3
# 13            Facebook_v1     1.38           2
# 14       Hepatitis_std_v1     0.68           7
# 15                Mesh_v1     0.04          29
# 16       Mooney_Family_v1     0.10          68
# 17           MuskSmall_v1     0.64           2
# 18                 NBA_v1     0.15           4
# 19                NCAA_v1    27.15           9
# 20                 PTE_v1     0.95          38
# 21                Pima_v1     0.11           9
# 22       PremierLeague_v1    17.20           4
# 23          Pyrimidine_v1     0.02           2
# 24                 SAP_v1   148.44           4
# 25                 SAT_v1     0.32          36
# 26             SalesDB_v1   269.25           4
# 27            Same_gen_v1     0.04           4
# 28        Student_loan_v1     0.09          10
# 29             Telstra_v1     3.87           5
# 30          Toxicology_v1     1.03           4
# 31            Triazine_v1     0.12           2
# 32         TubePricing_v1     9.67          20
# 33               UTube_v1     0.11           2
# 34              UW_std_v1     0.02           4
# 35               WebKP_v1     1.96           3
# 36      airbnb-simplified   293.14           2
# 37            fake_hotels     0.05           2
# 38   fake_hotels_extended     0.07           2
# 39           financial_v1    85.38           8
# 40                 ftp_v1     4.68           2
# 41               genes_v1     0.36           3
# 42           got_families     0.00           3
# 43      imdb_MovieLens_v1    39.20           7
# 44            imdb_ijs_v1   173.90           7
# 45          imdb_small_v1     0.15           7
# 46           legalActs_v1   130.30           5
# 47         mutagenesis_v1     0.37           3
# 48             nations_v1     0.45           3
# 49            restbase_v1     0.69           3
# 50               rossmann    73.33           2
# 51              trains_v1     0.01           2
# 52          university_v1     0.01           5
# 53                walmart    14.64           3
# 54               world_v1     0.23           3
