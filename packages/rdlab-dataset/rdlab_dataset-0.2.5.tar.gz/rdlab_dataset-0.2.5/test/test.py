from rdlab_dataset.module import KhmerWordLoader, KhmerAddressLoader, KhmerSentencesLoader
from rdlab_dataset.module import TextArrayListImageGenerator

# Load data
khmerwordloaders = KhmerWordLoader()
khmeraddressloaders = KhmerAddressLoader()
khmersentencesloaders = KhmerSentencesLoader()

# Get data
word = khmerwordloaders.get_all_words()
address = khmeraddressloaders.get_all_addresses()
sentences = khmersentencesloaders.get_all_sentences()

# Combine into one array
combined_texts = word + address + sentences

# Optional: print or inspect
print(f"Total combined items: {len(combined_texts)}")


text_image_gen = TextArrayListImageGenerator(customize_font=True)

text_image_gen.generate_images(text_list = combined_texts, font_folder= "/home/vitoupro/code/rdlab-dataset/test_font", output_count = 4 )