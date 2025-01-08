from importer import os, threading, pygame
from importer import customtkinter as ctk
from speech import voice_to_text, text_to_speech
from sentimental import analyze_sentiment_vader

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("green")

listening = False  # Flag to track if listening is active
recognized_text = ""  # To store the last recognized text
audio_file = "analysis_report.mp3"  # Default name for the analysis report file
audio_playing = False  # Flag to track if audio is playing
history_data = []  # List to store history of analyses


def toggle_listening(input_text_label, start_button):
    """Toggle the listening state."""
    global listening
    if not listening:
        start_button.configure(text="Stop Listening")
        listening = True
        start_speech_recognition(input_text_label)
    else:
        stop_listening(start_button)


def start_speech_recognition(input_text_label):
    """Handle the speech recognition process in a separate thread."""
    def recognize_speech():
        global listening, recognized_text
        try:
            recognized_text = voice_to_text()
            input_text_label.configure(text=f"You said: {recognized_text}")
        except Exception as e:
            input_text_label.configure(text=f"Error: {str(e)}")
        finally:
            listening = False

    threading.Thread(target=recognize_speech, daemon=True).start()


def stop_listening(start_button):
    global listening
    listening = False
    start_button.configure(text="Start Listening")


def analyze_and_speak(input_text_label, sentiment_label):
    global recognized_text, audio_file, history_data
    user_text = recognized_text.strip()
    if user_text:
        sentiment, scores = analyze_sentiment_vader(user_text)
        report = (
            f"You said: {user_text}\n\n"
            f"Sentiment: {sentiment}\n"
            f"Positive score: {scores['pos']:.2f}\n"
            f"Neutral score: {scores['neu']:.2f}\n"
            f"Negative score: {scores['neg']:.2f}\n"
            f"Compound score: {scores['compound']:.2f}."
        )
        sentiment_label.configure(text=report)

        # Save report to history
        history_data.append(report)

        # Generate audio report
        threading.Thread(target=text_to_speech, args=(report, audio_file), daemon=True).start()
    else:
        sentiment_label.configure(text="No text available for analysis. Please speak something first.")


def display_history(right_panel):
    """Display the history of analyses."""
    for widget in right_panel.winfo_children():
        widget.destroy()

    ctk.CTkLabel(right_panel, text="Analysis History", font=("Arial", 16)).pack(pady=10)
    if not history_data:
        ctk.CTkLabel(right_panel, text="No history available.", font=("Arial", 14)).pack(pady=10)
    else:
        for report in history_data:
            ctk.CTkLabel(right_panel, text=report, font=("Arial", 12), wraplength=450, anchor="w", justify="left").pack(
                fill="x", padx=10, pady=5
            )


def play_audio(slider):
    """Play the analysis report audio and update the slider."""
    global audio_file, audio_playing
    if os.path.exists(audio_file):
        try:
            pygame.mixer.init()
            pygame.mixer.music.load(audio_file)
            pygame.mixer.music.play(loops=0, start=slider.get())
            audio_playing = True
            update_slider(slider)
        except Exception as e:
            print(f"Error playing audio: {e}")
    else:
        print("Audio file not found. Please generate the report first.")


def update_slider(slider):
    global audio_playing
    if audio_playing:
        current_time = pygame.mixer.music.get_pos() / 1000  # Convert milliseconds to seconds
        slider.set(current_time)  # Update slider position
        if pygame.mixer.music.get_busy():
            slider.after(1000, update_slider, slider)  # Update every second


def stop_audio():
    global audio_playing
    pygame.mixer.music.stop()
    audio_playing = False


def setup_gui():
    root = ctk.CTk()
    root.title("Voice Sentiment Analysis")
    root.resizable(True, True)
    root.minsize(800, 600)

    main_frame = ctk.CTkFrame(root, corner_radius=15)
    main_frame.pack(fill="both", expand=True, padx=20, pady=20)

    left_panel = ctk.CTkFrame(main_frame, width=250, corner_radius=15)
    left_panel.pack(side="left", fill="y", padx=(10, 20), pady=20)

    ctk.CTkLabel(left_panel, text="Voice Sentiment", font=("Arial", 20)).pack(pady=20)

    start_button = ctk.CTkButton(
        left_panel, text="Start Listening",
        command=lambda: toggle_listening(input_text_label, start_button)
    )
    start_button.pack(pady=10)

    analyze_button = ctk.CTkButton(
        left_panel, text="Analyze Sentiment",
        command=lambda: analyze_and_speak(input_text_label, sentiment_label)
    )
    analyze_button.pack(pady=10)

    play_button = ctk.CTkButton(
        left_panel, text="Play Report",
        command=lambda: play_audio(slider)
    )
    play_button.pack(pady=10)

    stop_button = ctk.CTkButton(
        left_panel, text="Stop Audio",
        command=stop_audio
    )
    stop_button.pack(pady=10)

    # History button
    history_button = ctk.CTkButton(
        left_panel, text="History",
        command=lambda: display_history(right_panel)
    )
    history_button.pack(pady=10)

    # Appearance Switch (Dark/Light mode)
    appearance_switch = ctk.CTkSwitch(
        left_panel, text="Appearance Mode",
        command=lambda: switch_mode(appearance_switch, mode_label)
    )
    appearance_switch.pack(pady=30)

    mode_label = ctk.CTkLabel(left_panel, text="Current Mode: Dark Mode", font=("Arial", 14))
    mode_label.pack(pady=10)

    right_panel = ctk.CTkFrame(main_frame, corner_radius=15)
    right_panel.pack(side="right", fill="both", expand=True, padx=(10, 20), pady=20)

    ctk.CTkLabel(right_panel, text="Speech Input", font=("Arial", 16)).pack(pady=10)
    input_text_label = ctk.CTkLabel(right_panel, text="You said: ", wraplength=450, anchor="w", justify="left")
    input_text_label.pack(fill="x", padx=10, pady=10)

    ctk.CTkLabel(right_panel, text="Sentiment Report", font=("Arial", 16)).pack(pady=10)
    sentiment_label = ctk.CTkLabel(right_panel, text="Report will appear here.", wraplength=450, anchor="w", justify="left")
    sentiment_label.pack(fill="x", padx=10, pady=10)

    slider = ctk.CTkSlider(right_panel, from_=0, to=100, number_of_steps=100)
    slider.pack(padx=10, pady=10, fill="x")

    return root


def switch_mode(appearance_switch, mode_label):
    """Switch between Dark and Light modes and update the label."""
    if appearance_switch.get():
        ctk.set_appearance_mode("Light")
        mode_label.configure(text="Current Mode: Light Mode")
    else:
        ctk.set_appearance_mode("Dark")
        mode_label.configure(text="Current Mode: Dark Mode")


if __name__ == "__main__":
    app = setup_gui()
    app.mainloop()
