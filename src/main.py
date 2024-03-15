import generators
from utils import *
from config import *
from video import generate_subtitles, generate_video


def main():
    subject = "Facts about an animal"
    language = "English"

    topic = generators.generate_topic(subject)
    info(f"Generated Topic: {topic}")
    script = generators.generate_script(topic, language)
    info(f"Generated Script: {script}")
    metadata = generators.generate_metadata(topic, script, language)
    info(f"Generated Metadata: {metadata}")
    image_prompts = generators.generate_image_prompts(script, topic, 5)
    info(f"Generated Image Prompts: {image_prompts}")

    images_files = []
    for prompt in image_prompts:
        image = generators.generate_image(prompt)
        images_files.append(image)
        info(f"Generated Image: {image} for prompt: {prompt}")

    audio_file = generators.generate_script_to_speech(script)
    srt_file = generate_subtitles(audio_file)

    video_file = generate_video(images_files, audio_file, srt_file)


    # # Get user input
    # user_input = int(question("Select an option: "))
    #
    # # Start the selected option
    # if user_input == 1:
    #     info("Starting YT Shorts Automater...")
    #
    #     cached_accounts = get_accounts("youtube")
    #
    #     if len(cached_accounts) == 0:
    #         warning("No accounts found in cache. Create one now?")
    #         user_input = question("Yes/No: ")
    #
    #         if user_input.lower() == "yes":
    #             generated_uuid = str(uuid4())
    #
    #             success(f" => Generated ID: {generated_uuid}")
    #             nickname = question(" => Enter a nickname for this account: ")
    #             fp_profile = question(" => Enter the path to the Firefox profile: ")
    #             niche = question(" => Enter the account niche: ")
    #             language = question(" => Enter the account language: ")
    #
    #             add_account("youtube", {
    #                 "id": generated_uuid,
    #                 "nickname": nickname,
    #                 "firefox_profile": fp_profile,
    #                 "niche": niche,
    #                 "language": language,
    #                 "videos": []
    #             })
    #     else:
    #         table = PrettyTable()
    #         table.field_names = ["ID", "UUID", "Nickname", "Niche"]
    #
    #         for account in cached_accounts:
    #             table.add_row([cached_accounts.index(account) + 1, colored(account["id"], "cyan"), colored(account["nickname"], "blue"), colored(account["niche"], "green")])
    #
    #         print(table)
    #
    #         user_input = question("Select an account to start: ")
    #
    #         selected_account = None
    #
    #         for account in cached_accounts:
    #             if str(cached_accounts.index(account) + 1) == user_input:
    #                 selected_account = account
    #
    #         if selected_account is None:
    #             error("Invalid account selected. Please try again.", "red")
    #             main()
    #         else:
    #             youtube = YouTube(
    #                 selected_account["id"],
    #                 selected_account["nickname"],
    #                 selected_account["firefox_profile"],
    #                 selected_account["niche"],
    #                 selected_account["language"]
    #             )
    #
    #             while True:
    #                 rem_temp_files()
    #                 info("\n============ OPTIONS ============", False)
    #
    #                 for idx, youtube_option in enumerate(YOUTUBE_OPTIONS):
    #                     print(colored(f" {idx + 1}. {youtube_option}", "cyan"))
    #
    #                 info("=================================\n", False)
    #
    #                 # Get user input
    #                 user_input = int(question("Select an option: "))
    #                 tts = TTS()
    #
    #                 if user_input == 1:
    #                     youtube.generate_video(tts)
    #                     upload_to_yt = question("Do you want to upload this video to YouTube? (Yes/No): ")
    #                     if upload_to_yt.lower() == "yes":
    #                         youtube.upload_video()
    #                 elif user_input == 2:
    #                     videos = youtube.get_videos()
    #
    #                     if len(videos) > 0:
    #                         videos_table = PrettyTable()
    #                         videos_table.field_names = ["ID", "Date", "Title"]
    #
    #                         for video in videos:
    #                             videos_table.add_row([
    #                                 videos.index(video) + 1,
    #                                 colored(video["date"], "blue"),
    #                                 colored(video["title"][:60] + "...", "green")
    #                             ])
    #
    #                         print(videos_table)
    #                     else:
    #                         warning(" No videos found.")
    #                 elif user_input == 3:
    #                     info("How often do you want to upload?")
    #
    #                     info("\n============ OPTIONS ============", False)
    #                     for idx, cron_option in enumerate(YOUTUBE_CRON_OPTIONS):
    #                         print(colored(f" {idx + 1}. {cron_option}", "cyan"))
    #
    #                     info("=================================\n", False)
    #
    #                     user_input = int(question("Select an Option: "))
    #
    #                     cron_script_path = os.path.join(ROOT_DIR, "src", "cron.py")
    #                     command = f"python {cron_script_path} youtube {selected_account['id']}"
    #
    #                     def job():
    #                         subprocess.run(command)
    #
    #                     if user_input == 1:
    #                         # Upload Once
    #                         schedule.every(1).day.do(job)
    #                         success("Set up CRON Job.")
    #                     elif user_input == 2:
    #                         # Upload Twice a day
    #                         schedule.every().day.at("10:00").do(job)
    #                         schedule.every().day.at("16:00").do(job)
    #                         success("Set up CRON Job.")
    #                     else:
    #                         break
    #                 elif user_input == 4:
    #                     if get_verbose():
    #                         info(" => Climbing Options Ladder...", False)
    #                     break


if __name__ == "__main__":
    # Setup file tree
    assert_folder_structure()

    # Remove temporary files
    rem_temp_files()

    main()
