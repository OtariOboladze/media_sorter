# Media Sorting Script

This script sorts media files (images and videos) by their date. It organizes the files into folders based on the date they were created or last modified.


## Features

- Sorts media files by creation or modification date
- Organizes files into folders by year and month
- Supports various media formats (e.g., jpg, png, mp4, etc.)

## Requirements

- Docker Compose

## Usage

1. Clone the repository or download the script.
2. Place the script in the directory containing your media files.
3. Run ```docker compose up```

## Credits

Original script is from: https://gist.github.com/nikomiko/7492e5e82791c9ff989e2573ca180273
I just added the Docker Compose wrapper and recursive folder search.

## Example

If you have the following files:
- `photo1.jpg` (created on 2021-05-15)
- `video1.mp4` (created on 2020-12-20)

After running the script, your directory structure will be:
```
/2020/12/video1.mp4
/2021/05/photo1.jpg
```

