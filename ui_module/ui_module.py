def show_preview(text, max_chars=1000):
    preview = text if len(text) <= max_chars else text[:max_chars] + "\n...[truncated]"
    print("\n=== Preview ===\n")
    print(preview)
    print("\n=== End Preview ===\n")
