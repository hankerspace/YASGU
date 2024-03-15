from src.classes.generator import Generator
from src.utils.config import *
from src.utils.utils import rem_temp_files

def main():

    generators_configs = get_generators()
    for generator_config in generators_configs:
        generator = Generator(generator_config)
        data = generator.generate_video()
        generator.upload_video(data["video_path"], data["title"], data["description"])

if __name__ == "__main__":
    # Setup file tree
    assert_folder_structure()

    # Remove temporary files
    rem_temp_files()

    main()
