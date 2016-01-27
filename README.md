README
===

How to use
--
>put following files into ```video_file/```
>

* v_chapter_video.csv *(chapter-video map file)*
* video_record_12_7.csv *(mongoDB raw data file)*
* filter_just_pass.py  *(filter raw data file that just pass)*

run ```python filter_just_pass.py``` will generate

* video_record_12_7_filtered.csv

>files in source/
>

* run ```python to_weeks.py``` will generate files separated to weeks' videos ```to_weeks/...```

* run ```python preprocess_weeks_data.py``` generate files to dir ```to_weeks_preprecessed```

* run ```python subtitlePrepeocess.py``` generate files to dir ```it_done```

* run ```python generateHotKeyword.py``` generate files to dir ```hot_word```
