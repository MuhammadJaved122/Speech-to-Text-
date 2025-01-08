  # Generate audio report
        threading.Thread(target=text_to_speech, args=(report, audio_file), daemon=True).start()
    else:
        sentiment_label.configure(text="No text available for analysis