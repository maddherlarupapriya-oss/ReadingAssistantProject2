import asyncio
import edge_tts
import pyttsx3
import pygame
import time
import sys
from config.config import AUDIO_FILE

async def edge_save(text, voice, outfile, rate):
    comm = edge_tts.Communicate(text, voice, rate=rate)
    await comm.save(outfile)
    return outfile

def pyttsx3_save(text, outfile):
    engine = pyttsx3.init()
    engine.setProperty("rate", 150)
    engine.save_to_file(text, outfile)
    engine.runAndWait()
    return outfile

def generate_audio_with_fallback(text, voice, rate):
    try:
        asyncio.run(edge_save(text, voice, AUDIO_FILE, rate))
        return AUDIO_FILE, "edge"
    except Exception:
        try:
            pyttsx3_save(text, AUDIO_FILE)
            return AUDIO_FILE, "pyttsx3"
        except Exception:
            return None, None

def compute_word_timings(text, total_duration):
    words = text.split()
    if not words:
        return []
    
    word_weights = []
    for word in words:
        base_weight = len(word)
        syllable_estimate = max(1, len(word) // 3)
        weight = base_weight + (syllable_estimate * 0.5)
        word_weights.append(weight)
    
    total_weight = sum(word_weights)
    if total_weight == 0:
        avg = total_duration / len(words)
        return [avg * (i + 1) for i in range(len(words))]
    
    timings = []
    cumulative_time = 0.0
    
    for weight in word_weights:
        word_duration = (weight / total_weight) * total_duration
        cumulative_time += word_duration
        timings.append(cumulative_time)
    
    return timings

def format_karaoke_line(words, idx):
    line_parts = []
    words_per_line = 8
    
    start_idx = max(0, (idx // words_per_line) * words_per_line)
    end_idx = min(len(words), start_idx + words_per_line)
    
    for i in range(start_idx, end_idx):
        if i == idx:
            line_parts.append(f"\033[97;44m {words[i]} \033[0m")
        elif i < idx:
            line_parts.append(f"\033[2m{words[i]}\033[0m")
        else:
            line_parts.append(words[i])
    
    line = " ".join(line_parts)
    
    if len(line) > 100:
        line = line[:97] + "..."
    
    return line

def play_karaoke(audio_file, text):
    try:
        pygame.mixer.quit()
    except Exception:
        pass
    
    pygame.mixer.init()
    
    try:
        sound = pygame.mixer.Sound(audio_file)
    except Exception:
        pygame.mixer.music.load(audio_file)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
        return
    
    total_duration = sound.get_length()
    words = text.split()
    
    if not words:
        channel = sound.play()
        while channel.get_busy():
            time.sleep(0.1)
        return
    
    timings = compute_word_timings(text, total_duration)
    
    channel = sound.play()
    start_time = time.time()
    current_word_idx = 0
    last_displayed_idx = -1
    
    print("\n" + "="*70)
    print("KARAOKE MODE - Follow the highlighted word")
    print("="*70 + "\n")
    
    while channel.get_busy():
        elapsed = time.time() - start_time
        
        while current_word_idx < len(timings) and elapsed >= timings[current_word_idx]:
            current_word_idx += 1
        
        display_idx = min(current_word_idx, len(words) - 1)
        
        if display_idx != last_displayed_idx:
            line = format_karaoke_line(words, display_idx)
            print(f"\r{' '*100}\r{line}", end='', flush=True)
            last_displayed_idx = display_idx
        
        time.sleep(0.05)
    
    print("\n\n" + "="*70)
    print("Playback complete!")
    print("="*70 + "\n")

def play_with_controls(audio_file):
    try:
        pygame.mixer.quit()
    except Exception:
        pass
    
    pygame.mixer.init()
    pygame.mixer.music.load(audio_file)
    pygame.mixer.music.play()
    
    print("\n" + "="*80)
    print("PLAYBACK CONTROLS")
    print("="*80)
    
    while True:
        cmd = input("\n[P]ause [R]esume [S]top [Y]Replay [W]Rewind 5s [K]Karaoke [Q]Quit: ").strip().lower()
        
        if cmd == "p":
            pygame.mixer.music.pause()
            print("⏸ Paused")
        elif cmd == "r":
            pygame.mixer.music.unpause()
            print("▶ Resumed")
        elif cmd == "s":
            pygame.mixer.music.stop()
            print("⏹ Stopped")
        elif cmd == "y":
            pygame.mixer.music.stop()
            pygame.mixer.music.play()
            print("🔄 Replaying from start")
        elif cmd == "w":
            try:
                pos = pygame.mixer.music.get_pos() / 1000.0
                rewind = max(0, pos - 5)
                pygame.mixer.music.play(start=rewind)
                print("⏪ Rewound 5 seconds")
            except Exception:
                print("⚠ Rewind not supported for this audio format")
        elif cmd == "k":
            pygame.mixer.music.stop()
            print("🎤 Switching to karaoke mode...")
            return "karaoke"
        elif cmd == "q":
            pygame.mixer.music.stop()
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid command. Try again.")
    
    return None