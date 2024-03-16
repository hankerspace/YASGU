from src.classes.generator import Generator
from src.utils.config import *
from src.utils.utils import rem_temp_files
from utils.status import error, info

def main():

    generators_configs = get_generators()
    done = 0
    info(f"Generating {len(generators_configs)} videos...")
    for generator_config in generators_configs:
        try:
            generator = Generator(generator_config)
            data = generator.generate_video()
            generator.upload_video(data["video_path"], data["title"], data["description"])
            done += 1
        except Exception as e:
            error(f"Error occurred while generating video: {str(e)}")
            continue
    info(f"Generated {done} videos. Exiting...")

if __name__ == "__main__":
    # Setup file tree
    assert_folder_structure()

    # Remove temporary files
    rem_temp_files()

    main()
