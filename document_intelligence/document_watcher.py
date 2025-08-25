import os
import sys

# Explicitly add the parent folder of 'document_intelligence' to sys.path
base_path = os.path.dirname(os.path.dirname(__file__))  # This will point to Y:/YBAI/Document_AI/document_intelligence
sys.path.append(base_path)

from document_processing.chunk_pdfs import process_new_document  # Now importing from document_processing.chunk_pdfs

import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class Watcher(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return

        # Check if a new PDF file is uploaded
        if event.src_path.endswith(".pdf"):
            print(f"New file detected: {event.src_path}")
            process_new_document(event.src_path)  # Process the newly uploaded PDF

if __name__ == "__main__":
    # Directories to watch (add user_uploads folder)
    watch_directories = [
        "Y:/YBAI/Document_AI/document_intelligence/document_processing/pdfs", 
        "Y:/YBAI/Document_AI/document_intelligence/media/user_uploads"
    ]

    event_handler = Watcher()
    observer = Observer()

    # Watch both directories
    for watch_dir in watch_directories:
        observer.schedule(event_handler, watch_dir, recursive=False)

    print("Watching for new documents...")
    observer.start()

    try:
        while True:
            time.sleep(1)  # Keep the script running
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
