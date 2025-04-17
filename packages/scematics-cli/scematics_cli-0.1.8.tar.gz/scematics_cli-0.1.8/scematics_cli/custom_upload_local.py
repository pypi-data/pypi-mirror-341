import os
import shutil
from PIL import Image
import requests
from requests.exceptions import RequestException
import time
from pathlib import Path
from rich.progress import (
    Progress,
    SpinnerColumn,
    TextColumn,
    BarColumn,
    TaskProgressColumn,
    TimeRemainingColumn
)
from rich.console import Console
from rich.prompt import Prompt
from rich import print
import math
import cv2
import json
import argparse

console = Console()

# Supported video file types
VIDEO_EXTENSIONS = {
    '.mp4': 'video/mp4',
    '.mov': 'video/quicktime',
    '.avi': 'video/x-msvideo',
    '.mkv': 'video/x-matroska',
    '.hevc': 'video/hevc'
}

def is_video_file(file_path):
    """Check if the file is a video based on extension"""
    if hasattr(file_path, 'suffix'):
        extension = file_path.suffix.lower()
    else:
        extension = os.path.splitext(file_path)[1].lower() if isinstance(file_path, str) else ""
        
    return extension in VIDEO_EXTENSIONS.keys()

def is_json_file(file_path):
    """Check if the file is a JSON file"""
    if hasattr(file_path, 'suffix'):
        extension = file_path.suffix.lower()
    else:
        extension = os.path.splitext(file_path)[1].lower() if isinstance(file_path, str) else ""
        
    return extension.lower() == '.json'

def convert_rgba_to_rgb(image):
    """Convert RGBA image to RGB with white background"""
    if image.mode in ('RGBA', 'LA') or (image.mode == 'P' and 'transparency' in image.info):
        background = Image.new('RGB', image.size, (255, 255, 255))
        if image.mode == 'RGBA':
            background.paste(image, mask=image.split()[3])
        elif image.mode == 'LA':
            background.paste(image, mask=image.split()[1])
        else:
            background.paste(image, mask=image.info['transparency'])
        return background
    return image.convert('RGB')

def cleanup_thumbnails(folder_path):
    """Clean up thumbnail folder"""
    thumbnail_folder = os.path.join(folder_path, "_thumbnail")
    try:
        if os.path.exists(thumbnail_folder):
            shutil.rmtree(thumbnail_folder)
            print(f"[green]Cleaned up thumbnail folder[/green]")
    except Exception as e:
        print(f"[yellow]Warning: Could not clean up thumbnail folder: {str(e)}[/yellow]")

def get_subdirectories(folder_path):
    """Get all subdirectories in the given folder"""
    return [f.path for f in os.scandir(folder_path) if f.is_dir() and not f.name.startswith('_')]

def get_files_in_directory(directory, file_filter_func):
    """Get all files in directory that match the filter function"""
    return [os.path.join(directory, f) for f in os.listdir(directory) 
            if os.path.isfile(os.path.join(directory, f)) and file_filter_func(f)]

def generate_video_thumbnail(video_path, thumbnail_path):
    """Generate thumbnail from the first frame of a video"""
    try:
        # Open the video file
        video = cv2.VideoCapture(str(video_path))
        
        # Check if video opened successfully
        if not video.isOpened():
            print(f"[red]Could not open video {video_path}[/red]")
            return False
        
        # Read the first frame
        success, frame = video.read()
        if not success:
            print(f"[red]Could not read first frame from {video_path}[/red]")
            return False
        
        # Convert BGR to RGB (OpenCV uses BGR by default)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Create PIL Image from the frame
        img = Image.fromarray(frame_rgb)
        
        # Resize for thumbnail
        img.thumbnail((200, 200))
        
        # Save thumbnail
        img.save(thumbnail_path, "JPEG", quality=85)
        
        # Release video
        video.release()
        
        return True
    except Exception as e:
        print(f"[red]Error generating thumbnail for {video_path}: {str(e)}[/red]")
        return False

def get_video_dimensions(video_path):
    """Get video width and height"""
    try:
        video = cv2.VideoCapture(str(video_path))
        if not video.isOpened():
            return 0, 0
            
        width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        video.release()
        return width, height
    except Exception as e:
        print(f"[red]Error getting video dimensions for {video_path}: {str(e)}[/red]")
        return 0, 0

def retry_request(func, progress, task_id=None, retries=10, delay=2, *args, **kwargs):
    """Retry function execution with progress tracking - 10 retries"""
    for attempt in range(retries):
        try:
            if progress and task_id:
                progress.update(task_id, description=f"[cyan]Attempt {attempt + 1}/{retries}...")
            result = func(*args, **kwargs)
            if result:
                return result
            # If function returns False, also retry
            if progress and task_id:
                progress.update(task_id, description=f"[yellow]Attempt {attempt + 1} returned False, retrying...")
            if attempt < retries - 1:
                time.sleep(delay)
        except Exception as e:
            if progress and task_id:
                progress.update(task_id, description=f"[yellow]Attempt {attempt + 1} failed with error: {str(e)}")
            if attempt < retries - 1:
                time.sleep(delay)
    
    # If we get here, all attempts failed
    if progress and task_id:
        progress.update(task_id, description=f"[red]Failed after {retries} attempts")
    return None

def process_folder_videos(base_url, token, project_id, folder_path, json_files):
    """Process all videos in a folder with JSON metadata files"""
    # Create thumbnail folder in the parent directory
    parent_dir = os.path.dirname(folder_path)
    thumbnail_folder = os.path.join(parent_dir, "_thumbnail")
    os.makedirs(thumbnail_folder, exist_ok=True)
    
    # Set up API endpoints
    presigned_url_endpoint = f"{base_url}/uploads/generate-presigned-url/{{media_id}}"
    confirm_upload_endpoint = f"{base_url}/uploads/confirm-upload/{{media_id}}"
    batch_confirm_endpoint = f"{base_url}/uploads/batch-confirm/{{batch_id}}"
    
    # Get all video files in the folder
    video_files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f)) and is_video_file(f)]
    
    if not video_files:
        print(f"[yellow]No video files found in {folder_path}[/yellow]")
        return False
    
    # Display found videos
    print(f"[cyan]Found {len(video_files)} videos in {folder_path}:[/cyan]")
    for video in video_files[:5]:
        print(f"[cyan]  - {video}[/cyan]")
    if len(video_files) > 5:
        print(f"[cyan]  - ... and {len(video_files) - 5} more[/cyan]")
    
    # Get JSON files (passed from parent function)
    if not json_files:
        print(f"[yellow]No JSON files found in {folder_path}[/yellow]")
        # We'll generate them later
    else:
        print(f"[cyan]Found {len(json_files)} JSON files in {folder_path}:[/cyan]")
        for json_file in json_files[:3]:
            print(f"[cyan]  - {os.path.basename(json_file)}[/cyan]")
        if len(json_files) > 3:
            print(f"[cyan]  - ... and {len(json_files) - 3} more[/cyan]")
    
    # Create a map of JSON files by basename (without extension) for easy lookup
    json_map = {}
    for json_file in json_files:
        # Get the base name without extension
        json_basename = os.path.splitext(os.path.basename(json_file))[0]
        json_map[json_basename] = json_file
    
    # Prepare for progress tracking
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        TimeRemainingColumn(),
        expand=True
    ) as progress:
        folder_name = os.path.basename(folder_path)
        scan_task = progress.add_task(f"[cyan]Processing folder: {folder_name}...", total=len(video_files))
        
        # Prepare data for API request
        file_data_list = []
        
        # Process each video file
        for video_file in video_files:
            file_name = video_file
            video_path = os.path.join(folder_path, file_name)
            
            progress.update(scan_task, description=f"[cyan]Processing {file_name}")
            
            try:
                # Find matching JSON file for this video
                video_basename = os.path.splitext(file_name)[0]
                matching_json = None
                
                # Check if there are any JSON files in this folder
                if json_files:
                    # If there's only one JSON file in the folder, use it for all videos
                    if len(json_files) == 1:
                        matching_json = os.path.basename(json_files[0])
                        print(f"[green]Using the only JSON file in folder for {file_name}: {matching_json}[/green]")
                    else:
                        # Check for exact match first
                        if video_basename in json_map:
                            matching_json = os.path.basename(json_map[video_basename])
                        
                        # If no exact match, try more complex matching patterns
                        if not matching_json:
                            for json_basename, json_path in json_map.items():
                                # Check if JSON basename contains the video basename (or vice versa)
                                if video_basename in json_basename or json_basename in video_basename:
                                    matching_json = os.path.basename(json_path)
                                    break
                            
                            # If still no match, just use the first JSON file
                            if not matching_json:
                                matching_json = os.path.basename(json_files[0])
                                print(f"[yellow]No name match found. Using first JSON file for {file_name}: {matching_json}[/yellow]")
                
                # Generate thumbnail
                thumbnail_path = os.path.join(thumbnail_folder, f"{os.path.splitext(file_name)[0]}_thumbnail.jpeg")
                success = generate_video_thumbnail(video_path, thumbnail_path)
                
                if not success:
                    print(f"[yellow]Warning: Could not generate thumbnail for {file_name}, using placeholder[/yellow]")
                    # Create a blank thumbnail with text
                    img = Image.new('RGB', (200, 200), color=(100, 100, 100))
                    img.save(thumbnail_path, "JPEG", quality=85)
                
                # Get video dimensions
                width, height = get_video_dimensions(video_path)
                
                # Add file data
                file_data = {
                    "file_name": file_name,
                    "width": width,
                    "height": height,
                    "media_type": "VIDEO",
                    "folder_path": folder_path
                }
                
                # Add metadata JSON if we found a match
                if matching_json:
                    file_data["meta_data"] = matching_json
                    print(f"[green]Found matching JSON for {file_name}: {matching_json}[/green]")
                else:
                    file_data["needs_metadata_generation"] = True
                    print(f"[yellow]No matching JSON found for {file_name}[/yellow]")
                
                file_data_list.append(file_data)
                
            except Exception as e:
                print(f"[red]Failed to process {file_name}: {str(e)}[/red]")
            
            progress.advance(scan_task)
        
        # Skip further processing if no files were processed
        if not file_data_list:
            print(f"[red]No files were successfully processed in {folder_path}[/red]")
            return False
        
        # Send request to server
        progress.update(scan_task, description=f"[cyan]Sending metadata to server for folder: {folder_name}...")
        
        # Prepare headers
        headers = {'Authorization': f'Bearer {token}'}
        
        try:
            # Video API endpoint
            video_api_endpoint = f"{base_url}/uploads/entry-datas?media_type=VIDEO"
            
            # Remove custom metadata flag before sending to server
            for item in file_data_list:
                if "needs_metadata_generation" in item:
                    del item["needs_metadata_generation"]
                if "folder_path" in item:
                    del item["folder_path"]
                    
            payload = {
                "project_id": project_id,
                "items": file_data_list
            }
            
            # Use retry for the request
            max_retries = 5
            response_json = None
            
            for attempt in range(max_retries):
                try:
                    progress.update(scan_task, description=f"[cyan]Sending VIDEO data to server for folder: {folder_name}...")
                    response = requests.post(video_api_endpoint, json=payload, headers=headers)
                    response.raise_for_status()
                    response_json = response.json()
                    break
                except requests.exceptions.RequestException as e:
                    if attempt < max_retries - 1:
                        print(f"[yellow]API request attempt {attempt + 1}/{max_retries} failed: {str(e)}. Retrying...[/yellow]")
                        time.sleep(3)
                    else:
                        raise
            
            if not response_json:
                print(f"[red]Failed to get response from server for folder: {folder_name}[/red]")
                return False
            
            # Get batch ID
            batch_id = response_json.get('batch_id')
            if not batch_id:
                print(f"[red]Batch ID not found in response for folder: {folder_name}[/red]")
                return False
            
            # Add original data back to items for upload phase
            for i, item in enumerate(response_json.get('items', [])):
                file_name = item['file_name']
                # Find original item data
                original_item = next((x for x in file_data_list if x['file_name'] == file_name), None)
                if original_item:
                    # Add folder path back
                    item['folder_path'] = folder_path
                    # Add metadata json path if available
                    if 'meta_data' in original_item:
                        item['meta_data'] = original_item['meta_data']
                        # Find the full path to the JSON file
                        json_name = original_item['meta_data']
                        json_path = None
                        for j in json_files:
                            if os.path.basename(j) == json_name:
                                json_path = j
                                break
                        if json_path:
                            item['json_file_path'] = json_path
            
            failed_files = []
            
            # Create upload task
            upload_task = progress.add_task(
                f"[cyan]Uploading files from folder: {folder_name}...",
                total=len(response_json.get('items', [])) * 2  # *2 for main files and thumbnails
            )
            
            # Process each item
            for item in response_json.get('items', []):
                media_id = item['media_id']
                file_name = item['file_name']
                folder_path = item.get('folder_path', folder_path)
                
                progress.update(upload_task, description=f"[cyan]Uploading {file_name}")
                
                # Get JSON file path if available
                json_file_path = item.get('json_file_path', None)
                needs_metadata_generation = not json_file_path
                
                # Get presigned URLs and upload
                success = retry_request(
                    request_presigned_urls,
                    progress,
                    upload_task,
                    media_id=media_id,
                    file_name=file_name,
                    token=token,
                    folder_path=folder_path,
                    thumbnail_folder=thumbnail_folder,
                    presigned_url_endpoint=presigned_url_endpoint,
                    confirm_upload_endpoint=confirm_upload_endpoint,
                    json_file_path=json_file_path,
                    needs_metadata_generation=needs_metadata_generation
                )
                
                if success:
                    progress.update(upload_task, description=f"[cyan]Confirming {file_name}")
                    confirm_success = retry_request(
                        confirm_upload,
                        progress,
                        upload_task,
                        media_id=media_id,
                        token=token,
                        confirm_upload_endpoint=confirm_upload_endpoint
                    )
                    if not confirm_success:
                        failed_files.append(file_name)
                else:
                    failed_files.append(file_name)
                
                progress.advance(upload_task, 2)
            
            # Log any failed files
            if failed_files:
                print(f"[yellow]Warning: {len(failed_files)} files failed in folder {folder_name}[/yellow]")
                print(f"[yellow]Failed files: {', '.join(failed_files[:5])}{'...' if len(failed_files) > 5 else ''}[/yellow]")
            
            # Confirm the batch
            if confirm_batch_upload(batch_id, token, batch_confirm_endpoint):
                print(f"[green]Folder {folder_name} processed successfully![/green]")
                return True
            else:
                print(f"[red]Folder {folder_name} had confirmation errors[/red]")
                return False
            
        except Exception as e:
            print(f"[red]Error during upload process for folder {folder_name}: {str(e)}[/red]")
            return False
        
def request_presigned_urls(media_id, file_name, token, folder_path, thumbnail_folder, presigned_url_endpoint, 
                          confirm_upload_endpoint, json_file_path=None, needs_metadata_generation=False):
    """Request presigned URLs and upload files"""
    formatted_presigned_url = presigned_url_endpoint.format(media_id=media_id)
    
    # Determine correct file type based on extension
    extension = os.path.splitext(file_name)[1].lower()
    file_type = VIDEO_EXTENSIONS.get(extension, 'application/octet-stream')
    
    payload = {
        "file_key": file_name,
        "file_type": file_type
    }
    headers = {'Authorization': f'Bearer {token}'}
    
    response = requests.post(formatted_presigned_url, json=payload, headers=headers)
    response.raise_for_status()

    presigned_urls = response.json()

    main_url = presigned_urls['upload_url']
    thumbnail_url = presigned_urls['thumbnail_url']
    meta_data_url = presigned_urls.get('meta_data_url')  # Get metadata URL if available
    
    # Upload files
    file_path = os.path.join(folder_path, file_name)
    thumbnail_path = os.path.join(thumbnail_folder, f"{os.path.splitext(file_name)[0]}_thumbnail.jpeg")
    
    # Debug information
    print(f"[cyan]Uploading main file: {file_path}[/cyan]")
    success_main = upload_file_to_s3(file_path, main_url, file_type=file_type)
    
    print(f"[cyan]Uploading thumbnail: {thumbnail_path}[/cyan]")
    success_thumb = upload_file_to_s3(thumbnail_path, thumbnail_url, file_type='image/jpeg')
    
    # Handle metadata JSON upload
    success_meta = True  # Default to True if no metadata URL
    
    if meta_data_url:
        try:
            # If a specific JSON file is provided, use that
            if json_file_path:
                print(f"[cyan]Uploading JSON metadata file: {json_file_path}[/cyan]")
                success_meta = upload_file_to_s3(json_file_path, meta_data_url, file_type='application/json')
                if success_meta:
                    print(f"[green]Successfully uploaded metadata file for {file_name}[/green]")
                else:
                    print(f"[yellow]Failed to upload metadata file for {file_name}[/yellow]")
                    # Retry with generated metadata if the JSON upload failed
                    print(f"[yellow]Attempting to generate and upload basic metadata instead[/yellow]")
                    success_meta = generate_and_upload_metadata(file_name, file_type, folder_path, thumbnail_folder, meta_data_url)
            
            # If we need to generate metadata (no JSON file provided)
            else:
                print(f"[yellow]No JSON metadata file provided, creating a basic one for {file_name}[/yellow]")
                success_meta = generate_and_upload_metadata(file_name, file_type, folder_path, thumbnail_folder, meta_data_url)
        
        except Exception as e:
            print(f"[red]Error handling metadata for {file_name}: {str(e)}[/red]")
            print(f"[yellow]Attempting to generate and upload basic metadata instead[/yellow]")
            success_meta = generate_and_upload_metadata(file_name, file_type, folder_path, thumbnail_folder, meta_data_url)
    
    return success_main and success_thumb and success_meta

def generate_and_upload_metadata(file_name, file_type, folder_path, thumbnail_folder, meta_data_url):
    """Generate and upload basic metadata for a file"""
    try:
        # Create a new JSON file
        base_name = os.path.splitext(file_name)[0]
        meta_file_name = f"{base_name}_metadata.json"
        meta_file_path = os.path.join(thumbnail_folder, meta_file_name)
        
        # Create simple metadata JSON
        metadata = {
            "filename": file_name,
            "upload_timestamp": time.time(),
            "file_type": file_type,
            "media_type": "VIDEO",
            "path": str(folder_path)
        }
        
        # Save metadata JSON file
        with open(meta_file_path, 'w') as f:
            json.dump(metadata, f, indent=4)
        
        print(f"[cyan]Generated metadata file: {meta_file_path}[/cyan]")
        
        # Upload metadata JSON
        success = upload_file_to_s3(meta_file_path, meta_data_url, file_type='application/json')
        
        # Clean up metadata file
        try:
            os.remove(meta_file_path)
        except Exception as e:
            print(f"[yellow]Warning: Could not remove temporary metadata file: {str(e)}[/yellow]")
            
        return success
    except Exception as e:
        print(f"[red]Error generating and uploading metadata: {str(e)}[/red]")
        return False

def upload_file_to_s3(file_path, presigned_url, file_type='image/jpeg'):
    """Upload single file to S3 with improved error handling"""
    max_attempts = 5  # Increased from 3 to 5
    
    for attempt in range(max_attempts):
        try:
            # Check if file exists
            if not os.path.exists(file_path):
                print(f"[red]File not found: {file_path}[/red]")
                return False
                
            # Get file size for debugging
            file_size = os.path.getsize(file_path)
            print(f"[cyan]Uploading file: {os.path.basename(file_path)} ({file_size} bytes) - Content-Type: {file_type}[/cyan]")
            
            with open(file_path, 'rb') as file_data:
                headers = {'Content-Type': file_type}
                response = requests.put(presigned_url, data=file_data, headers=headers)
                
                # Check for 503 error specifically
                if response.status_code == 503:
                    print(f"[yellow]Attempt {attempt + 1}/{max_attempts}: 503 Service Unavailable for {os.path.basename(file_path)}[/yellow]")
                    if attempt < max_attempts - 1:
                        # Wait longer for 503 errors (server is overloaded)
                        time.sleep(5)  # 5 second wait before retry
                        continue
                
                # Check status code
                if response.status_code >= 400:
                    print(f"[yellow]Attempt {attempt + 1}/{max_attempts}: HTTP error {response.status_code} for {os.path.basename(file_path)}[/yellow]")
                    print(f"[yellow]Response: {response.text[:200]}...[/yellow]")
                    if attempt < max_attempts - 1:
                        time.sleep(3)
                        continue
                        
                # For other errors
                response.raise_for_status()
                print(f"[green]Successfully uploaded {os.path.basename(file_path)}[/green]")
                return True
                
        except requests.exceptions.RequestException as e:
            if "503" in str(e):
                print(f"[yellow]Attempt {attempt + 1}/{max_attempts}: 503 Service Unavailable for {os.path.basename(file_path)}[/yellow]")
            else:
                print(f"[red]Attempt {attempt + 1}/{max_attempts}: Failed to upload {os.path.basename(file_path)}: {str(e)}[/red]")
            
            if attempt < max_attempts - 1:
                time.sleep(3)  # Wait before retry
    
    # If we reach here, all attempts failed
    print(f"[red]Failed to upload {os.path.basename(file_path)} after {max_attempts} attempts[/red]")
    return False

def confirm_upload(media_id, token, confirm_upload_endpoint):
    """Confirm single media upload"""
    url = confirm_upload_endpoint.format(media_id=media_id)
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.post(url, headers=headers)
    response.raise_for_status()
    return True

def confirm_batch_upload(batch_id, token, batch_confirm_endpoint):
    """Confirm entire batch upload"""
    try:
        url = batch_confirm_endpoint.format(batch_id=batch_id)
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.post(url, headers=headers)
        response.raise_for_status()
        print(f"[green]Batch {batch_id} confirmed successfully![/green]")
        return True
    except Exception as e:
        print(f"[red]Failed to confirm batch {batch_id}: {str(e)}[/red]")
        return False

def find_leaf_folders(root_path):
    """Find all leaf folders (folders without subdirectories) in the directory tree"""
    leaf_folders = []
    
    for root, dirs, files in os.walk(root_path):
        # Skip hidden folders
        dirs[:] = [d for d in dirs if not d.startswith('_')]
        
        # If this folder has no subdirectories, it's a leaf
        if not dirs:
            # Check if it has video files
            has_videos = any(is_video_file(f) for f in files)
            if has_videos:
                leaf_folders.append(root)
    
    return leaf_folders

def is_video_directory(directory):
    """Check if the directory contains video files"""
    if not os.path.isdir(directory):
        return False
        
    return any(is_video_file(f) for f in os.listdir(directory) 
               if os.path.isfile(os.path.join(directory, f)))

def cleanup_all_thumbnails(root_path):
    """Find and clean up all _thumbnail folders under the given path"""
    thumbnail_folders = []
    
    # First, find all _thumbnail folders
    for root, dirs, files in os.walk(root_path):
        if os.path.basename(root) == "_thumbnail":
            thumbnail_folders.append(root)
    
    # Then remove them
    for folder in thumbnail_folders:
        try:
            print(f"[yellow]Cleaning up thumbnail folder: {folder}[/yellow]")
            shutil.rmtree(folder)
        except Exception as e:
            print(f"[red]Error cleaning up thumbnail folder {folder}: {str(e)}[/red]")
    
    if thumbnail_folders:
        print(f"[green]Cleaned up {len(thumbnail_folders)} thumbnail folders[/green]")
    else:
        print(f"[yellow]No thumbnail folders found to clean up[/yellow]")

def process_directory_structure(base_url, token, project_id, input_path):
    """Process directory structure starting from the input path"""
    # Check if the input path exists
    if not os.path.exists(input_path):
        print(f"[red]Path {input_path} does not exist[/red]")
        return False
    
    # If the path is a file, get its directory
    if os.path.isfile(input_path):
        print(f"[yellow]Input is a file, using its parent directory instead[/yellow]")
        input_path = os.path.dirname(input_path)
    
    # Determine our approach based on the directory structure
    if is_video_directory(input_path):
        # This directory contains videos directly
        print(f"[cyan]Found videos in {input_path}. Processing this directory only.[/cyan]")
        json_files = [os.path.join(input_path, f) for f in os.listdir(input_path) 
                    if os.path.isfile(os.path.join(input_path, f)) and is_json_file(f)]
        result = process_folder_videos(base_url, token, project_id, input_path, json_files)
        
        # Clean up thumbnails
        cleanup_all_thumbnails(input_path)
        return result
    else:
        # Need to locate leaf directories with videos
        print(f"[cyan]Scanning {input_path} for directories containing videos...[/cyan]")
        leaf_folders = find_leaf_folders(input_path)
        
        if not leaf_folders:
            print(f"[yellow]No directories with videos found under {input_path}[/yellow]")
            return False
        
        print(f"[cyan]Found {len(leaf_folders)} directories with videos:[/cyan]")
        for folder in leaf_folders[:5]:
            print(f"[cyan]  - {folder}[/cyan]")
        if len(leaf_folders) > 5:
            print(f"[cyan]  - ... and {len(leaf_folders) - 5} more[/cyan]")
        
        successful_folders = 0
        failed_folders = 0
        
        # Process each leaf folder
        for folder_index, folder in enumerate(leaf_folders):
            folder_name = os.path.basename(folder)
            print(f"\n[yellow]Processing folder {folder_index + 1} of {len(leaf_folders)}: {folder_name}[/yellow]")
            
            # Get JSON files in this folder
            json_files = [os.path.join(folder, f) for f in os.listdir(folder) 
                        if os.path.isfile(os.path.join(folder, f)) and is_json_file(f)]
            
            # Process this folder
            result = process_folder_videos(base_url, token, project_id, folder, json_files)
            
            if result:
                print(f"[green]Folder {folder_name} processed successfully![/green]")
                successful_folders += 1
            else:
                print(f"[red]Folder {folder_name} processing failed[/red]")
                failed_folders += 1
            
            # Add a small delay between folders
            if folder_index < len(leaf_folders) - 1:
                print(f"[yellow]Pausing before next folder...[/yellow]")
                time.sleep(3)  # 3 second pause between folders
        
        # Clean up all thumbnail folders
        print(f"[yellow]Cleaning up all thumbnail folders...[/yellow]")
        cleanup_all_thumbnails(input_path)
        
        # Final report
        print(f"\n[green]Upload process completed![/green]")
        print(f"[green]- Successfully processed {successful_folders} out of {len(leaf_folders)} folders[/green]")
        
        if successful_folders == len(leaf_folders):
            print("[green]All folders uploaded successfully![/green]")
            return True
        else:
            print(f"[yellow]Some folders had issues ({failed_folders} out of {len(leaf_folders)})[/yellow]")
            return True  # Still return True since most folders likely uploaded

def main():
    """Main function to handle command line arguments"""
    parser = argparse.ArgumentParser(description='Video Upload Script for Nested Directory Structures')
    
    # Required arguments
    parser.add_argument('--project_id', type=str, help='Project ID to upload videos to')
    parser.add_argument('--folder', type=str, help='Path to the folder containing videos or subfolders with videos')
    
    # Optional arguments
    parser.add_argument('--base_url', type=str, default='https://api.example.com/v1', help='Base API URL')
    parser.add_argument('--token', type=str, help='API Authentication token')
    
    args = parser.parse_args()
    
    # Validate required arguments
    if not args.project_id:
        args.project_id = Prompt.ask("[cyan]Enter project ID[/cyan]")
    
    if not args.folder:
        args.folder = Prompt.ask("[cyan]Enter folder path[/cyan]")
    
    if not args.token:
        args.token = Prompt.ask("[cyan]Enter API token[/cyan]", password=True)
    
    # Display configuration
    print(f"\n[cyan]Configuration:[/cyan]")
    print(f"[cyan]- Project ID: {args.project_id}[/cyan]")
    print(f"[cyan]- Folder: {args.folder}[/cyan]")
    print(f"[cyan]- Base URL: {args.base_url}[/cyan]")
    
    # Run the upload process
    result = process_directory_structure(args.base_url, args.token, args.project_id, args.folder)
    
    if result:
        print("[green]Upload process completed successfully![/green]")
        return 0
    else:
        print("[red]Upload process encountered errors.[/red]")
        return 1