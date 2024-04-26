from tqdm import tqdm
from logging import info
import os


def volumizer_filter(condition: str) -> callable:
    if condition == 'all':
        return lambda _: True
    
    return lambda x: x in [int(v) for v in condition.split(",")]

def compile_volumes(volume_dir: str, chapter_dir: str, volumes: list) -> None:
    chapters = os.listdir(chapter_dir)

    for volume_name, volume_range in volumes:
        volume_file = volume_name.replace(":", "").replace(" ", "_").lower()

        chapters_start, chapters_end = volume_range
        chapters_in_volume = chapters[chapters_start: chapters_end]

        volume_content = f"<h1 style='page-break-after: always; text-align: center;'>{volume_name}</h1>"

        with open(f"{volume_dir}/{volume_file}.html", "w") as vw:
            print(f"Writing volume: {volume_name}")

            for i in tqdm(range(len(chapters_in_volume)), desc="Compiling volume", ascii=False, ncols=100):
                chapter = chapters_in_volume[i]
                with open(f"{chapter_dir}/{chapter}", "r") as cr:
                    chapter_content = cr.read()
                    volume_content = f"{volume_content}{chapter_content}"
            
            info("Volumes Compiled Successfully!")
            volume_content = f"<body style='font-size: 1.8em;'>{volume_content}</body>"
            vw.write(volume_content)
