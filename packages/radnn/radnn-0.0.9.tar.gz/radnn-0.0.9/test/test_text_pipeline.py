from radnn import mlsys, FileSystem
from datasets import StratifiedCytaChatbotDataset

mlsys.filesys = FileSystem()
oDataset = StratifiedCytaChatbotDataset(mlsys.filesys.datasets.subfs("CYTACHATBOT"))
if not oDataset.load_cache():
  if oDataset.load_questions("EL"):
    oDataset.split()
    oDataset.print_info()
    oDataset.save_cache()


for nIndex in range(oDataset.ts_sample_count):
  print(f"{oDataset.ts_sample_ids[nIndex]}§{oDataset.ts_labels[nIndex]}§{oDataset.ts_samples[nIndex]}")
print("="*80)
for nIndex in range(oDataset.vs_sample_count):
  print(f"{oDataset.vs_sample_ids[nIndex]}§{oDataset.vs_labels[nIndex]}§{oDataset.vs_samples[nIndex]}")
